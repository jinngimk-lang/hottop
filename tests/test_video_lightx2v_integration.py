from pathlib import Path

from pydantic import ValidationError

from hottop.rendering import CreativeRenderFrame, CreativeRenderRequest
from hottop.video_execution import inspect_video_environment, run_video_production
from hottop.video_production import VideoProductionConfig, build_video_production_plan
from hottop.video_reference import VideoReference


def _request(tmp_path: Path) -> CreativeRenderRequest:
    reference = tmp_path / "hero.png"
    reference.write_bytes(b"png")
    return CreativeRenderRequest(
        topic_id="lightx2v-test",
        topic_title="LightX2V test",
        subject_name="InkClawAgent",
        expression_form="faux-film-still",
        visual_medium="animation-low-poly",
        genre_treatment="anti-polish",
        distribution_mode="motion",
        in_asset_cta_policy="no-destination",
        motion_continuity_required=True,
        category_default="manual setup",
        deleted_constraint="manual setup",
        new_competition_axis="time to useful work",
        bridge_type="role",
        bridge="the product breaks the obstacle",
        frames=[
            CreativeRenderFrame(
                index=1,
                scene="Same original bovine programmer crosses the workshop.",
                caption="继续干活。",
                intent="setup",
                speaker="hero",
                delivery="deadpan Mandarin",
                reference=VideoReference(
                    image_path=str(reference),
                    rights="generated-original",
                    subject_id="hero",
                    role="original bovine programmer",
                    identity_lock=["orange rough fur", "short dark horns", "gray muzzle"],
                ),
            )
        ],
        master_prompt="original low-budget cinematic 3D",
        negative_prompt="actor likeness, copied film frame, identity drift",
        punchlines=["先把活干完。"],
        risk_flags=["original staging only"],
        claim_status="satire",
    )


def _config(tmp_path: Path) -> VideoProductionConfig:
    return VideoProductionConfig.model_validate(
        {
            "name": "lightx2v-wan22-i2v",
            "style_profile": "anti-polish",
            "roughness_score": 65,
            "generation_backend": "lightx2v-operator",
            "compositor_backend": "external",
            "encoder_backend": "external",
            "width": 720,
            "height": 1280,
            "fps": 24,
            "duration_seconds": 2,
            "shot_policy": {"min_shot_seconds": 1, "max_shot_seconds": 3},
            "audio": {"bgm_style": "original", "foley_style": "original"},
            "text": {},
            "lightx2v": {
                "root": str(tmp_path / "LightX2V"),
                "model_path": str(tmp_path / "Wan2.2-I2V-A14B"),
                "config_json": str(tmp_path / "wan_moe_i2v.json"),
                "model_cls": "wan2.2_moe",
                "task": "i2v",
                "seed": 42,
                "code_license": "Apache-2.0",
                "weights_license": "Apache-2.0",
                "cost_per_unit": 0,
                "operator_managed": True,
                "auto_install": False,
                "auto_download_models": False,
            },
        }
    )


def test_lightx2v_backend_requires_its_config(tmp_path):
    payload = _config(tmp_path).model_dump(mode="json")
    payload.pop("lightx2v")
    try:
        VideoProductionConfig.model_validate(payload)
    except ValidationError as exc:
        assert "lightx2v" in str(exc)
    else:
        raise AssertionError("lightx2v-operator must require lightx2v configuration")


def test_lightx2v_plan_emits_per_shot_command_with_reference(tmp_path):
    plan = build_video_production_plan(_request(tmp_path), _config(tmp_path))

    assert plan.generation_backend == "lightx2v-operator"
    assert len(plan.generation_command_specs) == 1
    command = plan.generation_command_specs[0]
    assert command.args[:2] == ["-m", "hottop.video_lightx2v"]
    assert "--reference-image" in command.args
    assert "--reference-rights" in command.args
    assert "generated-original" in command.args
    assert "offline" in " ".join(plan.execution_notes).lower()


def test_lightx2v_doctor_fails_closed_until_operator_assets_exist(tmp_path):
    status = inspect_video_environment(_config(tmp_path), project_root=tmp_path)

    assert status.ready is False
    assert status.lightx2v is not None
    assert status.lightx2v.ready is False
    assert "LightX2V" in " ".join(status.lightx2v.missing)
    assert any("will not" in action.lower() for action in status.actions_required)


def test_lightx2v_dry_run_resolves_operator_paths_and_reference(tmp_path):
    config = _config(tmp_path)
    assert config.lightx2v is not None
    root = tmp_path / "LightX2V"
    (root / "lightx2v").mkdir(parents=True)
    (root / "lightx2v" / "infer.py").write_text("# local\n", encoding="utf-8")
    Path(config.lightx2v.model_path).mkdir()
    Path(config.lightx2v.config_json).write_text("{}\n", encoding="utf-8")

    result = run_video_production(
        _request(tmp_path),
        config,
        output_dir=tmp_path / "run",
        project_root=tmp_path,
        execute=False,
    )

    generation = [command for command in result.runtime_commands if command.stage == "generation"]
    assert result.ready is True
    assert len(generation) == 1
    command = generation[0]
    assert command.args[:2] == ["-m", "hottop.video_lightx2v"]
    assert command.args[command.args.index("--root") + 1] == str(root.resolve())
    assert command.args[command.args.index("--model-path") + 1] == str(
        Path(config.lightx2v.model_path).resolve()
    )
    reference = command.args[command.args.index("--reference-image") + 1]
    assert reference == str((tmp_path / "hero.png").resolve())
