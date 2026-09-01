from __future__ import annotations

import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

from hottop.video_lightx2v import LightX2VAdapterConfig, run_lightx2v_shot


def test_lightx2v_artifact_records_actual_checkout_revision(tmp_path: Path) -> None:
    root = tmp_path / "LightX2V"
    (root / "lightx2v").mkdir(parents=True)
    (root / "lightx2v" / "infer.py").write_text("# operator checkout\n", encoding="utf-8")
    config_json = root / "configs" / "wan22" / "wan_moe_i2v.json"
    config_json.parent.mkdir(parents=True)
    config_json.write_text("{}\n", encoding="utf-8")

    subprocess.run(["git", "init", str(root)], check=True, capture_output=True, text=True)
    subprocess.run(
        ["git", "-C", str(root), "config", "user.name", "Hottop Test"],
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["git", "-C", str(root), "config", "user.email", "hottop-test@example.invalid"],
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["git", "-C", str(root), "add", "lightx2v/infer.py", "configs/wan22/wan_moe_i2v.json"],
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["git", "-C", str(root), "commit", "-m", "test operator checkout"],
        check=True,
        capture_output=True,
        text=True,
    )
    revision = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    model_path = tmp_path / "Wan2.2-I2V-A14B"
    model_path.mkdir()
    (model_path / "weights.bin").write_bytes(b"test-model-bytes")
    output = tmp_path / "shot-001.mp4"
    artifact_manifest = tmp_path / "shot-001.artifact.json"
    config = LightX2VAdapterConfig(
        root=root,
        model_path=model_path,
        config_json=config_json,
        model_cls="wan2.2_moe",
        task="t2v",
    )

    def runner(command, **_kwargs):
        output.write_bytes(b"generated-video")
        return subprocess.CompletedProcess(command, 0, "ok", "")

    run_lightx2v_shot(
        config,
        prompt="original cinematic subject",
        negative_prompt="identity drift",
        output=output,
        shot_index=1,
        artifact_manifest=artifact_manifest,
        runner=runner,
        gpu_probe=lambda: None,
        quality_inspector=lambda _path, _policy: SimpleNamespace(pass_=True, reasons=[]),
    )

    artifact = json.loads(artifact_manifest.read_text(encoding="utf-8"))["shots"][0]
    assert artifact["candidate_id"] == "lightx2v-wan22-t2v"
    assert artifact["candidate_revision"] == revision
