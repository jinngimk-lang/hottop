import httpx
import pytest

from hottop.collectors.base import SourceError
from hottop.integrations.plain_http import PlainHttpAdapter


@pytest.mark.asyncio
async def test_plain_http_converts_basic_html_to_readable_markdown():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url == httpx.URL("https://example.com/story")
        return httpx.Response(
            200,
            headers={"content-type": "text/html; charset=utf-8"},
            text="""
            <html><head><title>Noise title</title></head><body>
              <nav>Menu</nav>
              <article>
                <h1>Useful headline</h1>
                <p>First paragraph.</p>
                <p>Second <strong>paragraph</strong>.</p>
              </article>
              <script>ignore()</script>
            </body></html>
            """,
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        adapter = PlainHttpAdapter(client=client)
        markdown = await adapter.markdown("https://example.com/story")

    assert markdown == "# Useful headline\n\nFirst paragraph.\n\nSecond paragraph."


@pytest.mark.asyncio
async def test_plain_http_accepts_markdown_and_text_responses():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            headers={"content-type": "text/markdown"},
            text="# Already markdown\n\nBody",
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        adapter = PlainHttpAdapter(client=client)
        markdown = await adapter.markdown("https://example.com/readme.md")

    assert markdown == "# Already markdown\n\nBody"


@pytest.mark.asyncio
async def test_plain_http_rejects_non_text_content():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "image/png"}, content=b"png")

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        adapter = PlainHttpAdapter(client=client)
        with pytest.raises(SourceError, match="unsupported content type"):
            await adapter.markdown("https://example.com/image.png")
