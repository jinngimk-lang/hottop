from datetime import UTC, datetime

import pytest

from hottop.models import Evidence, ProductProfile, TrendCandidate


def test_trend_candidate_requires_core_identity():
    candidate = TrendCandidate(
        id="dailyhot:1",
        title="A current topic",
        url="https://example.com/topic",
        source="dailyhot",
    )
    assert candidate.source == "dailyhot"
    assert candidate.tags == []
    assert candidate.evidence == []


def test_product_profile_defaults_to_satirical_comparison_posture():
    product = ProductProfile(name="InkClawAgent", url="https://inkclawagent.com/home")
    assert product.name == "InkClawAgent"
    assert product.default_claim_status == "satire"


def test_evidence_keeps_timestamp_timezone_aware():
    now = datetime.now(UTC)
    evidence = Evidence(url="https://example.com/a", source="example", observed_at=now)
    assert evidence.observed_at.tzinfo is not None


def test_empty_title_is_rejected():
    with pytest.raises(ValueError):
        TrendCandidate(id="x", title="", url="https://example.com", source="x")
