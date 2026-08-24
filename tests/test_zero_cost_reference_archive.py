from pathlib import Path

from hottop.rendering import CreativeRenderRequest
from hottop.video_production import build_video_production_plan, load_video_production_config


ROOT = Path(__file__).resolve().parents[1]


def test_zero_cost_reference_i2v_archive_is_rights_safe_and_executable_by_contract():
    source_path = ROOT / "examples/video/hottop-zero-cost-reference-i2v.render.json"
    reference_path = ROOT / "assets/generated-original/hottop-signal-orb.ppm"

    assert source_path.is_file()
    assert reference_path.is_file()
    assert reference_path.read_text(encoding="ascii").startswith("P3\n")

    render = CreativeRenderRequest.model_validate_json(source_path.read_text(encoding="utf-8"))
    assert render.distribution_mode == "motion"
    assert render.motion_continuity_required is True
    assert render.in_asset_cta_policy == "no-destination"
    assert render.frames
    assert all(frame.reference is not None for frame in render.frames)
    assert all(frame.reference.image_path == "assets/generated-original/hottop-signal-orb.ppm" for frame in render.frames if frame.reference is not None)
    assert all(frame.reference.rights == "generated-original" for frame in render.frames if frame.reference is not None)

    config = load_video_production_config(ROOT / "config/video/cinematic-zero-cost.yml")
    plan = build_video_production_plan(render, config)

    assert plan.generation_backend == "zero-cost-router"
    assert config.zero_cost is not None
    assert any(candidate.profile == "ltx23" for candidate in config.zero_cost.candidates)
    assert all(shot.reference is not None for shot in plan.shots)
    assert all(shot.reference.rights == "generated-original" for shot in plan.shots if shot.reference is not None)
