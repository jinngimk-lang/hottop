import json

from typer.testing import CliRunner

from hottop.cli import app
from hottop.comparison_research import ComparisonResearchResult, adapt_comparison_research_results

runner = CliRunner()


def test_adapter_builds_evidence_bearing_comparison_candidate():
    results = [
        ComparisonResearchResult(
            name="Legacy Workflow",
            relation="legacy-workflow",
            url="https://example.com/research",
            source="Example Research",
            note="Requires repeated manual handoffs for this job.",
            source_quality=0.8,
            pain_point_contrast=0.9,
            claim_posture="supported",
        )
    ]

    [candidate] = adapt_comparison_research_results(results)

    assert candidate.name == "Legacy Workflow"
    assert candidate.evidence_quality == 0.8
    assert candidate.claim_posture == "supported"
    assert len(candidate.evidence) == 1
    assert str(candidate.evidence[0].url) == "https://example.com/research"
    assert candidate.evidence[0].note == "Requires repeated manual handoffs for this job."


def test_position_accepts_research_results_without_manual_candidate_json(tmp_path):
    research_path = tmp_path / "research.json"
    research_path.write_text(
        json.dumps(
            {
                "research_results": [
                    {
                        "name": "Manual spreadsheet workflow",
                        "relation": "manual-workaround",
                        "url": "https://example.com/manual-workflow",
                        "source": "Example Research",
                        "note": "The documented workflow uses repeated manual reconciliation.",
                        "source_quality": 0.75,
                        "pain_point_contrast": 0.95,
                        "claim_posture": "supported",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["position", "Example Product", "--comparisons", str(research_path)],
    )

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    candidate = payload["comparison_candidates"][0]
    assert candidate["name"] == "Manual spreadsheet workflow"
    assert candidate["relation"] == "manual-workaround"
    assert candidate["evidence_quality"] == 0.75
    assert candidate["claim_posture"] == "supported"
    assert candidate["evidence"][0]["source"] == "Example Research"
    assert payload["selected_comparison"]["name"] == "Manual spreadsheet workflow"
