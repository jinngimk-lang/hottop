from pathlib import Path

from hottop.rendering import CreativeRenderFrame, CreativeRenderRequest
from hottop.video_production import build_video_production_plan, load_video_production_config


def _request() -> CreativeRenderRequest:
    return CreativeRenderRequest(
        topic_id="odyssey-witch",
        topic_title="mythic banquet coding curse",
        subject_name="InkClawAgent",
        expression_form="faux-film-still",
        visual_medium="live-action-cinematic",
        genre_treatment="original mythic cinematic meme",
        distribution_mode="motion",
        in_asset_cta_policy="no-destination",
        motion_continuity_required=True,
        frames=[
            CreativeRenderFrame(
                index=1,
                scene="Sailors code at one banquet table in an original mythic hall.",
                caption="今晚先把这个包接上。",
                intent="setup",
                speaker="sailor",
                delivery="casual, confident",
            ),
            CreativeRenderFrame(
                index=2,
                scene="The same sailors transform into pigs while the camera stays in the hall.",
                caption="怎么全变猪了？",
                intent="curse escalation",
                speaker="sailor",
                delivery="panicked",
            ),
        ],
        master_prompt="original cinematic mythic meme with believable faces and practical torchlight",
        negative_prompt="copied film frame, actor likeness, official character design, glossy AI ad",
        punchlines=["先把人变回来，再谈依赖。"],
        risk_flags=["original characters only"],
        claim_status="satire",
    )


def test_wangp_operator_profile_is_zero_cost_and_operator_controlled():
    config = load_video_production_config(Path("config/video/wangp-operator.yml"))

    assert config.generation_backend == "external"
    assert config.external_generation is not None
    assert config.external_generation.adapter == "wangp"
    assert config.external_generation.cost_per_unit == 0
    assert config.external_generation.operator_managed is True
    assert config.external_generation.auto_install is False
    assert config.external_generation.auto_download_models is False


def test_wangp_operator_profile_emits_one_structured_generation_command_per_shot():
    config = load_video_production_config(Path("config/video/wangp-operator.yml"))
    plan = build_video_production_plan(_request(), config)

    assert len(plan.generation_command_specs) == len(plan.shots)
    first = plan.generation_command_specs[0]
    assert first.stage == "generation"
    assert first.program == "python"
    assert first.args[:3] == ["-m", "hottop.video_wangp", "--root"]
    assert "--settings" in first.args
    assert "--prompt" in first.args
    assert "--duration-seconds" in first.args
    assert "--fps" in first.args
    assert "--output" in first.args
    assert "shots/shot-001.mp4" in first.args
    assert "HF_TOKEN" not in " ".join(first.args)
    assert any("operator-managed WanGP" in note for note in plan.execution_notes)
