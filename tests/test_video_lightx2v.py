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
    (model_path / "weights.bin").write_bytes(b"test-model-bytes")
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


def test_lightx2v_fails_closed_before_gpu_when_config_json_is_invalid(tmp_path):
    config = _config(tmp_path, task="t2v")
    config.config_json.write_text("{not valid json", encoding="utf-8")

    def gpu_probe():
        raise AssertionError("GPU probe must not start when config JSON is invalid")

    with pytest.raises(LightX2VError, match="config JSON"):
        run_lightx2v_shot(
            config,
            prompt="test",
            negative_prompt="",
            output=tmp_path / "shot.mp4",
            runner=lambda *_args, **_kwargs: None,
            gpu_probe=gpu_probe,
        )


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
        gpu_probe=lambda: None,
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
        gpu_probe=lambda: None,
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


def test_lightx2v_artifact_manifest_binds_exact_generation_request(tmp_path):
    config = _config(tmp_path, task="t2v")
    output = tmp_path / "shots" / "shot-007.mp4"
    artifact_manifest = tmp_path / "shots" / "shot-007.artifact.json"
    prompt = "原创角色沿走廊冲刺，在门前急停"
    negative_prompt = "identity drift, frozen motion"

    def runner(command, **_kwargs):
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(b"generated-from-exact-request")
        return subprocess.CompletedProcess(command, 0, "ok", "")

    run_lightx2v_shot(
        config,
        prompt=prompt,
        negative_prompt=negative_prompt,
        output=output,
        shot_index=7,
        artifact_manifest=artifact_manifest,
        runner=runner,
        gpu_probe=lambda: None,
        quality_inspector=lambda _path, _policy: SimpleNamespace(pass_=True, reasons=[]),
    )

    request_bytes = json.dumps(
        {
            "schema_version": "hottop.lightx2v-generation-request.v1",
            "model_cls": "wan2.2_moe",
            "task": "t2v",
            "seed": 42,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    shot = json.loads(artifact_manifest.read_text(encoding="utf-8"))["shots"][0]
    assert shot["generation_request_sha256"] == hashlib.sha256(request_bytes).hexdigest()
    assert shot["generation_request_size_bytes"] == len(request_bytes)


def test_lightx2v_i2v_manifest_binds_reference_bytes_and_rights(tmp_path):
    config = _config(tmp_path)
    reference = tmp_path / "hero.png"
    reference_bytes = b"rights-safe-original-reference"
    reference.write_bytes(reference_bytes)
    output = tmp_path / "shots" / "shot-006.mp4"
    artifact_manifest = tmp_path / "shots" / "shot-006.artifact.json"

    def runner(command, **_kwargs):
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(b"generated-from-bound-reference")
        return subprocess.CompletedProcess(command, 0, "ok", "")

    run_lightx2v_shot(
        config,
        prompt="same original hero performs the requested action",
        negative_prompt="identity drift",
        output=output,
        reference_image=reference,
        reference_rights="generated-original",
        shot_index=6,
        artifact_manifest=artifact_manifest,
        runner=runner,
        gpu_probe=lambda: None,
        quality_inspector=lambda _path, _policy: SimpleNamespace(pass_=True, reasons=[]),
    )

    shot = json.loads(artifact_manifest.read_text(encoding="utf-8"))["shots"][0]
    assert shot["reference_sha256"] == hashlib.sha256(reference_bytes).hexdigest()
    assert shot["reference_size_bytes"] == len(reference_bytes)
    assert shot["reference_rights"] == "generated-original"


def test_lightx2v_rejects_source_mutation_during_generation(tmp_path):
    config = _config(tmp_path, task="t2v")
    output = tmp_path / "shots" / "shot-004.mp4"
    artifact_manifest = tmp_path / "shots" / "shot-004.artifact.json"
    entrypoint = config.root / "lightx2v" / "infer.py"

    def runner(command, **_kwargs):
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(b"generated-under-original-source")
        entrypoint.write_text("# mutated while generation was running\n", encoding="utf-8")
        return subprocess.CompletedProcess(command, 0, "ok", "")

    with pytest.raises(LightX2VError, match="source changed during generation"):
        run_lightx2v_shot(
            config,
            prompt="original cinematic shot",
            negative_prompt="identity drift",
            output=output,
            shot_index=4,
            artifact_manifest=artifact_manifest,
            runner=runner,
            gpu_probe=lambda: None,
            quality_inspector=lambda _path, _policy: SimpleNamespace(pass_=True, reasons=[]),
        )

    assert not output.exists()
    assert not artifact_manifest.exists()


def test_lightx2v_rejects_reference_mutation_during_generation(tmp_path):
    config = _config(tmp_path)
    reference = tmp_path / "hero.png"
    reference.write_bytes(b"original-reference-bytes")
    output = tmp_path / "shots" / "shot-005.mp4"
    artifact_manifest = tmp_path / "shots" / "shot-005.artifact.json"

    def runner(command, **_kwargs):
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(b"generated-under-original-reference")
        reference.write_bytes(b"replacement-reference-bytes")
        return subprocess.CompletedProcess(command, 0, "ok", "")

    with pytest.raises(LightX2VError, match="reference image changed during generation"):
        run_lightx2v_shot(
            config,
            prompt="same original hero crosses one continuous room",
            negative_prompt="identity drift",
            output=output,
            reference_image=reference,
            reference_rights="generated-original",
            shot_index=5,
            artifact_manifest=artifact_manifest,
            runner=runner,
            gpu_probe=lambda: None,
            quality_inspector=lambda _path, _policy: SimpleNamespace(pass_=True, reasons=[]),
        )

    assert not output.exists()
    assert not artifact_manifest.exists()


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
            gpu_probe=lambda: None,
            quality_inspector=lambda _path, _policy: SimpleNamespace(
                pass_=False,
                reasons=["duplicate frames"],
            ),
        )

    assert not output.exists()
