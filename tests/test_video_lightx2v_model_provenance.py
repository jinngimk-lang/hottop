from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from hottop.video_lightx2v import LightX2VAdapterConfig, LightX2VError, run_lightx2v_shot


def _config(tmp_path: Path) -> LightX2VAdapterConfig:
    root = tmp_path / "LightX2V"
    (root / "lightx2v").mkdir(parents=True)
    (root / "lightx2v" / "infer.py").write_text("# operator checkout\n", encoding="utf-8")
    config_json = root / "configs" / "wan22" / "wan_moe_i2v.json"
    config_json.parent.mkdir(parents=True)
    config_json.write_text("{}\n", encoding="utf-8")
    model_path = tmp_path / "Wan2.2-I2V-A14B"
    model_path.mkdir()
    (model_path / "configuration.json").write_bytes(b'{"model":"wan2.2"}\n')
    (model_path / "weights.bin").write_bytes(b"operator-owned-weight-bytes")
    return LightX2VAdapterConfig(
        root=root,
        model_path=model_path,
        config_json=config_json,
        model_cls="wan2.2_moe",
        task="t2v",
        code_license="Apache-2.0",
        weights_license="Apache-2.0",
    )


def _tree_identity(model_path: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    total_size = 0
    for path in sorted(item for item in model_path.rglob("*") if item.is_file()):
        relative = path.relative_to(model_path).as_posix().encode("utf-8")
        payload = path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
        total_size += len(payload)
    return digest.hexdigest(), total_size


def test_lightx2v_manifest_binds_exact_local_model_tree_bytes(tmp_path):
    config = _config(tmp_path)
    output = tmp_path / "shots" / "shot-001.mp4"
    manifest_path = tmp_path / "shots" / "shot-001.artifact.json"
    expected_sha256, expected_size = _tree_identity(config.model_path)

    def runner(command, **_kwargs):
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(b"generated-video")
        return subprocess.CompletedProcess(command, 0, "ok", "")

    run_lightx2v_shot(
        config,
        prompt="original subject performs the requested action",
        negative_prompt="identity drift",
        output=output,
        shot_index=1,
        artifact_manifest=manifest_path,
        runner=runner,
        gpu_probe=lambda: None,
        quality_inspector=lambda _path, _policy: SimpleNamespace(pass_=True, reasons=[]),
    )

    shot = json.loads(manifest_path.read_text(encoding="utf-8"))["shots"][0]
    assert shot["generation_model_sha256"] == expected_sha256
    assert shot["generation_model_size_bytes"] == expected_size


def test_lightx2v_rejects_model_mutation_during_generation(tmp_path):
    config = _config(tmp_path)
    output = tmp_path / "shots" / "shot-002.mp4"
    manifest_path = tmp_path / "shots" / "shot-002.artifact.json"
    weights = config.model_path / "weights.bin"

    def runner(command, **_kwargs):
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(b"generated-under-original-model")
        weights.write_bytes(b"replacement-weight-bytes")
        return subprocess.CompletedProcess(command, 0, "ok", "")

    with pytest.raises(LightX2VError, match="model changed during generation"):
        run_lightx2v_shot(
            config,
            prompt="original subject performs the requested action",
            negative_prompt="identity drift",
            output=output,
            shot_index=2,
            artifact_manifest=manifest_path,
            runner=runner,
            gpu_probe=lambda: None,
            quality_inspector=lambda _path, _policy: SimpleNamespace(pass_=True, reasons=[]),
        )

    assert not output.exists()
    assert not manifest_path.exists()


def test_lightx2v_rejects_empty_local_model_tree_before_gpu_generation(tmp_path):
    config = _config(tmp_path)
    for path in config.model_path.iterdir():
        path.unlink()
    output = tmp_path / "shots" / "shot-empty-model.mp4"
    calls = {"gpu": 0, "runner": 0}

    def gpu_probe() -> None:
        calls["gpu"] += 1

    def runner(command, **_kwargs):
        calls["runner"] += 1
        return subprocess.CompletedProcess(command, 0, "ok", "")

    with pytest.raises(LightX2VError, match="model tree contains no local file bytes"):
        run_lightx2v_shot(
            config,
            prompt="original subject performs the requested action",
            negative_prompt="identity drift",
            output=output,
            runner=runner,
            gpu_probe=gpu_probe,
            quality_inspector=lambda _path, _policy: SimpleNamespace(pass_=True, reasons=[]),
        )

    assert calls == {"gpu": 0, "runner": 0}
    assert not output.exists()


def test_lightx2v_rejects_model_symlink_that_escapes_model_root_before_gpu_generation(tmp_path):
    config = _config(tmp_path)
    outside = tmp_path / "outside-weights.bin"
    outside.write_bytes(b"bytes-outside-reviewed-model-root")
    escaping_link = config.model_path / "external-weights.bin"
    try:
        escaping_link.symlink_to(outside)
    except OSError as exc:
        pytest.skip(f"symlinks unavailable on this platform: {exc}")

    output = tmp_path / "shots" / "shot-escaping-model-link.mp4"
    calls = {"gpu": 0, "runner": 0}

    def gpu_probe() -> None:
        calls["gpu"] += 1

    def runner(command, **_kwargs):
        calls["runner"] += 1
        return subprocess.CompletedProcess(command, 0, "ok", "")

    with pytest.raises(LightX2VError, match="model tree contains a symlink that resolves outside"):
        run_lightx2v_shot(
            config,
            prompt="original subject performs the requested action",
            negative_prompt="identity drift",
            output=output,
            runner=runner,
            gpu_probe=gpu_probe,
            quality_inspector=lambda _path, _policy: SimpleNamespace(pass_=True, reasons=[]),
        )

    assert calls == {"gpu": 0, "runner": 0}
    assert not output.exists()
