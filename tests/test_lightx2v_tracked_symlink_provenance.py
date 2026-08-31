from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from hottop.video_lightx2v import LightX2VAdapterConfig, LightX2VError, run_lightx2v_shot


def _git(root: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
    )


@pytest.mark.skipif(shutil.which("git") is None, reason="git is required for provenance test")
def test_lightx2v_rejects_tracked_symlink_that_escapes_checkout_before_generation(
    tmp_path: Path,
) -> None:
    root = tmp_path / "LightX2V"
    (root / "lightx2v").mkdir(parents=True)
    (root / "lightx2v" / "infer.py").write_text("# operator entrypoint\n", encoding="utf-8")

    external_runtime = tmp_path / "external_runtime.py"
    external_runtime.write_text("VALUE = 'not bound by checkout HEAD'\n", encoding="utf-8")
    (root / "lightx2v" / "runtime.py").symlink_to(external_runtime)

    config_json = root / "configs" / "wan22" / "wan_moe_t2v.json"
    config_json.parent.mkdir(parents=True)
    config_json.write_text("{}\n", encoding="utf-8")

    _git(root, "init")
    _git(root, "config", "user.email", "hottop-tests@example.invalid")
    _git(root, "config", "user.name", "Hottop Tests")
    _git(root, "add", "lightx2v", "configs")
    _git(root, "commit", "-m", "fixture")

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

    def generation_runner(command: list[str], **_kwargs):
        generation_calls.append(command)
        raise AssertionError("generation must not start when tracked source escapes the checkout")

    with pytest.raises(LightX2VError, match="tracked symlink.*outside"):
        run_lightx2v_shot(
            config,
            prompt="same subject performs the planned action",
            negative_prompt="identity drift",
            output=tmp_path / "shot.mp4",
            runner=generation_runner,
        )

    assert generation_calls == []
