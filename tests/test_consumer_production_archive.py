import json
from pathlib import Path

from hottop.directives import build_creative_directive
from hottop.intake import CreativeIntent
from hottop.models import TrendCandidate, VisualReference
from hottop.orchestrator import OrchestrationInput, orchestrate

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "examples/runs/consumer-swipe-reveal-production.json"


def test_consumer_production_archive_exercises_full_flexible_path():
    raw = json.loads(ARCHIVE.read_text(encoding="utf-8"))

    assert raw["schema_version"] == "hottop.production-archive.v1"
    intent = CreativeIntent.model_validate(raw["intent"])
    candidate = TrendCandidate.model_validate(raw["enrichment"]["candidate"])
    assert raw["enrichment"]["schema_version"] == "hottop.creative-enrichment.v1"
    assert raw["enrichment"]["enrichment"]["markdown"]
    assert candidate.evidence

    orchestration_input = OrchestrationInput.model_validate(raw["orchestration_input"])
    assert orchestration_input.references
    reference = VisualReference.model_validate(raw["orchestration_input"]["references"][0])
    assert reference.rights_mode == "analysis-only"
    assert reference.what_not_to_copy

    directive = build_creative_directive(intent, orchestration_input.promotion_context)
    assert directive.project_shape == "consumer-product"
    assert directive.direction_lanes[0] == "bridge-led-metaphor"
    assert directive.preferred_forms[0] == "swipe-reveal"
    assert "misdirection-reveal" in directive.joke_mechanics

    result = orchestrate(orchestration_input)
    assert result.schema_version == "hottop.orchestration.v1"
    assert result.selected_concept.strategy.category_default
    assert result.selected_concept.strategy.deleted_constraint
    assert result.selected_concept.strategy.new_competition_axis
    assert result.selected_concept.strategy.expression_form == "swipe-reveal"
    assert result.selected_render.schema_version == "hottop.render.v2"
    assert len(result.selected_render.frames) == 3
