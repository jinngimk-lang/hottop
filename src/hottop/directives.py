from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from .intake import CreativeIntent
from .models import PromotionContext
from .profiles import ProjectShape, derive_routing_hints


class CreativeDirective(BaseModel):
    """Pre-generation routing contract for precise, varied creative exploration."""

    schema_version: Literal["hottop.creative-directive.v1"] = "hottop.creative-directive.v1"
    platform: str
    style: str
    project_shape: ProjectShape
    product_visibility: str
    distribution_mode: Literal["auto", "static", "motion"] = "auto"
    in_asset_cta_policy: Literal["no-destination", "conversion-destination"] = "no-destination"
    motion_continuity_required: bool = False
    direction_lanes: list[str] = Field(min_length=3)
    preferred_forms: list[str] = Field(min_length=1)
    bridge_biases: list[str] = Field(min_length=1)
    creative_emphasis: list[str] = Field(default_factory=list)
    humor_expected: bool
    joke_mechanics: list[str] = Field(default_factory=list)
    product_visibility_instruction: str
    platform_instructions: list[str] = Field(default_factory=list)
    precision_requirements: list[str] = Field(default_factory=list)
    reject_patterns: list[str] = Field(default_factory=list)


def _direction_lanes(intent: CreativeIntent) -> list[str]:
    if (
        intent.creative_ambition.value == "category-breaking"
        or intent.campaign_goal.value == "category-reframe"
    ):
        return ["constraint-deletion", "bridge-led-metaphor", "pain-point-contrast"]
    return ["bridge-led-metaphor", "constraint-deletion", "pain-point-contrast"]


def _humor_expected(intent: CreativeIntent) -> bool:
    if intent.style.value == "funny-meme":
        return True
    if (
        intent.creative_ambition.value == "witty"
        and intent.creative_ambition.source != "defaulted"
    ):
        return True
    return (
        intent.campaign_goal.value == "hotspot-participation"
        and intent.creative_ambition.value == "breakout"
    )


def _joke_mechanics(intent: CreativeIntent, promotion: PromotionContext) -> list[str]:
    mechanics: list[str] = []
    semantic_terms = " ".join(promotion.semantic_terms).lower()
    if intent.product_visibility.value == "metaphor-first":
        mechanics.append("misdirection-reveal")
    if any(
        token in semantic_terms
        for token in ("long", "elastic", "ribbon", "shape", "texture", "透明", "长", "弹")
    ):
        mechanics.append("visual-wordplay")
    if _humor_expected(intent):
        mechanics.extend(["recognition-reversal", "product-specific-punchline"])
    return list(dict.fromkeys(mechanics))


def _visibility_instruction(intent: CreativeIntent) -> str:
    visibility = intent.product_visibility.value
    if visibility == "metaphor-first":
        return (
            "Delay explicit product reveal until the visual bridge is understood; each earlier beat must add "
            "new information without giving away the full answer."
        )
    if visibility == "product-first":
        return "Show the promoted product or unmistakable attribution in the opening beat."
    return "Balance metaphor and attribution: establish the bridge early and make the product explicit before payoff."


def _destination_is_explicitly_blocked(intent: CreativeIntent) -> bool:
    lowered = intent.request.lower()
    return any(
        term in lowered
        for term in (
            "不要网址",
            "不要链接",
            "不要二维码",
            "别放网址",
            "别放链接",
            "别放二维码",
            "no url",
            "no link",
            "no qr",
        )
    )


def _in_asset_cta_policy(intent: CreativeIntent) -> Literal["no-destination", "conversion-destination"]:
    if _destination_is_explicitly_blocked(intent):
        return "no-destination"
    if intent.campaign_goal.value == "conversion" or intent.platform.value == "paid-social":
        return "conversion-destination"
    return "no-destination"


def _precision_requirements(intent: CreativeIntent, promotion: PromotionContext) -> list[str]:
    hints = derive_routing_hints(intent, promotion)
    requirements = [
        "Use a product-specific bridge; reject any concept that remains brand-swappable.",
        "Keep the core idea understandable in roughly 1–3 seconds.",
        "Ground named competitor negatives in evidence; otherwise use a generic category proxy or satire.",
    ]
    if hints.project_shape.shape == "consumer-product":
        requirements.extend(
            [
                "Anchor the concept in a real sensory or physical product property.",
                "Make texture, shape, material, ritual, or appetite cues do creative work rather than act as decoration.",
            ]
        )
    if hints.project_shape.shape == "software-b2b":
        requirements.extend(
            [
                "Name the workflow pain or category default before claiming the new axis.",
                "Use evidence-aware comparison language for factual workflow or competitor claims.",
            ]
        )
    if intent.campaign_goal.value == "category-reframe":
        requirements.append(
            "State category_default, deleted_constraint, and new_competition_axis before locking the concept."
        )
    if intent.distribution_mode.value == "motion":
        requirements.extend(
            [
                "Preserve scene geography, character identity, and action continuity across the motion sequence.",
                "Reject slideshow-like still-frame cuts when the concept is supposed to feel like continuous motion.",
                "Let benefits emerge through action or consequence before adding feature labels.",
            ]
        )
    return requirements


def build_creative_directive(
    intent: CreativeIntent,
    promotion: PromotionContext,
) -> CreativeDirective:
    """Turn resolved intent + promotion semantics into a deterministic generation brief."""

    hints = derive_routing_hints(intent, promotion)
    platform_instructions = list(hints.platform.notes)
    if hints.platform.early_product_bias >= 0.9:
        platform_instructions.append("Prioritize early brand attribution in the opening beat.")

    cta_policy = _in_asset_cta_policy(intent)
    if cta_policy == "no-destination":
        platform_instructions.append(
            "Keep the social asset ad-light: no in-asset URL or QR code; use compact brand/product attribution at payoff."
        )
    else:
        platform_instructions.append(
            "A conversion destination may appear because the brief is explicitly conversion/paid-social oriented."
        )

    if intent.distribution_mode.value == "motion":
        platform_instructions.append(
            "Use continuous motion grammar with camera/action continuity instead of a sequence of unrelated stills."
        )

    reject_patterns = [
        "Reject hot-character + logo concepts.",
        "Reject feature lists wearing a cultural costume.",
        "Reject brand-swappable concepts that could advertise any competitor unchanged.",
        "Reject copied protected frames, likenesses, proprietary UI, or distinctive trade dress.",
    ]

    return CreativeDirective(
        platform=hints.platform.platform,
        style=hints.style.style,
        project_shape=hints.project_shape.shape,
        product_visibility=intent.product_visibility.value,
        distribution_mode=intent.distribution_mode.value,
        in_asset_cta_policy=cta_policy,
        motion_continuity_required=intent.distribution_mode.value == "motion",
        direction_lanes=_direction_lanes(intent),
        preferred_forms=hints.preferred_forms,
        bridge_biases=hints.project_shape.bridge_biases,
        creative_emphasis=hints.creative_emphasis,
        humor_expected=_humor_expected(intent),
        joke_mechanics=_joke_mechanics(intent, promotion),
        product_visibility_instruction=_visibility_instruction(intent),
        platform_instructions=platform_instructions,
        precision_requirements=_precision_requirements(intent, promotion),
        reject_patterns=reject_patterns,
    )
