from __future__ import annotations

import sys
from pathlib import Path

import hottop.video_lightx2v as video_lightx2v


def test_lightx2v_cli_preserves_explicit_seed(monkeypatch, tmp_path: Path):
    captured: dict[str, object] = {}

    def fake_run(config, **kwargs):
        captured["config"] = config
        captured["kwargs"] = kwargs
        return Path(kwargs["output"])

    monkeypatch.setattr(video_lightx2v, "run_lightx2v_shot", fake_run)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "hottop.video_lightx2v",
            "--root",
            str(tmp_path / "LightX2V"),
            "--model-path",
            str(tmp_path / "Wan2.2-I2V-A14B"),
            "--config-json",
            str(tmp_path / "wan_moe_i2v.json"),
            "--model-cls",
            "wan2.2_moe",
            "--task",
            "t2v",
            "--seed",
            "314159",
            "--prompt",
            "原创角色完成明确动作",
            "--output",
            str(tmp_path / "shot.mp4"),
        ],
    )

    video_lightx2v.main()

    assert captured["config"].seed == 314159
    assert captured["kwargs"]["prompt"] == "原创角色完成明确动作"
