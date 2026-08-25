from __future__ import annotations

import pytest

import hottop.video_moviepy as moviepy_runtime
from hottop.video_moviepy import MoviePyTimelineDialogueTrack


def _track(duration_seconds: float = 2.0) -> MoviePyTimelineDialogueTrack:
    return MoviePyTimelineDialogueTrack(
        source="audio/dialogue-001.wav",
        start_seconds=0.0,
        duration_seconds=duration_seconds,
        character="crew",
        delivery="clear conversational Mandarin",
        duck_bgm_db=-8.0,
    )


def test_dialogue_duration_gate_rejects_material_voice_clipping() -> None:
    with pytest.raises(RuntimeError, match="dialogue audio exceeds its planned window"):
        moviepy_runtime._validate_dialogue_track_duration(  # noqa: SLF001
            actual_duration_seconds=3.2,
            track=_track(),
        )


def test_dialogue_duration_gate_allows_small_encoder_tail() -> None:
    moviepy_runtime._validate_dialogue_track_duration(  # noqa: SLF001
        actual_duration_seconds=2.1,
        track=_track(),
    )
