from pathlib import Path

import pytest
from pydantic import ValidationError

from hottop.rendering import CreativeRenderFrame, CreativeRenderRequest
from hottop.video_execution import _runtime_audio_commands, _voice_readiness
from hottop.video_production import VideoProductionConfig, build_video_production_plan


def _prepare_cosyvoice(tmp_path: Path) -> tuple[Path, Path, Path]:
    root = tmp_path / "CosyVoice"
    model = tmp_path / "models" / "Fun-CosyVoice3-0.5B-2512"
    reference = tmp_path / "voice.wav"
    (root / "cosyvoice" / "cli").mkdir(parents=True)
    (root / "cosyvoice" / "cli" / "cosyvoice.py").write_text("# stub", encoding="utf-8")
    model.mkdir(parents=True)
    (model / "cosyvoice3.yaml").write_text("sample_rate: 24000", encoding="utf-8")
    (model / "llm.pt").write_bytes(b"weights")
    reference.write_bytes(b"wav")
    return root, model, reference


def _request() -> CreativeRenderRequest:
    return CreativeRenderRequest(
        topic_id="cosyvoice-runtime",
        topic_title="CosyVoice3 runtime",
        subject_name="InkClawAgent",
        expression_form="four-panel",
        visual_medium="animation-native-3d",
        genre_treatment="original low-poly comedy",
        distribution_mode="motion",
        in_asset_cta_policy="no-destination",
        motion_continuity_required=True,
        category_default="manual setup",
        deleted_constraint="setup ceremony",
        new_competition_axis="time to useful work",
        bridge_type="role",
        bridge="product breaks the obstruction",
        frames=[
            CreativeRenderFrame(
                index=1,
                scene="Original worker looks at a terminal.",
                caption="又要配环境？",
                intent="setup",
                speaker="worker",
                delivery="tired Mandarin",
            ),
            CreativeRenderFrame(
                index=2,
                scene="Original helper opens the product.",
                caption="直接开始。",
                intent="solution",
                speaker="helper",
                delivery="calm Mandarin",
            ),
        ],
        master_prompt="original low-poly comedy",
        negative_prompt="copied character design",
        punchlines=["直接开始。"],
        risk_flags=["original staging only"],
        claim_status="satire",
    )


def _config(tmp_path: Path, *, include_cosyvoice: bool = True) -> VideoProductionConfig:
    root, model, reference = _prepare_cosyvoice(tmp_path)
    audio: dict[str, object] = {
        "bgm_style": "original synthetic comedy",
        "foley_style": "procedural",
        "voice_backend": "cosyvoice3",
        "voice_profile": "local-rights-cleared-reference",
        "voice_language": "zh",
        "music_backend": "none",
        "sfx_backend": "none",
    }
    if include_cosyvoice:
        audio["cosyvoice3"] = {
            "root": str(root),
            "model_dir": str(model),
            "reference_audio": str(reference),
            "reference_text": "这是项目自有的参考声音。",
            "reference_rights": "generated-original",
            "operator_managed": True,
            "auto_install": False,
            "auto_download_models": False,
        }
    return VideoProductionConfig.model_validate(
        {
            "name": "cosyvoice-runtime-test",
            "style_profile": "anti-polish",
            "roughness_score": 70,
            "generation_backend": "software3d",
            "compositor_backend": "external",
            "encoder_backend": "external",
            "width": 540,
            "height": 960,
            "fps": 15,
            "duration_seconds": 4,
            "shot_policy": {"min_shot_seconds": 1, "max_shot_seconds": 3},
            "audio": audio,
            "text": {},
        }
    )


def test_cosyvoice3_backend_requires_explicit_operator_profile(tmp_path: Path):
    with pytest.raises(ValidationError, match="cosyvoice3"):
        _config(tmp_path, include_cosyvoice=False)


def test_cosyvoice3_readiness_uses_only_operator_local_assets(tmp_path: Path):
    config = _config(tmp_path)

    status = _voice_readiness(config, tmp_path)

    assert status.backend == "cosyvoice3"
    assert status.ready is True
    assert status.missing == []
    assert any("auto_install=False" in check for check in status.checks)
    assert any("auto_download_models=False" in check for check in status.checks)


def test_cosyvoice3_runtime_commands_preserve_reference_rights_and_dialogue(tmp_path: Path):
    config = _config(tmp_path)
    plan = build_video_production_plan(_request(), config)
    audio_dir = tmp_path / "audio"

    commands = _runtime_audio_commands(
        plan,
        config,
        project_root=tmp_path,
        audio_dir=audio_dir,
    )

    assert len(commands) == 2
    assert all(command.stage == "audio" for command in commands)
    assert all(command.args[:2] == ["-m", "hottop.audio_cosyvoice3"] for command in commands)
    assert all("--reference-rights" in command.args for command in commands)
    assert all("generated-original" in command.args for command in commands)
    assert all("--reference-text" in command.args for command in commands)
    assert all("--reference-audio" in command.args for command in commands)
    assert all("--model-dir" in command.args for command in commands)
    assert all("--root" in command.args for command in commands)
    assert all("--output" in command.args for command in commands)
    assert "又要配环境？" in commands[0].args
    assert "直接开始。" in commands[1].args
    assert not any("download" in arg.lower() or "install" in arg.lower() for c in commands for arg in c.args)


def test_cosyvoice3_readiness_fails_before_execution_when_reference_disappears(tmp_path: Path):
    config = _config(tmp_path)
    reference = Path(config.audio.cosyvoice3.reference_audio)
    reference.unlink()

    status = _voice_readiness(config, tmp_path)

    assert status.ready is False
    assert "reference audio" in status.missing
