from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from .collectors.base import SourceError


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
