from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Protocol

from .collectors.base import SourceError
from .integrations.crawl4ai import Crawl4AIAdapter
from .integrations.firecrawl import FirecrawlAdapter
from .integrations.plain_http import PlainHttpAdapter


class MarkdownProvider(Protocol):
    async def markdown(self, url: str) -> str: ...


@dataclass(frozen=True)
class EnrichmentResult:
    provider: str
    markdown: str
    failures: list[str] = field(default_factory=list)


class EnrichmentPipeline:
    """Try enrichment providers in deterministic priority order.

    Providers are deliberately injected so Hottop can prefer a self-hosted
    Crawl4AI service, then use Firecrawl when configured, and finally fall
    back to a plain public-web reader without coupling the pipeline to any
    one vendor.
    """

    def __init__(self, providers: list[tuple[str, MarkdownProvider]]) -> None:
        self.providers = providers

    async def markdown(self, url: str) -> EnrichmentResult:
        failures: list[str] = []
        for name, provider in self.providers:
            try:
                markdown = await provider.markdown(url)
            except SourceError as exc:
                failures.append(f"{name}: {exc}")
                continue
            if markdown.strip():
                return EnrichmentResult(provider=name, markdown=markdown, failures=failures)
            failures.append(f"{name}: empty markdown")

        detail = "; ".join(failures) if failures else "no enrichment providers configured"
        raise SourceError(f"enrichment failed: {detail}")


def build_default_enrichment_pipeline() -> EnrichmentPipeline:
    """Build the normal enrichment chain from environment configuration.

    Crawl4AI is always attempted first because it is the preferred self-hosted
    browser/deep-page service. Firecrawl is only inserted when an API key is
    explicitly configured. Plain HTTP is always the final public-web fallback.
    """

    crawl4ai = Crawl4AIAdapter(
        base_url=os.getenv("CRAWL4AI_URL", "http://127.0.0.1:11235"),
        token=os.getenv("CRAWL4AI_TOKEN"),
    )
    providers: list[tuple[str, MarkdownProvider]] = [("crawl4ai", crawl4ai)]

    firecrawl_key = os.getenv("FIRECRAWL_API_KEY")
    if firecrawl_key:
        providers.append(
            (
                "firecrawl",
                FirecrawlAdapter(
                    api_key=firecrawl_key,
                    base_url=os.getenv("FIRECRAWL_URL", "https://api.firecrawl.dev"),
                ),
            )
        )

    providers.append(("plain-http", PlainHttpAdapter()))
    return EnrichmentPipeline(providers=providers)
