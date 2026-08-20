from __future__ import annotations

import httpx

from ..models import Evidence, TrendCandidate
from ..source_presets import resolve_source_quality
from .base import SourceError, parse_timestamp

DAILYHOT_SOURCE_QUALITY = 0.62


class DailyHotApiCollector:
    def __init__(
        self,
        route: str,
        client: httpx.AsyncClient | None = None,
        base_url: str = "https://api-hot.imsyy.top",
        timeout: float = 15.0,
        source_quality: float = DAILYHOT_SOURCE_QUALITY,
    ) -> None:
        self.route = route.strip("/")
        self.client = client
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.source_quality = source_quality

    async def collect(self, limit: int = 30) -> list[TrendCandidate]:
        owns_client = self.client is None
        client = self.client or httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)
        try:
            response = await client.get(f"/{self.route}")
            response.raise_for_status()
            payload = response.json()
        except (httpx.HTTPError, ValueError, TypeError) as exc:
            raise SourceError(f"dailyhot:{self.route}: {exc}") from exc
        finally:
            if owns_client:
                await client.aclose()

        data = payload.get("data") or []
        results: list[TrendCandidate] = []
        for index, item in enumerate(data[: max(0, limit)], start=1):
            title = str(item.get("title") or "").strip()
            url = item.get("url") or item.get("mobileUrl")
            if not title or not url:
                continue
            raw_id = item.get("id", index)
            hot = item.get("hot")
            metrics = {"source_rank_score": 1 / index}
            if isinstance(hot, (int, float)):
                metrics["hot"] = float(hot)
            published_at = parse_timestamp(item.get("timestamp"))
            source = f"dailyhot:{self.route}"
            quality = resolve_source_quality(url, fallback=self.source_quality)
            evidence = [
                Evidence(
                    url=url,
                    source=source,
                    published_at=published_at,
                    source_quality=quality,
                )
            ]
            results.append(
                TrendCandidate(
                    id=f"dailyhot:{self.route}:{raw_id}",
                    title=title,
                    url=url,
                    source=source,
                    source_rank=index,
                    source_quality=quality,
                    published_at=published_at,
                    summary=item.get("desc"),
                    metrics=metrics,
                    evidence=evidence,
                )
            )
        return results
