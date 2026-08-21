from hottop.intake import resolve_intent


def test_audience_is_only_explicit_when_front_end_supplies_it():
    intent = resolve_intent("做个广告", overrides={"promotion_target": "Thing", "audience": "B2B design leads"})

    assert intent.audience.value == "B2B design leads"
    assert intent.audience.source == "explicit"
