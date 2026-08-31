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


def test_continuity_benchmark_rejects_reassociated_generation_config_provenance(
    tmp_path: Path,
) -> None:
    reference_path = tmp_path / "reference.ppm"
    reference_path.write_bytes(b"generated-original-reference")
    shots = [tmp_path / "shot-001.mp4", tmp_path / "shot-002.mp4"]
    for index, shot in enumerate(shots, start=1):
        shot.write_bytes(f"generated-shot-{index}".encode())

    reference_sha = hashlib.sha256(reference_path.read_bytes()).hexdigest()
    shot_hashes = [hashlib.sha256(path.read_bytes()).hexdigest() for path in shots]
    manifest_config = b"actual-generation-config"
    evidence_config = b"different-generation-config"
    manifest = VideoArtifactManifest(
        planned_generation_backend="lightx2v-operator",
        shots=[
            VideoShotArtifact(
                shot_index=index,
                path=str(path),
                artifact_kind="ai-generated",
                backend="lightx2v:wan2.2_moe",
                candidate_id="lightx2v-wan22-i2v",
                candidate_revision="926299962ed32a142411e45468a289623432b4e4",
                sha256=shot_hashes[index - 1],
                size_bytes=path.stat().st_size,
                generation_config_sha256=hashlib.sha256(manifest_config).hexdigest(),
                generation_config_size_bytes=len(manifest_config),
            )
            for index, path in enumerate(shots, start=1)
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
                index=index,
                start_seconds=float((index - 1) * 2),
                end_seconds=float(index * 2),
                duration_seconds=2.0,
                scene=f"hero scene {index}",
                intent="show hero",
                continuity_instruction="preserve hero",
                generation_prompt="hero",
                negative_prompt="identity drift",
                reference=VideoReference(
                    image_path=str(reference_path),
                    rights="generated-original",
                    subject_id="hero",
                ),
            )
            for index in (1, 2)
        ],
    )
    evidence = ReferenceContinuityBenchmark(
        candidate_id="lightx2v-wan22-i2v",
        candidate_revision="926299962ed32a142411e45468a289623432b4e4",
        render_source="examples/video/reference.render.json",
        config_name="cinematic-lightx2v-wan22-i2v",
        generation_config_sha256=hashlib.sha256(evidence_config).hexdigest(),
        generation_config_size_bytes=len(evidence_config),
        evaluator_id="visual-evaluator",
        evaluator_revision="v1",
        subjects=[
            SubjectContinuityEvidence(
                subject_id="hero",
                reference_sha256=reference_sha,
                shot_sha256s=shot_hashes,
                reference_adherence=0.9,
                cross_shot_identity=0.9,
            )
        ],
    )

    with pytest.raises(ValueError, match="generation config provenance"):
        verify_reference_continuity_artifacts(
            evidence,
            manifest,
            {"hero": reference_path},
            plan=plan,
        )
