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


def test_continuity_evidence_must_cover_all_subject_bearing_plan_shots(tmp_path):
    reference_path = tmp_path / "hero.ppm"
    reference_path.write_bytes(b"hero-reference")

    shot_paths = [tmp_path / f"shot-{index:03d}.mp4" for index in (1, 2, 3)]
    for index, shot_path in enumerate(shot_paths, start=1):
        shot_path.write_bytes(f"hero-shot-{index}".encode())

    shot_hashes = [hashlib.sha256(path.read_bytes()).hexdigest() for path in shot_paths]
    reference_sha = hashlib.sha256(reference_path.read_bytes()).hexdigest()

    manifest = VideoArtifactManifest(
        planned_generation_backend="lightx2v-operator",
        shots=[
            VideoShotArtifact(
                shot_index=index,
                path=str(shot_path),
                artifact_kind="ai-generated",
                backend="lightx2v-operator",
                sha256=shot_hashes[index - 1],
                size_bytes=shot_path.stat().st_size,
            )
            for index, shot_path in enumerate(shot_paths, start=1)
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
        duration_seconds=6.0,
        output_format="mp4",
        in_asset_cta_policy="none",
        shots=[
            VideoShot(
                index=index,
                start_seconds=float((index - 1) * 2),
                end_seconds=float(index * 2),
                duration_seconds=2,
                scene=f"hero scene {index}",
                intent="preserve hero",
                continuity_instruction="preserve hero",
                generation_prompt="hero",
                negative_prompt="identity drift",
                reference=VideoReference(
                    image_path=str(reference_path),
                    rights="generated-original",
                    subject_id="hero",
                ),
            )
            for index in (1, 2, 3)
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
                reference_sha256=reference_sha,
                shot_sha256s=shot_hashes[:2],
                reference_adherence=0.95,
                cross_shot_identity=0.95,
            )
        ],
    )

    with pytest.raises(ValueError, match="cover|coverage|all.*shot|missing.*shot"):
        verify_reference_continuity_artifacts(
            evidence,
            manifest,
            {"hero": reference_path},
            plan=plan,
        )
