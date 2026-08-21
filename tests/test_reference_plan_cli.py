import json

from typer.testing import CliRunner

from hottop.cli import app

runner = CliRunner()


def test_reference_plan_emits_non_executing_public_capture_plan() -> None:
    result = runner.invoke(
        app,
        [
            "reference-plan",
            "https://example.com/campaign",
            "--question",
            "How does the reveal sequence keep curiosity?",
            "--mobile",
        ],
    )

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["schema_version"] == "hottop.reference-plan.v1"
    assert payload["url"] == "https://example.com/campaign"
    assert payload["question"] == "How does the reveal sequence keep curiosity?"
    assert payload["rights_mode"] == "analysis-only"
    assert payload["execute"] is False
    assert payload["persistent_profile"] is False
    assert payload["commands"][0][-1] == "--mobile"
    assert payload["commands"][-1][-1] == "close"


def test_reference_plan_rejects_non_http_urls() -> None:
    result = runner.invoke(
        app,
        [
            "reference-plan",
            "file:///tmp/private.html",
            "--question",
            "inspect",
        ],
    )

    assert result.exit_code != 0
    assert "http" in str(result.exception).lower()
