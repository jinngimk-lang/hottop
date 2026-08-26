from pathlib import Path

import yaml

from hottop.model_hub import load_model_hub, select_models


ROOT = Path(__file__).resolve().parents[1]


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


def test_dgx_cinematic_i2v_selection_prefers_local_zero_cost_real_motion() -> None:
    hub = load_model_hub(ROOT / "integrations/model-hub.yml")

    selected = select_models(
        hub,
        capability="image_to_video",
        operator_profile="dgx-spark-dual",
        zero_cost_only=True,
        executable_only=True,
    )

    ids = [entry.id for entry in selected]
    assert "lightx2v-wan22-i2v-a14b" in ids
    assert all(entry.cost_class == "self_owned_compute" for entry in selected)
    assert all(entry.status not in {"license_blocked", "paid_optional"} for entry in selected)


def test_post_processing_cannot_masquerade_as_a_cinematic_generator() -> None:
    hub = load_model_hub(ROOT / "integrations/model-hub.yml")

    generators = select_models(
        hub,
        capability="cinematic_real_motion",
        operator_profile="dgx-spark-dual",
        zero_cost_only=True,
        executable_only=True,
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
        executable_only=True,
    )

    assert all(entry.cost_class != "paid_service" for entry in selected)
    assert all(entry.status not in {"license_blocked", "paid_optional"} for entry in selected)
