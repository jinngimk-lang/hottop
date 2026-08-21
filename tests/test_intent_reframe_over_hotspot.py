from hottop.intake import resolve_intent


def test_reframe_language_has_goal_priority_over_generic_hotspot_language():
    intent = resolve_intent("热点联动，但核心要重构旧范式")

    assert intent.campaign_goal.value == "category-reframe"
