from __future__ import annotations

import pytest
from pydantic import ValidationError

from hottop.video_benchmark import ReferenceContinuityBenchmark, SubjectContinuityEvidence


def test_reference_continuity_benchmark_requires_unique_subject_ids() -> None:
    subject = SubjectContinuityEvidence(
        subject_id="hero-a",
        reference_sha256="a" * 64,
        shot_sha256s=["b" * 64, "c" * 64],
        reference_adherence=0.9,
        cross_shot_identity=0.9,
    )

    with pytest.raises(ValidationError, match="unique subject ids"):
        ReferenceContinuityBenchmark(
            candidate_id="lightx2v-wan22-i2v",
            candidate_revision="926299962ed32a142411e45468a289623432b4e4",
            render_source="examples/video/reference.render.json",
            config_name="cinematic-lightx2v-wan22-i2v",
            evaluator_id="visual-evaluator",
            evaluator_revision="v1",
            subjects=[subject, subject.model_copy()],
        )
