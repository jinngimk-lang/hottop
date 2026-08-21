import pytest

from hottop.collectors.base import SourceError
from hottop.enrichment import EnrichmentPipeline, EnrichmentResult


class StubAdapter:
    def __init__(self, name: str, result: str | None = None, error: str | None = None):
        self.name = name
        self.result = result
        self.error = error
        self.calls: list[str] = []

    async def markdown(self, url: str) -> str:
        self.calls.append(url)
        if self.error:
            raise SourceError(self.error)
        assert self.result is not None
        return self.result


@pytest.mark.asyncio
async def test_enrichment_prefers_first_successful_provider():
    crawl4ai = StubAdapter("crawl4ai", result="# primary")
    firecrawl = StubAdapter("firecrawl", result="# secondary")
    plain = StubAdapter("plain-http", result="# fallback")

    pipeline = EnrichmentPipeline(
        providers=[
            ("crawl4ai", crawl4ai),
            ("firecrawl", firecrawl),
            ("plain-http", plain),
        ]
    )

    result = await pipeline.markdown("https://example.com/story")

    assert result == EnrichmentResult(provider="crawl4ai", markdown="# primary")
    assert firecrawl.calls == []
    assert plain.calls == []


@pytest.mark.asyncio
async def test_enrichment_falls_back_in_declared_order():
    crawl4ai = StubAdapter("crawl4ai", error="offline")
    firecrawl = StubAdapter("firecrawl", error="not configured")
    plain = StubAdapter("plain-http", result="# public page")

    pipeline = EnrichmentPipeline(
        providers=[
            ("crawl4ai", crawl4ai),
            ("firecrawl", firecrawl),
            ("plain-http", plain),
        ]
    )

    result = await pipeline.markdown("https://example.com/story")

    assert result.provider == "plain-http"
    assert result.markdown == "# public page"
    assert result.failures == ["crawl4ai: offline", "firecrawl: not configured"]


@pytest.mark.asyncio
async def test_enrichment_raises_with_all_provider_failures():
    pipeline = EnrichmentPipeline(
        providers=[
            ("crawl4ai", StubAdapter("crawl4ai", error="offline")),
            ("plain-http", StubAdapter("plain-http", error="403")),
        ]
    )

    with pytest.raises(SourceError, match="crawl4ai: offline; plain-http: 403"):
        await pipeline.markdown("https://example.com/story")
