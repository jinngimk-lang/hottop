import pytest
from pydantic import ValidationError

from hottop.video_execution import VideoShotArtifact


def test_deterministic_fallback_artifact_is_explicitly_non_generative():
    artifact = VideoShotArtifact(
        shot_index=1,
        path="/tmp/shots/shot-001.mp4",
        artifact_kind="deterministic-non-generative",
        backend="deterministic-cpu",
        degraded_from="zero-cost-router",
        degradation_reason="zero_cost_routes_exhausted",
    )

    assert artifact.artifact_kind == "deterministic-non-generative"
    assert artifact.degraded_from == "zero-cost-router"
    assert artifact.degradation_reason == "zero_cost_routes_exhausted"


def test_deterministic_fallback_cannot_hide_its_degradation_provenance():
    with pytest.raises(ValidationError, match="deterministic fallback artifacts require degraded_from"):
        VideoShotArtifact(
            shot_index=1,
            path="/tmp/shots/shot-001.mp4",
            artifact_kind="deterministic-non-generative",
            backend="deterministic-cpu",
            degradation_reason="zero_cost_routes_exhausted",
        )

    with pytest.raises(ValidationError, match="deterministic fallback artifacts require degradation_reason"):
        VideoShotArtifact(
            shot_index=1,
            path="/tmp/shots/shot-001.mp4",
            artifact_kind="deterministic-non-generative",
            backend="deterministic-cpu",
            degraded_from="zero-cost-router",
        )


def test_ai_generated_artifact_cannot_claim_deterministic_degradation_metadata():
    with pytest.raises(ValidationError, match="AI-generated artifacts cannot carry deterministic degradation metadata"):
        VideoShotArtifact(
            shot_index=1,
            path="/tmp/shots/shot-001.mp4",
            artifact_kind="ai-generated",
            backend="zero-cost-router",
            degraded_from="zero-cost-router",
            degradation_reason="zero_cost_routes_exhausted",
        )
