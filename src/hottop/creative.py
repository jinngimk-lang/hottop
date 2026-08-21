from __future__ import annotations

from pydantic import BaseModel

from .models import BridgeType, ExpressionForm


class CreativeSignals(BaseModel):
    """Signals used to choose the smallest expression form that makes an idea land."""

    has_deleted_constraint: bool = False
    needs_reveal_sequence: bool = False
    product_embodies_bridge: bool = False
    bridge_type: BridgeType | None = None
    has_narrative_conflict: bool = False
    is_cinematic: bool = False


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
