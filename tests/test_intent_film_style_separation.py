from hottop.intake import resolve_intent


def test_movie_hotspot_does_not_force_cinematic_style_when_user_says_premium():
    intent = resolve_intent("给咖啡做个高级电影热点广告")

    assert intent.hotspot_preference.value == "film"
    assert intent.style.value == "minimal-premium"
