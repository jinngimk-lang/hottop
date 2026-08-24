from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, Field, model_validator

VideoArtifactKind = Literal["ai-generated", "deterministic-non-generative", "operator-provided"]
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class VideoShotArtifact(BaseModel):
    """Durable provenance for one shot artifact consumed by composition."""

    shot_index: int = Field(ge=1)
    path: str = Field(min_length=1)
    artifact_kind: VideoArtifactKind
    backend: str = Field(min_length=1)
    degraded_from: str | None = None
    degradation_reason: str | None = None
    sha256: str | None = None
    size_bytes: int | None = Field(default=None, gt=0)

    @model_validator(mode="after")
    def validate_provenance(self) -> VideoShotArtifact:
        if self.artifact_kind == "deterministic-non-generative":
            if not self.degraded_from:
                raise ValueError("deterministic fallback artifacts require degraded_from")
            if not self.degradation_reason:
                raise ValueError("deterministic fallback artifacts require degradation_reason")
        elif self.degraded_from is not None or self.degradation_reason is not None:
            raise ValueError(
                "AI-generated artifacts cannot carry deterministic degradation metadata"
                if self.artifact_kind == "ai-generated"
                else "operator-provided artifacts cannot carry deterministic degradation metadata"
            )

        if (self.sha256 is None) != (self.size_bytes is None):
            raise ValueError("artifact byte identity requires both sha256 and size_bytes")
        if self.sha256 is not None and not _SHA256_RE.fullmatch(self.sha256):
            raise ValueError("artifact sha256 must be a lowercase 64-character hex digest")
        return self


class VideoArtifactManifest(BaseModel):
    """Artifact-level truth for shot provenance after execution/degradation decisions."""

    schema_version: Literal["hottop.video-artifacts.v1"] = "hottop.video-artifacts.v1"
    planned_generation_backend: str = Field(min_length=1)
    shots: list[VideoShotArtifact] = Field(default_factory=list)
