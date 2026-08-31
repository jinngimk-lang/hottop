from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from hottop.video_artifacts import VideoArtifactManifest, VideoShotArtifact
from hottop.video_benchmark import (
    ReferenceContinuityBenchmark,
    SubjectContinuityEvidence,
    verify_reference_continuity_artifacts,
)
from hottop.video_production import VideoProductionPlan, VideoShot
from hottop.video_reference import VideoReference


def test_continuity_benchmark_rejects_duplicate_reference_bytes_across_subjects(
    tmp_path: Path,
) -> None:
    reference_paths = {
        "hero-a": tmp_path / "hero-a.ppm",
        "hero-b": tmp_path / "hero-b.ppm",
    }
    for path in reference_paths.values():
        path.write_bytes(b"same-reference-bytes-for-two-distinct-subjects")

    shot_paths = [tmp_path / "shot-001.mp4", tmp_path / "shot-002.mp4"]
    shot_paths[0].write_bytes(b"generated-shot-for-hero-a")
    shot_paths[1].write_bytes(b"generated-shot-for-hero-b")
    shot_shas = [hashlib.sha256(path.read_bytes()).hexdigest() for path in shot_paths]

    generation_config = b"actual-generation-config"
    config_sha = hashlib.sha256(generation_config).hexdigest()
    config_size = len(generation_config)
    candidate_revision = "926299962ed32a142411e45468a289623432b4e4"

    manifest = VideoArtifactManifest(
        planned_generation_backend="lightx2v-operator",
        shots=[
            VideoShotArtifact(
                shot_index=index,
                path=str(path),
                artifact_kind="ai-generated",
                backend="lightx2v:wan2.2_moe",
                candidate_id="lightx2v-wan22-i2v",
                candidate_revision=candidate_revision,
                sha256=shot_sha,
                size_bytes=path.stat().st_size,
                generation_config_sha256=config_sha,
                generation_config_size_bytes=config_size,
            )
            for index, (path, shot_sha) in enumerate(
                zip(shot_paths, shot_shas, strict=True),
                start=1,
            )
        ],
    )
    plan = VideoProductionPlan(
        config_name="cinematic-lightx2v-wan22-i2v",
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
        duration_seconds=4.0,
        output_format="mp4",
        in_asset_cta_policy="none",
        shots=[
            VideoShot(
                index=1,
                start_seconds=0.0,
                end_seconds=2.0,
                duration_seconds=2.0,
                scene="hero a scene",
                intent="show hero a action",
                continuity_instruction="preserve hero a identity",
                generation_prompt="hero a performs action",
                negative_prompt="identity drift",
                reference=VideoReference(
                    image_path=str(reference_paths["hero-a"]),
                    rights="generated-original",
                    subject_id="hero-a",
                ),
            ),
            VideoShot(
                index=2,
                start_seconds=2.0,
                end_seconds=4.0,
                duration_seconds=2.0,
                scene="hero b scene",
                intent="show hero b action",
                continuity_instruction="preserve hero b identity",
                generation_prompt="hero b performs action",
                negative_prompt="identity drift",
                reference=VideoReference(
                    image_path=str(reference_paths["hero-b"]),
                    rights="generated-original",
                    subject_id="hero-b",
                ),
            ),
        ],
    )
    reference_sha = hashlib.sha256(
        reference_paths["hero-a"].read_bytes()
    ).hexdigest()
    evidence = ReferenceContinuityBenchmark(
        candidate_id="lightx2v-wan22-i2v",
        candidate_revision=candidate_revision,
        render_source="examples/video/reference.render.json",
        config_name=plan.config_name,
        generation_config_sha256=config_sha,
        generation_config_size_bytes=config_size,
        evaluator_id="visual-evaluator",
        evaluator_revision="v1",
        subjects=[
            SubjectContinuityEvidence(
                subject_id=subject_id,
                reference_sha256=reference_sha,
                shot_sha256s=[shot_sha],
                reference_adherence=0.9,
                cross_shot_identity=0.9,
            )
            for subject_id, shot_sha in zip(
                reference_paths,
                shot_shas,
                strict=True,
            )
        ],
    )

    with pytest.raises(
        ValueError,
        match="distinct subjects require distinct reference artifacts",
    ):
        verify_reference_continuity_artifacts(
            evidence,
            manifest,
            reference_paths,
            plan=plan,
        )
