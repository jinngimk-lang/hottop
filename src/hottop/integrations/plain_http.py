from __future__ import annotations

from html.parser import HTMLParser

import httpx

from ..collectors.base import SourceError


class _ReadableHTMLParser(HTMLParser):
    _skip_tags = {"script", "style", "noscript", "nav", "footer", "head", "aside"}
    _block_tags = {"p", "div", "section", "article", "main", "li", "blockquote"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0
        self.heading_level: int | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in self._skip_tags:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.heading_level = int(tag[1])
            self._break()
            self.parts.append("#" * self.heading_level + " ")
        elif tag in self._block_tags or tag == "br":
            self._break()

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in self._skip_tags:
            if self.skip_depth:
                self.skip_depth -= 1
            return
        if self.skip_depth:
            return
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.heading_level = None
            self._break()
        elif tag in self._block_tags:
            self._break()

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        text = " ".join(data.split())
        if not text:
            return
        punctuation = ".,;:!?)]}%"
        needs_space = (
            self.parts
            and not self.parts[-1].endswith((" ", "\n", "(", "[", "{"))
            and not text.startswith(tuple(punctuation))
        )
        if needs_space:
            self.parts.append(" ")
        self.parts.append(text)

    def _break(self) -> None:
        if not self.parts:
            return
        current = "".join(self.parts)
        if not current.endswith("\n\n"):
            if current.endswith("\n"):
                self.parts.append("\n")
            else:
                self.parts.append("\n\n")

    def markdown(self) -> str:
        text = "".join(self.parts).strip()
        lines = [line.strip() for line in text.splitlines()]
        compact: list[str] = []
        blank = False
        for line in lines:
            if not line:
                if compact and not blank:
                    compact.append("")
                blank = True
                continue
            compact.append(line)
            blank = False
        return "\n".join(compact).strip()


class PlainHttpAdapter:
    """Last-resort reader for public text/HTML pages.

    This adapter intentionally does not execute JavaScript, bypass access
    controls, or reuse browser authentication. It is only a lightweight
    fallback when Crawl4AI and Firecrawl are unavailable or unnecessary.
    """

    def __init__(
        self,
        client: httpx.AsyncClient | None = None,
        timeout: float = 20.0,
        user_agent: str = "hottop/0.1 (+public-web-enrichment)",
    ) -> None:
        self.client = client
        self.timeout = timeout
        self.user_agent = user_agent

    async def markdown(self, url: str) -> str:
        owns_client = self.client is None
        client = self.client or httpx.AsyncClient(timeout=self.timeout, follow_redirects=True)
        try:
            response = await client.get(url, headers={"User-Agent": self.user_agent})
            response.raise_for_status()
            content_type = response.headers.get("content-type", "").lower()
            if content_type.startswith("text/markdown") or content_type.startswith("text/plain"):
                text = response.text.strip()
            elif content_type.startswith("text/html") or not content_type:
                parser = _ReadableHTMLParser()
                parser.feed(response.text)
                text = parser.markdown()
            else:
                raise SourceError(f"plain-http unsupported content type: {content_type or 'unknown'}")
            if not text:
                raise SourceError("plain-http returned empty text")
            return text
        except SourceError:
            raise
        except httpx.HTTPError as exc:
            raise SourceError(f"plain-http fetch: {exc}") from exc
        finally:
            if owns_client:
                await client.aclose()
