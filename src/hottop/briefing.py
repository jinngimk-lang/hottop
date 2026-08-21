from __future__ import annotations

from .guardrails import classify_claim
from .mapping import build_role_map
from .models import ClaimStatus, MemeBrief, Panel, ProductProfile, TrendCandidate
from .positioning import infer_promotion_context

_NEGATIVE_PROMPT = (
    "No actor likeness, no celebrity face, no exact film frame, no official poster recreation, "
    "no copied costume design, no studio logo, no title lockup, no protected character-design replica. "
    "Do not copy competitor logos, proprietary UI, packaging trade dress, or ad layouts. "
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
    context = infer_promotion_context(product)
    comparison_name = comparison_target or "旧办法"
    lines = (punchlines or _default_punchlines(product))[:3]
    claim_status = _worst_status(lines, comparison_evidence_count)

    pain_point = context.primary_pain_point or "当前最影响结果的痛点"
    differentiator = context.primary_differentiator or (
        product.strengths[0] if product.strengths else "更适合这个场景的解决方式"
    )

    panels = [
        Panel(
            scene=(
                f"用原创视觉重新演绎“{candidate.title}”的世界：先建立最有辨识度的环境、危机和角色关系，"
                f"并把现实用户痛点“{pain_point}”自然嵌进冲突。"
            ),
            caption="热点里的这道坎，看着就不好过。",
            intent="setup",
        ),
        Panel(
            scene=(
                f"把 {comparison_name} 映射成当前冲突里的阻碍角色或不合适的旧解法；"
                "只表现与本次痛点有关的摩擦，不编造对方不存在的产品缺陷。"
            ),
            caption=f"{comparison_name}：这关你慢慢耗吧。",
            intent="escalation",
        ),
        Panel(
            scene=(
                f"让代表 {product.name} 的原创破局者进入，用“{role_map.product_role}”的方式改变局势；"
                f"视觉上突出“{differentiator}”如何解决“{pain_point}”。"
            ),
            caption=f"{product.name}：换个解法，这事没那么复杂。",
            intent="reversal",
        ),
        Panel(
            scene=(
                f"痛点被化解，画面给 {product.name} 一个干净的结果落点；"
                "保留热点世界感，但人物、服装、产品道具、包装和构图保持原创。"
            ),
            caption=lines[0],
            intent="punchline",
        ),
    ]

    semantic_strengths = product.differentiators or product.strengths
    strengths = "、".join(semantic_strengths[:3]) if semantic_strengths else differentiator
    image_prompt = (
        "Create an original four-panel marketing meme matched to the visual medium of the current trend. "
        f"Topic: {candidate.title}. Conflict archetype: {role_map.archetype}. Promoted subject: {product.name} "
        f"({context.subject_type}, category: {context.category}). User pain point: {pain_point}. "
        f"Panel 1 establishes the recognizable predicament. Panel 2 metaphorically casts {comparison_name} as an "
        "inadequate or friction-heavy approach only for this specific pain point, without inventing factual defects. "
        f"Panel 3 introduces an original solver representing {product.name}, emphasizing {strengths}. "
        f"Panel 4 resolves the conflict with the caption: {lines[0]}. Panels may vary in composition and shot scale. "
        "Chinese captions must be large, legible, concise, and visually separated from the artwork."
    )

    risk_flags = ["copyright-transform-required", "competitor-comparison"] if comparison_target else [
        "copyright-transform-required"
    ]
    if comparison_target:
        risk_flags.append("competitor-claim-must-match-evidence")
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
