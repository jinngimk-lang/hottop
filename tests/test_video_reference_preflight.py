from pathlib import Path
from types import SimpleNamespace

import pytest

from hottop.rendering import CreativeRenderFrame, CreativeRenderRequest
from hottop.video_execution import VideoExecutionError, run_video_production
from hottop.video_production import load_video_production_config
from hottop.video_reference import VideoReference


def _request_with_missing_reference() -> CreativeRenderRequest:
    return CreativeRenderRequest(
        topic_id="reference-preflight",
        topic_title="reference preflight",
        subject_name="Example Product",
        expression_form="faux-film-still",
        visual_medium="animation-low-poly",
        genre_treatment="original cinematic animation",
        distribution_mode="motion",
        in_asset_cta_policy="no-destination",
        motion_continuity_required=True,
        frames=[
            CreativeRenderFrame(
                index=1,
                scene="The same original character walks through one continuous workshop.",
                intent="preserve character identity",
                reference=VideoReference(
                    image_path="assets/missing-character.png",
                    rights="generated-original",
                ),
            )
        ],
        master_prompt="original character continuity",
        negative_prompt="identity drift",
        punchlines=["keep the same character"],
        claim_status="satire",
    )


def test_video_run_preflights_all_reference_assets_before_spawning(monkeypatch, tmp_path):
    config = load_video_production_config(Path("config/video/cinematic-zero-cost.yml"))
    monkeypatch.setattr(
        "hottop.video_execution.inspect_video_environment",
        lambda *_args, **_kwargs: SimpleNamespace(ready=True, actions_required=[]),
    )

    def forbidden_run(*_args, **_kwargs):
        raise AssertionError("missing reference must fail before any external stage is spawned")

    monkeypatch.setattr("hottop.video_execution.subprocess.run", forbidden_run)

    with pytest.raises(VideoExecutionError, match="reference image.*missing"):
        run_video_production(
            _request_with_missing_reference(),
            config,
            output_dir=tmp_path / "run",
            project_root=tmp_path,
            execute=True,
        )
