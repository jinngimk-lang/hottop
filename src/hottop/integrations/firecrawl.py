from __future__ import annotations

from typing import Any

import httpx

from ..collectors.base import SourceError


class FirecrawlAdapter:
    """Optional Firecrawl v2 enrichment client.

    Firecrawl is a fallback for pages that need hosted scraping infrastructure.
    Crawl4AI remains the preferred self-hostable browser/deep-page layer.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://api.firecrawl.dev",
        client: httpx.AsyncClient | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.client = client
        self.timeout = timeout

    async def doctor(self) -> dict[str, Any]:
        return {
            "configured": bool(self.api_key),
            "base_url": self.base_url,
            "api_version": "v2",
        }

    async def markdown(self, url: str) -> str:
        if not self.api_key:
            raise SourceError("firecrawl is not configured: missing API key")

        payload = {
            "url": url,
            "formats": ["markdown"],
            "onlyMainContent": True,
        }
        data = await self._post_json("/v2/scrape", payload)
        if not data.get("success"):
            raise SourceError("firecrawl scrape reported failure")

        result = data.get("data") or {}
        markdown = result.get("markdown") if isinstance(result, dict) else None
        if not isinstance(markdown, str) or not markdown.strip():
            raise SourceError("firecrawl result did not contain markdown")
        return markdown

    async def _post_json(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        owns_client = self.client is None
        client = self.client or httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)
        try:
            response = await client.post(
                path,
                json=payload,
                headers={"Authorization": f"Bearer {self.api_key}"},
            )
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict):
                raise TypeError("response must be an object")
            return data
        except (httpx.HTTPError, ValueError, TypeError) as exc:
            raise SourceError(f"firecrawl {path}: {exc}") from exc
        finally:
            if owns_client:
                await client.aclose()
