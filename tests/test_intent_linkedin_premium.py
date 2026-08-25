from hottop.intake import resolve_intent


def test_linkedin_and_premium_can_be_inferred_together():
    intent = resolve_intent("给产品做个 LinkedIn 高级行业广告")

    assert intent.platform.value == "linkedin"
    assert intent.style.value == "minimal-premium"
