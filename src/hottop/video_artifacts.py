from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator

VideoArtifactKind = Literal["ai-generated", "deterministic-non-generative", "operator-provided"]


class VideoShotArtifact(BaseModel):
    """Durable provenance for one shot artifact consumed by composition."""

    shot_index: int = Field(ge=1)
    path: str = Field(min_length=1)
    artifact_kind: VideoArtifactKind
    backend: str = Field(min_length=1)
    degraded_from: str | None = None
    degradation_reason: str | None = None

    @model_validator(mode="after")
    def validate_degradation_provenance(self) -> VideoShotArtifact:
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
        return self


class VideoArtifactManifest(BaseModel):
    """Artifact-level truth for shot provenance after execution/degradation decisions."""

    schema_version: Literal["hottop.video-artifacts.v1"] = "hottop.video-artifacts.v1"
    planned_generation_backend: str = Field(min_length=1)
    shots: list[VideoShotArtifact] = Field(default_factory=list)
