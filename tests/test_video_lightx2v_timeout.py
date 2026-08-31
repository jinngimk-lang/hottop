from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from hottop.video_lightx2v import LightX2VAdapterConfig, LightX2VError, run_lightx2v_shot


def _config(tmp_path: Path) -> LightX2VAdapterConfig:
    root = tmp_path / "LightX2V"
    (root / "lightx2v").mkdir(parents=True)
    (root / "lightx2v" / "infer.py").write_text("# operator checkout\n", encoding="utf-8")
    config_json = root / "configs" / "wan22" / "wan_moe_t2v.json"
    config_json.parent.mkdir(parents=True)
    config_json.write_text("{}\n", encoding="utf-8")
    model_path = tmp_path / "Wan2.2-T2V-A14B"
    model_path.mkdir()
    return LightX2VAdapterConfig(
        root=root,
        model_path=model_path,
        config_json=config_json,
        model_cls="wan2.2_moe",
        task="t2v",
        seed=42,
        generation_timeout_seconds=3600,
    )


def test_lightx2v_passes_bounded_timeout_to_operator_process(tmp_path):
    config = _config(tmp_path)
    output = tmp_path / "shot.mp4"
    captured: dict[str, object] = {}

    def runner(command, **kwargs):
        captured.update(kwargs)
        output.write_bytes(b"generated-video")
        return subprocess.CompletedProcess(command, 0, "ok", "")

    run_lightx2v_shot(
        config,
        prompt="original cinematic shot",
        negative_prompt="identity drift",
        output=output,
        runner=runner,
        quality_inspector=lambda _path, _policy: type(
            "Report", (), {"pass_": True, "reasons": []}
        )(),
    )

    assert captured["timeout"] == 3600


def test_lightx2v_timeout_fails_closed_and_deletes_partial_output(tmp_path):
    config = _config(tmp_path)
    output = tmp_path / "shot.mp4"

    def runner(command, **kwargs):
        output.write_bytes(b"partial-video")
        raise subprocess.TimeoutExpired(command, timeout=kwargs.get("timeout"))

    with pytest.raises(LightX2VError, match="timed out"):
        run_lightx2v_shot(
            config,
            prompt="original cinematic shot",
            negative_prompt="identity drift",
            output=output,
            runner=runner,
        )

    assert not output.exists()
