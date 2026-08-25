from hottop.intake import resolve_intent


def test_paid_conversion_override_can_force_product_first_visibility():
    intent = resolve_intent(
        "做一个广告",
        overrides={
            "promotion_target": "Thing",
            "campaign_goal": "conversion",
            "platform": "paid-social",
            "product_visibility": "product-first",
        },
    )

    assert intent.product_visibility.value == "product-first"
    assert intent.product_visibility.source == "explicit"
