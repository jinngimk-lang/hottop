from __future__ import annotations

from pathlib import Path

import numpy as np

from hottop import video_moviepy
from hottop.rendering import CreativeRenderFrame, CreativeRenderRequest
from hottop.video_moviepy import build_moviepy_timeline
from hottop.video_production import build_video_production_plan, load_video_production_config


def _request() -> CreativeRenderRequest:
    return CreativeRenderRequest(
        topic_id="dialogue-duck",
        topic_title="dialogue duck contract",
        subject_name="InkClawAgent",
        expression_form="faux-film-still",
        visual_medium="animation-low-poly",
        genre_treatment="rough 3D comedy",
        distribution_mode="motion",
        in_asset_cta_policy="no-destination",
        motion_continuity_required=True,
        category_default="setup ceremony",
        deleted_constraint="deployment ceremony",
        new_competition_axis="time to useful work",
        bridge_type="role",
        bridge="dialogue over original music",
        frames=[
            CreativeRenderFrame(
                index=1,
                scene="A cow speaks while the music continues.",
                caption="妈——！",
                intent="reaction",
                speaker="young-cow",
                delivery="panicked Mandarin",
            ),
            CreativeRenderFrame(
                index=2,
                scene="The mother replies in the same workshop.",
                caption="直接干活。",
                intent="solution",
                speaker="mother-cow",
                delivery="deadpan Mandarin",
            ),
        ],
        master_prompt="original rough 3D",
        negative_prompt="glossy ad",
        punchlines=["直接干活。"],
        risk_flags=[],
        claim_status="satire",
    )


def _duck_helper():
    helper = getattr(video_moviepy, "_apply_dialogue_ducking", None)
    assert helper is not None, "MoviePy must execute dialogue ducking instead of dropping plan metadata"
    return helper


def test_moviepy_timeline_preserves_per_dialogue_ducking() -> None:
    config = load_video_production_config(Path("config/video/anti-polish-software3d.yml"))
    plan = build_video_production_plan(_request(), config)

    timeline = build_moviepy_timeline(plan, shots_dir=Path("shots"), audio_dir=Path("audio"))

    assert [track.duck_bgm_db for track in timeline.dialogue_tracks] == [
        config.audio.dialogue_duck_db,
        config.audio.dialogue_duck_db,
    ]


def test_dialogue_ducking_changes_only_the_dialogue_window() -> None:
    audio = np.ones((10, 2), dtype=float)
    track = video_moviepy.MoviePyTimelineDialogueTrack(
        source="dialogue.wav",
        start_seconds=0.2,
        duration_seconds=0.4,
        duck_bgm_db=-6,
    )

    ducked = _duck_helper()(audio, sample_rate=10, dialogue_tracks=[track])

    expected_gain = 10 ** (-6 / 20)
    np.testing.assert_allclose(ducked[:2], 1.0)
    np.testing.assert_allclose(ducked[2:6], expected_gain)
    np.testing.assert_allclose(ducked[6:], 1.0)
    np.testing.assert_allclose(audio, 1.0)


def test_effective_dialogue_duck_track_uses_actual_voice_duration() -> None:
    track = video_moviepy.MoviePyTimelineDialogueTrack(
        source="dialogue.wav",
        start_seconds=2.0,
        duration_seconds=2.0,
        duck_bgm_db=-8.0,
    )

    effective = video_moviepy._effective_dialogue_duck_track(  # noqa: SLF001
        track,
        actual_duration_seconds=0.9,
    )

    assert effective.duration_seconds == 0.9
    assert effective.start_seconds == track.start_seconds
    assert effective.duck_bgm_db == track.duck_bgm_db
    assert track.duration_seconds == 2.0
