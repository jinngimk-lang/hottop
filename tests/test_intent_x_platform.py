from hottop.intake import resolve_intent


def test_x_platform_can_be_inferred_without_confusing_normal_text():
    assert resolve_intent("发到 X 上的产品梗图").platform.value == "x"
