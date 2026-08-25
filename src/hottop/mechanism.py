from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

from .models import MemeBrief


class HotspotMechanism(BaseModel):
    """Structured analysis of what makes a specific hotspot culturally legible."""

    topic_id: str = Field(min_length=1)
    source_mode: Literal["user-supplied", "fresh-discovered"]
    recognition_hook: str = Field(min_length=1)
    causal_chain: list[str] = Field(min_length=2, max_length=8)
    native_visual_grammar: str = Field(min_length=1)
    native_dialogue_grammar: str = Field(min_length=1)
    native_audio_grammar: str | None = None

    @field_validator(
        "topic_id",
        "recognition_hook",
        "native_visual_grammar",
        "native_dialogue_grammar",
        "native_audio_grammar",
    )
    @classmethod
    def normalize_text(cls, value: str | None, info) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError(f"hotspot mechanism {info.field_name.replace('_', ' ')} must not be blank")
        return value

    @field_validator("causal_chain")
    @classmethod
    def normalize_causal_chain(cls, values: list[str]) -> list[str]:
        normalized = [value.strip() for value in values]
        if any(not value for value in normalized):
            raise ValueError("hotspot mechanism causal chain must not contain blank steps")
        return normalized


class ProductMechanismMapping(BaseModel):
    """Binds a product truth to a hotspot mechanism without inventing a generic hero template."""

    mechanism: HotspotMechanism
    promoted_product: str = Field(min_length=1)
    product_role: str = Field(min_length=1)
    product_bridge: str = Field(min_length=1)
    outcome_before: str = Field(min_length=1)
    outcome_after: str = Field(min_length=1)
    punchline: str = Field(min_length=1)
    comparison_target: str | None = None
    comparison_role: str | None = None
    product_changes_outcome: bool = True

    @field_validator(
        "promoted_product",
        "product_role",
        "product_bridge",
        "outcome_before",
        "outcome_after",
        "punchline",
        "comparison_target",
        "comparison_role",
    )
    @classmethod
    def normalize_text(cls, value: str | None, info) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError(f"mechanism mapping {info.field_name.replace('_', ' ')} must not be blank")
        return value

    @model_validator(mode="after")
    def require_real_outcome_change(self) -> ProductMechanismMapping:
        if not self.product_changes_outcome:
            raise ValueError("product must change the story outcome")
        if self.outcome_before.casefold() == self.outcome_after.casefold():
            raise ValueError("outcome after must differ from outcome before")
        if self.comparison_role and not self.comparison_target:
            raise ValueError("comparison role requires a comparison target")
        return self


class MechanismMemeBrief(MemeBrief):
    """Explicit four-panel legacy handoff with the source mechanism preserved as evidence."""

    mechanism_mapping: ProductMechanismMapping
