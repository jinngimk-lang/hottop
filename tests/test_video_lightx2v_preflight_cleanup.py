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
