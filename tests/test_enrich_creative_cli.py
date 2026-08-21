import json

from typer.testing import CliRunner

from hottop.cli import app
from hottop.enrichment import EnrichmentResult

runner = CliRunner()


class FakeEnrichmentPipeline:
    async def markdown(self, url: str) -> EnrichmentResult:
        assert url == "https://example.com/trend"
        return EnrichmentResult(
            provider="test-provider",
            markdown="# Source context\n\nA richer explanation of the trend and why it matters.",
            failures=["crawl4ai: unavailable"],
        )


def test_enrich_creative_emits_selected_trend_plus_source_context(tmp_path, monkeypatch):
    input_path = tmp_path / "trends.json"
    input_path.write_text(
        json.dumps(
            [
                {
                    "id": "trend-1",
                    "title": "A current cultural trend",
                    "url": "https://example.com/trend",
                    "source": "test",
                    "summary": "Short discovery summary",
                    "tags": ["consumer"],
                }
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "hottop.cli.build_default_enrichment_pipeline",
        lambda: FakeEnrichmentPipeline(),
    )

    result = runner.invoke(app, ["enrich-creative", str(input_path), "--index", "0"])

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["schema_version"] == "hottop.creative-enrichment.v1"
    assert payload["candidate"]["id"] == "trend-1"
    assert payload["candidate"]["summary"] == "Short discovery summary"
    assert payload["enrichment"]["provider"] == "test-provider"
    assert "richer explanation" in payload["enrichment"]["markdown"]
    assert payload["enrichment"]["failures"] == ["crawl4ai: unavailable"]
