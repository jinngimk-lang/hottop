from pathlib import Path

from hottop.model_hub import load_model_hub, select_models

ROOT = Path(__file__).resolve().parents[1]


def test_crispasr_qwen3_tts_is_local_vulkan_benchmark_only() -> None:
    hub = load_model_hub(ROOT / "integrations/model-hub.yml")
    candidate = next(entry for entry in hub.models if entry.id == "qwen3-tts-crispasr-1b7")

    assert candidate.repository == "https://github.com/CrispStrobe/CrispASR"
    assert candidate.code_license == "MIT"
    assert candidate.cost_class == "self_owned_compute"
    assert candidate.status == "benchmark_candidate"
    assert candidate.integration_ready is False
    assert candidate.runtime_status == "unprobed"
    assert "mandarin_tts" in candidate.capabilities
    assert "vulkan_inference" in candidate.capabilities
    assert "cpu_inference" in candidate.capabilities

    boundary = candidate.runtime_boundary.lower()
    assert "bb77301c4dbde1fca217e1a19584b1ae0167ee03" in boundary
    assert "-m auto" in boundary
    assert "must not" in boundary
    assert "1.7b" in boundary

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
