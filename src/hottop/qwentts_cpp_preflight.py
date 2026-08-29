from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

GGUF_MAGIC = b"GGUF"
GGUF_HEADER_BYTES = 24
HASH_CHUNK_BYTES = 1024 * 1024


class LocalArtifactIdentity(BaseModel):
    path: str
    size_bytes: int
    sha256: str


class QwenTtsCppPreflight(BaseModel):
    schema_version: Literal["hottop.qwentts-cpp-preflight.v1"] = (
        "hottop.qwentts-cpp-preflight.v1"
    )
    ready: bool
    executed: Literal[False] = False
    network_access: Literal[False] = False
    auto_download: Literal[False] = False
    executable: LocalArtifactIdentity | None = None
    talker_gguf: LocalArtifactIdentity | None = None
    tokenizer_gguf: LocalArtifactIdentity | None = None
    blockers: list[str]


def _stream_sha256_and_header(path: Path) -> tuple[str, bytes]:
    digest = hashlib.sha256()
    header = b""
    with path.open("rb") as handle:
        while chunk := handle.read(HASH_CHUNK_BYTES):
            if len(header) < GGUF_HEADER_BYTES:
                missing = GGUF_HEADER_BYTES - len(header)
                header += chunk[:missing]
            digest.update(chunk)
    return digest.hexdigest(), header


def _snapshot_signature(path: Path) -> tuple[int, int, int, int, int, int]:
    stat = path.stat()
    return (
        stat.st_dev,
        stat.st_ino,
        stat.st_size,
        stat.st_mtime_ns,
        stat.st_ctime_ns,
        stat.st_mode,
    )


def _gguf_header_blockers(header: bytes, *, path: Path, label: str) -> list[str]:
    if not header.startswith(GGUF_MAGIC):
        return [f"{label} has invalid GGUF header: {path}"]
    if len(header) < GGUF_HEADER_BYTES:
        return [f"{label} has truncated GGUF header: {path}"]
    tensor_count = int.from_bytes(header[8:16], "little")
    if tensor_count == 0:
        return [f"{label} has zero tensors: {path}"]
    return []


def _identity(
    path: Path,
    *,
    label: str,
    require_executable: bool = False,
    require_gguf: bool = False,
) -> tuple[LocalArtifactIdentity | None, list[str]]:
    blockers: list[str] = []
    try:
        resolved_path = path.resolve(strict=True)
    except FileNotFoundError:
        return None, [f"{label} does not exist: {path}"]
    except OSError:
        return None, [f"{label} could not be resolved: {path}"]

    if not resolved_path.is_file():
        return None, [f"{label} is not a file: {path}"]

    snapshot_before = _snapshot_signature(resolved_path)
    size_bytes = snapshot_before[2]
    if size_bytes <= 0:
        blockers.append(f"{label} is empty: {path}")
    if require_executable and not os.access(resolved_path, os.X_OK):
        blockers.append(f"{label} is not executable: {path}")

    try:
        sha256, header = _stream_sha256_and_header(resolved_path)
        snapshot_after = _snapshot_signature(resolved_path)
    except OSError:
        return None, blockers + [f"{label} changed during preflight: {path}"]

    if snapshot_before != snapshot_after:
        return None, blockers + [f"{label} changed during preflight: {path}"]

    if require_gguf and size_bytes > 0:
        blockers.extend(_gguf_header_blockers(header, path=resolved_path, label=label))

    identity = LocalArtifactIdentity(
        path=str(resolved_path),
        size_bytes=size_bytes,
        sha256=sha256,
    )
    return identity, blockers


def inspect_qwentts_cpp_inputs(
    *,
    executable: Path,
    talker_gguf: Path,
    tokenizer_gguf: Path,
) -> QwenTtsCppPreflight:
    """Bind operator-provisioned qwentts.cpp benchmark inputs without executing anything."""

    executable_identity, executable_blockers = _identity(
        executable,
        label="qwentts executable",
        require_executable=True,
    )
    talker_identity, talker_blockers = _identity(
        talker_gguf,
        label="talker GGUF",
        require_gguf=True,
    )
    tokenizer_identity, tokenizer_blockers = _identity(
        tokenizer_gguf,
        label="tokenizer GGUF",
        require_gguf=True,
    )
    blockers = executable_blockers + talker_blockers + tokenizer_blockers

    if executable_identity is not None:
        model_identities = [identity for identity in (talker_identity, tokenizer_identity) if identity]
        executable_reused_as_model = any(
            executable_identity.path == identity.path or executable_identity.sha256 == identity.sha256
            for identity in model_identities
        )
        if executable_reused_as_model:
            blockers.append("qwentts executable and model GGUF artifacts must be distinct")

    if talker_identity is not None and tokenizer_identity is not None:
        same_path = talker_identity.path == tokenizer_identity.path
        same_bytes = talker_identity.sha256 == tokenizer_identity.sha256
        if same_path or same_bytes:
            blockers.append("talker GGUF and tokenizer GGUF must be distinct artifacts")

    return QwenTtsCppPreflight(
        ready=not blockers,
        executable=executable_identity,
        talker_gguf=talker_identity,
        tokenizer_gguf=tokenizer_identity,
        blockers=blockers,
    )
