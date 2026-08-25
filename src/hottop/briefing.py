from __future__ import annotations

from .guardrails import classify_claim
from .mapping import build_role_map
from .mechanism import MechanismMemeBrief, ProductMechanismMapping
from .models import ClaimStatus, Panel, ProductProfile, TrendCandidate
from .positioning import infer_promotion_context

_NEGATIVE_PROMPT = (
    "No actor likeness, no celebrity face, no exact film frame, no official poster recreation, "
    "no copied costume design, no studio logo, no title lockup, no protected character-design replica. "
    "Do not copy competitor logos, proprietary UI, packaging trade dress, or ad layouts. "
    "Use an original reinterpretation of the topic's mechanism and native medium grammar."
)


def _worst_status(lines: list[str], comparison_evidence_count: int) -> ClaimStatus:
    statuses = [classify_claim(line, evidence_count=comparison_evidence_count) for line in lines]
    if "needs_evidence" in statuses:
        return "needs_evidence"
    if statuses and all(status == "supported" for status in statuses):
        return "supported"
    return "satire"


def _four_panel_steps(mapping: ProductMechanismMapping) -> tuple[str, str, str, str]:
    chain = mapping.mechanism.causal_chain
    setup = chain[0]
    if len(chain) == 2:
        escalation = chain[0]
        source_resolution = chain[1]
    else:
        escalation = " → ".join(chain[1:-1])
        source_resolution = chain[-1]
    reversal = (
        f"{mapping.promoted_product} acts as {mapping.product_role}: {mapping.product_bridge}"
    )
    resolution = f"{source_resolution}; outcome becomes: {mapping.outcome_after}"
    return setup, escalation, reversal, resolution


def build_brief(
    candidate: TrendCandidate,
    product: ProductProfile,
    comparison_target: str | None = None,
    punchlines: list[str] | None = None,
    comparison_evidence_count: int = 0,
    mechanism_mapping: ProductMechanismMapping | None = None,
) -> MechanismMemeBrief:
    """Build an explicit four-panel brief from a reviewed mechanism mapping.

    This is a compatibility four-panel route. It intentionally fails closed when callers have not
    supplied current hotspot analysis; flexible/motion creative should use CreativeConcept/render.v2.
    """

    if mechanism_mapping is None:
        raise ValueError(
            "mechanism_mapping is required; legacy keyword template inference is disabled"
        )

    role_map = build_role_map(
        candidate,
        product,
        mechanism_mapping=mechanism_mapping,
        comparison_target=comparison_target,
    )
    context = infer_promotion_context(product)
    effective_comparison = role_map.comparison_target
    lines = (punchlines or [mechanism_mapping.punchline])[:3]
    claim_status = _worst_status(lines, comparison_evidence_count)

    pain_point = context.primary_pain_point or mechanism_mapping.outcome_before
    differentiator = context.primary_differentiator or (
        product.strengths[0] if product.strengths else mechanism_mapping.product_bridge
    )
    setup, escalation, reversal, resolution = _four_panel_steps(mechanism_mapping)
    visual = mechanism_mapping.mechanism.native_visual_grammar
    dialogue = mechanism_mapping.mechanism.native_dialogue_grammar

    panels = [
        Panel(
            scene=(
                f"Use the hotspot's native visual grammar: {visual}. Establish the recognition hook "
                f"'{mechanism_mapping.mechanism.recognition_hook}' through this causal step: {setup}."
            ),
            caption=setup,
            intent="setup",
        ),
        Panel(
            scene=(
                f"Continue the same world and relationship logic rather than switching to ad grammar. "
                f"Escalate through: {escalation}. Dialogue/caption rhythm follows: {dialogue}."
            ),
            caption=escalation,
            intent="escalation",
        ),
        Panel(
            scene=(
                f"Keep the product native to the hotspot mechanism. {reversal}. Show the real product "
                f"truth '{differentiator}' changing the concrete pain/outcome '{pain_point}'."
            ),
            caption=reversal,
            intent="reversal",
        ),
        Panel(
            scene=(
                f"Resolve the source mechanism through the product-caused consequence, not a feature card: "
                f"{resolution}. Keep the same visual and dialogue grammar through the final beat."
            ),
            caption=lines[0],
            intent="punchline",
        ),
    ]

    comparison_instruction = ""
    if effective_comparison:
        comparison_instruction = (
            f" Comparison target: {effective_comparison}; its mapped role is "
            f"{mechanism_mapping.comparison_role or 'only the specifically evidenced friction in this mechanism'}."
        )

    image_prompt = (
        "Create an original four-panel execution of an already-selected hotspot mechanism; do not infer a "
        "generic hero template from keywords. "
        f"Topic: {candidate.title}. Recognition hook: {mechanism_mapping.mechanism.recognition_hook}. "
        f"Causal mechanism: {' → '.join(mechanism_mapping.mechanism.causal_chain)}. "
        f"Native visual grammar: {visual}. Native dialogue/language rhythm: {dialogue}. "
        f"Promoted subject: {product.name}. Product role: {mechanism_mapping.product_role}. "
        f"Natural bridge: {mechanism_mapping.product_bridge}. Outcome before: {mechanism_mapping.outcome_before}. "
        f"Outcome after: {mechanism_mapping.outcome_after}. Punchline: {lines[0]}."
        f"{comparison_instruction} Every retained hotspot element must have a causal job. "
        "Benefits appear as consequences of the scene; no generic feature-card ending. Chinese captions, when "
        "used, must be concise and phone-legible."
    )

    risk_flags = ["copyright-transform-required"]
    if effective_comparison:
        risk_flags.extend(["competitor-comparison", "competitor-claim-must-match-evidence"])
    if claim_status == "needs_evidence":
        risk_flags.append("unsupported-comparison")

    return MechanismMemeBrief(
        topic=candidate,
        role_map=role_map,
        mechanism_mapping=mechanism_mapping,
        panels=panels,
        punchlines=lines,
        image_prompt=image_prompt,
        negative_prompt=_NEGATIVE_PROMPT,
        risk_flags=risk_flags,
        claim_status=claim_status,
    )
