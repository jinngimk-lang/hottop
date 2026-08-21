import asyncio

from hottop.batch_config import BatchConfig, BatchSourceConfig
from hottop.cli import _discover_configured
from hottop.models import TrendCandidate
from hottop.source_presets import resolve_source_quality


def test_source_quality_respects_selected_preset_before_fallback():
    assert resolve_source_quality(
        "https://techcrunch.com/story",
        fallback=0.5,
        preset="ai-tech",
    ) == 0.84
    assert resolve_source_quality(
        "https://techcrunch.com/story",
        fallback=0.5,
        preset="film-entertainment",
    ) == 0.5


def test_configured_batch_passes_preset_into_collector(monkeypatch):
    seen: list[tuple[str, str | None]] = []

    class FakeDailyHotCollector:
        def __init__(self, route: str, preset: str | None = None) -> None:
            seen.append((route, preset))

        async def collect(self, limit: int = 30) -> list[TrendCandidate]:
            return []

    monkeypatch.setattr("hottop.cli.DailyHotApiCollector", FakeDailyHotCollector)
    config = BatchConfig(
        name="culture",
        sources=[
            BatchSourceConfig(
                type="dailyhot",
                key="douban-movie",
                limit=5,
                preset="film-entertainment",
            )
        ],
    )

    asyncio.run(_discover_configured(config))

    assert seen == [("douban-movie", "film-entertainment")]
