import hashlib
import importlib


def test_reference_continuity_gate_requires_byte_bound_visual_evidence():
    benchmark = importlib.import_module("hottop.video_benchmark")

    evidence = benchmark.ReferenceContinuityBenchmark(
        candidate_id="lightx2v-wan22-i2v",
        candidate_revision="ModelTC/LightX2V@926299962ed32a142411e45468a289623432b4e4",
        render_source="examples/video/hottop-zero-cost-reference-i2v.render.json",
        config_name="cinematic-lightx2v-wan22-i2v",
        evaluator_id="operator-visual-continuity-review",
        evaluator_revision="v1",
        subjects=[
            benchmark.SubjectContinuityEvidence(
                subject_id="hottop-signal-orb",
                reference_sha256="a" * 64,
                shot_sha256s=["b" * 64, "c" * 64, "d" * 64],
                reference_adherence=0.91,
                cross_shot_identity=0.88,
            )
        ],
    )
    report = benchmark.evaluate_reference_continuity(
        evidence,
        benchmark.ReferenceContinuityPolicy(
            min_reference_adherence=0.8,
            min_cross_shot_identity=0.8,
            min_evaluated_shots=2,
        ),
    )

    assert report.pass_ is True
    assert report.reasons == []
    assert report.subject_reports[0].subject_id == "hottop-signal-orb"
    assert report.subject_reports[0].evaluated_shots == 3


def test_reference_continuity_gate_rejects_identity_drift():
    benchmark = importlib.import_module("hottop.video_benchmark")

    evidence = benchmark.ReferenceContinuityBenchmark(
        candidate_id="candidate",
        candidate_revision="revision",
        render_source="examples/video/reference.render.json",
        config_name="reference-profile",
        evaluator_id="visual-evaluator",
        evaluator_revision="2026-08-25",
        subjects=[
            benchmark.SubjectContinuityEvidence(
                subject_id="hero",
                reference_sha256="1" * 64,
                shot_sha256s=["2" * 64, "3" * 64],
                reference_adherence=0.86,
                cross_shot_identity=0.54,
            )
        ],
    )
    report = benchmark.evaluate_reference_continuity(evidence)

    assert report.pass_ is False
    assert any("cross-shot identity" in reason for reason in report.reasons)


def test_reference_continuity_benchmark_verifies_reference_and_shot_bytes(tmp_path):
    benchmark = importlib.import_module("hottop.video_benchmark")
    artifacts = importlib.import_module("hottop.video_artifacts")

    reference_path = tmp_path / "reference.ppm"
    shot_one = tmp_path / "shot-001.mp4"
    shot_two = tmp_path / "shot-002.mp4"
    reference_path.write_bytes(b"generated-original-reference")
    shot_one.write_bytes(b"generated-shot-one")
    shot_two.write_bytes(b"generated-shot-two")

    reference_sha = hashlib.sha256(reference_path.read_bytes()).hexdigest()
    shot_one_sha = hashlib.sha256(shot_one.read_bytes()).hexdigest()
    shot_two_sha = hashlib.sha256(shot_two.read_bytes()).hexdigest()
    manifest = artifacts.VideoArtifactManifest(
        planned_generation_backend="lightx2v-operator",
        shots=[
            artifacts.VideoShotArtifact(
                shot_index=1,
                path=str(shot_one),
                artifact_kind="ai-generated",
                backend="lightx2v-operator",
                sha256=shot_one_sha,
                size_bytes=shot_one.stat().st_size,
            ),
            artifacts.VideoShotArtifact(
                shot_index=2,
                path=str(shot_two),
                artifact_kind="ai-generated",
                backend="lightx2v-operator",
                sha256=shot_two_sha,
                size_bytes=shot_two.stat().st_size,
            ),
        ],
    )
    evidence = benchmark.ReferenceContinuityBenchmark(
        candidate_id="lightx2v-wan22-i2v",
        candidate_revision="revision",
        render_source="examples/video/reference.render.json",
        config_name="reference-profile",
        evaluator_id="visual-evaluator",
        evaluator_revision="v1",
        subjects=[
            benchmark.SubjectContinuityEvidence(
                subject_id="hero",
                reference_sha256=reference_sha,
                shot_sha256s=[shot_one_sha, shot_two_sha],
                reference_adherence=0.9,
                cross_shot_identity=0.9,
            )
        ],
    )

    benchmark.verify_reference_continuity_artifacts(
        evidence,
        manifest,
        {"hero": reference_path},
    )

    shot_two.write_bytes(b"tampered-shot-two")
    try:
        benchmark.verify_reference_continuity_artifacts(
            evidence,
            manifest,
            {"hero": reference_path},
        )
    except ValueError as exc:
        assert "artifact content mismatch" in str(exc)
    else:
        raise AssertionError("tampered generated shot bytes must fail closed")
