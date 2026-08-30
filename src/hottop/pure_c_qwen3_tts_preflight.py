from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from .qwentts_cpp_preflight import (
    HASH_CHUNK_BYTES,
    LocalArtifactIdentity,
    _identity,
    _snapshot_signature,
)

REQUIRED_MODEL_FILES = (
    "config.json",
    "generation_config.json",
    "tokenizer_config.json",
    "preprocessor_config.json",
    "model.safetensors",
    "vocab.json",
    "merges.txt",
    "speech_tokenizer/config.json",
    "speech_tokenizer/configuration.json",
    "speech_tokenizer/model.safetensors",
    "speech_tokenizer/preprocessor_config.json",
)
SAFETENSORS_HEADER_LENGTH_BYTES = 8
SAFETENSORS_MAX_HEADER_SIZE_BYTES = 100_000_000
SAFETENSORS_MODEL_FILES = frozenset(
    {"model.safetensors", "speech_tokenizer/model.safetensors"}
)


class PureCQwen3TtsPreflight(BaseModel):
    schema_version: Literal["hottop.qwen3-tts-pure-c-preflight.v1"] = (
        "hottop.qwen3-tts-pure-c-preflight.v1"
    )
    ready: bool
    executed: Literal[False] = False
    network_access: Literal[False] = False
    auto_download: Literal[False] = False
    model_dir: str | None = None
    checkpoint_model_type: str | None = None
    checkpoint_model_size: str | None = None
    executable: LocalArtifactIdentity | None = None
    artifacts: dict[str, LocalArtifactIdentity]
    blockers: list[str]


def _read_bound_config(
    config_identity: LocalArtifactIdentity,
) -> tuple[dict[str, object] | None, list[str]]:
    path = Path(config_identity.path)
    try:
        config_bytes = path.read_bytes()
    except OSError:
        return None, [f"Pure-C Qwen3-TTS config.json changed after artifact binding: {path}"]

    if hashlib.sha256(config_bytes).hexdigest() != config_identity.sha256:
        return None, [f"Pure-C Qwen3-TTS config.json changed after artifact binding: {path}"]

    try:
        parsed = json.loads(config_bytes)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None, [f"Pure-C Qwen3-TTS config.json is not valid JSON: {path}"]
    if not isinstance(parsed, dict):
        return None, [f"Pure-C Qwen3-TTS config.json must contain a JSON object: {path}"]
    return parsed, []


def _safetensors_header_blockers(
    header_bytes: bytes,
    *,
    data_size: int,
    path: Path,
    label: str,
) -> list[str]:
    if not header_bytes.startswith(b"{"):
        return [f"{label} has invalid safetensors JSON header: {path}"]
    try:
        header = json.loads(header_bytes)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return [f"{label} has invalid safetensors JSON header: {path}"]
    if not isinstance(header, dict):
        return [f"{label} safetensors header must be a JSON object: {path}"]

    blockers: list[str] = []
    tensor_count = 0
    for tensor_name, descriptor in header.items():
        if tensor_name == "__metadata__":
            if not isinstance(descriptor, dict) or not all(
                isinstance(key, str) and isinstance(value, str)
                for key, value in descriptor.items()
            ):
                blockers.append(f"{label} has invalid safetensors metadata: {path}")
            continue

        tensor_count += 1
        if not isinstance(descriptor, dict):
            blockers.append(f"{label} has invalid safetensors tensor descriptor: {path}")
            continue
        dtype = descriptor.get("dtype")
        shape = descriptor.get("shape")
        offsets = descriptor.get("data_offsets")
        valid_shape = isinstance(shape, list) and all(
            isinstance(dimension, int) and not isinstance(dimension, bool) and dimension >= 0
            for dimension in shape
        )
        valid_offsets = (
            isinstance(offsets, list)
            and len(offsets) == 2
            and all(isinstance(offset, int) and not isinstance(offset, bool) for offset in offsets)
        )
        if not isinstance(dtype, str) or not dtype or not valid_shape or not valid_offsets:
            blockers.append(f"{label} has invalid safetensors tensor descriptor: {path}")
            continue
        begin, end = offsets
        if begin < 0 or end < begin or end > data_size:
            blockers.append(f"{label} has out-of-range safetensors data offsets: {path}")

    if tensor_count == 0:
        blockers.append(f"{label} safetensors header contains no tensors: {path}")
    return blockers


