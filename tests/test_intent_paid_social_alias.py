from hottop.intake import resolve_intent


def test_paid_social_language_infers_paid_platform():
    assert resolve_intent("做一版广告投放素材").platform.value == "paid-social"
