from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator

from .creative import CreativeReview
from .models import CreativeConcept, VisualReference
from .rendering import CreativeRenderRequest, build_creative_render_request


class CreativePackageOption(BaseModel):
    """One front-end creative proposal paired with an explicit quality review."""

    concept: CreativeConcept
    review: CreativeReview
    label: str = Field(min_length=1)

    @model_validator(mode="after")
    def bind_review_to_option(self) -> CreativePackageOption:
        if self.review.name != self.label:
            raise ValueError("review name must match option label")
        return self


ReviewedCreativeOption = CreativePackageOption


class CreativePackageInput(BaseModel):
    """Conversation/front-end handoff containing alternatives and abstract reference research."""

    options: list[CreativePackageOption] = Field(min_length=1, max_length=12)
    references: list[VisualReference] = Field(default_factory=list, max_length=24)


class CreativeOptionDiagnostic(BaseModel):
    index: int = Field(ge=0)
    label: str | None = None
    total: float = Field(ge=0, le=1)
    passes: bool
    expression_form: str
    bridge: str | None = None


class CreativePackageResult(BaseModel):
    """Durable selected concept plus diagnostics and provider-neutral renderer handoff."""

    schema_version: Literal["hottop.creative-package.v1"] = "hottop.creative-package.v1"
    selected_index: int = Field(ge=0)
    selected_concept: CreativeConcept
    selected_review: CreativeReview
    selected_render: CreativeRenderRequest
    option_diagnostics: list[CreativeOptionDiagnostic]
    references: list[VisualReference] = Field(default_factory=list)


def build_creative_package(package: CreativePackageInput) -> CreativePackageResult:
    """Select the strongest option that already passes Hottop's hard creative review gate.

    Creative invention stays in the conversational/LLM front end. This deterministic layer only
    validates supplied concepts and reviews, refuses weak packages, and preserves the chosen
    concept plus reference provenance for later rendering/archive steps.
    """

    diagnostics = [
        CreativeOptionDiagnostic(
            index=index,
            label=option.label,
            total=option.review.total,
            passes=option.review.passes,
            expression_form=option.concept.strategy.expression_form,
            bridge=option.concept.strategy.bridge,
        )
        for index, option in enumerate(package.options)
    ]
    eligible = [
        (index, option)
        for index, option in enumerate(package.options)
        if option.review.passes
    ]
    if not eligible:
        raise ValueError("no creative option passed the creative review gate")

    selected_index, selected = max(eligible, key=lambda item: item[1].review.total)
    return CreativePackageResult(
        selected_index=selected_index,
        selected_concept=selected.concept,
        selected_review=selected.review,
        selected_render=build_creative_render_request(selected.concept),
        option_diagnostics=diagnostics,
        references=package.references,
    )
