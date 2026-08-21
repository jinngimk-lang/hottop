from hottop.intake import resolve_intent


def test_category_reframe_goal_beats_generic_hotspot_language_when_explicitly_requested():
    intent = resolve_intent("做一个热点联动，但要破框重构这个类目的广告")

    assert intent.campaign_goal.value == "category-reframe"
