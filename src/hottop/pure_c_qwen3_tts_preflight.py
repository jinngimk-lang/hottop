from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from .qwentts_cpp_preflight import LocalArtifactIdentity, _identity

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
            identity, artifact_blockers = _identity(
                resolved_model_dir / relative_path,
                label=f"Pure-C Qwen3-TTS {relative_path}",
            )
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
