import json
from pathlib import Path

import yaml
from typer.testing import CliRunner

from hottop.model_hub import load_model_hub, select_models
from hottop.model_hub_cli import app

ROOT = Path(__file__).resolve().parents[1]
RUNNER = CliRunner()


def test_dual_dgx_operator_profile_preserves_known_hardware_and_probe_unknowns() -> None:
    profile = yaml.safe_load(
        (ROOT / "config/operator/dgx-spark-dual.yml").read_text(encoding="utf-8")
    )

    assert profile["schema_version"] == "hottop.operator-profile.v1"
    assert profile["operator_pool"]["node_count"] == 2
    assert profile["operator_pool"]["per_node"]["accelerator"] == "NVIDIA GB10 Blackwell"
    assert profile["operator_pool"]["per_node"]["unified_memory_gb"] == 128
    assert profile["operator_pool"]["aggregate_physical_memory_gb"] == 256
    assert profile["operator_pool"]["shared_address_space_across_nodes"] is False
    assert profile["runtime_probe"]["driver_version"] is None
    assert profile["runtime_probe"]["cuda_version"] is None
    assert profile["runtime_probe"]["probe_required"] is True
    assert profile["policy"]["paid_fallback"] is False
    assert profile["policy"]["auto_download_models"] is False


def test_model_hub_covers_generation_continuity_post_and_audio() -> None:
    hub = load_model_hub(ROOT / "integrations/model-hub.yml")
    ids = {entry.id for entry in hub.models}

    required = {
        "lightx2v-wan22-i2v-a14b",
        "lightx2v-wan22-nvfp4-sparse",
        "wan22-ti2v-5b",
        "wan22-animate-14b",
        "qwen-image-2",
        "real-esrgan",
        "rife",
        "qwen3-tts-customvoice-1b7",
        "comfyui-interop",
    }
    assert required <= ids

    capabilities = {capability for entry in hub.models for capability in entry.capabilities}
    assert {
        "text_to_image",
        "image_to_video",
        "text_to_video",
        "character_animation",
        "image_restoration",
        "frame_interpolation",
        "mandarin_tts",
    } <= capabilities


def test_stand_in_wan22_is_registered_only_as_unprobed_identity_benchmark_candidate() -> None:
    hub = load_model_hub(ROOT / "integrations/model-hub.yml")
    candidate = next(entry for entry in hub.models if entry.id == "stand-in-wan22-a14b")

    assert candidate.repository == "https://github.com/WeChatCV/Stand-In"
    assert candidate.code_license == "Apache-2.0"
    assert candidate.cost_class == "self_owned_compute"
    assert candidate.status == "benchmark_candidate"
    assert candidate.integration_ready is False
    assert candidate.runtime_status == "unprobed"
    assert "dgx-spark-dual" in candidate.operator_profiles
    assert "identity_conditioned_motion" in candidate.capabilities
    assert "reference_conditioning" in candidate.capabilities
    assert "automatic download" in candidate.runtime_boundary.lower()


def test_dgx_cinematic_i2v_selection_prefers_integrated_zero_cost_real_motion() -> None:
    hub = load_model_hub(ROOT / "integrations/model-hub.yml")

    selected = select_models(
        hub,
        capability="image_to_video",
        operator_profile="dgx-spark-dual",
        zero_cost_only=True,
        integration_ready_only=True,
    )

    ids = [entry.id for entry in selected]
    assert "lightx2v-wan22-i2v-a14b" in ids
    assert all(entry.cost_class == "self_owned_compute" for entry in selected)
    assert all(entry.integration_ready for entry in selected)
    assert all(entry.status not in {"license_blocked", "paid_optional"} for entry in selected)


def test_registry_never_claims_unprobed_dgx_runtime_is_ready() -> None:
    hub = load_model_hub(ROOT / "integrations/model-hub.yml")
    local_entries = [entry for entry in hub.models if "dgx-spark-dual" in entry.operator_profiles]

    assert local_entries
    assert all(entry.runtime_status in {"unprobed", "not_provisioned", "blocked"} for entry in local_entries)
    assert not any(entry.runtime_status == "operator_provisioned" for entry in local_entries)


def test_one_stop_cli_lists_integrations_but_runtime_ready_filter_fails_closed() -> None:
    default = RUNNER.invoke(
        app,
        ["list", "--hub", str(ROOT / "integrations/model-hub.yml"), "--capability", "image_to_video"],
    )
    assert default.exit_code == 0, default.stdout
    default_payload = json.loads(default.stdout)
    assert default_payload
    assert all(item["integration_ready"] for item in default_payload)
    assert all(item["runtime_status"] != "operator_provisioned" for item in default_payload)
    assert all(item["cost_class"] != "paid_service" for item in default_payload)

    runtime_ready = RUNNER.invoke(
        app,
        [
            "list",
            "--hub",
            str(ROOT / "integrations/model-hub.yml"),
            "--capability",
            "image_to_video",
            "--runtime-ready-only",
        ],
    )
    assert runtime_ready.exit_code == 0, runtime_ready.stdout
    assert json.loads(runtime_ready.stdout) == []


def test_post_processing_cannot_masquerade_as_a_cinematic_generator() -> None:
    hub = load_model_hub(ROOT / "integrations/model-hub.yml")

    generators = select_models(
        hub,
        capability="cinematic_real_motion",
        operator_profile="dgx-spark-dual",
        zero_cost_only=True,
        integration_ready_only=True,
    )
    ids = {entry.id for entry in generators}

    assert "real-esrgan" not in ids
    assert "rife" not in ids
    assert ids


def test_paid_and_license_blocked_models_are_never_default_selected() -> None:
    hub = load_model_hub(ROOT / "integrations/model-hub.yml")

    selected = select_models(
        hub,
        operator_profile="dgx-spark-dual",
        zero_cost_only=True,
        integration_ready_only=True,
    )

    assert all(entry.cost_class != "paid_service" for entry in selected)
    assert all(entry.status not in {"license_blocked", "paid_optional"} for entry in selected)
