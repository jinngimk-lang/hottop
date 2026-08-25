from hottop.intake import resolve_intent


def test_explicit_constraints_are_preserved_without_interpretation():
    intent = resolve_intent(
        "给产品做一个广告",
        overrides={"promotion_target": "Thing", "constraints": ["不要人物", "必须中文"]},
    )

    assert intent.constraints == ["不要人物", "必须中文"]
