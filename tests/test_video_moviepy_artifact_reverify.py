import hashlib
import json
from pathlib import Path

import pytest

from hottop import video_moviepy
from hottop.video_moviepy import MoviePyTimeline, MoviePyTimelineShot


def test_moviepy_rejects_shot_mutated_after_generation_provenance_check(tmp_path: Path):
    shots_dir = tmp_path / "shots"
    shots_dir.mkdir()
    shot = shots_dir / "shot-001.mp4"
    accepted_bytes = b"accepted-generation-bytes"
    shot.write_bytes(accepted_bytes)
    (shots_dir / "shot-001.artifact.json").write_text(
        json.dumps(
            {
                "schema_version": "hottop.video-artifacts.v1",
                "planned_generation_backend": "zero-cost-router",
                "shots": [
                    {
                        "shot_index": 1,
                        "path": str(shot),
                        "artifact_kind": "ai-generated",
                        "backend": "hf-public",
                        "degraded_from": None,
                        "degradation_reason": None,
                        "sha256": hashlib.sha256(accepted_bytes).hexdigest(),
                        "size_bytes": len(accepted_bytes),
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    timeline = MoviePyTimeline(
        width=720,
        height=1280,
        fps=24,
        duration_seconds=2,
        shots=[
            MoviePyTimelineShot(
                index=1,
                source=str(shot),
                start_seconds=0,
                duration_seconds=2,
            )
        ],
        bgm_description="none",
        generate_synthetic_bgm=False,
        generate_procedural_sfx=False,
    )

    shot.write_bytes(b"mutated-before-composition")

    with pytest.raises(ValueError, match="content mismatch"):
        video_moviepy.verify_moviepy_shot_artifacts(timeline)
