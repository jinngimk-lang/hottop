from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from .qwentts_cpp_preflight import LocalArtifactIdentity, _identity


class AudioCppPreflight(BaseModel):
    schema_version: Literal["hottop.audio-cpp-preflight.v1"] = "hottop.audio-cpp-preflight.v1"
    ready: bool
    executed: Literal[False] = False
    network_access: Literal[False] = False
    auto_download: Literal[False] = False
    model_dir: str | None = None
    executable: LocalArtifactIdentity | None = None
    talker_gguf: LocalArtifactIdentity | None = None
    tokenizer_gguf: LocalArtifactIdentity | None = None
    blockers: list[str]


def inspect_audio_cpp_inputs(*, executable: Path, model_dir: Path) -> AudioCppPreflight:
    """Bind operator-provisioned audio.cpp CustomVoice inputs without executing anything."""

    blockers: list[str] = []
    resolved_model_dir: Path | None = None
    try:
        resolved_model_dir = model_dir.resolve(strict=True)
    except OSError:
        blockers.append(f"audio.cpp model directory does not exist: {model_dir}")

    if resolved_model_dir is not None and not resolved_model_dir.is_dir():
        blockers.append(f"audio.cpp model directory is not a directory: {resolved_model_dir}")
        resolved_model_dir = None

    executable_identity, executable_blockers = _identity(
        executable,
        label="audio.cpp executable",
        require_executable=True,
    )
    blockers.extend(executable_blockers)

    talker_identity: LocalArtifactIdentity | None = None
    tokenizer_identity: LocalArtifactIdentity | None = None
    if resolved_model_dir is not None:
        talker_path = resolved_model_dir / "model.gguf"
        tokenizer_path = resolved_model_dir / "speech_tokenizer" / "model.gguf"
        talker_identity, talker_blockers = _identity(
            talker_path,
            label="audio.cpp model.gguf",
            require_gguf=True,
        )
        tokenizer_identity, tokenizer_blockers = _identity(
            tokenizer_path,
            label="audio.cpp speech_tokenizer/model.gguf",
            require_gguf=True,
        )
        blockers.extend(talker_blockers)
        blockers.extend(tokenizer_blockers)

    if executable_identity is not None:
        model_identities = [identity for identity in (talker_identity, tokenizer_identity) if identity]
        executable_reused_as_model = any(
            executable_identity.path == identity.path or executable_identity.sha256 == identity.sha256
            for identity in model_identities
        )
        if executable_reused_as_model:
            blockers.append("audio.cpp executable and model GGUF artifacts must be distinct")

    if talker_identity is not None and tokenizer_identity is not None:
        same_path = talker_identity.path == tokenizer_identity.path
        same_bytes = talker_identity.sha256 == tokenizer_identity.sha256
        if same_path or same_bytes:
            blockers.append(
                "audio.cpp model.gguf and speech_tokenizer/model.gguf must be distinct artifacts"
            )

    return AudioCppPreflight(
        ready=not blockers,
        model_dir=str(resolved_model_dir) if resolved_model_dir is not None else None,
        executable=executable_identity,
        talker_gguf=talker_identity,
        tokenizer_gguf=tokenizer_identity,
        blockers=blockers,
    )
