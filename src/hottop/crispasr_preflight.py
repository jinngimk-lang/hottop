from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from .qwentts_cpp_preflight import LocalArtifactIdentity, _identity


class CrispAsrPreflight(BaseModel):
    schema_version: Literal["hottop.crispasr-preflight.v1"] = "hottop.crispasr-preflight.v1"
    ready: bool
    executed: Literal[False] = False
    network_access: Literal[False] = False
    auto_download: Literal[False] = False
    executable: LocalArtifactIdentity | None = None
    talker_gguf: LocalArtifactIdentity | None = None
    tokenizer_gguf: LocalArtifactIdentity | None = None
    blockers: list[str]


def inspect_crispasr_inputs(
    *,
    executable: Path,
    talker_gguf: Path,
    tokenizer_gguf: Path,
) -> CrispAsrPreflight:
    """Bind operator-provisioned CrispASR benchmark inputs without executing anything."""

    executable_identity, executable_blockers = _identity(
        executable,
        label="CrispASR executable",
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
            blockers.append("CrispASR executable and model GGUF artifacts must be distinct")

    if talker_identity is not None and tokenizer_identity is not None:
        same_path = talker_identity.path == tokenizer_identity.path
        same_bytes = talker_identity.sha256 == tokenizer_identity.sha256
        if same_path or same_bytes:
            blockers.append("talker GGUF and tokenizer GGUF must be distinct artifacts")

    return CrispAsrPreflight(
        ready=not blockers,
        executable=executable_identity,
        talker_gguf=talker_identity,
        tokenizer_gguf=tokenizer_identity,
        blockers=blockers,
    )
