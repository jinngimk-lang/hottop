from __future__ import annotations

import hashlib
from dataclasses import dataclass


@dataclass(frozen=True)
class EspeakDialogueStyle:
    """Bounded deterministic eSpeak controls derived from preserved dialogue metadata."""

    pitch: int
    rate_wpm: int


def _character_pitch(character: str | None) -> int:
    normalized = (character or "").strip().casefold()
    if not normalized:
        return 50
    # Stable across processes/runs, unlike Python's randomized hash(). Keep named
    # roles in conservative spaced buckets so non-colliding characters remain
    # perceptibly distinct without pushing the guaranteed fallback into caricature.
    bucket = hashlib.sha256(normalized.encode("utf-8")).digest()[0] % 7
    return 32 + (bucket * 6)


def _delivery_rate_offset(delivery: str | None) -> int:
    normalized = (delivery or "").strip().casefold()
    if not normalized:
        return 0

    urgent = ("panicked", "startled", "frustrated", "anxious", "urgent")
    surprised = ("surprised", "skeptical", "upward reaction", "excited")
    restrained = ("calm", "deadpan", "quiet", "understated", "matter-of-fact")
    authoritative = ("command", "authority", "firm")

    if any(token in normalized for token in urgent):
        return 14
    if any(token in normalized for token in surprised):
        return 7
    if any(token in normalized for token in authoritative):
        return -5
    if any(token in normalized for token in restrained):
        return -8
    return 0


def resolve_espeak_dialogue_style(
    *,
    character: str | None,
    delivery: str | None,
    base_rate_wpm: int,
) -> EspeakDialogueStyle:
    """Map role/delivery metadata to conservative built-in eSpeak controls.

    This is a guaranteed zero-cost fallback, not a claim of neural voice quality.
    Character identity only affects pitch so the same role stays stable across shots;
    delivery affects cadence within the configured voice-rate safety range.
    """

    rate = max(80, min(320, base_rate_wpm + _delivery_rate_offset(delivery)))
    return EspeakDialogueStyle(
        pitch=_character_pitch(character),
        rate_wpm=rate,
    )
