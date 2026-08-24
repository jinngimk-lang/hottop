import subprocess
from pathlib import Path

import pytest

from hottop.rendering import CreativeRenderFrame, CreativeRenderRequest
from hottop.video_execution import VideoExecutionError, run_video_production
from hottop.video_production import VideoProductionConfig


def _request() -> CreativeRenderRequest:
    return CreativeRenderRequest(
        topic_id="artifact-integrity",
        topic_title="artifact integrity",
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
                scene="One continuous original room.",
                intent="solution",
            )
        ],
        master_prompt="original cinematic meme",
        negative_prompt="copied film frame",
        risk_flags=["original staging only"],
        claim_status="satire",
    )


def _config() -> VideoProductionConfig:
    return VideoProductionConfig.model_validate(
        {
            "name": "zero-cost-artifact-integrity",
            "style_profile": "cinematic",
            "roughness_score": 30,
            "generation_backend": "zero-cost-router",
            "compositor_backend": "external",
            "encoder_backend": "external",
            "width": 720,
            "height": 1280,
            "fps": 24,
            "duration_seconds": 2,
            "shot_policy": {"min_shot_seconds": 1, "max_shot_seconds": 2},
            "audio": {
                "bgm_style": "none",
                "foley_style": "none",
                "voice_backend": "none",
                "music_backend": "none",
                "sfx_backend": "none",
            },
            "text": {},
            "zero_cost": {
                "enabled": True,
                "allow_paid_fallback": False,
                "max_attempts_per_shot": 1,
                "candidates": [
                    {
                        "id": "hf-public",
                        "profile": "ltx23",
                        "space_url": "https://example.hf.space",
                        "api_name": "generate_video",
                        "allow_anonymous": True,
                        "cost_per_unit": 0,
                        "weights_license_review": "required",
                    }
                ],
            },
        }
    )


def test_execute_rejects_video_without_fresh_artifact_provenance(monkeypatch, tmp_path: Path):
    def fake_run(argv, **kwargs):
        output = Path(argv[argv.index("--output") + 1])
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(b"video-without-provenance")
        return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")

    monkeypatch.setattr("hottop.video_execution.subprocess.run", fake_run)

    with pytest.raises(VideoExecutionError, match="artifact provenance"):
        run_video_production(
            _request(),
            _config(),
            output_dir=tmp_path / "run",
            project_root=tmp_path,
            execute=True,
        )

    assert not (tmp_path / "run" / "shots" / "shot-001.artifact.json").exists()
