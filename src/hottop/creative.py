from __future__ import annotations

from pydantic import BaseModel, Field

from .models import BridgeType, ExpressionForm


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
