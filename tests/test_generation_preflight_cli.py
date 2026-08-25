import json
from datetime import UTC, datetime, timedelta

from typer.testing import CliRunner

from hottop.cli import app

runner = CliRunner()
NOW = datetime(2026, 8, 25, 9, 30, tzinfo=UTC)


def _payload(*, researched_at: datetime | None = None) -> dict:
    published_at = NOW - timedelta(hours=2)
    return {
        "output_kind": "video",
        "product": {
            "name": "Dynamic Product",
            "subject_type": "service",
        },
        "hotspot": {
            "id": "current-news",
            "title": "Current news event",
            "url": "https://news.example.com/current-news",
            "source": "news-example",
            "published_at": published_at.isoformat(),
            "evidence": [
                {
                    "url": "https://news.example.com/current-news",
                    "source": "news-example",
                    "observed_at": (NOW - timedelta(minutes=10)).isoformat(),
                    "published_at": published_at.isoformat(),
                }
            ],
        },
        "visual_style": "cinematic live-action with restrained documentary texture",
        "style_rationale": "The live current event benefits from credible real-world staging rather than a reused historical meme style.",
        "output_format": "short-cinematic-video",
        "researched_at": (researched_at or NOW - timedelta(minutes=5)).isoformat(),
    }


def test_generation_preflight_cli_emits_ready_contract(tmp_path) -> None:
    path = tmp_path / "preflight.json"
    path.write_text(json.dumps(_payload()), encoding="utf-8")

    result = runner.invoke(
        app,
        ["generation-preflight", str(path), "--now", NOW.isoformat()],
    )

    assert result.exit_code == 0, result.stdout
    output = json.loads(result.stdout)
    assert output["schema_version"] == "hottop.generation-preflight.v1"
    assert output["ready"] is True
    assert output["subject_name"] == "Dynamic Product"
    assert output["hotspot_id"] == "current-news"
    assert output["visual_style"].startswith("cinematic live-action")


def test_generation_preflight_cli_exits_nonzero_when_research_is_stale(tmp_path) -> None:
    path = tmp_path / "preflight.json"
    path.write_text(
        json.dumps(_payload(researched_at=NOW - timedelta(hours=7))),
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        ["generation-preflight", str(path), "--now", NOW.isoformat()],
    )

    assert result.exit_code != 0
    assert "research-observation-stale" in result.output
