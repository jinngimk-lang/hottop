from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from hottop.models import ClaimStatus, MemeBrief


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
