from pathlib import Path

import yaml


def _registry() -> dict:
    path = Path("integrations/video-candidates.yml")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_video_candidate_registry_is_zero_cost_and_license_explicit():
    registry = _registry()
    policy = registry["policy"]

    assert policy["zero_cost_default"] is True
    assert policy["auto_download_models"] is False
    assert policy["auto_accept_licenses"] is False
    assert policy["paid_fallback"] is False

    for candidate in registry["candidates"].values():
        assert candidate["code_license"]
        assert candidate["weights_license"]
        assert candidate["status"]
        assert candidate["integration_strategy"]
        assert candidate["runtime_boundary"]


def test_reviewed_character_candidates_keep_execution_gates():
    candidates = _registry()["candidates"]

    longcat = candidates["longcat_video_avatar_1_5"]
    assert longcat["code_license"] == "MIT"
    assert longcat["weights_license"] == "MIT"
    assert longcat["status"] == "high_priority_benchmark"
    assert "audio_driven_character_animation" in longcat["target_gaps"]
    assert "animal_character_support" in longcat["capabilities"]

    scail = candidates["scail_2"]
    assert scail["status"] == "high_priority_benchmark"
    assert "multi_reference_identity" in scail["target_gaps"]

    h3 = candidates["minimax_h3"]
    assert h3["code_license"] == "Apache-2.0-repository"
    assert h3["weights_license"] == "MiniMax-H3-Community-License"
    assert h3["status"] == "blocked_by_weights_license_review"


def test_qwen3_customvoice_is_normal_dialogue_benchmark_and_base_stays_rights_gated():
    candidates = _registry()["candidates"]
    custom = candidates["qwen3_tts_0_6b_customvoice"]

    assert custom["code_license"] == "Apache-2.0"
    assert custom["weights_license"] == "Apache-2.0"
    assert custom["status"] == "benchmark_ready_operator_local"
    assert "natural_mandarin_dialogue" in custom["target_gaps"]
    assert "nine_preset_timbres" in custom["capabilities"]
    assert "style_control_without_voice_cloning" in custom["target_gaps"]
    custom_boundary = custom["runtime_boundary"].lower()
    assert "already provisioned local model directory" in custom_boundary
    assert "never downloads" in custom_boundary
    assert "espeak" in custom_boundary

    base = candidates["qwen3_tts_0_6b_base"]
    assert base["code_license"] == "Apache-2.0"
    assert base["weights_license"] == "Apache-2.0"
    assert base["status"] == "rights_gated_voice_clone_benchmark"
    assert "voice_clone_capability" in base["capabilities"]
    base_boundary = base["runtime_boundary"].lower()
    assert "reference voice audio" in base_boundary
    assert "rights provenance" in base_boundary
    assert "must not silently download" in base_boundary


def test_wangp_remains_interop_only():
    wangp = _registry()["candidates"]["wangp"]

    assert wangp["integration_strategy"] == "interoperate_do_not_vendor"
    assert wangp["weights_license"] == "model_specific"
