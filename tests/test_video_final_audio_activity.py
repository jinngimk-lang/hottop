from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

from hottop.video_final_output import inspect_final_video_output
from hottop.video_production import FFmpegConfig


def _ffmpeg_config() -> FFmpegConfig:
    return FFmpegConfig(
        video_codec="libx264",
        audio_codec="aac",
        pixel_format="yuv420p",
        movflags="+faststart",
    )


def _ffprobe_success(*, audio_duration: float = 12.0) -> SimpleNamespace:
    return SimpleNamespace(
        returncode=0,
        stdout=json.dumps(
            {
                "format": {"duration": "12.0"},
                "streams": [
                    {
                        "codec_type": "video",
                        "codec_name": "h264",
                        "pix_fmt": "yuv420p",
                        "duration": "12.0",
                    },
                    {
                        "codec_type": "audio",
                        "codec_name": "aac",
                        "duration": str(audio_duration),
                    },
                ],
            }
        ),
        stderr="",
    )


def test_final_output_rejects_aac_stream_that_is_actually_silent(tmp_path: Path) -> None:
    output = tmp_path / "silent.mp4"
    output.write_bytes(b"media-bytes")
    calls: list[list[str]] = []

    def fake_runner(command, **_kwargs):
        calls.append(list(command))
        if command[0] == "ffprobe":
            return _ffprobe_success()
        assert command[0] == "ffmpeg"
        return SimpleNamespace(
            returncode=0,
            stdout="",
            stderr="[Parsed_volumedetect_0] mean_volume: -inf dB\n"
            "[Parsed_volumedetect_0] max_volume: -inf dB\n",
        )

    report = inspect_final_video_output(output, _ffmpeg_config(), runner=fake_runner)

    assert report.pass_ is False
    assert "audio is silent" in report.reasons
    assert any(command[0] == "ffmpeg" and "volumedetect" in command for command in calls)


def test_final_output_accepts_conservatively_audible_track(tmp_path: Path) -> None:
    output = tmp_path / "audible.mp4"
    output.write_bytes(b"media-bytes")

    def fake_runner(command, **_kwargs):
        if command[0] == "ffprobe":
            return _ffprobe_success()
        return SimpleNamespace(
            returncode=0,
            stdout="",
            stderr="[Parsed_volumedetect_0] mean_volume: -32.0 dB\n"
            "[Parsed_volumedetect_0] max_volume: -18.0 dB\n",
        )

    report = inspect_final_video_output(output, _ffmpeg_config(), runner=fake_runner)

    assert report.pass_ is True
    assert report.audio_max_volume_db == -18.0


def test_final_output_rejects_short_audible_track_that_does_not_cover_video(
    tmp_path: Path,
) -> None:
    output = tmp_path / "short-audio.mp4"
    output.write_bytes(b"media-bytes")

    def fake_runner(command, **_kwargs):
        if command[0] == "ffprobe":
            return _ffprobe_success(audio_duration=0.25)
        return SimpleNamespace(
            returncode=0,
            stdout="",
            stderr="[Parsed_volumedetect_0] mean_volume: -18.0 dB\n"
            "[Parsed_volumedetect_0] max_volume: -3.0 dB\n",
        )

    report = inspect_final_video_output(output, _ffmpeg_config(), runner=fake_runner)

    assert report.pass_ is False
    assert "audio duration does not cover final video" in report.reasons
