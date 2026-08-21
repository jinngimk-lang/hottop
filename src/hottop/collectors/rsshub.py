from __future__ import annotations

import os
from urllib.parse import urlparse

import httpx

from ..models import TrendCandidate
from .rss import RSSCollector, RSS_SOURCE_QUALITY


class RSSHubCollector:
    """Treat RSSHub as an optional external feed router and reuse the RSS parser."""

    def __init__(
        self,
        route: str,
        *,
        base_url: str | None = None,
        client: httpx.AsyncClient | None = None,
        timeout: float = 15.0,
        source_quality: float = RSS_SOURCE_QUALITY,
    ) -> None:
        normalized_route = route.strip().lstrip("/")
        if not normalized_route:
            raise ValueError("RSSHub route must not be blank")

        resolved_base = (base_url or os.getenv("RSSHUB_BASE_URL") or "").strip().rstrip("/")
        if not resolved_base:
            raise ValueError("RSSHUB_BASE_URL must be configured for rsshub sources")
        parsed = urlparse(resolved_base)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("RSSHUB_BASE_URL must be an absolute HTTP(S) URL")

        self.route = normalized_route
        self.base_url = resolved_base
        self.feed_url = f"{resolved_base}/{normalized_route}"
        self.source_name = f"rsshub:{normalized_route}"
        self._collector = RSSCollector(
            feed_url=self.feed_url,
            source_name=self.source_name,
            client=client,
            timeout=timeout,
            source_quality=source_quality,
        )

    async def collect(self, limit: int = 30) -> list[TrendCandidate]:
        return await self._collector.collect(limit=limit)
