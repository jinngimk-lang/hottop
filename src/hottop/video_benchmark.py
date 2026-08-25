from __future__ import annotations

import hashlib
import pathlib
import typing

import pydantic

from .video_artifacts import VideoArtifactManifest

Sha256 = typing.Annotated[str, pydantic.Field(pattern=r"^[0-9a-f]{64}$")]


class ReferenceContinuityPolicy(pydantic.BaseModel):
    min_reference_adherence: float = pydantic.Field(default=0.75, ge=0, le=1)
    min_cross_shot_identity: float = pydantic.Field(default=0.75, ge=0, le=1)
    min_evaluated_shots: int = pydantic.Field(default=2, ge=2)


class SubjectContinuityEvidence(pydantic.BaseModel):
    subject_id: str = pydantic.Field(min_length=1)
    reference_sha256: Sha256
    shot_sha256s: list[Sha256] = pydantic.Field(min_length=1)
    reference_adherence: float = pydantic.Field(ge=0, le=1)
    cross_shot_identity: float = pydantic.Field(ge=0, le=1)

    @pydantic.field_validator("shot_sha256s")
    @classmethod
    def require_unique_shot_artifacts(cls, value: list[str]) -> list[str]:
        if len(set(value)) != len(value):
            raise ValueError("reference continuity benchmark requires unique shot artifacts")
        return value


class ReferenceContinuityBenchmark(pydantic.BaseModel):
    schema_version: typing.Literal["hottop.reference-continuity-benchmark.v1"] = (
        "hottop.reference-continuity-benchmark.v1"
    )
    candidate_id: str = pydantic.Field(min_length=1)
    candidate_revision: str = pydantic.Field(min_length=1)
    render_source: str = pydantic.Field(min_length=1)
    config_name: str = pydantic.Field(min_length=1)
    evaluator_id: str = pydantic.Field(min_length=1)
    evaluator_revision: str = pydantic.Field(min_length=1)
    subjects: list[SubjectContinuityEvidence] = pydantic.Field(min_length=1)


class SubjectContinuityReport(pydantic.BaseModel):
    subject_id: str
    evaluated_shots: int
    pass_: bool
    reasons: list[str] = pydantic.Field(default_factory=list)


class ReferenceContinuityReport(pydantic.BaseModel):
    schema_version: typing.Literal["hottop.reference-continuity-report.v1"] = (
        "hottop.reference-continuity-report.v1"
    )
    pass_: bool
    subject_reports: list[SubjectContinuityReport]
    reasons: list[str] = pydantic.Field(default_factory=list)


def _sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def verify_reference_continuity_artifacts(
    evidence: ReferenceContinuityBenchmark,
    manifest: VideoArtifactManifest,
    reference_paths: dict[str, pathlib.Path],
) -> None:
    """Bind visual-continuity scores to the exact reference and generated shot bytes."""

    manifest.verify_required_byte_identity()
    manifest_hashes: set[str] = set()
    for artifact in manifest.shots:
        if artifact.sha256 is None or artifact.size_bytes is None:
            raise ValueError("continuity benchmark requires byte-bound shot artifacts")
        manifest_hashes.add(artifact.sha256)

    for subject in evidence.subjects:
        reference_path = reference_paths.get(subject.subject_id)
        if reference_path is None:
            raise ValueError(f"reference path missing for subject {subject.subject_id}")
        if not reference_path.is_file():
            raise ValueError(f"reference path is not a file: {reference_path}")
        if _sha256(reference_path) != subject.reference_sha256:
            raise ValueError(f"reference content mismatch for subject {subject.subject_id}")
        missing_hashes = set(subject.shot_sha256s) - manifest_hashes
        if missing_hashes:
            raise ValueError(
                f"benchmark shot hashes not bound to artifact manifest for {subject.subject_id}"
            )


def evaluate_reference_continuity(
    evidence: ReferenceContinuityBenchmark,
    policy: ReferenceContinuityPolicy | None = None,
) -> ReferenceContinuityReport:
    """Evaluate byte-bound visual identity evidence without choosing an evaluator implementation."""

    policy = policy or ReferenceContinuityPolicy()
    subject_reports: list[SubjectContinuityReport] = []
    reasons: list[str] = []

    for subject in evidence.subjects:
        subject_reasons: list[str] = []
        evaluated_shots = len(subject.shot_sha256s)
        if evaluated_shots < policy.min_evaluated_shots:
            subject_reasons.append(
                f"evaluated shots {evaluated_shots} below {policy.min_evaluated_shots}"
            )
        if subject.reference_adherence < policy.min_reference_adherence:
            subject_reasons.append(
                "reference adherence "
                f"{subject.reference_adherence:.3f} below {policy.min_reference_adherence:.3f}"
            )
        if subject.cross_shot_identity < policy.min_cross_shot_identity:
            subject_reasons.append(
                "cross-shot identity "
                f"{subject.cross_shot_identity:.3f} below {policy.min_cross_shot_identity:.3f}"
            )

        subject_reports.append(
            SubjectContinuityReport(
                subject_id=subject.subject_id,
                evaluated_shots=evaluated_shots,
                pass_=not subject_reasons,
                reasons=subject_reasons,
            )
        )
        reasons.extend(f"{subject.subject_id}: {reason}" for reason in subject_reasons)

    return ReferenceContinuityReport(
        pass_=not reasons,
        subject_reports=subject_reports,
        reasons=reasons,
    )
