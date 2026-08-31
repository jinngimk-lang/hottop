from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from hottop.video_lightx2v import LightX2VAdapterConfig, LightX2VError, run_lightx2v_shot


def _config(tmp_path: Path) -> LightX2VAdapterConfig:
    root = tmp_path / "LightX2V"
    (root / "lightx2v").mkdir(parents=True)
    (root / "lightx2v" / "infer.py").write_text("# operator checkout\n", encoding="utf-8")
    config_json = root / "configs" / "wan22" / "wan_moe_i2v.json"
    config_json.parent.mkdir(parents=True)
    config_json.write_text('{"num_inference_steps": 6}\n', encoding="utf-8")
    model_path = tmp_path / "Wan2.2-I2V-A14B"
    model_path.mkdir()
    return LightX2VAdapterConfig(
        root=root,
        model_path=model_path,
        config_json=config_json,
        model_cls="wan2.2_moe",
        task="t2v",
        seed=42,
    )


def test_lightx2v_artifact_manifest_binds_generation_config_bytes(tmp_path: Path) -> None:
    config = _config(tmp_path)
    output = tmp_path / "shots" / "shot-001.mp4"
    manifest_path = tmp_path / "shots" / "shot-001.artifact.json"
    config_bytes = config.config_json.read_bytes()

    def runner(command, **_kwargs):
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(b"generated-video")
        return subprocess.CompletedProcess(command, 0, "ok", "")

    run_lightx2v_shot(
        config,
        prompt="original cinematic shot",
        negative_prompt="identity drift",
        output=output,
        shot_index=1,
        artifact_manifest=manifest_path,
        runner=runner,
        quality_inspector=lambda _path, _policy: SimpleNamespace(pass_=True, reasons=[]),
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    shot = manifest["shots"][0]
    assert shot["generation_config_sha256"] == hashlib.sha256(config_bytes).hexdigest()
    assert shot["generation_config_size_bytes"] == len(config_bytes)


def test_lightx2v_rejects_generation_config_mutation_during_generation(tmp_path: Path) -> None:
    config = _config(tmp_path)
    output = tmp_path / "shots" / "shot-002.mp4"
    manifest_path = tmp_path / "shots" / "shot-002.artifact.json"

    def runner(command, **_kwargs):
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(b"generated-under-original-config")
        config.config_json.write_text('{"num_inference_steps": 99}\n', encoding="utf-8")
        return subprocess.CompletedProcess(command, 0, "ok", "")

    with pytest.raises(LightX2VError, match="config changed during generation"):
        run_lightx2v_shot(
            config,
            prompt="original cinematic shot",
            negative_prompt="identity drift",
            output=output,
            shot_index=2,
            artifact_manifest=manifest_path,
            runner=runner,
            quality_inspector=lambda _path, _policy: SimpleNamespace(pass_=True, reasons=[]),
        )

    assert not output.exists()
    assert not manifest_path.exists()
