from pathlib import Path

from hottop.model_hub import load_model_hub, select_models

ROOT = Path(__file__).resolve().parents[1]


def test_audio_cpp_is_discoverable_only_as_unprobed_1b7_benchmark_candidate() -> None:
    hub = load_model_hub(ROOT / "integrations/model-hub.yml")
    candidate = next(entry for entry in hub.models if entry.id == "qwen3-tts-audio-cpp-1b7")

    assert candidate.repository == "https://github.com/0xShug0/audio.cpp"
    assert candidate.code_license == "Apache-2.0"
    assert candidate.cost_class == "self_owned_compute"
    assert candidate.status == "benchmark_candidate"
    assert candidate.integration_ready is False
    assert candidate.runtime_status == "unprobed"
    assert "mandarin_tts" in candidate.capabilities
    assert "cpu_inference" in candidate.capabilities
    assert "cuda_inference" in candidate.capabilities
    assert "hip_inference" in candidate.capabilities
    assert "vulkan_inference" in candidate.capabilities
    assert "metal_inference" in candidate.capabilities

    boundary = candidate.runtime_boundary.lower()
    assert "a76ec04f620da829e4a53032247369083ba1ad45" in boundary
    assert "auto" in boundary and "download" in boundary
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
