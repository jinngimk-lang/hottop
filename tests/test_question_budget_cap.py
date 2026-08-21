from hottop.intake import next_question, resolve_intent


def test_question_budget_is_capped_at_three():
    intent = resolve_intent("做个广告")

    state = next_question(intent, budget=9)

    assert state.question_budget_remaining <= 3
