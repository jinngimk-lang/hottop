import json
from pathlib import Path

from hottop.rendering import CreativeRenderRequest
from hottop.video_production import build_video_production_plan, load_video_production_config

ROOT = Path(__file__).resolve().parents[1]
RENDER_ARCHIVE = ROOT / "examples/video/inkclaw-cow-snake.render.json"
CONFIG = ROOT / "config/video/anti-polish-direct.yml"


def test_anti_polish_cow_story_archive_is_config_driven_and_rights_safe():
    request = CreativeRenderRequest.model_validate(
        json.loads(RENDER_ARCHIVE.read_text(encoding="utf-8"))
    )
    config = load_video_production_config(CONFIG)
    plan = build_video_production_plan(request, config)

    assert request.distribution_mode == "motion"
    assert request.motion_continuity_required is True
    assert request.in_asset_cta_policy == "no-destination"
    assert len(request.frames) == 5
    assert [frame.caption for frame in request.frames if frame.caption] == [
        "哎呀！又来绊我！",
        "妈——！",
        "傻孩子，用 InkClawAgent。",
        "啊？这么直接？",
        "别被蛇绊住。",
    ]
    assert "不用部署" in request.frames[3].scene
    assert "开发零门槛" in request.frames[3].scene
    assert "Free Token 入门" in request.frames[3].scene
    assert not any("http" in (frame.caption or "").lower() for frame in request.frames)
    assert "original staging" in " ".join(request.risk_flags).lower()
    assert "protected" in request.negative_prompt.lower()

    assert plan.schema_version == "hottop.video-plan.v1"
    assert plan.compositor_backend == "moviepy"
    assert plan.encoder_backend == "ffmpeg"
    assert len(plan.generation_command_specs) == 5
    assert all(shot.continuity_instruction for shot in plan.shots)
    assert plan.finalization_command_spec is not None
    assert "yuv420p" in plan.finalization_command_spec.args
