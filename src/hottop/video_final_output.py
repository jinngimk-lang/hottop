from __future__ import annotations

import json
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from .video_production import FfmpegConfig


class FinalVideoOutputError(RuntimeError):
    """Raised when the finalized delivery artifact violates the media contract."""


class FinalVideoOutputReport(BaseModel):
    pass_: bool
    duration: float = 0
    video_codec: str | None = None
    pixel_format: str | None = None
    audio_codec: str | None = None
    reasons: list[str] = Field(default_factory=list)


def _expected_codec(configured: str) -> str:
    aliases = {
        "libx264": "h264",
        "libx265": "hevc",
        "libvpx-vp9": "vp9",
    }
    return aliases.get(configured, configured)


def inspect_final_video_output(
    path: Path,
    config: FfmpegConfig,
    *,
    runner: Callable[..., Any] = subprocess.run,
) -> FinalVideoOutputReport:
    if not path.is_file() or path.stat().st_size <= 0:
        return FinalVideoOutputReport(pass_=False, reasons=["final output missing or empty"])

    probe = runner(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=codec_type,codec_name,pix_fmt",
            "-of",
            "json",
            str(path),
        ],
        capture_output=True,
        check=False,
        text=True,
    )
    if int(getattr(probe, "returncode", 1)) != 0:
        return FinalVideoOutputReport(pass_=False, reasons=["ffprobe failed"])

    try:
        raw = json.loads(str(getattr(probe, "stdout", "") or "{}"))
    except json.JSONDecodeError:
        return FinalVideoOutputReport(pass_=False, reasons=["ffprobe returned invalid JSON"])

    streams = raw.get("streams") if isinstance(raw, dict) else None
    streams = streams if isinstance(streams, list) else []
    video = next(
        (item for item in streams if isinstance(item, dict) and item.get("codec_type") == "video"),
        None,
    )
    audio = next(
        (item for item in streams if isinstance(item, dict) and item.get("codec_type") == "audio"),
        None,
    )
    try:
        duration = float(raw.get("format", {}).get("duration") or 0)
    except (TypeError, ValueError):
        duration = 0

    video_codec = str(video.get("codec_name")) if video else None
    pixel_format = str(video.get("pix_fmt")) if video else None
    audio_codec = str(audio.get("codec_name")) if audio else None
    reasons: list[str] = []
    if video is None:
        reasons.append("video stream missing")
    if duration <= 0:
        reasons.append("duration is zero")

    expected_video_codec = _expected_codec(config.video_codec)
    if video_codec != expected_video_codec:
        reasons.append(
            f"video codec {video_codec or 'missing'} does not match {expected_video_codec}"
        )
    if pixel_format != config.pixel_format:
        reasons.append(
            f"pixel format {pixel_format or 'missing'} does not match {config.pixel_format}"
        )

    expected_audio_codec = _expected_codec(config.audio_codec)
    if audio_codec != expected_audio_codec:
        reasons.append(
            f"audio codec {audio_codec or 'missing'} does not match {expected_audio_codec}"
        )

    return FinalVideoOutputReport(
        pass_=not reasons,
        duration=duration,
        video_codec=video_codec,
        pixel_format=pixel_format,
        audio_codec=audio_codec,
        reasons=reasons,
    )


def assert_final_video_output(report: FinalVideoOutputReport) -> None:
    if report.pass_:
        return
    reasons = "; ".join(report.reasons) or "final output media contract failed"
    raise FinalVideoOutputError(reasons)
