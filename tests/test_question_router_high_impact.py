from hottop.intake import next_question, resolve_intent


def test_platform_is_asked_only_when_it_materially_changes_format():
    intent = resolve_intent("给这个咖啡新品做一个广告", overrides={"promotion_target": "Coffee Drop"})

    state = next_question(intent)

    assert state.question is not None
    assert state.question.field in {"campaign_goal", "platform", "creative_ambition", "product_visibility"}
    assert state.question.field != "audience"
