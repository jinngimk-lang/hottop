from __future__ import annotations

from pathlib import Path

import hottop.video_lightx2v as video_lightx2v


def test_lightx2v_offline_environment_drops_inherited_pythonpath(
    tmp_path: Path, monkeypatch
) -> None:
    root = tmp_path / "LightX2V"
    root.mkdir()
    monkeypatch.setenv("PYTHONPATH", "/tmp/unbound-python-source")

    env = video_lightx2v._offline_environment(root)

    assert env["PYTHONPATH"] == str(root)
    assert "/tmp/unbound-python-source" not in env["PYTHONPATH"]
