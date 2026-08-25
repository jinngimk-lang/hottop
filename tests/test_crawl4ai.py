import json

import httpx
import pytest

from hottop.integrations.crawl4ai import Crawl4AIAdapter


@pytest.mark.asyncio
async def test_crawl4ai_health_does_not_require_token():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/health"
        assert "authorization" not in request.headers
        return httpx.Response(200, json={"status": "ok", "version": "0.9.2"})

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler), base_url="http://crawl4ai.test"
    ) as client:
        result = await Crawl4AIAdapter(client=client).doctor()
    assert result["version"] == "0.9.2"


@pytest.mark.asyncio
async def test_crawl4ai_markdown_uses_bearer_token_and_crawl_endpoint():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/crawl"
        assert request.headers["authorization"] == "Bearer secret"
        payload = json.loads(request.content)
        assert payload["urls"] == ["https://example.com/story"]
        return httpx.Response(
            200,
            json={
                "success": True,
                "results": [
                    {
                        "url": "https://example.com/story",
                        "success": True,
                        "markdown": "clean markdown",
                    }
                ],
            },
        )

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler), base_url="http://crawl4ai.test"
    ) as client:
        text = await Crawl4AIAdapter(client=client, token="secret").markdown(
            "https://example.com/story"
        )
    assert text == "clean markdown"
