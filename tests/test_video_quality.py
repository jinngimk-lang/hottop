import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from hottop.video_quality import (
    VideoQualityError,
    VideoQualityPolicy,
    assert_video_quality,
    evaluate_motion_frames,
    inspect_video_quality,
)


def test_duplicate_frames_fail_motion_gate():
    policy = VideoQualityPolicy(min_motion_delta=2.0, max_duplicate_ratio=0.6)

    report = evaluate_motion_frames([bytes([10] * 16), bytes([10] * 16)], policy)

    assert report.pass_ is False
    assert report.duplicate_ratio == 1.0
    assert any("motion" in reason or "duplicate" in reason for reason in report.reasons)


def test_changing_frames_pass_motion_gate():
    policy = VideoQualityPolicy(min_motion_delta=2.0, max_duplicate_ratio=0.6)

    report = evaluate_motion_frames(
        [bytes([0] * 16), bytes([8] * 16), bytes([20] * 16)],
        policy,
    )

    assert report.pass_ is True
    assert report.mean_motion_delta >= 2.0
    assert report.duplicate_ratio == 0.0


def test_inspect_video_quality_rejects_missing_video_stream(tmp_path: Path):
    path = tmp_path / "bad.mp4"
    path.write_bytes(b"not-empty")

    def runner(args, **kwargs):
        assert args[0] == "ffprobe"
        return SimpleNamespace(
            returncode=0,
            stdout=json.dumps({"format": {"duration": "2.0"}, "streams": []}),
            stderr="",
        )

    report = inspect_video_quality(path, VideoQualityPolicy(), runner=runner)

    assert report.pass_ is False
    assert "video stream missing" in report.reasons


def test_inspect_video_quality_rejects_media_below_output_floor(tmp_path: Path):
    path = tmp_path / "tiny.mp4"
    path.write_bytes(b"video")

    def runner(args, **kwargs):
        if args[0] == "ffprobe":
            return SimpleNamespace(
                returncode=0,
                stdout=json.dumps(
                    {
                        "format": {"duration": "0.2"},
                        "streams": [
                            {
                                "codec_type": "video",
                                "codec_name": "h264",
                                "width": 96,
                                "height": 64,
                                "avg_frame_rate": "4/1",
                            }
                        ],
                    }
                ),
                stderr="",
            )
        if "-sseof" in args:
            return SimpleNamespace(returncode=0, stdout=b"frame", stderr=b"")
        return SimpleNamespace(
            returncode=0,
            stdout=bytes([0] * (96 * 54)) + bytes([10] * (96 * 54)),
            stderr=b"",
        )

    report = inspect_video_quality(path, VideoQualityPolicy(), runner=runner)

    assert report.pass_ is False
    assert any("duration" in reason for reason in report.reasons)
    assert any("width" in reason for reason in report.reasons)
    assert any("height" in reason for reason in report.reasons)
    assert any("fps" in reason.lower() for reason in report.reasons)


def test_inspect_video_quality_reports_terminal_decode_failure(tmp_path: Path):
    path = tmp_path / "shot.mp4"
    path.write_bytes(b"video")
    calls = 0

    def runner(args, **kwargs):
        nonlocal calls
        calls += 1
        if args[0] == "ffprobe":
            return SimpleNamespace(
                returncode=0,
                stdout=json.dumps(
                    {
                        "format": {"duration": "2.0"},
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
            return SimpleNamespace(returncode=1, stdout=b"", stderr=b"decode failed")
        return SimpleNamespace(
            returncode=0,
            stdout=bytes([0] * (96 * 54)) + bytes([10] * (96 * 54)),
            stderr=b"",
        )

    report = inspect_video_quality(path, VideoQualityPolicy(), runner=runner)

    assert calls == 3
    assert report.terminal_frame_decodable is False
    assert "terminal frame not decodable" in report.reasons
    with pytest.raises(VideoQualityError):
        assert_video_quality(report)


def test_inspect_video_quality_requires_terminal_frame_bytes(tmp_path: Path):
    path = tmp_path / "truncated-tail.mp4"
    path.write_bytes(b"video")

    def runner(args, **kwargs):
        if args[0] == "ffprobe":
            return SimpleNamespace(
                returncode=0,
                stdout=json.dumps(
                    {
                        "format": {"duration": "2.0"},
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
            return SimpleNamespace(returncode=0, stdout=b"", stderr=b"")
        return SimpleNamespace(
            returncode=0,
            stdout=bytes([0] * (96 * 54)) + bytes([10] * (96 * 54)),
            stderr=b"",
        )

    report = inspect_video_quality(path, VideoQualityPolicy(), runner=runner)

    assert report.pass_ is False
    assert report.terminal_frame_decodable is False
    assert "terminal frame not decodable" in report.reasons
