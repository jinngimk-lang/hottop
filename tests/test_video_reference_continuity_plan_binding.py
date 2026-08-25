import hashlib

import pytest

from hottop.video_artifacts import VideoArtifactManifest, VideoShotArtifact
from hottop.video_benchmark import (
    ReferenceContinuityBenchmark,
    SubjectContinuityEvidence,
    verify_reference_continuity_artifacts,
)
from hottop.video_production import VideoProductionPlan, VideoShot
from hottop.video_reference import VideoReference


def test_continuity_reference_bytes_must_match_plan_reference(tmp_path):
    plan_reference = tmp_path / "plan-reference.ppm"
    substituted_reference = tmp_path / "substituted-reference.ppm"
    shot_path = tmp_path / "shot-001.mp4"
    plan_reference.write_bytes(b"actual-production-reference")
    substituted_reference.write_bytes(b"different-reference-used-only-for-scoring")
    shot_path.write_bytes(b"generated-shot")

    shot_sha = hashlib.sha256(shot_path.read_bytes()).hexdigest()
    substituted_sha = hashlib.sha256(substituted_reference.read_bytes()).hexdigest()
    manifest = VideoArtifactManifest(
        planned_generation_backend="lightx2v-operator",
        shots=[
            VideoShotArtifact(
                shot_index=1,
                path=str(shot_path),
                artifact_kind="ai-generated",
                backend="lightx2v-operator",
                sha256=shot_sha,
                size_bytes=shot_path.stat().st_size,
            )
        ],
    )
    plan = VideoProductionPlan(
        config_name="reference-profile",
        topic_id="topic",
        topic_title="topic",
        subject_name="product",
        style_profile="cinematic",
        generation_backend="lightx2v-operator",
        compositor_backend="moviepy",
        encoder_backend="ffmpeg",
        width=720,
        height=1280,
        fps=24,
        duration_seconds=2.0,
        output_format="mp4",
        in_asset_cta_policy="none",
        shots=[
            VideoShot(
                index=1,
                start_seconds=0,
                end_seconds=2,
                duration_seconds=2,
                scene="hero scene",
                intent="preserve hero",
                continuity_instruction="preserve hero",
                generation_prompt="hero",
                negative_prompt="identity drift",
                reference=VideoReference(
                    image_path=str(plan_reference),
                    rights="generated-original",
                    subject_id="hero",
                ),
            )
        ],
    )
    evidence = ReferenceContinuityBenchmark(
        candidate_id="lightx2v-wan22-i2v",
        candidate_revision="revision",
        render_source="examples/video/reference.render.json",
        config_name="reference-profile",
        evaluator_id="visual-evaluator",
        evaluator_revision="v1",
        subjects=[
            SubjectContinuityEvidence(
                subject_id="hero",
                reference_sha256=substituted_sha,
                shot_sha256s=[shot_sha],
                reference_adherence=0.9,
                cross_shot_identity=0.9,
            )
        ],
    )

    with pytest.raises(ValueError, match="reference.*plan|plan.*reference"):
        verify_reference_continuity_artifacts(
            evidence,
            manifest,
            {"hero": substituted_reference},
            plan=plan,
        )
