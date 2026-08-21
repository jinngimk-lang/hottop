from __future__ import annotations

from pydantic import BaseModel, Field

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

    @property
    def score(self) -> float:
        return (
            0.35 * self.product_specificity
            + 0.30 * self.hotspot_fit
            + 0.20 * self.visual_clarity
            + 0.15 * self.surprise
        )


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
