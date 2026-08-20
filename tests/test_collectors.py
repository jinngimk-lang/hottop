from __future__ import annotations

import httpx
import pytest

from hottop.collectors.dailyhot import DailyHotApiCollector
from hottop.collectors.newsnow import NewsNowCollector
from hottop.collectors.rss import RSSCollector


@pytest.mark.asyncio
async def test_dailyhot_normalizes_router_data():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/zhihu"
        return httpx.Response(
            200,
            json={
                "name": "zhihu",
                "title": "知乎",
                "type": "热榜",
                "total": 2,
                "updateTime": "2026-08-20T10:00:00Z",
                "fromCache": False,
                "data": [
                    {
                        "id": "q1",
                        "title": "奥德赛热映",
                        "desc": "电影讨论",
                        "hot": 920000,
                        "timestamp": 1787216400,
                        "url": "https://example.com/q1",
                        "mobileUrl": "https://example.com/q1",
                    },
                    {
                        "id": "q2",
                        "title": "AI Agent 新工具",
                        "hot": 810000,
                        "url": "https://example.com/q2",
                        "mobileUrl": "https://example.com/q2",
                    },
                ],
            },
        )

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler), base_url="https://dailyhot.test"
    ) as client:
        items = await DailyHotApiCollector(route="zhihu", client=client).collect(limit=1)

    assert len(items) == 1
    assert items[0].id == "dailyhot:zhihu:q1"
    assert items[0].source == "dailyhot:zhihu"
    assert items[0].source_rank == 1
    assert items[0].metrics["hot"] == 920000


@pytest.mark.asyncio
async def test_newsnow_normalizes_source_response():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/s"
        assert request.url.params["id"] == "aihot"
        return httpx.Response(
            200,
            json={
                "status": "success",
                "id": "aihot",
                "updatedTime": 1787216400000,
                "items": [
                    {
                        "id": "n1",
                        "title": "Agent workflow release",
                        "url": "https://example.com/n1",
                        "pubDate": 1787216200000,
                        "extra": {"hover": "details"},
                    }
                ],
            },
        )

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler), base_url="https://newsnow.test"
    ) as client:
        items = await NewsNowCollector(source_id="aihot", client=client).collect(limit=5)

    assert items[0].id == "newsnow:aihot:n1"
    assert items[0].summary == "details"
    assert items[0].published_at is not None


@pytest.mark.asyncio
async def test_rss_collector_normalizes_feed_items():
    feed = b'''<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0"><channel><title>Test</title>
      <item><guid>r1</guid><title>Fresh movie trend</title><link>https://example.com/r1</link><description>summary</description><pubDate>Thu, 20 Aug 2026 09:00:00 GMT</pubDate></item>
    </channel></rss>'''

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=feed, headers={"content-type": "application/rss+xml"})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        items = await RSSCollector(
            feed_url="https://feeds.test/hot.xml", source_name="rss:test", client=client
        ).collect(limit=5)

    assert items[0].id == "rss:test:r1"
    assert items[0].title == "Fresh movie trend"
    assert items[0].published_at is not None
