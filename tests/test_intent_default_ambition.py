from hottop.intake import resolve_intent


def test_default_ambition_is_witty_not_category_breaking():
    intent = resolve_intent("给产品做个广告", overrides={"promotion_target": "Thing"})

    assert intent.creative_ambition.value == "witty"
    assert intent.creative_ambition.source == "defaulted"
