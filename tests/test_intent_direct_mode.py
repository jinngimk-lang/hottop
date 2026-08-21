from hottop.intake import next_question, resolve_intent


def test_direct_mode_can_proceed_with_inference_when_target_and_core_direction_are_clear():
    intent = resolve_intent(
        "给 Coffee Drop 做一个小红书出圈高级电影热点广告，产品最后再揭示",
        overrides={"promotion_target": "Coffee Drop"},
    )

    state = next_question(intent)

    assert state.ready_to_create is True
    assert state.question is None
