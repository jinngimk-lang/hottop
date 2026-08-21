from hottop.directives import build_creative_directive
from hottop.intake import resolve_intent
from hottop.models import PromotionContext


def test_consumer_breakout_directive_prefers_reveal_and_product_specific_joke_mechanics():
    intent = resolve_intent(
        "给云朵拉面做小红书出圈有梗广告，最后再揭示产品",
        overrides={"campaign_goal": "hotspot-participation"},
    )
    promotion = PromotionContext(
        subject_name="云朵拉面",
        subject_type="product",
        category="food consumer",
        primary_job="make a memorable quick meal",
        primary_pain_point="food ads look interchangeable",
        primary_differentiator="long elastic ribbon-like noodles",
        semantic_terms=["long", "elastic", "ribbon", "slippery"],
    )

    directive = build_creative_directive(intent, promotion)

    assert directive.schema_version == "hottop.creative-directive.v1"
    assert directive.project_shape == "consumer-product"
    assert directive.direction_lanes == [
        "bridge-led-metaphor",
        "constraint-deletion",
        "pain-point-contrast",
    ]
    assert directive.preferred_forms[0] == "swipe-reveal"
    assert "shape-material" in directive.bridge_biases
    assert directive.humor_expected is True
    assert "misdirection-reveal" in directive.joke_mechanics
    assert "visual-wordplay" in directive.joke_mechanics
    assert "delay explicit product reveal" in directive.product_visibility_instruction.lower()
    assert any("sensory" in item.lower() for item in directive.precision_requirements)
    assert any("brand-swappable" in item.lower() for item in directive.reject_patterns)


def test_software_category_breaking_directive_prioritizes_constraint_deletion_and_evidence():
    intent = resolve_intent(
        "给 FlowPilot 做 LinkedIn 破框创意，重构旧工作流",
        overrides={"campaign_goal": "category-reframe"},
    )
    promotion = PromotionContext(
        subject_name="FlowPilot",
        subject_type="tool",
        category="B2B software",
        primary_job="coordinate a multi-step workflow",
        primary_pain_point="work is fragmented across handoffs",
        primary_differentiator="one coordinated workflow",
        semantic_terms=["coordinate", "handoff", "workflow"],
    )

    directive = build_creative_directive(intent, promotion)

    assert directive.project_shape == "software-b2b"
    assert directive.direction_lanes[0] == "constraint-deletion"
    assert "split-old-vs-new" in directive.preferred_forms[:2]
    assert "function" in directive.bridge_biases
    assert directive.humor_expected is False
    assert any("evidence" in item.lower() for item in directive.precision_requirements)
    assert any("workflow" in item.lower() for item in directive.precision_requirements)


def test_paid_social_product_first_directive_requires_early_attribution():
    intent = resolve_intent(
        "给 GlowPatch 做广告投放转化创意，产品优先",
        overrides={"style": "commercial-product"},
    )
    promotion = PromotionContext(
        subject_name="GlowPatch",
        subject_type="product",
        category="beauty retail",
        primary_job="make a skincare ritual easy to understand",
        primary_differentiator="visible translucent patch texture",
        semantic_terms=["translucent", "patch", "ritual"],
    )

    directive = build_creative_directive(intent, promotion)

    assert directive.platform == "paid-social"
    assert directive.product_visibility == "product-first"
    assert "opening beat" in directive.product_visibility_instruction.lower()
    assert any("attribution" in item.lower() for item in directive.platform_instructions)


def test_default_witty_does_not_force_humor_into_minimal_premium_work():
    intent = resolve_intent(
        "给 Luma Glass 做 Instagram 极简高级广告",
        overrides={"promotion_target": "Luma Glass"},
    )
    promotion = PromotionContext(
        subject_name="Luma Glass",
        subject_type="product",
        category="consumer product",
        primary_job="make hydration feel visually distinctive",
        primary_differentiator="clear faceted glass geometry",
        semantic_terms=["clear", "faceted", "glass"],
    )

    assert intent.creative_ambition.source == "defaulted"
    assert intent.creative_ambition.value == "witty"

    directive = build_creative_directive(intent, promotion)

    assert directive.style == "minimal-premium"
    assert directive.humor_expected is False
    assert directive.joke_mechanics == []
