from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, model_validator

VideoArtifactKind = Literal[
    "ai-generated",
    "deterministic-generated",
    "deterministic-non-generative",
    "operator-provided",
]
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _file_byte_identity(path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    size_bytes = 0
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
            size_bytes += len(chunk)
    return digest.hexdigest(), size_bytes


class VideoShotArtifact(BaseModel):
    """Durable provenance for one shot artifact consumed by composition."""

    shot_index: int = Field(ge=1)
    path: str = Field(min_length=1)
    artifact_kind: VideoArtifactKind
    backend: str = Field(min_length=1)
    candidate_id: str | None = None
    candidate_revision: str | None = None
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
            labels = {
                "ai-generated": "AI-generated",
                "deterministic-generated": "deterministic generated",
                "operator-provided": "operator-provided",
            }
            raise ValueError(
                f"{labels[self.artifact_kind]} artifacts cannot carry deterministic degradation metadata"
            )

        if (self.candidate_id is None) != (self.candidate_revision is None):
            raise ValueError("candidate provenance requires both candidate_id and candidate_revision")
        if self.candidate_id is not None:
            self.candidate_id = self.candidate_id.strip()
            self.candidate_revision = self.candidate_revision.strip() if self.candidate_revision else ""
            if not self.candidate_id or not self.candidate_revision:
                raise ValueError("candidate provenance must not be blank")

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

    def verify_required_byte_identity(self) -> None:
        required_backends = {"zero-cost-router", "software3d", "lightx2v-operator"}
        if self.planned_generation_backend not in required_backends:
            return
        labels = {
            "zero-cost-router": "zero-cost",
            "software3d": "software3d",
            "lightx2v-operator": "LightX2V",
        }
        backend_label = labels[self.planned_generation_backend]
        for artifact in self.shots:
            if artifact.sha256 is None or artifact.size_bytes is None:
                raise ValueError(f"{backend_label} artifact byte identity missing")
            artifact_path = Path(artifact.path)
            if not artifact_path.is_file():
                raise ValueError(f"{backend_label} artifact path is not a file: {artifact.path}")
            actual_sha256, actual_size = _file_byte_identity(artifact_path)
            if actual_size != artifact.size_bytes or actual_sha256 != artifact.sha256:
                raise ValueError(f"{backend_label} artifact content mismatch")

    def verify_zero_cost_byte_identity(self) -> None:
        """Backward-compatible alias retained for callers that predate software3d provenance."""

        self.verify_required_byte_identity()

    @classmethod
    def model_validate_json(
        cls,
        json_data: str | bytes | bytearray,
        **kwargs: object,
    ) -> VideoArtifactManifest:
        manifest = super().model_validate_json(json_data, **kwargs)
        manifest.verify_required_byte_identity()
        return manifest
