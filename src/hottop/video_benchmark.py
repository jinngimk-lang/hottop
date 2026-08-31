from __future__ import annotations

import hashlib
import json
import pathlib
import typing

import pydantic

from .video_artifacts import VideoArtifactManifest, VideoShotArtifact
from .video_production import VideoProductionPlan

Sha256 = typing.Annotated[str, pydantic.Field(pattern=r"^[0-9a-f]{64}$")]


class ReferenceContinuityPolicy(pydantic.BaseModel):
    min_reference_adherence: float = pydantic.Field(default=0.75, ge=0, le=1)
    min_cross_shot_identity: float = pydantic.Field(default=0.75, ge=0, le=1)
    min_evaluated_shots: int = pydantic.Field(default=2, ge=2)
    require_motion_fidelity: bool = False
    min_motion_fidelity: float = pydantic.Field(default=0.65, ge=0, le=1)
    min_reference_pose_diversity: float = pydantic.Field(default=0.20, ge=0, le=1)


class SubjectContinuityEvidence(pydantic.BaseModel):
    subject_id: str = pydantic.Field(min_length=1)
    reference_sha256: Sha256
    shot_sha256s: list[Sha256] = pydantic.Field(min_length=1)
    reference_adherence: float = pydantic.Field(ge=0, le=1)
    cross_shot_identity: float = pydantic.Field(ge=0, le=1)
    motion_fidelity: float | None = pydantic.Field(default=None, ge=0, le=1)
    reference_pose_diversity: float | None = pydantic.Field(default=None, ge=0, le=1)
    motion_spec_sha256: Sha256 | None = None

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
    generation_config_sha256: Sha256 | None = None
    generation_config_size_bytes: int | None = pydantic.Field(default=None, gt=0)
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


