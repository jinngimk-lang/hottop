from pathlib import Path

from hottop.model_hub import load_model_hub, select_models

ROOT = Path(__file__).resolve().parents[1]


def test_qwentts_cpp_1b7_is_local_benchmark_only_and_never_auto_provisioned() -> None:
    hub = load_model_hub(ROOT / "integrations/model-hub.yml")
    candidate = next(entry for entry in hub.models if entry.id == "qwen3-tts-qwentts-cpp-1b7")

    assert candidate.repository == "https://github.com/ServeurpersoCom/qwentts.cpp"
    assert candidate.code_license == "MIT"
    assert candidate.cost_class == "self_owned_compute"
    assert candidate.status == "benchmark_candidate"
    assert candidate.integration_ready is False
    assert candidate.runtime_status == "unprobed"
    assert "mandarin_tts" in candidate.capabilities
    assert "role_aware_tts" in candidate.capabilities
    assert "cpu_inference" in candidate.capabilities
    assert "cuda_inference" in candidate.capabilities
    assert "vulkan_inference" in candidate.capabilities

    boundary = candidate.runtime_boundary.lower()
    assert "a8a7716b530e49fed537c57711247c12fbbb903c" in boundary
    assert "1.7b" in boundary
    assert "gguf" in boundary
    assert "auto-download" in boundary or "download" in boundary
    assert "customvoice" in boundary

    integration_ready = select_models(
        hub,
        capability="mandarin_tts",
        integration_ready_only=True,
    )
    runtime_ready = select_models(
        hub,
        capability="mandarin_tts",
        integration_ready_only=False,
        runtime_ready_only=True,
    )
    assert candidate not in integration_ready
    assert candidate not in runtime_ready
