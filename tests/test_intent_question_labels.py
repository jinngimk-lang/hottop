from hottop.intake import next_question, resolve_intent


def test_guided_question_is_compact_and_user_facing():
    intent = resolve_intent("做一个有梗广告")

    state = next_question(intent)

    assert state.question is not None
    assert state.question.prompt
    assert state.question.field == "promotion_target"
    assert len(state.question.prompt) < 80
