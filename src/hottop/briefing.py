from __future__ import annotations

from .guardrails import classify_claim
from .mapping import build_role_map
from .models import ClaimStatus, MemeBrief, Panel, ProductProfile, TrendCandidate

_NEGATIVE_PROMPT = (
    "No actor likeness, no celebrity face, no exact film frame, no official poster recreation, "
    "no copied costume design, no studio logo, no title lockup, no protected character-design replica. "
    "Use an original reinterpretation of the topic's narrative archetype and visual atmosphere."
)


def _default_punchlines(product: ProductProfile) -> list[str]:
    return [
        f"还得是 {product.name} 强",
        f"真破局，还得看 {product.name}",
        f"别跟困局耗，直接上 {product.name}",
    ]


def _worst_status(lines: list[str], comparison_evidence_count: int) -> ClaimStatus:
    statuses = [classify_claim(line, evidence_count=comparison_evidence_count) for line in lines]
    if "needs_evidence" in statuses:
        return "needs_evidence"
    if statuses and all(status == "supported" for status in statuses):
        return "supported"
    return "satire"


def build_brief(
    candidate: TrendCandidate,
    product: ProductProfile,
    comparison_target: str | None = None,
    punchlines: list[str] | None = None,
    comparison_evidence_count: int = 0,
) -> MemeBrief:
    role_map = build_role_map(candidate, product, comparison_target=comparison_target)
    comparison_name = comparison_target or "旧工作流"
    lines = (punchlines or _default_punchlines(product))[:3]
    claim_status = _worst_status(lines, comparison_evidence_count)

    panels = [
        Panel(
            scene=(
                f"用原创视觉重新演绎“{candidate.title}”的世界：先建立最有辨识度的环境、危机和角色关系，"
                "不要复刻电影官方画面。"
            ),
            caption="热点里的这道坎，看着就不好过。",
            intent="setup",
        ),
        Panel(
            scene=(
                f"把 {comparison_name} 隐喻成当前冲突里的阻碍角色：强势占据画面，让主角被流程、工具或困局卡住。"
            ),
            caption=f"{comparison_name}：这关你慢慢耗吧。",
            intent="escalation",
        ),
        Panel(
            scene=(
                f"让代表 {product.name} 的原创破局者进入，用“{role_map.product_role}”的方式改变局势；"
                "重点表现更聪明的工作方式，而不是照搬原作英雄造型。"
            ),
            caption=f"{product.name}：换个解法，这事没那么复杂。",
            intent="reversal",
        ),
        Panel(
            scene=(
                f"障碍被破解，画面给 {product.name} 一个干净的胜利落点；保留热点世界感，但使用原创角色、服装、构图。"
            ),
            caption=lines[0],
            intent="punchline",
        ),
    ]

    strengths = "、".join(product.strengths[:3]) if product.strengths else "更完整的 Agent 工作流"
    image_prompt = (
        "Create an original four-panel cinematic meme illustration inspired by the narrative archetype of the current trend, "
        f"not by copying protected film assets. Topic: {candidate.title}. Conflict archetype: {role_map.archetype}. "
        f"Panel 1 establishes the recognizable predicament. Panel 2 metaphorically casts {comparison_name} as the obstacle. "
        f"Panel 3 introduces an original hero/solver representing {product.name}, emphasizing {strengths}. "
        f"Panel 4 resolves the conflict with the caption: {lines[0]}. Panels may vary in composition and shot scale. "
        "Chinese captions must be large, legible, concise, and visually separated from the artwork."
    )

    risk_flags = ["copyright-transform-required", "competitor-comparison"] if comparison_target else [
        "copyright-transform-required"
    ]
    if claim_status == "needs_evidence":
        risk_flags.append("unsupported-comparison")

    return MemeBrief(
        topic=candidate,
        role_map=role_map,
        panels=panels,
        punchlines=lines,
        image_prompt=image_prompt,
        negative_prompt=_NEGATIVE_PROMPT,
        risk_flags=risk_flags,
        claim_status=claim_status,
    )
