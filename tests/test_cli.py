import json

from typer.testing import CliRunner

from hottop.cli import app
from hottop.models import TrendCandidate

runner = CliRunner()


def test_legacy_brief_command_fails_closed_without_hotspot_mechanism_analysis(tmp_path):
    candidate_path = tmp_path / "candidate.json"
    candidate_path.write_text(
        json.dumps(
            {
                "id": "film:1",
                "title": "独眼巨人守住山洞出口",
                "url": "https://example.com/t",
                "source": "test",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    product_path = tmp_path / "product.yml"
    product_path.write_text(
        "name: InkClawAgent\nurl: https://inkclawagent.com/home\nstrengths:\n  - multi-agent collaboration\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "brief",
            str(candidate_path),
            "--product",
            str(product_path),
            "--compare",
            "work巴迪",
        ],
    )

    assert result.exit_code != 0
    assert "mechanism_mapping is required" in str(result.exception)


def test_rank_command_orders_candidates_by_score(tmp_path):
    input_path = tmp_path / "candidates.json"
    input_path.write_text(
        json.dumps(
            [
                {
                    "id": "weak",
                    "title": "old",
                    "url": "https://example.com/weak",
                    "source": "test",
                    "metrics": {"recognizability": 0.1},
                },
                {
                    "id": "strong",
                    "title": "visual conflict",
                    "url": "https://example.com/strong",
                    "source": "test",
                    "metrics": {
                        "recognizability": 0.9,
                        "conflict_clarity": 0.9,
                        "visual_potential": 0.9,
                        "product_fit": 0.8,
                        "cross_source_count": 4,
                    },
                },
            ]
        ),
        encoding="utf-8",
    )

    result = runner.invoke(app, ["rank", str(input_path), "--top", "1"])

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload[0]["candidate"]["id"] == "strong"


def test_doctor_command_is_nonfatal_without_optional_integrations(monkeypatch):
    monkeypatch.delenv("FIRECRAWL_API_KEY", raising=False)
    monkeypatch.delenv("CRAWL4AI_TOKEN", raising=False)

    result = runner.invoke(app, ["doctor"])

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["core"] == "ok"
    assert payload["agent_reach"]["required"] is False
    assert payload["crawl4ai"]["required"] is False
    assert payload["crawl4ai"]["configured"] is True
    assert payload["firecrawl"]["required"] is False
    assert payload["firecrawl"]["configured"] is False
    assert payload["firecrawl"]["api_version"] == "v2"


def test_legacy_render_command_fails_closed_without_hotspot_mechanism_analysis(tmp_path):
    candidate_path = tmp_path / "candidate.json"
    candidate_path.write_text(
        json.dumps(
            {
                "id": "film:render",
                "title": "洞穴破局",
                "url": "https://example.com/render",
                "source": "test",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    product_path = tmp_path / "product.yml"
    product_path.write_text("name: InkClawAgent\n", encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "render",
            str(candidate_path),
            "--product",
            str(product_path),
            "--compare",
            "work巴迪",
        ],
    )

    assert result.exit_code != 0
    assert "mechanism_mapping is required" in str(result.exception)


def test_batch_command_fans_in_sources_but_does_not_invent_creative_briefs(monkeypatch, tmp_path):
    product_path = tmp_path / "product.yml"
    product_path.write_text("name: InkClawAgent\n", encoding="utf-8")
    calls: list[tuple[str, str, int]] = []

    async def fake_discover(source: str, key: str, limit: int) -> list[TrendCandidate]:
        calls.append((source, key, limit))
        return [
            TrendCandidate(
                id=f"{source}:{key}",
                title=f"{key} visual conflict",
                url=f"https://example.com/{source}/{key}",
                source=source,
            )
        ]

    monkeypatch.setattr("hottop.cli._discover", fake_discover)

    result = runner.invoke(
        app,
        [
            "batch",
            "--product",
            str(product_path),
            "--source",
            "dailyhot:zhihu",
            "--source",
            "newsnow:tech",
            "--limit-per-source",
            "7",
            "--top",
            "2",
        ],
    )

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert calls == [("dailyhot", "zhihu", 7), ("newsnow", "tech", 7)]
    assert payload["input_count"] == 2
    assert payload["briefs"] == []
    assert set(payload["mechanism_required_ids"]) == {"dailyhot:zhihu", "newsnow:tech"}


def test_batch_command_loads_stored_yaml_config_without_template_briefing(monkeypatch, tmp_path):
    product_path = tmp_path / "product.yml"
    product_path.write_text("name: InkClawAgent\n", encoding="utf-8")
    config_path = tmp_path / "batch.yml"
    config_path.write_text(
        """
name: stored-batch
sources:
  - type: dailyhot
    key: zhihu
    limit: 4
  - type: newsnow
    key: tech
    limit: 9
top: 1
comparison_target: work巴迪
""",
        encoding="utf-8",
    )
    calls: list[tuple[str, str, int]] = []

    async def fake_discover(source: str, key: str, limit: int) -> list[TrendCandidate]:
        calls.append((source, key, limit))
        return [
            TrendCandidate(
                id=f"{source}:{key}",
                title=f"{key} visual conflict",
                url=f"https://example.com/{source}/{key}",
                source=source,
            )
        ]

    monkeypatch.setattr("hottop.cli._discover", fake_discover)

    result = runner.invoke(
        app,
        [
            "batch",
            "--product",
            str(product_path),
            "--config",
            str(config_path),
        ],
    )

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert calls == [("dailyhot", "zhihu", 4), ("newsnow", "tech", 9)]
    assert payload["briefs"] == []
    assert len(payload["mechanism_required_ids"]) == 1
