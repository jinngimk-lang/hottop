from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from .models import ProductProfile, TrendCandidate


class GenerationPreflightInput(BaseModel):
    """Per-request evidence gate required before creating a new image or video asset."""

    output_kind: Literal["image", "video"]
    product: ProductProfile
    hotspot: TrendCandidate
    visual_style: str = Field(min_length=1)
    style_rationale: str = Field(min_length=1)
    output_format: str = Field(min_length=1)
    researched_at: datetime
    max_research_age_hours: float = Field(default=6.0, gt=0)
    max_publication_age_hours: float = Field(default=168.0, gt=0)

    @field_validator("visual_style", "style_rationale", "output_format")
    @classmethod
    def normalize_required_text(cls, value: str, info) -> str:
        value = value.strip()
        if not value:
            raise ValueError(f"generation preflight {info.field_name.replace('_', ' ')} must not be blank")
        return value

    @field_validator("researched_at")
    @classmethod
    def ensure_research_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("generation preflight researched_at must be timezone-aware")
        return value


class GenerationPreflightResult(BaseModel):
    schema_version: Literal["hottop.generation-preflight.v1"] = "hottop.generation-preflight.v1"
    ready: bool
    blockers: list[str] = Field(default_factory=list)
    subject_name: str
    hotspot_id: str
    output_kind: Literal["image", "video"]
    visual_style: str
    output_format: str
    research_age_hours: float
    publication_age_hours: float | None = None
    evidence_count: int = Field(ge=0)
    fresh_evidence_count: int = Field(ge=0)


def _age_hours(timestamp: datetime, now: datetime) -> float:
    return max(0.0, (now - timestamp.astimezone(UTC)).total_seconds() / 3600)


def _publication_timestamp(hotspot: TrendCandidate) -> datetime | None:
    if hotspot.published_at is not None:
        published_at = hotspot.published_at
        if published_at.tzinfo is None:
            published_at = published_at.replace(tzinfo=UTC)
        return published_at

    evidence_publications = [
        evidence.published_at
        for evidence in hotspot.evidence
        if evidence.published_at is not None
    ]
    if not evidence_publications:
        return None
    return max(timestamp.astimezone(UTC) for timestamp in evidence_publications)


def evaluate_generation_preflight(
    preflight: GenerationPreflightInput,
    *,
    now: datetime | None = None,
) -> GenerationPreflightResult:
    """Fail closed when the current-hotspot evidence is absent or too old."""

    current = now or datetime.now(UTC)
    if current.tzinfo is None:
        current = current.replace(tzinfo=UTC)
    current = current.astimezone(UTC)

    blockers: list[str] = []
    research_age_hours = _age_hours(preflight.researched_at, current)
    if research_age_hours > preflight.max_research_age_hours:
        blockers.append("research-observation-stale")

    evidence_count = len(preflight.hotspot.evidence)
    if evidence_count == 0:
        blockers.append("hotspot-evidence-missing")
        fresh_evidence_count = 0
    else:
        fresh_evidence_count = sum(
            _age_hours(evidence.observed_at, current) <= preflight.max_research_age_hours
            for evidence in preflight.hotspot.evidence
        )
        if fresh_evidence_count == 0:
            blockers.append("hotspot-evidence-stale")

    publication_timestamp = _publication_timestamp(preflight.hotspot)
    publication_age_hours = (
        _age_hours(publication_timestamp, current)
        if publication_timestamp is not None
        else None
    )
    if (
        publication_age_hours is not None
        and publication_age_hours > preflight.max_publication_age_hours
    ):
        blockers.append("hotspot-publication-stale")

    return GenerationPreflightResult(
        ready=not blockers,
        blockers=blockers,
        subject_name=preflight.product.name,
        hotspot_id=preflight.hotspot.id,
        output_kind=preflight.output_kind,
        visual_style=preflight.visual_style,
        output_format=preflight.output_format,
        research_age_hours=research_age_hours,
        publication_age_hours=publication_age_hours,
        evidence_count=evidence_count,
        fresh_evidence_count=fresh_evidence_count,
    )
