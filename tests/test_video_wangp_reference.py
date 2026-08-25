from pathlib import Path

import pytest

from hottop.rendering import CreativeRenderFrame, CreativeRenderRequest
from hottop.video_execution import VideoExecutionError, run_video_production
from hottop.video_production import load_video_production_config
from hottop.video_reference import VideoReference
from hottop.video_wangp import (
    WanGPAdapterConfig,
    WanGPError,
    prepare_wangp_settings,
    run_wangp_shot,
)

REFERENCE_PLACEHOLDER = "__HOTTOP_REFERENCE_IMAGE__"


def _request(reference: VideoReference | None) -> CreativeRenderRequest:
    return CreativeRenderRequest(
        topic_id="wangp-reference",
        topic_title="operator-managed WanGP reference I2V",
        subject_name="InkClawAgent",
        expression_form="faux-film-still",
        visual_medium="live-action-cinematic",
        genre_treatment="original cinematic meme",
        distribution_mode="motion",
        in_asset_cta_policy="no-destination",
        motion_continuity_required=True,
        frames=[
            CreativeRenderFrame(
                index=1,
                scene="The same original hero crosses the workshop.",
                caption="继续。",
                intent="preserve identity while moving",
                speaker="hero",
                delivery="calm",
                reference=reference,
            )
        ],
        master_prompt="original cinematic meme with stable character identity",
        negative_prompt="actor likeness, copied film frame, identity drift",
        punchlines=["继续。"],
        risk_flags=["original characters only"],
        claim_status="satire",
    )


def _prepare_operator_install(root: Path, *, with_placeholder: bool = True) -> None:
    install = root / "integrations" / "WanGP-operator"
    (install / "shared").mkdir(parents=True)
    (install / "wgp.py").write_text("# operator-managed stub\n", encoding="utf-8")
    (install / "shared" / "api.py").write_text("# operator-managed stub\n", encoding="utf-8")
    image_value = REFERENCE_PLACEHOLDER if with_placeholder else "operator-default.png"
    (install / "hottop-settings.json").write_text(
        "{\n"
        '  "model_type": "wan2.2_i2v",\n'
        '  "prompt": "template",\n'
        f'  "image_start": "{image_value}"\n'
        "}\n",
        encoding="utf-8",
    )


def _patch_local_runtime(monkeypatch) -> None:
    monkeypatch.setattr(
        "hottop.video_execution.shutil.which",
        lambda name: f"/usr/bin/{name}" if name in {"espeak", "ffmpeg"} else None,
    )
    monkeypatch.setattr("hottop.video_execution.importlib.util.find_spec", lambda _name: object())


def test_prepare_wangp_settings_binds_reference_marker_without_guessing_provider_field():
    template = {
        "model_type": "wan2.2_i2v",
        "prompt": "template",
        "image_start": REFERENCE_PLACEHOLDER,
        "nested": {"reference_images": [REFERENCE_PLACEHOLDER]},
    }

    settings = prepare_wangp_settings(
        template,
        prompt="same hero moves through frame",
        duration_seconds=2.5,
        fps=24,
        reference_image=Path("/safe/original-hero.png"),
    )

    assert settings["image_start"] == "/safe/original-hero.png"
    assert settings["nested"]["reference_images"] == ["/safe/original-hero.png"]
    assert template["image_start"] == REFERENCE_PLACEHOLDER


def test_prepare_wangp_settings_fails_closed_when_reference_has_no_exported_marker():
    template = {"model_type": "wan2.2_i2v", "prompt": "template"}

    with pytest.raises(WanGPError, match="reference placeholder"):
        prepare_wangp_settings(
            template,
            prompt="same hero moves through frame",
            duration_seconds=2.5,
            fps=24,
            reference_image=Path("/safe/original-hero.png"),
        )


def test_wangp_reference_file_is_checked_before_session_creation(tmp_path):
    settings_path = tmp_path / "settings.json"
    settings_path.write_text(
        '{"model_type":"wan2.2_i2v","image_start":"__HOTTOP_REFERENCE_IMAGE__"}',
        encoding="utf-8",
    )
    config = WanGPAdapterConfig(root=tmp_path / "WanGP", settings_path=settings_path)
    session_created = []

    def factory(**_kwargs):
        session_created.append(True)
        raise AssertionError("session must not be created for a missing reference image")

    with pytest.raises(WanGPError, match="reference image is missing"):
        run_wangp_shot(
            config,
            prompt="same hero",
            duration_seconds=2.0,
            fps=24,
            output=tmp_path / "shot.mp4",
            reference_image=tmp_path / "missing-hero.png",
            reference_rights="generated-original",
            session_factory=factory,
        )

    assert session_created == []


def test_video_run_wangp_reference_is_absolute_and_rights_bound(monkeypatch, tmp_path):
    _prepare_operator_install(tmp_path)
    _patch_local_runtime(monkeypatch)
    reference_path = tmp_path / "assets" / "hero.png"
    reference_path.parent.mkdir(parents=True)
    reference_path.write_bytes(b"original-reference")
    reference = VideoReference(
        image_path="assets/hero.png",
        rights="generated-original",
        subject_id="hero",
        identity_lock=["same face", "same dark coat"],
    )
    config = load_video_production_config(Path("config/video/wangp-operator.yml"))

    result = run_video_production(
        _request(reference),
        config,
        output_dir=tmp_path / "run",
        project_root=tmp_path,
        execute=False,
    )

    generation = [command for command in result.runtime_commands if command.stage == "generation"]
    assert len(generation) == 1
    command = generation[0]
    reference_arg = Path(command.args[command.args.index("--reference-image") + 1])
    rights_arg = command.args[command.args.index("--reference-rights") + 1]
    assert reference_arg == reference_path.resolve()
    assert rights_arg == "generated-original"
    assert result.ready is True


def test_video_run_wangp_missing_reference_fails_before_execute(monkeypatch, tmp_path):
    _prepare_operator_install(tmp_path)
    _patch_local_runtime(monkeypatch)
    reference = VideoReference(
        image_path="assets/missing-hero.png",
        rights="generated-original",
        subject_id="hero",
        identity_lock=["same face"],
    )
    config = load_video_production_config(Path("config/video/wangp-operator.yml"))

    dry_run = run_video_production(
        _request(reference),
        config,
        output_dir=tmp_path / "dry-run",
        project_root=tmp_path,
        execute=False,
    )

    assert dry_run.ready is False
    assert any("reference image for shot 1 is missing" in item for item in dry_run.actions_required)

    with pytest.raises(VideoExecutionError, match="reference image for shot 1 is missing"):
        run_video_production(
            _request(reference),
            config,
            output_dir=tmp_path / "execute",
            project_root=tmp_path,
            execute=True,
        )
