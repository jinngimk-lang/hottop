from __future__ import annotations

from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree as ET

import httpx

from ..models import Evidence, TrendCandidate
from .base import SourceError

RSS_SOURCE_QUALITY = 0.75


def _text(node: ET.Element | None, tag: str) -> str | None:
    if node is None:
        return None
    child = node.find(tag)
    if child is not None and child.text:
        return child.text.strip()
    return None


def _parse_rfc822(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        return parsed.astimezone(UTC)
    except (TypeError, ValueError):
        return None


class RSSCollector:
    def __init__(
        self,
        feed_url: str,
        source_name: str,
        client: httpx.AsyncClient | None = None,
        timeout: float = 15.0,
        source_quality: float = RSS_SOURCE_QUALITY,
    ) -> None:
        self.feed_url = feed_url
        self.source_name = source_name
        self.client = client
        self.timeout = timeout
        self.source_quality = source_quality

    def _candidate(
        self,
        *,
        raw_id: str,
        title: str,
        url: str,
        index: int,
        published_at: datetime | None,
        summary: str | None,
    ) -> TrendCandidate:
        return TrendCandidate(
            id=f"{self.source_name}:{raw_id}",
            title=title,
            url=url,
            source=self.source_name,
            source_rank=index,
            source_quality=self.source_quality,
            published_at=published_at,
            summary=summary,
            metrics={"source_rank_score": 1 / index},
            evidence=[
                Evidence(
                    url=url,
                    source=self.source_name,
                    published_at=published_at,
                    source_quality=self.source_quality,
                )
            ],
        )

    async def collect(self, limit: int = 30) -> list[TrendCandidate]:
        owns_client = self.client is None
        client = self.client or httpx.AsyncClient(timeout=self.timeout)
        try:
            response = await client.get(self.feed_url)
            response.raise_for_status()
            root = ET.fromstring(response.content)
        except (httpx.HTTPError, ET.ParseError, ValueError, TypeError) as exc:
            raise SourceError(f"{self.source_name}: {exc}") from exc
        finally:
            if owns_client:
                await client.aclose()

        results: list[TrendCandidate] = []
        rss_items = root.findall("./channel/item")
        if rss_items:
            for index, item in enumerate(rss_items[: max(0, limit)], start=1):
                title = _text(item, "title")
                url = _text(item, "link")
                if not title or not url:
                    continue
                raw_id = _text(item, "guid") or url
                published_at = _parse_rfc822(_text(item, "pubDate"))
                results.append(
                    self._candidate(
                        raw_id=raw_id,
                        title=title,
                        url=url,
                        index=index,
                        published_at=published_at,
                        summary=_text(item, "description"),
                    )
                )
            return results

        ns = {"atom": "http://www.w3.org/2005/Atom"}
        for index, entry in enumerate(root.findall("atom:entry", ns)[: max(0, limit)], start=1):
            title = _text(entry, "{http://www.w3.org/2005/Atom}title")
            link_node = entry.find("atom:link", ns)
            url = link_node.get("href") if link_node is not None else None
            if not title or not url:
                continue
            raw_id = _text(entry, "{http://www.w3.org/2005/Atom}id") or url
            published_raw = _text(entry, "{http://www.w3.org/2005/Atom}published") or _text(
                entry, "{http://www.w3.org/2005/Atom}updated"
            )
            published_at = None
            if published_raw:
                try:
                    published_at = datetime.fromisoformat(published_raw.replace("Z", "+00:00"))
                except ValueError:
                    pass
            results.append(
                self._candidate(
                    raw_id=raw_id,
                    title=title,
                    url=url,
                    index=index,
                    published_at=published_at,
                    summary=_text(entry, "{http://www.w3.org/2005/Atom}summary"),
                )
            )
        return results
