from hottop.intake import resolve_intent
from hottop.models import PromotionContext
from hottop.profiles import (
    derive_routing_hints,
    get_platform_profile,
    get_style_profile,
    infer_project_shape,
)


def test_platform_profiles_change_creative_grammar_not_only_size():
    xhs = get_platform_profile("xiaohongshu")
    douyin = get_platform_profile("douyin")
    linkedin = get_platform_profile("linkedin")
    paid = get_platform_profile("paid-social")

    assert "swipe-reveal" in xhs.preferred_forms
    assert xhs.hook_priority > 0.8
    assert douyin.motion_priority > 0.9
    assert linkedin.evidence_priority > 0.9
    assert "split-old-vs-new" in linkedin.preferred_forms
    assert paid.early_product_bias > 0.9


def test_style_profiles_change_copy_and_humor_behavior():
    minimal = get_style_profile("minimal-premium")
    funny = get_style_profile("funny-meme")
    product = get_style_profile("commercial-product")

    assert minimal.text_density == "low"
    assert funny.reversal_weight > minimal.reversal_weight
    assert funny.punchline_weight > 0.9
    assert product.product_texture_weight > 0.9


def test_project_shape_routes_consumer_and_software_differently():
    consumer = infer_project_shape("food beverage")
    software = infer_project_shape("AI software SaaS")

    assert consumer.shape == "consumer-product"
    assert "shape-material" in consumer.bridge_biases
    assert "swipe-reveal" in consumer.format_biases
    assert software.shape == "software-b2b"
    assert "split-old-vs-new" in software.format_biases
    assert "function" in software.bridge_biases


def test_routing_hints_apply_ambition_and_product_visibility():
    intent = resolve_intent(
        "给这个咖啡新品做一个小红书破框高级广告，产品最后再揭示"
    )
    context = PromotionContext(
        subject_name="Coffee Drop",
        subject_type="product",
        category="food beverage",
        primary_job="memorable refreshment",
        primary_pain_point="generic launch ads",
        primary_differentiator="dense cold foam texture",
        semantic_terms=["foam", "cold", "layered"],
    )

    hints = derive_routing_hints(intent, context)

    assert hints.product_visibility == "metaphor-first"
    assert "constraint deletion" in hints.creative_emphasis
    assert "product texture" in hints.creative_emphasis
    assert "swipe-reveal" in hints.preferred_forms
