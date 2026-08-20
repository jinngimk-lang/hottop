from __future__ import annotations

from collections.abc import Mapping
from urllib.parse import urlparse

_SOURCE_PRESETS: dict[str, dict[str, float]] = {
    "film-entertainment": {
        "apnews.com": 0.95,
        "reuters.com": 0.96,
        "theguardian.com": 0.90,
        "variety.com": 0.86,
        "hollywoodreporter.com": 0.86,
    },
    "ai-tech": {
        "reuters.com": 0.96,
        "apnews.com": 0.95,
        "openai.com": 0.98,
        "blog.google": 0.96,
        "deepmind.google": 0.96,
        "anthropic.com": 0.96,
        "techcrunch.com": 0.84,
        "theverge.com": 0.82,
    },
    "zh-internet-culture": {
        "ithome.com": 0.84,
        "36kr.com": 0.82,
        "jiemian.com": 0.84,
        "thepaper.cn": 0.86,
        "caixin.com": 0.92,
        "people.com.cn": 0.88,
    },
}


def source_preset(name: str) -> Mapping[str, float]:
    """Return a copy-safe mapping for a named editorial source preset."""
    try:
        return dict(_SOURCE_PRESETS[name])
    except KeyError as exc:
        raise ValueError(f"unknown source preset: {name}") from exc


def _hostname(value: str) -> str:
    parsed = urlparse(value if "://" in value else f"//{value}")
    host = (parsed.hostname or value).lower().strip(".")
    return host.removeprefix("www.")


def resolve_source_quality(source: str, *, fallback: float) -> float:
    """Resolve a direct publisher quality score, preserving collector fallback when unknown."""
    host = _hostname(source)
    for preset in _SOURCE_PRESETS.values():
        for domain, quality in preset.items():
            if host == domain or host.endswith(f".{domain}"):
                return quality
    return fallback
