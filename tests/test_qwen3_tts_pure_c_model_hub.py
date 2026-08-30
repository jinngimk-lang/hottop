from pathlib import Path

from hottop.model_hub import load_model_hub, select_models

ROOT = Path(__file__).resolve().parents[1]


def test_pure_c_qwen3_tts_is_discoverable_only_as_unprobed_1b7_benchmark_candidate() -> None:
    hub = load_model_hub(ROOT / "integrations/model-hub.yml")
    candidate = next(entry for entry in hub.models if entry.id == "qwen3-tts-pure-c-1b7")

    assert candidate.repository == "https://github.com/gabriele-mastrapasqua/qwen3-tts"
    assert candidate.code_license == "MIT"
    assert candidate.cost_class == "self_owned_compute"
    assert candidate.status == "benchmark_candidate"
    assert candidate.integration_ready is False
    assert candidate.runtime_status == "unprobed"
    assert "mandarin_tts" in candidate.capabilities
    assert "role_aware_tts" in candidate.capabilities
    assert "delivery_instruction" in candidate.capabilities
    assert "cpu_inference" in candidate.capabilities
    assert "cuda_inference" in candidate.capabilities
    assert "metal_inference" in candidate.capabilities

    boundary = candidate.runtime_boundary.lower()
    assert "f1b6865713d12a2a2365282fc02e19a5a384a565" in boundary
    assert "download_model.sh" in boundary
    assert "operator-provisioned" in boundary

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
