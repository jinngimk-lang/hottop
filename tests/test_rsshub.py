import asyncio

import pytest
from hottop.collectors.rsshub import RSSHubCollector

from hottop.batch_config import BatchSourceConfig
from hottop.cli import _discover
from hottop.models import TrendCandidate


def test_rsshub_requires_explicit_base_url(monkeypatch):
    monkeypatch.delenv("RSSHUB_BASE_URL", raising=False)

    with pytest.raises(ValueError, match="RSSHUB_BASE_URL"):
        RSSHubCollector(route="bilibili/ranking/0")


def test_rsshub_normalizes_base_url_and_route():
    collector = RSSHubCollector(
        route="/bilibili/ranking/0",
        base_url="https://rsshub.example/",
    )

    assert collector.feed_url == "https://rsshub.example/bilibili/ranking/0"
    assert collector.source_name == "rsshub:bilibili/ranking/0"


def test_batch_source_config_accepts_rsshub():
    source = BatchSourceConfig(type="rsshub", key="bilibili/ranking/0", limit=5)

    assert source.spec == "rsshub:bilibili/ranking/0"


def test_cli_discover_delegates_rsshub_source(monkeypatch):
    calls: list[tuple[str, int]] = []

    class FakeRSSHubCollector:
        def __init__(self, route: str):
            self.route = route

        async def collect(self, limit: int = 30) -> list[TrendCandidate]:
            calls.append((self.route, limit))
            return [
                TrendCandidate(
                    id="rsshub:test",
                    title="RSSHub trend",
                    url="https://example.com/rsshub",
                    source="rsshub:test",
                )
            ]

    monkeypatch.setattr("hottop.cli.RSSHubCollector", FakeRSSHubCollector)

    result = asyncio.run(_discover("rsshub", "bilibili/ranking/0", 7))

    assert calls == [("bilibili/ranking/0", 7)]
    assert result[0].source == "rsshub:test"
