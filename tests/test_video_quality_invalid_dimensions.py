import json
from pathlib import Path
from types import SimpleNamespace

from hottop.video_quality import VideoQualityPolicy, inspect_video_quality


def test_inspect_video_quality_rejects_noninteger_dimensions_without_crashing(
    tmp_path: Path,
):
    path = tmp_path / "invalid-dimensions.mp4"
    path.write_bytes(b"video")

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
                                "width": "not-a-number",
                                "height": 512,
                                "avg_frame_rate": "24/1",
                            }
                        ],
                    }
                ),
                stderr="",
            )
        raise AssertionError("invalid dimensions must fail before frame decoding")

    report = inspect_video_quality(
        path,
        VideoQualityPolicy(),
        runner=runner,
    )

    assert report.pass_ is False
    assert report.width == 0
    assert report.height == 512
    assert "video dimensions are invalid" in report.reasons
