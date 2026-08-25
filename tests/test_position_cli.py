import json

from typer.testing import CliRunner

from hottop.cli import app

runner = CliRunner()


def test_position_command_accepts_term_and_emits_research_handoff():
    result = runner.invoke(app, ["position", "InkClawAgent"])

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["schema_version"] == "hottop.position.v1"
    assert payload["profile"]["name"] == "InkClawAgent"
    assert payload["context"]["subject_name"] == "InkClawAgent"
    assert payload["context"]["subject_type"] == "keyword"
    assert '"InkClawAgent" competitors' in payload["research_queries"]
    assert '"InkClawAgent" alternatives' in payload["research_queries"]
    assert payload["comparison_candidates"] == []


def test_position_command_accepts_profile_yaml(tmp_path):
    profile_path = tmp_path / "coffee.yml"
    profile_path.write_text(
        """
name: Example Coffee
subject_type: brand
category: coffee chain
jobs_to_be_done:
  - get coffee quickly before work
pain_points_solved:
  - long ordering waits
differentiators:
  - quick pickup
known_alternatives:
  - Incumbent Cafe
""".strip()
        + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["position", "--product", str(profile_path)])

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["context"]["subject_type"] == "brand"
    assert payload["context"]["primary_pain_point"] == "long ordering waits"
    assert "best coffee chain for get coffee quickly before work" in payload["research_queries"]
    assert '"Example Coffee" vs "Incumbent Cafe"' in payload["research_queries"]
