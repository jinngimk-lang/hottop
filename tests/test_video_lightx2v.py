from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from hottop.video_lightx2v import (
    LightX2VAdapterConfig,
    LightX2VError,
    build_lightx2v_command,
    run_lightx2v_shot,
)


def _installation(tmp_path: Path) -> tuple[Path, Path, Path]:
    root = tmp_path / "LightX2V"
    (root / "lightx2v").mkdir(parents=True)
    (root / "lightx2v" / "infer.py").write_text("# operator checkout\n", encoding="utf-8")
    config_json = root / "configs" / "wan22" / "wan_moe_i2v.json"
    config_json.parent.mkdir(parents=True)
    config_json.write_text("{}\n", encoding="utf-8")
    model_path = tmp_path / "Wan2.2-I2V-A14B"
    model_path.mkdir()
    return root, config_json, model_path


def _config(tmp_path: Path, *, task: str = "i2v") -> LightX2VAdapterConfig:
    root, config_json, model_path = _installation(tmp_path)
    return LightX2VAdapterConfig(
        root=root,
        model_path=model_path,
        config_json=config_json,
        model_cls="wan2.2_moe",
        task=task,
        seed=42,
        code_license="Apache-2.0",
        weights_license="Apache-2.0",
    )


def test_lightx2v_command_uses_official_module_entrypoint_and_local_paths(tmp_path):
    config = _config(tmp_path)
    reference = tmp_path / "hero.png"
    reference.write_bytes(b"png")
    output = tmp_path / "shot.mp4"

    command = build_lightx2v_command(
        config,
        prompt="same original hero crosses one continuous room",
        negative_prompt="identity drift, copied film frame",
        output=output,
        reference_image=reference,
    )

    assert command[:3] == [config.python_executable, "-m", "lightx2v.infer"]
    assert ["--model_cls", "wan2.2_moe"] == command[3:5]
    assert "--task" in command and command[command.index("--task") + 1] == "i2v"
    assert command[command.index("--model_path") + 1] == str(config.model_path.resolve())
    assert command[command.index("--config_json") + 1] == str(config.config_json.resolve())
    assert command[command.index("--image_path") + 1] == str(reference.resolve())
    assert command[command.index("--save_result_path") + 1] == str(output.resolve())


def test_lightx2v_fails_closed_before_runner_when_local_model_is_missing(tmp_path):
    config = _config(tmp_path, task="t2v")
    config = config.model_copy(update={"model_path": tmp_path / "missing-model"})
    calls: list[list[str]] = []

    def runner(command, **_kwargs):
        calls.append(command)
        raise AssertionError("runner must not start when model files are missing")

    with pytest.raises(LightX2VError, match="model path"):
        run_lightx2v_shot(
            config,
            prompt="test",
            negative_prompt="",
            output=tmp_path / "shot.mp4",
            runner=runner,
        )

    assert calls == []


def test_lightx2v_i2v_requires_rights_safe_reference(tmp_path):
    config = _config(tmp_path)
    reference = tmp_path / "hero.png"
    reference.write_bytes(b"png")

    with pytest.raises(LightX2VError, match="rights-safe"):
        run_lightx2v_shot(
            config,
            prompt="test",
            negative_prompt="",
            output=tmp_path / "shot.mp4",
            reference_image=reference,
            runner=lambda *_args, **_kwargs: None,
        )


def test_lightx2v_executes_offline_and_quality_gates_output(tmp_path):
    config = _config(tmp_path)
    reference = tmp_path / "hero.png"
    reference.write_bytes(b"png")
    output = tmp_path / "shots" / "shot-001.mp4"
    captured: dict[str, object] = {}

    def runner(command, **kwargs):
        captured["command"] = command
        captured["kwargs"] = kwargs
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(b"generated-video")
        return subprocess.CompletedProcess(command, 0, "ok", "")

    result = run_lightx2v_shot(
        config,
        prompt="original low-budget cinematic bovine programmer",
        negative_prompt="identity drift",
        output=output,
        reference_image=reference,
        reference_rights="generated-original",
        runner=runner,
        quality_inspector=lambda _path, _policy: SimpleNamespace(pass_=True, reasons=[]),
    )

    assert result == output.resolve()
    kwargs = captured["kwargs"]
    assert kwargs["cwd"] == config.root.resolve()
    assert kwargs["shell"] is False
    env = kwargs["env"]
    assert env["HF_HUB_OFFLINE"] == "1"
    assert env["TRANSFORMERS_OFFLINE"] == "1"
    assert env["HF_DATASETS_OFFLINE"] == "1"
    assert str(config.root.resolve()) in env["PYTHONPATH"].split("\n")[0].split(":")
    assert config.auto_install is False
    assert config.auto_download_models is False


def test_lightx2v_writes_byte_bound_artifact_manifest_after_quality_pass(tmp_path):
    config = _config(tmp_path, task="t2v")
    output = tmp_path / "shots" / "shot-003.mp4"
    artifact_manifest = tmp_path / "shots" / "shot-003.artifact.json"
    payload = b"model-generated-video-bytes"

    def runner(command, **_kwargs):
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(payload)
        return subprocess.CompletedProcess(command, 0, "ok", "")

    run_lightx2v_shot(
        config,
        prompt="original cinematic shot",
        negative_prompt="identity drift",
        output=output,
        shot_index=3,
        artifact_manifest=artifact_manifest,
        runner=runner,
        quality_inspector=lambda _path, _policy: SimpleNamespace(pass_=True, reasons=[]),
    )

    manifest = json.loads(artifact_manifest.read_text(encoding="utf-8"))
    assert manifest["schema_version"] == "hottop.video-artifacts.v1"
    assert manifest["planned_generation_backend"] == "lightx2v-operator"
    assert len(manifest["shots"]) == 1
    shot = manifest["shots"][0]
    assert shot["shot_index"] == 3
    assert shot["path"] == str(output.resolve())
    assert shot["artifact_kind"] == "ai-generated"
    assert shot["backend"] == "lightx2v:wan2.2_moe"
    assert shot["size_bytes"] == len(payload)
    assert shot["sha256"] == hashlib.sha256(payload).hexdigest()


def test_lightx2v_rejected_output_is_deleted(tmp_path):
    config = _config(tmp_path, task="t2v")
    output = tmp_path / "shot.mp4"

    def runner(command, **_kwargs):
        output.write_bytes(b"bad-video")
        return subprocess.CompletedProcess(command, 0, "", "")

    with pytest.raises(LightX2VError, match="quality gate"):
        run_lightx2v_shot(
            config,
            prompt="test",
            negative_prompt="",
            output=output,
            runner=runner,
            quality_inspector=lambda _path, _policy: SimpleNamespace(
                pass_=False,
                reasons=["duplicate frames"],
            ),
        )

    assert not output.exists()
