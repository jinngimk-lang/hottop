from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator

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
VisualMedium = Literal[
    "live-action-cinematic",
    "animation-2d",
    "animation-3d",
    "animation-low-poly",
    "documentary-social",
    "technology-realism",
    "commercial-product",
    "internet-native",
]
ReferenceRightsMode = Literal[
    "analysis-only",
    "public-domain",
    "rights-cleared",
    "unknown",
]


class Evidence(BaseModel):
    url: HttpUrl
    source: str = Field(min_length=1)
    observed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    published_at: datetime | None = None
    source_quality: float | None = Field(default=None, ge=0, le=1)
    note: str | None = None

    @field_validator("source")
    @classmethod
    def normalize_source_identity(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("evidence source must not be blank")
        return value

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

    @field_validator("id")
    @classmethod
    def normalize_id_identity(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("trend id must not be blank")
        return value

    @field_validator("title")
    @classmethod
    def strip_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("title must not be blank")
        return value

    @field_validator("source")
    @classmethod
    def normalize_source_identity(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("trend source must not be blank")
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

    @field_validator("name")
    @classmethod
    def normalize_name_identity(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("product profile name must not be blank")
        return value


class PromotionContext(BaseModel):
    subject_name: str
    subject_type: PromotionSubjectType
    category: str
    primary_job: str | None = None
    primary_pain_point: str | None = None
    primary_differentiator: str | None = None
    semantic_terms: list[str] = Field(default_factory=list)

    @field_validator("subject_name", "category")
    @classmethod
    def normalize_identity_field(cls, value: str, info) -> str:
        value = value.strip()
        if not value:
            field_name = info.field_name.replace("_", " ")
            raise ValueError(f"promotion {field_name} must not be blank")
        return value

    @field_validator("primary_job", "primary_pain_point", "primary_differentiator")
    @classmethod
    def normalize_optional_semantic_field(cls, value: str | None, info) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            field_name = info.field_name.replace("_", " ")
            raise ValueError(f"promotion {field_name} must not be blank")
        return value


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

    @field_validator("name")
    @classmethod
    def normalize_name_identity(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("comparison candidate name must not be blank")
        return value


class CreativeStrategy(BaseModel):
    """Durable creative reframe independent of a specific output renderer."""

    category_default: str | None = None
    deleted_constraint: str | None = None
    new_competition_axis: str | None = None
    bridge_type: BridgeType | None = None
    bridge: str | None = None
    expression_form: ExpressionForm

    @field_validator("category_default", "deleted_constraint", "new_competition_axis", "bridge")
    @classmethod
    def normalize_optional_strategy_text(cls, value: str | None, info) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            field_name = info.field_name.replace("_", " ")
            raise ValueError(f"creative strategy {field_name} must not be blank")
        return value


class VisualReference(BaseModel):
    """Provenance-first abstraction of a visual reference, not a reproduction target."""

    source_url: HttpUrl
    source_title: str = Field(min_length=1)
    source_type: str = Field(min_length=1)
    observed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    visual_medium: VisualMedium | None = None
    expression_form: ExpressionForm | None = None
    bridge_type: BridgeType | None = None
    composition_grammar: list[str] = Field(default_factory=list)
    reveal_pattern: str | None = None
    text_grammar: str | None = None
    why_effective: str | None = None
    what_not_to_copy: list[str] = Field(default_factory=list)
    rights_mode: ReferenceRightsMode = "unknown"
    artifact_hash: str | None = None
    provenance_note: str = Field(min_length=1)

    @field_validator("source_title", "source_type", "provenance_note")
    @classmethod
    def normalize_provenance_identity(cls, value: str, info) -> str:
        value = value.strip()
        if not value:
            field_name = info.field_name.replace("_", " ")
            raise ValueError(f"visual reference {field_name} must not be blank")
        return value

    @field_validator("observed_at")
    @classmethod
    def ensure_reference_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("visual reference timestamp must be timezone-aware")
        return value


class CreativeBeat(BaseModel):
    """One visual beat in a flexible single-image, carousel, split, or narrative concept."""

    scene: str = Field(min_length=1)
    caption: str | None = None
    intent: str = Field(min_length=1)

    @field_validator("scene", "intent")
    @classmethod
    def normalize_render_text(cls, value: str, info) -> str:
        value = value.strip()
        if not value:
            raise ValueError(f"creative beat {info.field_name} must not be blank")
        return value


class CreativeConcept(BaseModel):
    """Renderer-neutral creative contract that is not tied to a four-panel layout."""

    topic: TrendCandidate
    promotion: PromotionContext
    strategy: CreativeStrategy
    comparison_target: str | None = None
    comparison_evidence: list[Evidence] = Field(default_factory=list)
    beats: list[CreativeBeat] = Field(min_length=1, max_length=8)
    visual_medium: VisualMedium
    genre_treatment: str = Field(min_length=1)
    punchlines: list[str] = Field(min_length=1, max_length=3)
    image_prompt: str = Field(min_length=1)
    negative_prompt: str = Field(min_length=1)
    risk_flags: list[str] = Field(default_factory=list)
    claim_status: ClaimStatus = "satire"

    @field_validator("comparison_target")
    @classmethod
    def normalize_comparison_target(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("comparison target must not be blank")
        return value

    @field_validator("genre_treatment", "image_prompt", "negative_prompt")
    @classmethod
    def normalize_required_render_text(cls, value: str, info) -> str:
        value = value.strip()
        if not value:
            field_name = info.field_name.replace("_", " ")
            raise ValueError(f"creative concept {field_name} must not be blank")
        return value

    @field_validator("punchlines")
    @classmethod
    def normalize_punchlines(cls, values: list[str]) -> list[str]:
        normalized = [value.strip() for value in values]
        if any(not value for value in normalized):
            raise ValueError("creative concept punchlines must not contain blank text")
        return normalized

    @model_validator(mode="after")
    def enforce_comparison_claim_safety(self) -> CreativeConcept:
        if self.claim_status == "supported" and not self.comparison_evidence:
            raise ValueError("supported creative claims require comparison evidence")
        if self.comparison_target and self.claim_status == "needs_evidence":
            raise ValueError(
                "named creative comparisons must be supported by evidence or explicit satire"
            )
        return self


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
