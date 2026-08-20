from __future__ import annotations

from typing import Any

import httpx

from ..collectors.base import SourceError


class Crawl4AIAdapter:
    """Small client for a self-hosted Crawl4AI Docker API.

    The adapter intentionally uses the hardened HTTP boundary rather than
    embedding Crawl4AI internals in Hottop. `/health` is unauthenticated in
    Crawl4AI 0.9+, while crawl endpoints receive the bearer token when set.
    """

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:11235",
        token: str | None = None,
        client: httpx.AsyncClient | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.client = client
        self.timeout = timeout

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    async def doctor(self) -> dict[str, Any]:
        owns_client = self.client is None
        client = self.client or httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)
        try:
            response = await client.get("/health")
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict):
                raise TypeError("health response must be an object")
            return payload
        except (httpx.HTTPError, ValueError, TypeError) as exc:
            raise SourceError(f"crawl4ai health: {exc}") from exc
        finally:
            if owns_client:
                await client.aclose()

    async def markdown(self, url: str) -> str:
        payload = {
            "urls": [url],
            "browser_config": {"type": "BrowserConfig", "params": {"headless": True}},
            "crawler_config": {
                "type": "CrawlerRunConfig",
                "params": {"cache_mode": "BYPASS"},
            },
        }
        data = await self._post_json("/crawl", payload)
        if not data.get("success"):
            raise SourceError("crawl4ai crawl reported failure")
        results = data.get("results") or []
        if not results:
            raise SourceError("crawl4ai crawl returned no results")
        markdown = results[0].get("markdown")
        if isinstance(markdown, str):
            return markdown
        if isinstance(markdown, dict):
            for key in ("fit_markdown", "raw_markdown", "markdown"):
                value = markdown.get(key)
                if isinstance(value, str):
                    return value
        raise SourceError("crawl4ai result did not contain markdown")

    async def screenshot(self, url: str) -> dict[str, Any]:
        return await self._post_json("/screenshot", {"url": url})

    async def _post_json(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        owns_client = self.client is None
        client = self.client or httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)
        try:
            response = await client.post(path, json=payload, headers=self._headers())
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict):
                raise TypeError("response must be an object")
            return data
        except (httpx.HTTPError, ValueError, TypeError) as exc:
            raise SourceError(f"crawl4ai {path}: {exc}") from exc
        finally:
            if owns_client:
                await client.aclose()
