from pathlib import Path

from hottop.model_hub import load_model_hub, select_models

ROOT = Path(__file__).resolve().parents[1]


def test_wan_animate_2_is_registered_only_as_unprobed_identity_motion_benchmark() -> None:
    hub = load_model_hub(ROOT / "integrations/model-hub.yml")
    candidate = next(entry for entry in hub.models if entry.id == "wan-animate-2")

    assert candidate.repository == "https://github.com/Wan-Video/Wan-Animate-2"
    assert candidate.code_license == "Apache-2.0"
    assert candidate.cost_class == "self_owned_compute"
    assert candidate.status == "benchmark_candidate"
    assert candidate.integration_ready is False
    assert candidate.runtime_status == "unprobed"
    assert "dgx-spark-dual" in candidate.operator_profiles
    assert "reference_conditioning" in candidate.capabilities
    assert "identity_conditioned_motion" in candidate.capabilities
    assert "motion_conditioning" in candidate.capabilities
    assert "performance_transfer" in candidate.capabilities

    boundary = candidate.runtime_boundary.lower()
    assert "8" in boundary and "a800" in boundary
    assert "480p" in boundary and "2" in boundary
    assert "auto-download" in boundary
    assert "rights-safe" in boundary

    integration_ready = select_models(
        hub,
        capability="performance_transfer",
        operator_profile="dgx-spark-dual",
        integration_ready_only=True,
    )
    runtime_ready = select_models(
        hub,
        capability="performance_transfer",
        operator_profile="dgx-spark-dual",
        integration_ready_only=False,
        runtime_ready_only=True,
    )
    assert candidate not in integration_ready
    assert candidate not in runtime_ready
