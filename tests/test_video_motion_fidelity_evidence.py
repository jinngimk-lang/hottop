import importlib


def test_reference_continuity_gate_rejects_identity_preserving_frozen_motion():
    benchmark = importlib.import_module("hottop.video_benchmark")

    evidence = benchmark.ReferenceContinuityBenchmark(
        candidate_id="candidate",
        candidate_revision="revision",
        render_source="examples/video/reference.render.json",
        config_name="reference-profile",
        evaluator_id="visual-evaluator",
        evaluator_revision="2026-08-28",
        subjects=[
            benchmark.SubjectContinuityEvidence(
                subject_id="hero",
                reference_sha256="1" * 64,
                shot_sha256s=["2" * 64, "3" * 64],
                reference_adherence=0.94,
                cross_shot_identity=0.93,
                motion_fidelity=0.22,
                reference_pose_diversity=0.08,
            )
        ],
    )

    report = benchmark.evaluate_reference_continuity(
        evidence,
        benchmark.ReferenceContinuityPolicy(
            require_motion_fidelity=True,
            min_motion_fidelity=0.65,
            min_reference_pose_diversity=0.20,
        ),
    )

    assert report.pass_ is False
    assert any("motion fidelity" in reason for reason in report.reasons)
    assert any("reference-pose diversity" in reason for reason in report.reasons)


def test_motion_claim_fails_closed_when_motion_evidence_is_missing():
    benchmark = importlib.import_module("hottop.video_benchmark")

    evidence = benchmark.ReferenceContinuityBenchmark(
        candidate_id="candidate",
        candidate_revision="revision",
        render_source="examples/video/reference.render.json",
        config_name="reference-profile",
        evaluator_id="visual-evaluator",
        evaluator_revision="2026-08-28",
        subjects=[
            benchmark.SubjectContinuityEvidence(
                subject_id="hero",
                reference_sha256="1" * 64,
                shot_sha256s=["2" * 64, "3" * 64],
                reference_adherence=0.94,
                cross_shot_identity=0.93,
            )
        ],
    )

    report = benchmark.evaluate_reference_continuity(
        evidence,
        benchmark.ReferenceContinuityPolicy(require_motion_fidelity=True),
    )

    assert report.pass_ is False
    assert any("motion evidence missing" in reason for reason in report.reasons)
