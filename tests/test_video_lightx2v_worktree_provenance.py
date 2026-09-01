from __future__ import annotations

import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

from hottop.video_lightx2v import LightX2VAdapterConfig, run_lightx2v_shot


def _git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def test_lightx2v_linked_worktree_binds_actual_git_commit(tmp_path: Path) -> None:
    repository = tmp_path / "operator-repo"
    repository.mkdir()
    _git(repository, "init")
    _git(repository, "config", "user.name", "Hottop Test")
    _git(repository, "config", "user.email", "hottop@example.invalid")

    (repository / "lightx2v").mkdir()
    (repository / "lightx2v" / "infer.py").write_text(
        "# stable entrypoint\n",
        encoding="utf-8",
    )
    (repository / "lightx2v" / "runtime.py").write_text(
        "REVISION = 1\n",
        encoding="utf-8",
    )
    config_json = repository / "configs" / "wan22" / "wan_moe_i2v.json"
    config_json.parent.mkdir(parents=True)
    config_json.write_text("{}\n", encoding="utf-8")
    _git(repository, "add", ".")
    _git(repository, "commit", "-m", "initial operator checkout")

    worktree = tmp_path / "LightX2V-worktree"
    _git(repository, "worktree", "add", "-b", "benchmark-worktree", str(worktree))
    (worktree / "lightx2v" / "runtime.py").write_text(
        "REVISION = 2\n",
        encoding="utf-8",
    )
    _git(worktree, "add", "lightx2v/runtime.py")
    _git(worktree, "commit", "-m", "change tracked runtime without changing infer")
    expected_revision = _git(worktree, "rev-parse", "HEAD")

    model_path = tmp_path / "Wan2.2-I2V-A14B"
    model_path.mkdir()
    (model_path / "weights.bin").write_bytes(b"test-model-bytes")
    config = LightX2VAdapterConfig(
        root=worktree,
        model_path=model_path,
        config_json=worktree / "configs" / "wan22" / "wan_moe_i2v.json",
        model_cls="wan2.2_moe",
        task="t2v",
        seed=42,
        code_license="Apache-2.0",
        weights_license="Apache-2.0",
    )
    output = tmp_path / "shots" / "shot-001.mp4"
    artifact_manifest = tmp_path / "shots" / "shot-001.artifact.json"

    def runner(command, **_kwargs):
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(b"generated-video")
        return subprocess.CompletedProcess(command, 0, "ok", "")

    run_lightx2v_shot(
        config,
        prompt="original subject crosses one continuous room",
        negative_prompt="identity drift",
        output=output,
        shot_index=1,
        artifact_manifest=artifact_manifest,
        runner=runner,
        gpu_probe=lambda: None,
        quality_inspector=lambda _path, _policy: SimpleNamespace(pass_=True, reasons=[]),
    )

    manifest = json.loads(artifact_manifest.read_text(encoding="utf-8"))
    shot = manifest["shots"][0]
    assert shot["candidate_revision"] == expected_revision
