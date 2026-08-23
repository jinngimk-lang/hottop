import pytest

from hottop.models import TrendCandidate


def _trend(**overrides):
    payload = {
        "id": "dailyhot:1",
        "title": "A current topic",
        "url": "https://example.com/topic",
        "source": "dailyhot",
    }
    payload.update(overrides)
    return TrendCandidate(**payload)


def test_trend_candidate_normalizes_optional_summary_when_present():
    candidate = _trend(summary="  concise source-grounded context  ")

    assert candidate.summary == "concise source-grounded context"


def test_trend_candidate_rejects_blank_optional_summary_when_present():
    with pytest.raises(ValueError, match="trend summary must not be blank"):
        _trend(summary="   ")


def test_trend_candidate_normalizes_tags():
    candidate = _trend(tags=["  consumer-culture  ", "  food  "])

    assert candidate.tags == ["consumer-culture", "food"]


def test_trend_candidate_rejects_blank_tags():
    with pytest.raises(ValueError, match="trend tags must not contain blank text"):
        _trend(tags=["consumer-culture", "   "])
