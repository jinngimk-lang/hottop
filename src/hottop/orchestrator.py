from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

from .creative import (
    ContextualCreativeReview,
    CreativeContextReview,
    CreativeReview,
    review_with_context,
)
from .intake import CreativeIntent
from .models import CreativeConcept, PromotionContext, VisualReference
from .profiles import derive_routing_hints
from .rendering import CreativeRenderRequest, build_creative_render_request


class OrchestrationOption(BaseModel):
    label: str = Field(min_length=1)
    concept: CreativeConcept
    review: CreativeReview
    context_review: CreativeContextReview

    @field_validator("label")
    @classmethod
    def normalize_label(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("option label must not be blank")
        return value

    @model_validator(mode="after")
    def bind_review_to_option(self) -> OrchestrationOption:
        if self.review.name != self.label:
            raise ValueError("review name must match option label")
        return self


class OrchestrationInput(BaseModel):
    intent: CreativeIntent
    promotion_context: PromotionContext
    options: list[OrchestrationOption] = Field(min_length=1, max_length=12)
    references: list[VisualReference] = Field(default_factory=list, max_length=24)


class AlternateSummary(BaseModel):
    label: str
    expression_form: str
    bridge: str | None = None
    score: float = Field(ge=0, le=1)


class OrchestrationResult(BaseModel):
    schema_version: Literal["hottop.orchestration.v1"] = "hottop.orchestration.v1"
    intent: CreativeIntent
    promotion_context: PromotionContext
    selected_index: int = Field(ge=0)
    selected_label: str
    selected_concept: CreativeConcept
    selected_review: ContextualCreativeReview
    selected_render: CreativeRenderRequest
    selection_rationale: str
    alternates: list[AlternateSummary] = Field(default_factory=list)
    references: list[VisualReference] = Field(default_factory=list)


def orchestrate(payload: OrchestrationInput) -> OrchestrationResult:
    reviewed = [
        review_with_context(option.review, option.context_review)
        for option in payload.options
    ]
    eligible = [
        (index, option, reviewed[index])
        for index, option in enumerate(payload.options)
        if reviewed[index].passes
    ]
    if not eligible:
        raise ValueError("no orchestration option passed the creative review gate")

    selected_index, selected, selected_review = max(
        eligible,
        key=lambda item: item[2].total,
    )
    hints = derive_routing_hints(payload.intent, payload.promotion_context)
    alternates = [
        AlternateSummary(
            label=option.label,
            expression_form=option.concept.strategy.expression_form,
            bridge=option.concept.strategy.bridge,
            score=reviewed[index].total,
        )
        for index, option in enumerate(payload.options)
        if index != selected_index and reviewed[index].passes
    ]
    alternates.sort(key=lambda item: item.score, reverse=True)
    rationale = (
        f"Selected {selected.label} for platform {hints.platform.platform}, "
        f"style {hints.style.style}, project shape {hints.project_shape.shape}; "
        "the concept cleared the base creative gate and ranked highest on contextual fit."
    )
    return OrchestrationResult(
        intent=payload.intent,
        promotion_context=payload.promotion_context,
        selected_index=selected_index,
        selected_label=selected.label,
        selected_concept=selected.concept,
        selected_review=selected_review,
        selected_render=build_creative_render_request(selected.concept),
        selection_rationale=rationale,
        alternates=alternates,
        references=payload.references,
    )


def revision_overrides(intent: CreativeIntent, action: str) -> dict[str, str]:
    """Translate compact conversational revision controls into intent mutations.

    The caller applies these as explicit overrides through `resolve_intent`, so only the
    dimension the user asked to change is rerouted.
    """

    normalized = action.strip().lower()
    if normalized in {"更大胆", "破框", "bolder", "more bold"}:
        return {"creative_ambition": "category-breaking"}
    if normalized in {"更有梗", "更搞笑", "funnier", "more witty"}:
        return {"style": "funny-meme"}
    if normalized in {"产品更明显", "产品优先", "show product", "product first"}:
        return {"product_visibility": "product-first"}
    if normalized in {"更高级", "高级一点", "more premium"}:
        return {"style": "minimal-premium"}
    if normalized in {"换平台", "change platform"}:
        return {"platform": "auto"}
    if normalized in {"换方向", "new direction"}:
        return {"hotspot_preference": "current-best"}
    return {}