import json
from pathlib import Path

from hottop.rendering import CreativeRenderRequest
from hottop.video_production import build_video_production_plan, load_video_production_config

ROOT = Path(__file__).resolve().parents[1]
RENDER = ROOT / "examples/video/inkclaw-odyssey-witch-pigs.render.json"
CONFIG = ROOT / "config/video/cinematic-meme-direct.yml"


def test_odyssey_witch_pigs_archive_is_cinematic_audio_first_and_rights_safe():
    request = CreativeRenderRequest.model_validate_json(RENDER.read_text(encoding="utf-8"))
    config = load_video_production_config(CONFIG)
    plan = build_video_production_plan(request, config)

    assert request.visual_medium == "live-action-cinematic"
    assert request.distribution_mode == "motion"
    assert request.motion_continuity_required is True
    assert request.in_asset_cta_policy == "no-destination"
    assert len(request.frames) == 5
    assert [frame.speaker for frame in request.frames if frame.caption] == [
        "crew",
        "witch",
        "crew",
        "hero",
        "crew",
    ]
    assert all(frame.delivery for frame in request.frames if frame.caption)
    assert "不用部署" in request.frames[4].scene
    assert "开发零门槛" in request.frames[4].scene
    assert "Free Token 入门" in request.frames[4].scene
    assert request.claim_status == "satire"
    assert not any("http" in (frame.caption or "").lower() for frame in request.frames)
    assert "actor likeness" in request.negative_prompt.lower()
    assert "copied film frame" in request.negative_prompt.lower()

    assert plan.style_profile == "cinematic"
    assert plan.roughness_score == 28
    assert plan.audio_profile is not None
    assert plan.audio_profile.voice_profile == "natural-mandarin-cinematic"
    assert plan.audio_profile.music_profile == "mythic-dark-comedy-original"
    assert plan.audio_profile.sfx_profile == "cinematic-mythic-foley"
    assert any(cue.kind == "dialogue" and cue.character == "witch" for cue in plan.audio_cues)
    assert any(cue.kind == "bgm" for cue in plan.audio_cues)
    assert any(cue.kind == "foley" for cue in plan.audio_cues)
