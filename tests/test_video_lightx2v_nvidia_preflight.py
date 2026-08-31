from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from hottop.video_lightx2v import (
    LightX2VAdapterConfig,
    LightX2VError,
    require_nvidia_gpu,
    run_lightx2v_shot,
)


def test_lightx2v_nvidia_probe_accepts_one_visible_gpu():
    def runner(command, **kwargs):
        assert command == [
            "nvidia-smi",
            "--query-gpu=index,name,memory.total",
            "--format=csv,noheader,nounits",
        ]
        assert kwargs["shell"] is False
        assert kwargs["timeout"] == 10
        return subprocess.CompletedProcess(command, 0, "0, NVIDIA RTX, 24576\n", "")

    require_nvidia_gpu(runner=runner)


def test_lightx2v_nvidia_probe_fails_closed_when_driver_reports_no_gpu():
    def runner(command, **_kwargs):
        return subprocess.CompletedProcess(command, 0, "", "")

    with pytest.raises(LightX2VError, match="no usable NVIDIA GPU"):
        require_nvidia_gpu(runner=runner)


def test_lightx2v_nvidia_probe_fails_closed_when_nvidia_smi_is_missing():
    def runner(_command, **_kwargs):
        raise FileNotFoundError("nvidia-smi")

    with pytest.raises(LightX2VError, match="nvidia-smi"):
        require_nvidia_gpu(runner=runner)


def test_lightx2v_generation_fails_before_runner_when_gpu_probe_rejects(tmp_path: Path):
    root = tmp_path / "LightX2V"
    (root / "lightx2v").mkdir(parents=True)
    (root / "lightx2v" / "infer.py").write_text("# operator checkout\n", encoding="utf-8")
    config_json = root / "configs" / "wan22" / "wan_moe_t2v.json"
    config_json.parent.mkdir(parents=True)
    config_json.write_text("{}\n", encoding="utf-8")
    model_path = tmp_path / "Wan2.2-T2V-A14B"
    model_path.mkdir()
    config = LightX2VAdapterConfig(
        root=root,
        model_path=model_path,
        config_json=config_json,
        model_cls="wan2.2_moe",
        task="t2v",
    )
    generation_calls: list[list[str]] = []

    def generation_runner(command, **_kwargs):
        generation_calls.append(command)
        raise AssertionError("generation must not start without a usable NVIDIA GPU")

    def rejecting_gpu_probe():
        raise LightX2VError("LightX2V has no usable NVIDIA GPU visible to nvidia-smi")

    with pytest.raises(LightX2VError, match="no usable NVIDIA GPU"):
        run_lightx2v_shot(
            config,
            prompt="original cinematic shot",
            negative_prompt="identity drift",
            output=tmp_path / "shot.mp4",
            runner=generation_runner,
            gpu_probe=rejecting_gpu_probe,
        )

    assert generation_calls == []
