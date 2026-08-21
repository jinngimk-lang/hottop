from hottop.intake import next_question, resolve_intent


def test_router_does_not_repeat_fields_already_resolved_from_request():
    intent = resolve_intent(
        "给咖啡新品做一个小红书能出圈的高级电影热点广告，产品最后再揭示"
    )

    state = next_question(intent)

    assert state.question is None
    assert state.ready_to_create is True
    assert "platform" not in state.missing_high_impact_fields
    assert "style" not in state.missing_high_impact_fields
    assert "creative_ambition" not in state.missing_high_impact_fields


def test_router_prioritizes_missing_promotion_target():
    intent = resolve_intent("做一个小红书有梗广告")

    state = next_question(intent)

    assert state.ready_to_create is False
    assert state.question is not None
    assert state.question.field == "promotion_target"
    assert len(state.question.options) <= 6


def test_router_does_not_ask_audience_for_ordinary_consumer_request():
    intent = resolve_intent("给这个饮料新品做一个抖音有梗广告")

    state = next_question(intent)

    assert "audience" not in state.missing_high_impact_fields
    assert state.question is None or state.question.field != "audience"


def test_router_budget_zero_never_emits_questionnaire():
    intent = resolve_intent("宣传一下这个新产品")

    state = next_question(intent, budget=0)

    assert state.question is None
    assert state.ready_to_create is True
    assert state.question_budget_remaining == 0
