import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from hottop.video_quality import VideoQualityPolicy, inspect_video_quality


def _runner_for_probe(*, duration: str, fps: str):
    frame_size = 96 * 54

    def runner(args, **kwargs):
        if args[0] == "ffprobe":
            return SimpleNamespace(
                returncode=0,
                stdout=json.dumps(
                    {
                        "format": {"duration": duration},
                        "streams": [
                            {
                                "codec_type": "video",
                                "codec_name": "h264",
                                "width": 768,
                                "height": 512,
                                "avg_frame_rate": fps,
                            }
                        ],
                    }
                ),
                stderr="",
            )
        if "-sseof" in args:
            return SimpleNamespace(
                returncode=0,
                stdout=bytes([0] * (768 * 512)),
                stderr=b"",
            )
        return SimpleNamespace(
            returncode=0,
            stdout=(bytes([0] * frame_size) + bytes([10] * frame_size)) * 8,
            stderr=b"",
        )

    return runner


@pytest.mark.parametrize(
    ("duration", "fps", "expected_reason"),
    [
        ("nan", "24/1", "video duration is not finite"),
        ("4.0", "nan/1", "video fps is not finite"),
    ],
)
def test_inspect_video_quality_rejects_nonfinite_probe_metadata(
    tmp_path: Path,
    duration: str,
    fps: str,
    expected_reason: str,
):
    path = tmp_path / "nonfinite.mp4"
    path.write_bytes(b"video")

    report = inspect_video_quality(
        path,
        VideoQualityPolicy(),
        runner=_runner_for_probe(duration=duration, fps=fps),
    )

    assert report.pass_ is False
    assert expected_reason in report.reasons
