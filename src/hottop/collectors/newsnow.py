from __future__ import annotations

import httpx

from ..models import Evidence, TrendCandidate
from .base import SourceError, parse_timestamp


class NewsNowCollector:
    def __init__(
        self,
        source_id: str,
        client: httpx.AsyncClient | None = None,
        base_url: str = "https://newsnow.busiyi.world",
        timeout: float = 15.0,
    ) -> None:
        self.source_id = source_id
        self.client = client
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def collect(self, limit: int = 30) -> list[TrendCandidate]:
        owns_client = self.client is None
        client = self.client or httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)
        try:
            response = await client.get("/api/s", params={"id": self.source_id})
            response.raise_for_status()
            payload = response.json()
        except (httpx.HTTPError, ValueError, TypeError) as exc:
            raise SourceError(f"newsnow:{self.source_id}: {exc}") from exc
        finally:
            if owns_client:
                await client.aclose()

        results: list[TrendCandidate] = []
        for index, item in enumerate((payload.get("items") or [])[: max(0, limit)], start=1):
            title = str(item.get("title") or "").strip()
            url = item.get("url") or item.get("mobileUrl")
            if not title or not url:
                continue
            extra = item.get("extra") or {}
            results.append(
                TrendCandidate(
                    id=f"newsnow:{self.source_id}:{item.get('id', index)}",
                    title=title,
                    url=url,
                    source=f"newsnow:{self.source_id}",
                    source_rank=index,
                    published_at=parse_timestamp(item.get("pubDate") or extra.get("date")),
                    summary=extra.get("hover") if isinstance(extra, dict) else None,
                    metrics={"source_rank_score": 1 / index},
                    evidence=[Evidence(url=url, source=f"newsnow:{self.source_id}")],
                )
            )
        return results
