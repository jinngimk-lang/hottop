from __future__ import annotations

import subprocess

import pytest

from hottop.video_lightx2v import LightX2VError, require_nvidia_gpu


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
