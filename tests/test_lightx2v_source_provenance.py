from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

import hottop.video_lightx2v as video_lightx2v
from hottop.video_lightx2v import LightX2VAdapterConfig, LightX2VError, run_lightx2v_shot


def test_lightx2v_rejects_tracked_dirty_git_checkout_before_generation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "LightX2V"
    (root / "lightx2v").mkdir(parents=True)
    (root / "lightx2v" / "infer.py").write_text("# modified operator source\n", encoding="utf-8")
    (root / ".git").mkdir()
    config_json = root / "configs" / "wan22" / "wan_moe_i2v.json"
    config_json.parent.mkdir(parents=True)
    config_json.write_text("{}\n", encoding="utf-8")
    model_path = tmp_path / "Wan2.2-I2V-A14B"
    model_path.mkdir()
    config = LightX2VAdapterConfig(
        root=root,
        model_path=model_path,
        config_json=config_json,
        model_cls="wan2.2_moe",
        task="t2v",
    )

    monkeypatch.setattr(video_lightx2v.shutil, "which", lambda name: "/usr/bin/git" if name == "git" else "/usr/bin/python")
    monkeypatch.setattr(
        video_lightx2v.subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args[0], 0, " M lightx2v/infer.py\n", ""
        ),
    )
    generation_calls: list[list[str]] = []

    def generation_runner(command: list[str], **_kwargs):
        generation_calls.append(command)
        raise AssertionError("generation must not start from a dirty tracked checkout")

    with pytest.raises(LightX2VError, match="uncommitted tracked changes"):
        run_lightx2v_shot(
            config,
            prompt="same subject performs the planned action",
            negative_prompt="identity drift",
            output=tmp_path / "shot.mp4",
            runner=generation_runner,
        )

    assert generation_calls == []
