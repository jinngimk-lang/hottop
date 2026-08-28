from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

GGUF_MAGIC = b"GGUF"


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


def _identity(
    path: Path,
    *,
    label: str,
    require_executable: bool = False,
    require_gguf: bool = False,
) -> tuple[LocalArtifactIdentity | None, list[str]]:
    blockers: list[str] = []
    if not path.exists():
        return None, [f"{label} does not exist: {path}"]
    if not path.is_file():
        return None, [f"{label} is not a file: {path}"]

    size_bytes = path.stat().st_size
    if size_bytes <= 0:
        blockers.append(f"{label} is empty: {path}")
    if require_executable and not os.access(path, os.X_OK):
        blockers.append(f"{label} is not executable: {path}")

    payload = path.read_bytes()
    if require_gguf and size_bytes > 0 and payload[: len(GGUF_MAGIC)] != GGUF_MAGIC:
        blockers.append(f"{label} has invalid GGUF header: {path}")

    identity = LocalArtifactIdentity(
        path=str(path.resolve()),
        size_bytes=size_bytes,
        sha256=hashlib.sha256(payload).hexdigest(),
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

    return QwenTtsCppPreflight(
        ready=not blockers,
        executable=executable_identity,
        talker_gguf=talker_identity,
        tokenizer_gguf=tokenizer_identity,
        blockers=blockers,
    )
