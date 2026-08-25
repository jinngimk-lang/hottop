import importlib
import importlib.util
from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from hottop.models import Evidence, ProductProfile, TrendCandidate

NOW = datetime(2026, 8, 25, 9, 30, tzinfo=UTC)


def _module():
    spec = importlib.util.find_spec("hottop.generation_preflight")
    assert spec is not None, "hottop.generation_preflight must exist before asset generation"
    return importlib.import_module("hottop.generation_preflight")


def _trend(*, published_at: datetime | None = None, observed_at: datetime | None = None, evidence: bool = True) -> TrendCandidate:
    evidence_items = []
    if evidence:
        evidence_items = [
            Evidence(
                url="https://news.example.com/current-topic",
                source="news-example",
                observed_at=observed_at or NOW - timedelta(minutes=20),
                published_at=published_at,
                source_quality=0.9,
            )
        ]
    return TrendCandidate(
        id="current-topic",
        title="A current cultural/news topic",
        url="https://news.example.com/current-topic",
        source="news-example",
        source_quality=0.9,
        published_at=published_at,
        evidence=evidence_items,
    )


def _preflight_payload(module, **overrides):
    payload = {
        "output_kind": "image",
        "product": ProductProfile(name="Example Product", subject_type="product"),
        "hotspot": _trend(published_at=NOW - timedelta(hours=2)),
        "visual_style": "documentary-social realism with restrained typography",
        "style_rationale": "The selected hotspot is real-world social/news material, so a social-native treatment fits better than inherited low-poly or four-panel defaults.",
        "output_format": "single-visual-metaphor",
        "researched_at": NOW - timedelta(minutes=15),
    }
    payload.update(overrides)
    return module.GenerationPreflightInput.model_validate(payload)


def test_fresh_research_and_hotspot_evidence_are_generation_ready() -> None:
    module = _module()
    preflight = _preflight_payload(module)

    result = module.evaluate_generation_preflight(preflight, now=NOW)

    assert result.ready is True
    assert result.blockers == []
    assert result.subject_name == "Example Product"
    assert result.hotspot_id == "current-topic"
    assert result.output_kind == "image"
    assert result.visual_style == preflight.visual_style
    assert result.output_format == "single-visual-metaphor"
    assert result.research_age_hours == pytest.approx(0.25)
    assert result.publication_age_hours == pytest.approx(2.0)


def test_missing_hotspot_evidence_blocks_generation() -> None:
    module = _module()
    preflight = _preflight_payload(module, hotspot=_trend(published_at=NOW - timedelta(hours=1), evidence=False))

    result = module.evaluate_generation_preflight(preflight, now=NOW)

    assert result.ready is False
    assert "hotspot-evidence-missing" in result.blockers


def test_stale_live_research_blocks_generation_even_when_story_is_recent() -> None:
    module = _module()
    preflight = _preflight_payload(module, researched_at=NOW - timedelta(hours=7))

    result = module.evaluate_generation_preflight(preflight, now=NOW)

    assert result.ready is False
    assert "research-observation-stale" in result.blockers


def test_stale_published_story_blocks_generation_by_default() -> None:
    module = _module()
    published = NOW - timedelta(days=8)
    preflight = _preflight_payload(
        module,
        hotspot=_trend(published_at=published, observed_at=NOW - timedelta(minutes=10)),
    )

    result = module.evaluate_generation_preflight(preflight, now=NOW)

    assert result.ready is False
    assert "hotspot-publication-stale" in result.blockers


def test_product_hotspot_style_and_format_are_required_per_request() -> None:
    module = _module()
    payload = {
        "output_kind": "video",
        "product": ProductProfile(name="Another Product", subject_type="service"),
        "hotspot": _trend(published_at=None),
        "researched_at": NOW - timedelta(minutes=5),
    }

    with pytest.raises(ValidationError):
        module.GenerationPreflightInput.model_validate(payload)


def test_unknown_publication_time_can_pass_with_fresh_observation_but_is_not_invented() -> None:
    module = _module()
    preflight = _preflight_payload(
        module,
        hotspot=_trend(published_at=None, observed_at=NOW - timedelta(minutes=5)),
    )

    result = module.evaluate_generation_preflight(preflight, now=NOW)

    assert result.ready is True
    assert result.publication_age_hours is None
    assert result.fresh_evidence_count == 1
