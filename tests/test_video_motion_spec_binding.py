import hashlib

import pytest

from hottop.video_artifacts import VideoArtifactManifest, VideoShotArtifact
from hottop.video_benchmark import (
    ReferenceContinuityBenchmark,
    SubjectContinuityEvidence,
    motion_spec_sha256_for_subject,
    verify_reference_continuity_artifacts,
)
from hottop.video_production import VideoProductionPlan, VideoShot
from hottop.video_reference import VideoReference


def _motion_case(tmp_path, *, motion_spec_sha256=None):
    reference = tmp_path / "hero-reference.ppm"
    shot_path = tmp_path / "shot-001.mp4"
    reference.write_bytes(b"rights-safe-reference")
    shot_path.write_bytes(b"generated-moving-shot")

    reference_sha = hashlib.sha256(reference.read_bytes()).hexdigest()
    shot_sha = hashlib.sha256(shot_path.read_bytes()).hexdigest()
    manifest = VideoArtifactManifest(
        planned_generation_backend="unit-test",
        shots=[
            VideoShotArtifact(
                shot_index=1,
                path=str(shot_path),
                artifact_kind="ai-generated",
                backend="unit-test",
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
        generation_backend="external",
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
                scene="hero crosses the room",
                intent="hero walks from left to right and raises the key",
                continuity_instruction="preserve hero identity while completing the walk",
                generation_prompt="same hero walks left-to-right, then raises the brass key",
                negative_prompt="identity drift, frozen pose, wrong action",
                reference=VideoReference(
                    image_path=str(reference),
                    rights="generated-original",
                    subject_id="hero",
                ),
            )
        ],
    )
    subject = SubjectContinuityEvidence(
        subject_id="hero",
        reference_sha256=reference_sha,
        shot_sha256s=[shot_sha],
        reference_adherence=0.94,
        cross_shot_identity=0.93,
        motion_fidelity=0.91,
        reference_pose_diversity=0.67,
        **({"motion_spec_sha256": motion_spec_sha256} if motion_spec_sha256 is not None else {}),
    )
    evidence = ReferenceContinuityBenchmark(
        candidate_id="candidate",
        candidate_revision="revision",
        render_source="examples/video/reference.render.json",
        config_name="reference-profile",
        evaluator_id="visual-evaluator",
        evaluator_revision="2026-08-28",
        subjects=[subject],
    )
    return evidence, manifest, plan, reference


def test_motion_spec_digest_binds_requested_action_fields_in_plan_order(tmp_path):
    _, _, plan, _ = _motion_case(tmp_path)

    assert motion_spec_sha256_for_subject(plan, "hero") == (
        "d0357d95fff57b84cd1f2b2578dc6c5e6b889b379f1ee6774a9c08bc4d73fa42"
    )


def test_motion_evidence_accepts_digest_for_exact_requested_action(tmp_path):
    evidence, manifest, plan, reference = _motion_case(tmp_path)
    evidence.subjects[0].motion_spec_sha256 = motion_spec_sha256_for_subject(plan, "hero")

    verify_reference_continuity_artifacts(
        evidence,
        manifest,
        {"hero": reference},
        plan=plan,
    )


def test_motion_evidence_requires_requested_action_binding(tmp_path):
    evidence, manifest, plan, reference = _motion_case(tmp_path)

    with pytest.raises(ValueError, match="motion spec"):
        verify_reference_continuity_artifacts(
            evidence,
            manifest,
            {"hero": reference},
            plan=plan,
        )


def test_motion_evidence_rejects_digest_from_different_requested_action(tmp_path):
    evidence, manifest, plan, reference = _motion_case(
        tmp_path,
        motion_spec_sha256="f" * 64,
    )

    with pytest.raises(ValueError, match="motion spec"):
        verify_reference_continuity_artifacts(
            evidence,
            manifest,
            {"hero": reference},
            plan=plan,
        )
