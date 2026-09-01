from __future__ import annotations

import sys
from pathlib import Path

import pytest

from hottop.video_lightx2v import LightX2VAdapterConfig, LightX2VError, run_lightx2v_shot


def test_preflight_failure_removes_stale_output_and_manifest(tmp_path: Path) -> None:
    root = tmp_path / "LightX2V"
    entrypoint = root / "lightx2v" / "infer.py"
    entrypoint.parent.mkdir(parents=True)
    entrypoint.write_text("# operator checkout fixture\n", encoding="utf-8")

    config_json = tmp_path / "wan_moe_t2v.json"
    config_json.write_text("{}\n", encoding="utf-8")
    missing_model = tmp_path / "Wan2.2-T2V-A14B"

    output = tmp_path / "shot.mp4"
    output.write_bytes(b"stale-video-from-previous-run")
    manifest = tmp_path / "shot.artifact.json"
    manifest.write_text('{"stale": true}\n', encoding="utf-8")

    config = LightX2VAdapterConfig(
        root=root,
        model_path=missing_model,
        config_json=config_json,
        model_cls="wan2.2_moe",
        task="t2v",
        python_executable=sys.executable,
    )

    with pytest.raises(LightX2VError, match="model path is not available locally"):
        run_lightx2v_shot(
            config,
            prompt="原创角色完成明确动作",
            negative_prompt="",
            output=output,
            shot_index=1,
            artifact_manifest=manifest,
        )

    assert not output.exists(), "failed fresh run must not leave a previous MP4 at the target path"
    assert not manifest.exists(), "failed fresh run must not leave a previous artifact manifest"


def test_output_path_cannot_delete_generation_config(tmp_path: Path) -> None:
    root = tmp_path / "LightX2V"
    entrypoint = root / "lightx2v" / "infer.py"
    entrypoint.parent.mkdir(parents=True)
    entrypoint.write_text("# operator checkout fixture\n", encoding="utf-8")

    model_path = tmp_path / "Wan2.2-T2V-A14B"
    model_path.mkdir()
    (model_path / "weights.bin").write_bytes(b"reviewed-model-bytes")
    config_json = tmp_path / "wan_moe_t2v.json"
    config_json.write_text("{}\n", encoding="utf-8")

    config = LightX2VAdapterConfig(
        root=root,
        model_path=model_path,
        config_json=config_json,
        model_cls="wan2.2_moe",
        task="t2v",
        python_executable=sys.executable,
    )

    with pytest.raises(LightX2VError, match="output path overlaps protected operator input"):
        run_lightx2v_shot(
            config,
            prompt="原创角色完成明确动作",
            negative_prompt="",
            output=config_json,
        )

    assert config_json.read_text(encoding="utf-8") == "{}\n"


def test_artifact_manifest_cannot_overwrite_verified_video(tmp_path: Path) -> None:
    root = tmp_path / "LightX2V"
    entrypoint = root / "lightx2v" / "infer.py"
    entrypoint.parent.mkdir(parents=True)
    entrypoint.write_text("# operator checkout fixture\n", encoding="utf-8")

    model_path = tmp_path / "Wan2.2-T2V-A14B"
    model_path.mkdir()
    (model_path / "weights.bin").write_bytes(b"reviewed-model-bytes")
    config_json = tmp_path / "wan_moe_t2v.json"
    config_json.write_text("{}\n", encoding="utf-8")
    output = tmp_path / "shot.mp4"

    config = LightX2VAdapterConfig(
        root=root,
        model_path=model_path,
        config_json=config_json,
        model_cls="wan2.2_moe",
        task="t2v",
        python_executable=sys.executable,
    )

    with pytest.raises(LightX2VError, match="artifact manifest path must differ from video output"):
        run_lightx2v_shot(
            config,
            prompt="原创角色完成明确动作",
            negative_prompt="",
            output=output,
            shot_index=1,
            artifact_manifest=output,
            gpu_probe=lambda: (_ for _ in ()).throw(
                AssertionError("GPU probe must not run when output and manifest collide")
            ),
        )