def _safetensors_identity(
    path: Path,
    *,
    label: str,
) -> tuple[LocalArtifactIdentity | None, list[str]]:
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
    blockers: list[str] = []
    if size_bytes <= SAFETENSORS_HEADER_LENGTH_BYTES:
        blockers.append(f"{label} has truncated safetensors header: {path}")

    digest = hashlib.sha256()
    header_bytes = b""
    header_length: int | None = None
    header_read_allowed = False
    try:
        with resolved_path.open("rb") as handle:
            prefix = handle.read(SAFETENSORS_HEADER_LENGTH_BYTES)
            digest.update(prefix)
            if len(prefix) == SAFETENSORS_HEADER_LENGTH_BYTES:
                header_length = int.from_bytes(prefix, "little")
                if header_length <= 0 or header_length > size_bytes - SAFETENSORS_HEADER_LENGTH_BYTES:
                    blockers.append(f"{label} has invalid safetensors header length: {path}")
                elif header_length > SAFETENSORS_MAX_HEADER_SIZE_BYTES:
                    blockers.append(f"{label} safetensors header is too large: {path}")
                else:
                    header_read_allowed = True
                    header_bytes = handle.read(header_length)
                    digest.update(header_bytes)
                    if len(header_bytes) != header_length:
                        blockers.append(f"{label} has truncated safetensors JSON header: {path}")
            while chunk := handle.read(HASH_CHUNK_BYTES):
                digest.update(chunk)
        snapshot_after = _snapshot_signature(resolved_path)
    except OSError:
        return None, blockers + [f"{label} changed during preflight: {path}"]

    if snapshot_before != snapshot_after:
        return None, blockers + [f"{label} changed during preflight: {path}"]

    if header_read_allowed and header_length is not None and len(header_bytes) == header_length:
        data_size = size_bytes - SAFETENSORS_HEADER_LENGTH_BYTES - header_length
        blockers.extend(
            _safetensors_header_blockers(
                header_bytes,
                data_size=data_size,
                path=resolved_path,
                label=label,
            )
        )

    return (
        LocalArtifactIdentity(
            path=str(resolved_path),
            size_bytes=size_bytes,
            sha256=digest.hexdigest(),
        ),
        blockers,
    )


def inspect_pure_c_qwen3_tts_inputs(
    *,
    executable: Path,
    model_dir: Path,
) -> PureCQwen3TtsPreflight:
    """Bind operator-provisioned Pure-C Qwen3-TTS inputs without executing anything."""

    blockers: list[str] = []
    resolved_model_dir: Path | None = None
    try:
        resolved_model_dir = model_dir.resolve(strict=True)
    except OSError:
        blockers.append(f"Pure-C Qwen3-TTS model directory does not exist: {model_dir}")

    if resolved_model_dir is not None and not resolved_model_dir.is_dir():
        blockers.append(
            f"Pure-C Qwen3-TTS model directory is not a directory: {resolved_model_dir}"
        )
        resolved_model_dir = None

    executable_identity, executable_blockers = _identity(
        executable,
        label="Pure-C Qwen3-TTS executable",
        require_executable=True,
    )
    blockers.extend(executable_blockers)

    artifacts: dict[str, LocalArtifactIdentity] = {}
    if resolved_model_dir is not None:
        for relative_path in REQUIRED_MODEL_FILES:
            artifact_path = resolved_model_dir / relative_path
            label = f"Pure-C Qwen3-TTS {relative_path}"
            if relative_path in SAFETENSORS_MODEL_FILES:
                identity, artifact_blockers = _safetensors_identity(artifact_path, label=label)
            else:
                identity, artifact_blockers = _identity(artifact_path, label=label)
            blockers.extend(artifact_blockers)
            if identity is not None:
                artifacts[relative_path] = identity

    checkpoint_model_type: str | None = None
    checkpoint_model_size: str | None = None
    config_identity = artifacts.get("config.json")
    if config_identity is not None:
        config, config_blockers = _read_bound_config(config_identity)
        blockers.extend(config_blockers)
        if config is not None:
            model_family = config.get("model_type")
            raw_model_type = config.get("tts_model_type")
            raw_model_size = config.get("tts_model_size")
            checkpoint_model_type = raw_model_type if isinstance(raw_model_type, str) else None
            checkpoint_model_size = raw_model_size if isinstance(raw_model_size, str) else None
            if model_family != "qwen3_tts":
                blockers.append("Pure-C Qwen3-TTS config.json must identify model_type qwen3_tts")
            if checkpoint_model_type != "custom_voice":
                blockers.append(
                    "Pure-C Qwen3-TTS benchmark requires tts_model_type custom_voice"
                )
            if checkpoint_model_size != "1b7":
                blockers.append("Pure-C Qwen3-TTS benchmark requires tts_model_size 1b7")

    if executable_identity is not None:
        executable_reused_as_model = any(
            executable_identity.path == identity.path
            or executable_identity.sha256 == identity.sha256
            for identity in artifacts.values()
        )
        if executable_reused_as_model:
            blockers.append("Pure-C Qwen3-TTS executable and model artifacts must be distinct")

    talker_identity = artifacts.get("model.safetensors")
    tokenizer_identity = artifacts.get("speech_tokenizer/model.safetensors")
    if talker_identity is not None and tokenizer_identity is not None:
        same_path = talker_identity.path == tokenizer_identity.path
        same_bytes = talker_identity.sha256 == tokenizer_identity.sha256
        if same_path or same_bytes:
            blockers.append(
                "Pure-C Qwen3-TTS model.safetensors and "
                "speech_tokenizer/model.safetensors must be distinct artifacts"
            )

    return PureCQwen3TtsPreflight(
        ready=not blockers,
        model_dir=str(resolved_model_dir) if resolved_model_dir is not None else None,
        checkpoint_model_type=checkpoint_model_type,
        checkpoint_model_size=checkpoint_model_size,
        executable=executable_identity,
        artifacts=artifacts,
        blockers=blockers,
    )
