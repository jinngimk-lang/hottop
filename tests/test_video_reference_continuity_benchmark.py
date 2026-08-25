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
