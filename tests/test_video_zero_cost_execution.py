import json
from pathlib import Path

from hottop.rendering import CreativeRenderFrame, CreativeRenderRequest
from hottop.video_execution import inspect_video_environment, run_video_production
from hottop.video_production import VideoProductionConfig


def _request() -> CreativeRenderRequest:
    return CreativeRenderRequest(
        topic_id="zero-cost-cinematic",
        topic_title="zero cost cinematic meme",
        subject_name="InkClawAgent",
        expression_form="faux-film-still",
        visual_medium="live-action-cinematic",
        genre_treatment="original cinematic meme",
        distribution_mode="motion",
        in_asset_cta_policy="no-destination",
        motion_continuity_required=True,
        category_default="setup ceremony",
        deleted_constraint="deployment ceremony",
        new_competition_axis="time to useful work",
        bridge_type="role",
        bridge="product resolves the obstacle",
        frames=[
            CreativeRenderFrame(
                index=1,
                scene="Original cinematic hero crosses one continuous mythic room.",
                caption="先把活干完。",
                intent="solution",
                speaker="hero",
                delivery="understated Mandarin",
            )
        ],
        master_prompt="original cinematic meme with consistent character and room",
        negative_prompt="actor likeness, copied film frame",
        punchlines=["先把活干完。"],
        risk_flags=["original staging only"],
        claim_status="satire",
    )


def _config() -> VideoProductionConfig:
    return VideoProductionConfig.model_validate(
        {
            "name": "cinematic-zero-cost-test",
            "style_profile": "cinematic",
            "roughness_score": 30,
            "generation_backend": "zero-cost-router",
            "compositor_backend": "external",
            "encoder_backend": "external",
            "width": 720,
            "height": 1280,
            "fps": 24,
            "duration_seconds": 4,
            "shot_policy": {"min_shot_seconds": 1, "max_shot_seconds": 4},
            "audio": {
                "bgm_style": "original restrained score",
                "foley_style": "cinematic foley",
                "voice_backend": "none",
                "music_backend": "none",
                "sfx_backend": "none",
            },
            "text": {},
            "zero_cost": {
                "enabled": True,
                "allow_paid_fallback": False,
                "max_attempts_per_shot": 2,
                "quality_gate": {
                    "min_motion_delta": 2,
                    "max_duplicate_ratio": 0.6,
                },
                "candidates": [
                    {
                        "id": "hf-public",
                        "kind": "hf-zerogpu",
                        "profile": "ltx23",
                        "space_url": "https://example.hf.space",
                        "api_name": "generate_video",
                        "token_env": "HF_TOKEN",
                        "allow_anonymous": True,
                        "cost_per_unit": 0,
                        "weights_license_review": "required",
                        "width": 768,
                        "height": 512,
                    }
                ],
            },
        }
    )


def test_zero_cost_readiness_allows_anonymous_candidate(monkeypatch, tmp_path: Path):
    monkeypatch.delenv("HF_TOKEN", raising=False)

    status = inspect_video_environment(_config(), project_root=tmp_path)

    assert status.zero_cost is not None
    assert status.zero_cost.ready is True
    assert status.ready is True


def test_zero_cost_dry_run_materializes_public_runtime_without_secret(monkeypatch, tmp_path: Path):
    monkeypatch.setenv("HF_TOKEN", "super-secret-free-token")
    output_dir = tmp_path / "run"

    result = run_video_production(
        _request(),
        _config(),
        output_dir=output_dir,
        project_root=tmp_path,
        execute=False,
    )

    generation = [command for command in result.runtime_commands if command.stage == "generation"]
    assert len(generation) == 1
    assert generation[0].args[:2] == ["-m", "hottop.video_zero_cost"]
    joined = " ".join(generation[0].args)
    assert "--config" in generation[0].args
    assert "--prompt" in generation[0].args
    assert "--duration-seconds" in generation[0].args
    assert "--output" in generation[0].args
    assert "super-secret-free-token" not in joined

    runtime_path = output_dir / "zero-cost-runtime.json"
    runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
    serialized = json.dumps(runtime, ensure_ascii=False)
    assert runtime["allow_paid_fallback"] is False
    assert runtime["candidates"][0]["token_env"] == "HF_TOKEN"
    assert "super-secret-free-token" not in serialized
    assert runtime["candidates"][0]["cost_per_unit"] == 0
