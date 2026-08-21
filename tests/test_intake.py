from hottop.intake import resolve_intent


def test_resolve_intent_infers_high_value_fields_from_natural_request():
    intent = resolve_intent(
        "给这个咖啡新品做一个小红书能出圈的电影热点广告，高级一点，产品别一上来全露"
    )

    assert "咖啡新品" in (intent.promotion_target.value or "")
    assert intent.promotion_target.source == "inferred"
    assert intent.platform.value == "xiaohongshu"
    assert intent.platform.source == "inferred"
    assert intent.style.value == "minimal-premium"
    assert intent.creative_ambition.value == "breakout"
    assert intent.product_visibility.value == "metaphor-first"
    assert intent.hotspot_preference.value == "film"
    assert intent.platform.confidence >= 0.8


def test_explicit_overrides_beat_natural_language_inference():
    intent = resolve_intent(
        "给咖啡新品做一个小红书出圈广告",
        overrides={
            "platform": "douyin",
            "creative_ambition": "safe",
            "style": "funny-meme",
        },
    )

    assert intent.platform.value == "douyin"
    assert intent.platform.source == "explicit"
    assert intent.platform.confidence == 1.0
    assert intent.creative_ambition.value == "safe"
    assert intent.creative_ambition.source == "explicit"
    assert intent.style.value == "funny-meme"
    assert intent.style.source == "explicit"


def test_unresolved_fields_remain_transparent_defaults():
    intent = resolve_intent("宣传一下这个新产品")

    assert intent.platform.value == "auto"
    assert intent.platform.source == "defaulted"
    assert intent.style.value == "auto"
    assert intent.style.source == "defaulted"
    assert intent.campaign_goal.value == "auto"
    assert intent.campaign_goal.source == "defaulted"
    assert intent.creative_ambition.value == "witty"
    assert intent.creative_ambition.source == "defaulted"
    assert intent.product_visibility.value == "balanced"
    assert intent.product_visibility.source == "defaulted"
