from __future__ import annotations

import typing

import pydantic


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
