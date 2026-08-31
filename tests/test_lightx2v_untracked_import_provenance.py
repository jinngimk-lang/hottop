from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

import hottop.video_lightx2v as video_lightx2v


def _init_git_checkout(root: Path) -> None:
    (root / "lightx2v").mkdir(parents=True)
    (root / "lightx2v" / "infer.py").write_text("# tracked entrypoint\n", encoding="utf-8")
    subprocess.run(["git", "init", str(root)], check=True, capture_output=True, text=True)
    subprocess.run(["git", "-C", str(root), "add", "lightx2v/infer.py"], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "-c",
            "user.name=Hottop CI",
            "-c",
            "user.email=hottop@example.invalid",
            "commit",
            "-m",
            "fixture",
        ],
        check=True,
        capture_output=True,
        text=True,
    )


def test_lightx2v_checkout_rejects_untracked_importable_python(tmp_path: Path) -> None:
    root = tmp_path / "LightX2V"
    _init_git_checkout(root)
    (root / "sitecustomize.py").write_text("raise RuntimeError('unbound code')\n", encoding="utf-8")

    with pytest.raises(video_lightx2v.LightX2VError, match="untracked importable"):
        video_lightx2v._require_clean_tracked_git_checkout(root)


def test_lightx2v_checkout_rejects_ignored_importable_python(tmp_path: Path) -> None:
    root = tmp_path / "LightX2V"
    _init_git_checkout(root)
    (root / ".gitignore").write_text("sitecustomize.py\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", ".gitignore"], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "-c",
            "user.name=Hottop CI",
            "-c",
            "user.email=hottop@example.invalid",
            "commit",
            "-m",
            "ignore fixture",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    (root / "sitecustomize.py").write_text("raise RuntimeError('ignored code')\n", encoding="utf-8")

    with pytest.raises(video_lightx2v.LightX2VError, match="untracked importable"):
        video_lightx2v._require_clean_tracked_git_checkout(root)


def test_lightx2v_checkout_allows_untracked_non_code_data(tmp_path: Path) -> None:
    root = tmp_path / "LightX2V"
    _init_git_checkout(root)
    (root / "operator-notes.txt").write_text("local notes\n", encoding="utf-8")

    video_lightx2v._require_clean_tracked_git_checkout(root)
