from pathlib import Path

import pytest
from pydantic import ValidationError

from hottop.rendering import CreativeRenderFrame
from hottop.video_execution import _zero_cost_runtime_generation_commands
from hottop.video_production import (
    VideoProductionPlan,
    VideoReference,
    VideoShot,
    load_video_production_config,
)
from hottop.video_zero_cost import run_zero_cost_shot


def test_video_reference_rejects_remote_and_inline_locators():
    for locator in (
        "https://example.com/character.png",
        "http://example.com/character.png",
        "data:image/png;base64,AAAA",
    ):
        with pytest.raises(ValidationError):
            VideoReference(image_path=locator, rights="generated-original")


def test_creative_frame_requires_rights_safe_local_reference():
    frame = CreativeRenderFrame(
        index=1,
        scene="same original character crosses the workshop",
        intent="preserve identity",
        reference={
            "image_path": "assets/original-character.png",
            "rights": "generated-original",
        },
    )

    assert frame.reference is not None
    assert frame.reference.image_path == "assets/original-character.png"
    assert frame.reference.rights == "generated-original"


def test_zero_cost_runtime_command_preserves_reference_locator_and_rights(tmp_path: Path):
    config = load_video_production_config(Path("config/video/cinematic-zero-cost.yml"))
    plan = VideoProductionPlan(
        config_name=config.name,
        topic_id="topic",
        topic_title="topic",
        subject_name="subject",
        style_profile=config.style_profile,
        roughness_score=config.roughness_score,
        generation_backend=config.generation_backend,
        compositor_backend=config.compositor_backend,
        encoder_backend=config.encoder_backend,
        width=config.width,
        height=config.height,
        fps=config.fps,
        duration_seconds=2,
        output_format=config.output_format,
        in_asset_cta_policy="no-destination",
        shots=[
            VideoShot(
                index=1,
                start_seconds=0,
                end_seconds=2,
                duration_seconds=2,
                scene="same original character crosses the workshop",
                intent="preserve identity",
                continuity_instruction="keep identity",
                generation_prompt="same original character crosses the workshop",
                negative_prompt="identity drift",
                reference=VideoReference(
                    image_path="assets/original-character.png",
                    rights="generated-original",
                ),
            )
        ],
    )

    commands = _zero_cost_runtime_generation_commands(
        plan,
        config,
        project_root=tmp_path,
        shots_dir=tmp_path / "out" / "shots",
    )

    assert len(commands) == 1
    args = commands[0].args
    assert "--reference-image" in args
    assert args[args.index("--reference-image") + 1] == str(
        (tmp_path / "assets/original-character.png").resolve()
    )
    assert args[args.index("--reference-rights") + 1] == "generated-original"


def test_zero_cost_shot_forwards_reference_to_hf_request(tmp_path: Path, monkeypatch):
    config_path = tmp_path / "runtime.json"
    config_path.write_text(
        """{
  "enabled": true,
  "allow_paid_fallback": false,
  "max_attempts_per_shot": 1,
  "candidates": [{
    "id": "ltx23",
    "kind": "hf-zerogpu",
    "profile": "ltx23",
    "space_url": "https://example.hf.space",
    "api_name": "generate_video",
    "allow_anonymous": true,
    "cost_per_unit": 0,
    "weights_license_review": "required"
  }]
}
""",
        encoding="utf-8",
    )
    reference = tmp_path / "character.png"
    reference.write_bytes(b"png")
    output = tmp_path / "shot.mp4"
    captured = {}

    def fake_generate(request):
        captured["reference_image"] = request.reference_image
        captured["reference_rights"] = request.reference_rights
        request.output.write_bytes(b"video")
        return request.output

    class PassReport:
        pass_ = True
        reasons = []

    monkeypatch.setattr("hottop.video_zero_cost.execute_hf_zerogpu", fake_generate)
    monkeypatch.setattr(
        "hottop.video_zero_cost.inspect_video_quality", lambda *_args, **_kwargs: PassReport()
    )

    result = run_zero_cost_shot(
        config_path,
        prompt="same original character crosses the workshop",
        duration_seconds=2,
        output=output,
        env={},
        reference_image=reference,
        reference_rights="generated-original",
    )

    assert result == output
    assert captured == {
        "reference_image": reference,
        "reference_rights": "generated-original",
    }
