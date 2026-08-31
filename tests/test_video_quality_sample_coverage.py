import json
from pathlib import Path
from types import SimpleNamespace

from hottop.video_quality import VideoQualityPolicy, inspect_video_quality


def test_inspect_video_quality_rejects_frame_aligned_but_truncated_motion_sampling(
    tmp_path: Path,
):
    path = tmp_path / "truncated-motion-sample.mp4"
    path.write_bytes(b"video")
    frame_size = 96 * 54

    def runner(args, **kwargs):
        if args[0] == "ffprobe":
            return SimpleNamespace(
                returncode=0,
                stdout=json.dumps(
                    {
                        "format": {"duration": "4.0"},
                        "streams": [
                            {
                                "codec_type": "video",
                                "codec_name": "h264",
                                "width": 768,
                                "height": 512,
                                "avg_frame_rate": "24/1",
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
            stdout=bytes([0] * frame_size) + bytes([10] * frame_size),
            stderr=b"",
        )

    report = inspect_video_quality(path, VideoQualityPolicy(), runner=runner)

    assert report.pass_ is False
    assert report.frame_count == 2
    assert "motion sample coverage incomplete" in report.reasons
