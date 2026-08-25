from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

from .models import BridgeType, CreativeStrategy, ExpressionForm, VisualMedium


class CreativeSignals(BaseModel):
    """Signals used to choose the smallest expression form that makes an idea land."""

    has_deleted_constraint: bool = False
    needs_reveal_sequence: bool = False
    product_embodies_bridge: bool = False
    bridge_type: BridgeType | None = None
    has_narrative_conflict: bool = False
    is_cinematic: bool = False


class BridgeCandidate(BaseModel):
    """A possible natural link between the promoted subject and the hotspot."""

    bridge_type: BridgeType
    bridge: str = Field(min_length=1)
    product_specificity: float = Field(ge=0, le=1)
    hotspot_fit: float = Field(ge=0, le=1)
    visual_clarity: float = Field(ge=0, le=1)
    surprise: float = Field(ge=0, le=1)

    @field_validator("bridge")
    @classmethod
    def normalize_bridge(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("bridge candidate text must not be blank")
        return value

    @property
    def score(self) -> float:
        return (
            0.35 * self.product_specificity
            + 0.30 * self.hotspot_fit
            + 0.20 * self.visual_clarity
            + 0.15 * self.surprise
        )


class CreativeReview(BaseModel):
    """Structured version of the repository's seven-part creative review gate."""

    name: str = Field(min_length=1)
    instant_comprehension: float = Field(ge=0, le=1)
    natural_linkage: float = Field(ge=0, le=1)
    product_centrality: float = Field(ge=0, le=1)
    surprise: float = Field(ge=0, le=1)
    ownability: float = Field(ge=0, le=1)
    evidence_safety: float = Field(ge=0, le=1)
    original_execution: float = Field(ge=0, le=1)

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("creative review name must not be blank")
        return value

    @property
    def total(self) -> float:
        return (
            0.15 * self.instant_comprehension
            + 0.18 * self.natural_linkage
            + 0.18 * self.product_centrality
            + 0.12 * self.surprise
            + 0.18 * self.ownability
            + 0.10 * self.evidence_safety
            + 0.09 * self.original_execution
        )

    @property
    def passes(self) -> bool:
        hard_floor = min(
            self.natural_linkage,
            self.product_centrality,
            self.ownability,
            self.original_execution,
        )
        return (
            self.total >= 0.70
            and self.instant_comprehension >= 0.60
            and self.evidence_safety >= 0.50
            and hard_floor >= 0.55
        )


class CreativeContextReview(BaseModel):
    """Request-specific ranking signals that never override the base creative hard gate."""

    name: str | None = None
    platform_fit: float = Field(ge=0, le=1)
    style_fit: float = Field(ge=0, le=1)
    campaign_goal_fit: float = Field(ge=0, le=1)
    ambition_fit: float = Field(ge=0, le=1)
    project_shape_fit: float = Field(ge=0, le=1)
    hotspot_native_fit: float = Field(ge=0, le=1)
    humor_or_delight: float = Field(default=0.5, ge=0, le=1)
    humor_expected: bool = False

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("context review name must not be blank")
        return value

    @property
    def total(self) -> float:
        base = (
            0.22 * self.platform_fit
            + 0.18 * self.style_fit
            + 0.18 * self.campaign_goal_fit
            + 0.14 * self.ambition_fit
            + 0.16 * self.project_shape_fit
            + 0.12 * self.hotspot_native_fit
        )
        if not self.humor_expected:
            return base
        return 0.94 * base + 0.06 * self.humor_or_delight


class ContextualCreativeReview(BaseModel):
    base: CreativeReview
    context: CreativeContextReview

    @property
    def passes(self) -> bool:
        return self.base.passes

    @property
    def context_total(self) -> float:
        return self.context.total

    @property
    def total(self) -> float:
        return 0.72 * self.base.total + 0.28 * self.context_total


def review_with_context(
    base: CreativeReview,
    context: CreativeContextReview,
) -> ContextualCreativeReview:
    return ContextualCreativeReview(base=base, context=context)


def select_best_contextual_review(
    candidates: list[ContextualCreativeReview],
) -> ContextualCreativeReview:
    if not candidates:
        raise ValueError("at least one contextual creative review is required")
    passing = [candidate for candidate in candidates if candidate.passes]
    return max(passing or candidates, key=lambda candidate: candidate.total)


def select_expression_form(signals: CreativeSignals) -> ExpressionForm:
    """Choose format by creative strength rather than a permanent four-panel default."""

    if signals.has_deleted_constraint:
        return "split-old-vs-new"
    if signals.needs_reveal_sequence:
        return "swipe-reveal"
    if signals.product_embodies_bridge:
        return "product-as-prop"
    if signals.has_narrative_conflict:
        return "four-panel"
    if signals.is_cinematic:
        return "faux-film-still"
    return "single-visual-metaphor"


def select_best_bridge(candidates: list[BridgeCandidate]) -> BridgeCandidate:
    """Prefer an ownable, hotspot-native visual link over a generic role mapping."""

    if not candidates:
        raise ValueError("at least one bridge candidate is required")
    return max(candidates, key=lambda candidate: candidate.score)


def select_best_review(candidates: list[CreativeReview]) -> CreativeReview:
    """Prefer a direction that clears the gate; otherwise return the strongest diagnostic candidate."""

    if not candidates:
        raise ValueError("at least one creative review is required")
    passing = [candidate for candidate in candidates if candidate.passes]
    return max(passing or candidates, key=lambda candidate: candidate.total)


def build_creative_strategy(
    *,
    category_default: str | None,
    deleted_constraint: str | None,
    new_competition_axis: str | None,
    bridge_candidates: list[BridgeCandidate],
    signals: CreativeSignals,
) -> CreativeStrategy:
    """Combine category reframing, bridge ranking and expression-form selection."""

    bridge = select_best_bridge(bridge_candidates)
    return CreativeStrategy(
        category_default=category_default,
        deleted_constraint=deleted_constraint,
        new_competition_axis=new_competition_axis,
        bridge_type=bridge.bridge_type,
        bridge=bridge.bridge,
        expression_form=select_expression_form(signals),
    )


def select_visual_medium(*, tags: list[str], subject_category: str | None = None) -> VisualMedium:
    """Match the hotspot's native medium first, then fall back to subject category."""

    normalized = {tag.strip().lower().replace("_", "-") for tag in tags if tag.strip()}
    category = (subject_category or "").strip().lower()

    if normalized & {"film", "movie", "cinema", "live-action", "live action"}:
        return "live-action-cinematic"

    if normalized & {"animation", "anime", "cartoon", "animated"}:
        if normalized & {"low-poly", "lowpoly", "low poly"}:
            return "animation-low-poly"
        if normalized & {"3d", "cgi", "cg"}:
            return "animation-3d"
        return "animation-2d"

    if normalized & {"social", "creator", "internet-personality", "documentary", "real-world"}:
        return "documentary-social"

    if normalized & {"technology", "tech", "ai", "software"}:
        return "technology-realism"

    if normalized & {"meme", "internet-native", "viral-format"}:
        return "internet-native"

    if any(
        term in category
        for term in ("food", "beverage", "consumer", "fashion", "beauty", "cosmetic", "retail")
    ):
        return "commercial-product"

    if any(term in category for term in ("software", "technology", "tech", "ai", "saas")):
        return "technology-realism"

    return "internet-native"
