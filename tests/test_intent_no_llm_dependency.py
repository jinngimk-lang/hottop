from hottop.intake import resolve_intent


def test_intent_resolver_is_deterministic_for_same_request():
    request = "给咖啡新品做一个小红书出圈高级广告"

    assert resolve_intent(request).model_dump() == resolve_intent(request).model_dump()
