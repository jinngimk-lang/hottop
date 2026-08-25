pathlib = __import__("pathlib")
rendering = __import__("hottop.rendering", fromlist=["CreativeRenderRequest"])
video_production = __import__(
    "hottop.video_production",
    fromlist=["build_video_production_plan", "load_video_production_config"],
)


ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPECTED_IDENTITY_LOCK = [
    "round symmetric silhouette",
    "warm amber outer glow",
    "pale golden center",
    "dark navy halo",
]


def test_zero_cost_reference_i2v_archive_is_rights_safe_and_executable_by_contract():
    source_path = ROOT / "examples/video/hottop-zero-cost-reference-i2v.render.json"
    reference_path = ROOT / "assets/generated-original/hottop-signal-orb.ppm"

    assert source_path.is_file()
    assert reference_path.is_file()
    assert reference_path.read_text(encoding="ascii").startswith("P3\n")

    render = rendering.CreativeRenderRequest.model_validate_json(
        source_path.read_text(encoding="utf-8")
    )
    assert render.distribution_mode == "motion"
    assert render.motion_continuity_required is True
    assert render.in_asset_cta_policy == "no-destination"
    assert render.frames
    assert all(frame.reference is not None for frame in render.frames)

    references = [frame.reference for frame in render.frames if frame.reference is not None]
    assert all(
        reference.image_path == "assets/generated-original/hottop-signal-orb.ppm"
        for reference in references
    )
    assert all(reference.rights == "generated-original" for reference in references)
    assert {reference.subject_id for reference in references} == {"hottop-signal-orb"}
    assert {reference.role for reference in references} == {
        "generated-original workflow signal orb"
    }
    assert all(reference.identity_lock == EXPECTED_IDENTITY_LOCK for reference in references)

    config = video_production.load_video_production_config(
        ROOT / "config/video/cinematic-zero-cost.yml"
    )
    plan = video_production.build_video_production_plan(render, config)

    assert plan.generation_backend == "zero-cost-router"
    assert config.zero_cost is not None
    assert any(candidate.profile == "ltx23" for candidate in config.zero_cost.candidates)
    assert all(shot.reference is not None for shot in plan.shots)
    assert all(
        shot.reference.rights == "generated-original"
        for shot in plan.shots
        if shot.reference is not None
    )
    assert all(
        shot.reference.subject_id == "hottop-signal-orb"
        for shot in plan.shots
        if shot.reference is not None
    )
    assert all("Identity anchor hottop-signal-orb" in shot.generation_prompt for shot in plan.shots)
    assert all("round symmetric silhouette" in shot.generation_prompt for shot in plan.shots)
    assert all("warm amber outer glow" in shot.generation_prompt for shot in plan.shots)
    assert all("pale golden center" in shot.generation_prompt for shot in plan.shots)
    assert all("dark navy halo" in shot.generation_prompt for shot in plan.shots)
