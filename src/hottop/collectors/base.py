from __future__ import annotations

from datetime import UTC, datetime
from typing import Any


class SourceError(RuntimeError):
    """A recoverable source acquisition failure."""


def parse_timestamp(value: Any) -> datetime | None:
    if value in (None, "", 0, "0"):
        return None
    if isinstance(value, str):
        stripped = value.strip()
        try:
            value = float(stripped)
        except ValueError:
            try:
                parsed = datetime.fromisoformat(stripped.replace("Z", "+00:00"))
                return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)
            except ValueError:
                return None
    if isinstance(value, (int, float)):
        seconds = float(value)
        if seconds > 100_000_000_000:
            seconds /= 1000.0
        try:
            return datetime.fromtimestamp(seconds, tz=UTC)
        except (OverflowError, OSError, ValueError):
            return None
    return None
