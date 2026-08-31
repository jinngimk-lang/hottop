from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

import hottop.video_lightx2v as video_lightx2v


def test_lightx2v_rejects_source_revision_change_during_generation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "LightX2V"
    (root / "lightx2v").mkdir(parents=True)
    (root / "lightx2v" / "infer.py").write_text("# reviewed source\n", encoding="utf-8")
    model_path = tmp_path / "model"
    model_path.mkdir()
    config_json = tmp_path / "config.json"
    config_json.write_text("{}\n", encoding="utf-8")
    output = tmp_path / "shot.mp4"
    manifest = tmp_path / "shot.artifact.json"

    revisions = iter(["source-a", "source-b"])
    monkeypatch.setattr(video_lightx2v, "_local_source_revision", lambda _root: next(revisions))
    monkeypatch.setattr(video_lightx2v, "_verify_quality", lambda *_args, **_kwargs: None)

    def runner(*_args, **_kwargs) -> subprocess.CompletedProcess[str]:
        output.write_bytes(b"fresh-video")
        return subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")

    config = video_lightx2v.LightX2VAdapterConfig(
        root=root,
        model_path=model_path,
        config_json=config_json,
        model_cls="wan2.2_moe",
        task="t2v",
        python_executable=sys.executable,
    )

    with pytest.raises(video_lightx2v.LightX2VError, match="source revision changed"):
        video_lightx2v.run_lightx2v_shot(
            config,
            prompt="move forward",
            negative_prompt="",
            output=output,
            shot_index=1,
            artifact_manifest=manifest,
            runner=runner,
        )

    assert not output.exists()
    assert not manifest.exists()
