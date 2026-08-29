from pathlib import Path

from hottop.model_hub import load_model_hub, select_models

ROOT = Path(__file__).resolve().parents[1]


def test_longcat_avatar_15_is_unprobed_benchmark_only_and_never_default_selected() -> None:
    hub = load_model_hub(ROOT / "integrations/model-hub.yml")
    candidate = next(entry for entry in hub.models if entry.id == "longcat-video-avatar-15")

    assert candidate.repository == "https://github.com/meituan-longcat/LongCat-Video"
    assert candidate.code_license == "MIT"
    assert candidate.weights_license == "MIT-official-model-card"
    assert candidate.cost_class == "self_owned_compute"
    assert candidate.status == "benchmark_candidate"
    assert candidate.integration_ready is False
    assert candidate.runtime_status == "unprobed"
    assert "dgx-spark-dual" in candidate.operator_profiles
    assert "audio_image_to_video" in candidate.capabilities
    assert "video_continuation" in candidate.capabilities
    assert "identity_conditioned_motion" in candidate.capabilities
    assert "multi_character_audio" in candidate.capabilities

    boundary = candidate.runtime_boundary.lower()
    assert "6b3f4b8582a8bc3f20f795735f5383716c4ba794" in boundary
    assert "hugging face" in boundary and "download" in boundary
    assert "2-process" in boundary

    integration_ready = select_models(
        hub,
        capability="audio_image_to_video",
        operator_profile="dgx-spark-dual",
        integration_ready_only=True,
    )
    runtime_ready = select_models(
        hub,
        capability="audio_image_to_video",
        operator_profile="dgx-spark-dual",
        integration_ready_only=False,
        runtime_ready_only=True,
    )
    assert candidate not in integration_ready
    assert candidate not in runtime_ready
