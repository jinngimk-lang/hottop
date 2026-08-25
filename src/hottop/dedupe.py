from __future__ import annotations

import re
import unicodedata
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from .models import TrendCandidate

_TRACKING_PREFIXES = ("utm_",)
_TRACKING_KEYS = {"gclid", "fbclid", "spm", "from", "source"}


def canonical_url(url: str) -> str:
    parts = urlsplit(url)
    query = [
        (key, value)
        for key, value in parse_qsl(parts.query, keep_blank_values=True)
        if key.lower() not in _TRACKING_KEYS
        and not any(key.lower().startswith(prefix) for prefix in _TRACKING_PREFIXES)
    ]
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, urlencode(query), ""))


def title_fingerprint(title: str) -> str:
    normalized = unicodedata.normalize("NFKC", title).lower().strip()
    normalized = re.sub(r"[^\w\u4e00-\u9fff]+", " ", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def merge_candidates(items: list[TrendCandidate]) -> list[TrendCandidate]:
    merged: list[TrendCandidate] = []
    key_to_index: dict[str, int] = {}
    source_sets: list[set[str]] = []

    for item in items:
        url_key = f"url:{canonical_url(str(item.url))}"
        title_key = f"title:{title_fingerprint(item.title)}"
        index = key_to_index.get(url_key)
        if index is None:
            index = key_to_index.get(title_key)

        if index is None:
            clone = item.model_copy(deep=True)
            sources = {item.source}
            clone.metrics["cross_source_count"] = float(len(sources))
            merged.append(clone)
            source_sets.append(sources)
            index = len(merged) - 1
        else:
            target = merged[index]
            source_sets[index].add(item.source)
            existing = {(str(e.url), e.source) for e in target.evidence}
            for evidence in item.evidence:
                key = (str(evidence.url), evidence.source)
                if key not in existing:
                    target.evidence.append(evidence)
                    existing.add(key)
            target.tags = sorted(set(target.tags).union(item.tags))
            for key, value in item.metrics.items():
                target.metrics.setdefault(key, value)
            target.metrics["cross_source_count"] = float(len(source_sets[index]))
            if target.summary is None and item.summary:
                target.summary = item.summary
            if target.published_at is None or (
                item.published_at is not None and item.published_at > target.published_at
            ):
                target.published_at = item.published_at

        key_to_index[url_key] = index
        key_to_index[title_key] = index

    return merged
