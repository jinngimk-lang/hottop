from hottop.intake import next_question, resolve_intent


def test_router_can_prioritize_campaign_goal_after_target_is_known():
    intent = resolve_intent("给 Coffee Drop 做个广告", overrides={"promotion_target": "Coffee Drop"})

    state = next_question(intent)

    assert state.question is None or state.question.field != "promotion_target"
