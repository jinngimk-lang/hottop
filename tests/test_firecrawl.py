import json

import httpx
import pytest

from hottop.integrations.firecrawl import FirecrawlAdapter


@pytest.mark.asyncio
async def test_firecrawl_markdown_uses_v2_scrape_and_bearer_token():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v2/scrape"
        assert request.headers["authorization"] == "Bearer fc-test"
        payload = json.loads(request.content)
        assert payload == {
            "url": "https://example.com/story",
            "formats": ["markdown"],
            "onlyMainContent": True,
        }
        return httpx.Response(
            200,
            json={"success": True, "data": {"markdown": "clean markdown"}},
        )

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler), base_url="https://api.firecrawl.dev"
    ) as client:
        text = await FirecrawlAdapter(api_key="fc-test", client=client).markdown(
            "https://example.com/story"
        )

    assert text == "clean markdown"


@pytest.mark.asyncio
async def test_firecrawl_doctor_reports_configured_without_network_call():
    adapter = FirecrawlAdapter(api_key="fc-test")
    result = await adapter.doctor()
    assert result == {
        "configured": True,
        "base_url": "https://api.firecrawl.dev",
        "api_version": "v2",
    }
