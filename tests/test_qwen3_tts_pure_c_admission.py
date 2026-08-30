from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_qwen3_tts_pure_c_benchmark_manifest_is_fail_closed() -> None:
    path = ROOT / "integrations" / "qwen3-tts-pure-c-benchmark.yml"
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))

    assert raw["id"] == "qwen3-tts-pure-c-1b7"
    assert raw["source_revision_reviewed"] == "f1b6865713d12a2a2365282fc02e19a5a384a565"
    assert raw["code_license"] == "MIT"
    assert raw["model_family"] == "Qwen3-TTS-12Hz-1.7B-CustomVoice"
    assert raw["cost_class"] == "self_owned_compute"
    assert raw["integration_ready"] is False
    assert raw["runtime_status"] == "unprobed"
    assert raw["auto_download_models"] is False
    assert raw["auto_build_upstream"] is False
    assert raw["normal_video_run_allowed"] is False
    assert "download_model.sh" in raw["forbidden_unattended_paths"]
    assert "Chinese" in raw["languages"]
    assert "seed" in raw["benchmark_controls"]
    assert "max_duration" in raw["benchmark_controls"]


def test_qwen3_tts_pure_c_admission_record_binds_rights_and_runtime() -> None:
    record = ROOT / "docs" / "research" / "2026-08-30-qwen3-tts-pure-c-admission.md"
    text = record.read_text(encoding="utf-8")

    assert "f1b6865713d12a2a2365282fc02e19a5a384a565" in text
    assert "MIT" in text
    assert "Qwen3-TTS-12Hz-1.7B-CustomVoice" in text
    assert "download_model.sh" in text
    assert "operator-provisioned" in text
    assert "same-line Mandarin" in text
    assert "runtime support is not Mandarin quality proof" in text
