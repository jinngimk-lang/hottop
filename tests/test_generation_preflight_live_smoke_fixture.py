import json
from datetime import UTC, datetime
from pathlib import Path

from hottop.generation_preflight import GenerationPreflightInput, evaluate_generation_preflight

ROOT = Path(__file__).resolve().parents[1]
NOW = datetime(2026, 8, 25, 9, 30, tzinfo=UTC)


def test_archived_live_reuters_preflight_passes_same_runtime_gate() -> None:
    raw = json.loads(
        (ROOT / "examples/preflight/live-smoke-2026-08-25.json").read_text(
            encoding="utf-8"
        )
    )

    result = evaluate_generation_preflight(
        GenerationPreflightInput.model_validate(raw),
        now=NOW,
    )

    assert result.ready is True
    assert result.subject_name == "Hottop"
    assert result.hotspot_id == "reuters-nvidia-ai-rally-2026-08-25"
    assert result.publication_age_hours is None
    assert result.fresh_evidence_count == 1
