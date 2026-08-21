from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from hottop.models import (
    BridgeType,
    ClaimStatus,
    CreativeConcept,
    Evidence,
    ExpressionForm,
    MemeBrief,
    VisualMedium,
)


class RenderPanel(BaseModel):
    index: int = Field(ge=1, le=4)
    scene: str
    caption: str
    intent: str


class RenderRequest(BaseModel):
    schema_version: Literal["hottop.render.v1"] = "hottop.render.v1"
    topic_id: str
    topic_title: str
    product_name: str
    comparison_target: str | None = None
    layout: Literal["four-panel-grid"] = "four-panel-grid"
    aspect_ratio: str = "1:1"
    panels: list[RenderPanel] = Field(min_length=4, max_length=4)
    master_prompt: str
    negative_prompt: str
    punchlines: list[str] = Field(min_length=1, max_length=3)
    risk_flags: list[str] = Field(default_factory=list)
    claim_status: ClaimStatus
    provider: str | None = None


class CreativeRenderFrame(BaseModel):
    index: int = Field(ge=1, le=8)
    scene: str
    caption: str | None = None
    intent: str


class CreativeRenderRequest(BaseModel):
    schema_version: Literal["hottop.render.v2"] = "hottop.render.v2"
    topic_id: str
    topic_title: str
    subject_name: str
    comparison_target: str | None = None
    comparison_evidence: list[Evidence] = Field(default_factory=list)
    expression_form: ExpressionForm
    visual_medium: VisualMedium
    genre_treatment: str
    category_default: str | None = None
    deleted_constraint: str | None = None
    new_competition_axis: str | None = None
    bridge_type: BridgeType | None = None
    bridge: str | None = None
    frames: list[CreativeRenderFrame] = Field(min_length=1, max_length=8)
    master_prompt: str
    negative_prompt: str
    punchlines: list[str] = Field(min_length=1, max_length=3)
    risk_flags: list[str] = Field(default_factory=list)
    claim_status: ClaimStatus
    provider: str | None = None


def build_render_request(brief: MemeBrief) -> RenderRequest:
    return RenderRequest(
        topic_id=brief.topic.id,
        topic_title=brief.topic.title,
        product_name=brief.role_map.promoted_product,
        comparison_target=brief.role_map.comparison_target,
        panels=[
            RenderPanel(
                index=index,
                scene=panel.scene,
                caption=panel.caption,
                intent=panel.intent,
            )
            for index, panel in enumerate(brief.panels, start=1)
        ],
        master_prompt=brief.image_prompt,
        negative_prompt=brief.negative_prompt,
        punchlines=brief.punchlines,
        risk_flags=brief.risk_flags,
        claim_status=brief.claim_status,
    )


def build_creative_render_request(concept: CreativeConcept) -> CreativeRenderRequest:
    strategy = concept.strategy
    return CreativeRenderRequest(
        topic_id=concept.topic.id,
        topic_title=concept.topic.title,
        subject_name=concept.promotion.subject_name,
        comparison_target=concept.comparison_target,
        comparison_evidence=concept.comparison_evidence,
        expression_form=strategy.expression_form,
        visual_medium=concept.visual_medium,
        genre_treatment=concept.genre_treatment,
        category_default=strategy.category_default,
        deleted_constraint=strategy.deleted_constraint,
        new_competition_axis=strategy.new_competition_axis,
        bridge_type=strategy.bridge_type,
        bridge=strategy.bridge,
        frames=[
            CreativeRenderFrame(
                index=index,
                scene=beat.scene,
                caption=beat.caption,
                intent=beat.intent,
            )
            for index, beat in enumerate(concept.beats, start=1)
        ],
        master_prompt=concept.image_prompt,
        negative_prompt=concept.negative_prompt,
        punchlines=concept.punchlines,
        risk_flags=concept.risk_flags,
        claim_status=concept.claim_status,
    )