def motion_spec_sha256_for_subject(plan: VideoProductionPlan, subject_id: str) -> str:
    """Hash the exact requested-action instructions for one subject in plan order."""

    motion_spec = []
    for shot in plan.shots:
        reference = shot.reference
        if reference is None or reference.subject_id != subject_id:
            continue
        motion_spec.append(
            {
                "shot_index": shot.index,
                "scene": shot.scene,
                "intent": shot.intent,
                "continuity_instruction": shot.continuity_instruction,
                "generation_prompt": shot.generation_prompt,
                "negative_prompt": shot.negative_prompt,
            }
        )
    if not motion_spec:
        raise ValueError(f"subject {subject_id} has no motion spec in the video plan")
    canonical = json.dumps(
        motion_spec,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _subject_plan_bindings(
    manifest: VideoArtifactManifest,
    plan: VideoProductionPlan,
) -> tuple[dict[str, set[str]], dict[str, pathlib.Path]]:
    artifacts_by_index = {artifact.shot_index: artifact for artifact in manifest.shots}
    if len(artifacts_by_index) != len(manifest.shots):
        raise ValueError("continuity benchmark requires unique artifact shot indexes")

    hashes_by_subject: dict[str, set[str]] = {}
    references_by_subject: dict[str, pathlib.Path] = {}
    for shot in plan.shots:
        reference = shot.reference
        if reference is None or reference.subject_id is None:
            continue
        artifact = artifacts_by_index.get(shot.index)
        if artifact is None or artifact.sha256 is None:
            raise ValueError(
                f"artifact missing for subject {reference.subject_id} plan shot {shot.index}"
            )
        subject_id = reference.subject_id
        subject_hashes = hashes_by_subject.setdefault(subject_id, set())
        if artifact.sha256 in subject_hashes:
            raise ValueError(
                f"subject {subject_id} continuity benchmark requires unique subject-bearing shot artifacts"
            )
        subject_hashes.add(artifact.sha256)
        planned_reference = pathlib.Path(reference.image_path).resolve()
        prior_reference = references_by_subject.get(subject_id)
        if prior_reference is not None and prior_reference != planned_reference:
            raise ValueError(f"subject {subject_id} has conflicting references in the video plan")
        references_by_subject[subject_id] = planned_reference
    return hashes_by_subject, references_by_subject


def _verify_candidate_provenance(
    evidence: ReferenceContinuityBenchmark,
    artifacts: list[VideoShotArtifact],
) -> None:
    lightx2v_generation_configs: set[tuple[str, int]] = set()
    for artifact in artifacts:
        requires_candidate_provenance = artifact.backend.startswith("lightx2v:")
        if requires_candidate_provenance and (
            artifact.candidate_id is None or artifact.candidate_revision is None
        ):
            raise ValueError("LightX2V continuity artifacts require candidate provenance")
        if artifact.candidate_id is not None:
            if artifact.candidate_id != evidence.candidate_id:
                raise ValueError(
                    "continuity benchmark candidate id does not match generated artifact provenance"
                )
            if artifact.candidate_revision != evidence.candidate_revision:
                raise ValueError(
                    "continuity benchmark candidate revision does not match generated artifact provenance"
                )
        if not requires_candidate_provenance:
            continue
        if (
            artifact.generation_config_sha256 is None
            or artifact.generation_config_size_bytes is None
        ):
            raise ValueError(
                "LightX2V continuity artifacts require generation config provenance"
            )
        lightx2v_generation_configs.add(
            (
                artifact.generation_config_sha256,
                artifact.generation_config_size_bytes,
            )
        )

    if len(lightx2v_generation_configs) > 1:
        raise ValueError(
            "LightX2V continuity artifacts must share one generation config provenance"
        )
    if lightx2v_generation_configs:
        if (
            evidence.generation_config_sha256 is None
            or evidence.generation_config_size_bytes is None
        ):
            raise ValueError(
                "LightX2V continuity benchmark requires generation config provenance"
            )
        evidence_generation_config = (
            evidence.generation_config_sha256,
            evidence.generation_config_size_bytes,
        )
        if lightx2v_generation_configs != {evidence_generation_config}:
            raise ValueError(
                "continuity benchmark generation config provenance does not match generated artifact provenance"
            )


def verify_reference_continuity_artifacts(
    evidence: ReferenceContinuityBenchmark,
    manifest: VideoArtifactManifest,
    reference_paths: dict[str, pathlib.Path],
    *,
    plan: VideoProductionPlan,
) -> None:
    """Bind visual-continuity scores to exact production reference and subject-shot bytes."""

    if evidence.config_name != plan.config_name:
        raise ValueError("continuity benchmark config name does not match the video plan config name")

    manifest.verify_required_byte_identity()
    subject_hashes, planned_references = _subject_plan_bindings(manifest, plan)
    subject_by_shot_hash: dict[str, str] = {}
    for subject_id, planned_hashes in subject_hashes.items():
        for shot_hash in planned_hashes:
            prior_subject = subject_by_shot_hash.setdefault(shot_hash, subject_id)
            if prior_subject != subject_id:
                raise ValueError(
                    "distinct subjects require distinct subject-bearing shot artifacts"
                )
    evidence_subject_ids = {subject.subject_id for subject in evidence.subjects}
    if set(subject_hashes) - evidence_subject_ids:
        raise ValueError(
            "continuity benchmark must cover every reference-bearing subject in the video plan"
        )
    artifacts_by_hash = {
        artifact.sha256: artifact for artifact in manifest.shots if artifact.sha256 is not None
    }

    for subject in evidence.subjects:
        reference_path = reference_paths.get(subject.subject_id)
        if reference_path is None:
            raise ValueError(f"reference path missing for subject {subject.subject_id}")
        if not reference_path.is_file():
            raise ValueError(f"reference path is not a file: {reference_path}")

        planned_reference = planned_references.get(subject.subject_id)
        if planned_reference is None:
            raise ValueError(
                f"subject {subject.subject_id} has no reference-bearing shots in the video plan"
            )
        if reference_path.resolve() != planned_reference:
            raise ValueError(
                f"reference path for subject {subject.subject_id} does not match the video plan reference"
            )
        if _sha256(reference_path) != subject.reference_sha256:
            raise ValueError(f"reference content mismatch for subject {subject.subject_id}")

        allowed_hashes = subject_hashes.get(subject.subject_id)
        if not allowed_hashes:
            raise ValueError(
                f"subject {subject.subject_id} has no referenced shots in the video plan"
            )
        evidence_hashes = set(subject.shot_sha256s)
        foreign_hashes = evidence_hashes - allowed_hashes
        if foreign_hashes:
            raise ValueError(
                f"benchmark shot hashes are not bound to subject {subject.subject_id} in the video plan"
            )
        missing_hashes = allowed_hashes - evidence_hashes
        if missing_hashes:
            raise ValueError(
                f"benchmark coverage for subject {subject.subject_id} must include all subject-bearing plan shots"
            )
        evaluated_artifacts = [artifacts_by_hash[shot_hash] for shot_hash in subject.shot_sha256s]
        _verify_candidate_provenance(evidence, evaluated_artifacts)

        has_motion_evidence = (
            subject.motion_fidelity is not None or subject.reference_pose_diversity is not None
        )
        if has_motion_evidence:
            if subject.motion_spec_sha256 is None:
                raise ValueError(
                    f"motion spec digest missing for subject {subject.subject_id} motion evidence"
                )
            expected_motion_spec = motion_spec_sha256_for_subject(plan, subject.subject_id)
            if subject.motion_spec_sha256 != expected_motion_spec:
                raise ValueError(
                    f"motion spec digest mismatch for subject {subject.subject_id} motion evidence"
                )


def evaluate_reference_continuity(
    evidence: ReferenceContinuityBenchmark,
    policy: ReferenceContinuityPolicy | None = None,
) -> ReferenceContinuityReport:
    """Evaluate byte-bound identity and explicit motion evidence without choosing an evaluator."""

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

        if policy.require_motion_fidelity:
            if subject.motion_fidelity is None or subject.reference_pose_diversity is None:
                subject_reasons.append("motion evidence missing for identity + motion claim")
            else:
                if subject.motion_fidelity < policy.min_motion_fidelity:
                    subject_reasons.append(
                        "motion fidelity "
                        f"{subject.motion_fidelity:.3f} below {policy.min_motion_fidelity:.3f}"
                    )
                if subject.reference_pose_diversity < policy.min_reference_pose_diversity:
                    subject_reasons.append(
                        "reference-pose diversity "
                        f"{subject.reference_pose_diversity:.3f} below "
                        f"{policy.min_reference_pose_diversity:.3f}"
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
