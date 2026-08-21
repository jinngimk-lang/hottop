from hottop.intake import next_question, resolve_intent


def test_router_never_returns_multiple_questions_at_once():
    state = next_question(resolve_intent("做个广告"))

    assert not hasattr(state, "questions")
    assert state.question is None or isinstance(state.question.prompt, str)
