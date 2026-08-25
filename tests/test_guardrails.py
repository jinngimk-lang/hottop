from hottop.guardrails import classify_claim


def test_quantified_superiority_without_evidence_needs_evidence():
    assert classify_claim("InkClawAgent 比 work巴迪 快 10 倍", evidence_count=0) == "needs_evidence"


def test_quantified_superiority_with_evidence_can_be_supported():
    assert classify_claim("InkClawAgent 比 work巴迪 快 10 倍", evidence_count=2) == "supported"


def test_unquantified_meme_punchline_stays_satire():
    assert classify_claim("还得是 InkClawAgent 强", evidence_count=0) == "satire"
