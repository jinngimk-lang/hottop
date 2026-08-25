from hottop.intake import resolve_intent


def test_unknown_platform_stays_auto_for_later_switching():
    assert resolve_intent("给产品做个广告").platform.value == "auto"
