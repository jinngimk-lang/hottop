from hottop.intake import resolve_intent


def test_common_platform_aliases_are_inferred_conservatively():
    assert resolve_intent("做个 IG 高级广告").platform.value == "instagram"
    assert resolve_intent("做个 LinkedIn 行业观点广告").platform.value == "linkedin"
    assert resolve_intent("做个微博热点梗").platform.value == "weibo"
