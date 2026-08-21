from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl, field_validator

ClaimStatus = Literal["satire", "supported", "needs_evidence"]
PromotionSubjectType = Literal[
    "brand",
    "product",
    "service",
    "feature",
    "campaign",
    "person",
    "idea",
    "keyword",
    "tool",
]
ComparisonRelation = Literal[
    "direct-competitor",
    "adjacent-substitute",
    "incumbent-default",
    "legacy-workflow",
    "manual-workaround",
]
BridgeType = Literal[
    "shape-material",
    "action-motion",
    "role",
    "function",
    "emotion-ritual",
    "language-symbol",
]
ExpressionForm = Literal[
    "single-visual-metaphor",
    "swipe-reveal",
    "four-panel",
    "faux-film-still",
    "split-old-vs-new",
    "product-as-prop",
]


class Evidence(BaseModel):
    url: HttpUrl
    source: str = Field(min_length=1)
    observed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    published_at: datetime | None = None
    source_quality: float | None = Field(default=None, ge=0, le=1)
    note: str | None = None

    @field_validator("observed_at", "published_at")
    @classmethod
    def ensure_timezone(cls, value: datetime | None) -> datetime | None:
        if value is not None and value.tzinfo is None:
            raise ValueError("evidence timestamps must be timezone-aware")
        return value


class TrendCandidate(BaseModel):
    id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    url: HttpUrl
    source: str = Field(min_length=1)
    source_rank: int | None = Field(default=None, ge=1)
    source_quality: float | None = Field(default=None, ge=0, le=1)
    published_at: datetime | None = None
    summary: str | None = None
    tags: list[str] = Field(default_factory=list)
    metrics: dict[str, float] = Field(default_factory=dict)
    evidence: list[Evidence] = Field(default_factory=list)

    @field_validator("title")
    @classmethod
    def strip_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("title must not be blank")
        return value


class TrendScore(BaseModel):
    total: float = Field(ge=0, le=100)
    dimensions: dict[str, float]


class ProductProfile(BaseModel):
    """Backward-compatible promotion profile for any subject, not only AI products."""

    name: str = Field(min_length=1)
    url: HttpUrl | None = None
    subject_type: PromotionSubjectType = "product"
    category: str | None = None
    keywords: list[str] = Field(default_factory=list)
    jobs_to_be_done: list[str] = Field(default_factory=list)
    pain_points_solved: list[str] = Field(default_factory=list)
    differentiators: list[str] = Field(default_factory=list)
    known_alternatives: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    preferred_roles: list[str] = Field(default_factory=lambda: ["solver", "breaker", "winner"])
    default_claim_status: ClaimStatus = "satire"


class PromotionContext(BaseModel):
    subject_name: str
    subject_type: PromotionSubjectType
    category: str
    primary_job: str | None = None
    primary_pain_point: str | None = None
    primary_differentiator: str | None = None
    semantic_terms: list[str] = Field(default_factory=list)


class ComparisonCandidate(BaseModel):
    name: str = Field(min_length=1)
    category: str | None = None
    relation: ComparisonRelation
    recognizability: float = Field(default=0.5, ge=0, le=1)
    category_overlap: float = Field(default=0.5, ge=0, le=1)
    pain_point_contrast: float = Field(default=0.5, ge=0, le=1)
    evidence_quality: float = Field(default=0, ge=0, le=1)
    evidence: list[Evidence] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    claim_posture: ClaimStatus = "satire"


class CreativeStrategy(BaseModel):
    """Durable creative reframe independent of a specific output renderer."""

    category_default: str | None = None
    deleted_constraint: str | None = None
    new_competition_axis: str | None = None
    bridge_type: BridgeType | None = None
    bridge: str | None = None
    expression_form: ExpressionForm


class RoleMap(BaseModel):
    topic_world: str
    conflict: str
    promoted_product: str
    product_role: str
    comparison_target: str | None = None
    comparison_role: str | None = None
    archetype: str
    why_it_maps: str


class Panel(BaseModel):
    scene: str
    caption: str
    intent: str


class MemeBrief(BaseModel):
    topic: TrendCandidate
    role_map: RoleMap
    panels: list[Panel] = Field(min_length=4, max_length=4)
    punchlines: list[str] = Field(min_length=1, max_length=3)
    image_prompt: str
    negative_prompt: str
    risk_flags: list[str] = Field(default_factory=list)
    claim_status: ClaimStatus = "satire"
