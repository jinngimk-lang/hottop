from hottop.intake import resolve_intent


def test_explicit_premium_language_can_coexist_with_film_hotspot_preference():
    intent = resolve_intent("给咖啡做一个高级电影热点广告")

    assert intent.style.value == "minimal-premium"
    assert intent.hotspot_preference.value == "film"
