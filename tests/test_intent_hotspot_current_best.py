from hottop.intake import resolve_intent


def test_current_best_hotspot_request_is_preserved_as_preference():
    intent = resolve_intent("给产品挑今天最适合的热点做广告")

    assert intent.hotspot_preference.value == "current-best"
