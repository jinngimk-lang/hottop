from hottop.intake import resolve_intent


def test_original_request_is_preserved_for_audit_and_revision():
    request = "给产品做个小红书广告"
    assert resolve_intent(request).request == request
