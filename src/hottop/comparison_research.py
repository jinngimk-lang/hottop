from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, Field, HttpUrl, field_validator

from .models import (
    ClaimStatus,
    ComparisonCandidate,
    ComparisonRelation,
    Evidence,
)


class ComparisonResearchResult(BaseModel):
    """One public research observation that can be normalized into a comparison candidate."""

    name: str = Field(min_length=1)
    relation: ComparisonRelation
    url: HttpUrl
    source: str = Field(min_length=1)
    note: str | None = None
    category: str | None = None
    observed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    published_at: datetime | None = None
    source_quality: float | None = Field(default=None, ge=0, le=1)
    recognizability: float = Field(default=0.5, ge=0, le=1)
    category_overlap: float = Field(default=0.5, ge=0, le=1)
    pain_point_contrast: float = Field(default=0.5, ge=0, le=1)
    claim_posture: ClaimStatus = "satire"

    @field_validator("observed_at", "published_at")
    @classmethod
    def ensure_timezone(cls, value: datetime | None) -> datetime | None:
        if value is not None and value.tzinfo is None:
            raise ValueError("comparison research timestamps must be timezone-aware")
        return value


def adapt_comparison_research_results(
    results: list[ComparisonResearchResult],
) -> list[ComparisonCandidate]:
    """Convert public research observations into evidence-bearing internal candidates."""

    candidates: list[ComparisonCandidate] = []
    for result in results:
        evidence = Evidence(
            url=result.url,
            source=result.source,
            observed_at=result.observed_at,
            published_at=result.published_at,
            source_quality=result.source_quality,
            note=result.note,
        )
        candidates.append(
            ComparisonCandidate(
                name=result.name,
                category=result.category,
                relation=result.relation,
                recognizability=result.recognizability,
                category_overlap=result.category_overlap,
                pain_point_contrast=result.pain_point_contrast,
                evidence_quality=result.source_quality if result.source_quality is not None else 0.5,
                evidence=[evidence],
                notes=[result.note] if result.note else [],
                claim_posture=result.claim_posture,
            )
        )
    return candidates
