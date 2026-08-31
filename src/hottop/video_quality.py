from __future__ import annotations

import json
import math
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class VideoQualityError(RuntimeError):
    """Raised when a generated video artifact fails deterministic quality checks."""


class VideoQualityPolicy(BaseModel):
    min_motion_delta: float = Field(default=2.0, ge=0)
    max_duplicate_ratio: float = Field(default=0.6, ge=0, le=1)
    duplicate_delta: float = Field(default=1.0, ge=0)
    sample_fps: int = Field(default=4, ge=1, le=12)
    sample_width: int = Field(default=96, ge=32, le=320)
    sample_height: int = Field(default=54, ge=18, le=180)
    min_duration_seconds: float = Field(default=0.5, ge=0)
    min_width: int = Field(default=256, ge=1)
    min_height: int = Field(default=256, ge=1)
    min_fps: float = Field(default=8.0, ge=0)


class VideoQualityReport(BaseModel):
    pass_: bool
    duration: float = 0
    width: int = 0
    height: int = 0
    fps: float = 0
    terminal_frame_decodable: bool = False
    frame_count: int = 0
    mean_motion_delta: float = 0
    duplicate_ratio: float = 1
    reasons: list[str] = Field(default_factory=list)


def _mean_absolute_delta(left: bytes, right: bytes) -> float:
    if not left or len(left) != len(right):
        raise ValueError("motion frames must be non-empty and equal length")
    return sum(abs(a - b) for a, b in zip(left, right, strict=True)) / len(left)


def evaluate_motion_frames(
    frames: list[bytes],
    policy: VideoQualityPolicy,
) -> VideoQualityReport:
    if len(frames) < 2:
        return VideoQualityReport(
            pass_=False,
            frame_count=len(frames),
            reasons=["insufficient motion samples"],
        )

    deltas: list[float] = []
    duplicates = 0
    for previous, current in zip(frames, frames[1:], strict=False):
        delta = _mean_absolute_delta(previous, current)
        deltas.append(delta)
        if delta <= policy.duplicate_delta:
            duplicates += 1

    mean_delta = sum(deltas) / len(deltas)
    duplicate_ratio = duplicates / len(deltas)
    reasons: list[str] = []
    if mean_delta < policy.min_motion_delta:
        reasons.append(
            f"motion delta {mean_delta:.3f} below {policy.min_motion_delta:.3f}"
        )
    if duplicate_ratio > policy.max_duplicate_ratio:
        reasons.append(
            f"duplicate ratio {duplicate_ratio:.3f} above {policy.max_duplicate_ratio:.3f}"
        )
    return VideoQualityReport(
        pass_=not reasons,
        frame_count=len(frames),
        mean_motion_delta=mean_delta,
        duplicate_ratio=duplicate_ratio,
        terminal_frame_decodable=True,
        reasons=reasons,
    )


def _parse_rate(value: Any) -> float:
    text = str(value or "")
    if not text:
        return 0
    numerator, _, denominator = text.partition("/")
    try:
        n = float(numerator)
        d = float(denominator or "1")
    except ValueError:
        return 0
    return n / d if d else 0


def _parse_dimension(value: Any) -> tuple[int, bool]:
    try:
        return int(value or 0), True
    except (TypeError, ValueError, OverflowError):
        return 0, False


def _result_stdout(result: Any) -> Any:
    return getattr(result, "stdout", "")


def _run(
    runner: Callable[..., Any],
    args: list[str],
    *,
    text: bool,
) -> Any:
    return runner(
        args,
        capture_output=True,
        check=False,
        text=text,
    )


def inspect_video_quality(
    path: Path,
    policy: VideoQualityPolicy,
    *,
    runner: Callable[..., Any] = subprocess.run,
) -> VideoQualityReport:
    """Inspect media integrity and observable motion without optional heavy dependencies."""

    if not path.is_file() or path.stat().st_size <= 0:
        return VideoQualityReport(pass_=False, reasons=["video file missing or empty"])

    probe = _run(
        runner,
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=codec_type,codec_name,width,height,avg_frame_rate",
            "-of",
            "json",
            str(path),
        ],
        text=True,
    )
    if int(getattr(probe, "returncode", 1)) != 0:
        return VideoQualityReport(pass_=False, reasons=["ffprobe failed"])
    try:
        raw_probe = json.loads(str(_result_stdout(probe) or "{}"))
    except json.JSONDecodeError:
        return VideoQualityReport(pass_=False, reasons=["ffprobe returned invalid JSON"])

    if not isinstance(raw_probe, dict):
        return VideoQualityReport(
            pass_=False,
            reasons=["ffprobe metadata structure invalid"],
        )
    format_info = raw_probe.get("format")
    streams = raw_probe.get("streams")
    if (
        not isinstance(format_info, dict)
        or not isinstance(streams, list)
        or any(not isinstance(stream, dict) for stream in streams)
    ):
        return VideoQualityReport(
            pass_=False,
            reasons=["ffprobe metadata structure invalid"],
        )
    video = next(
        (stream for stream in streams if stream.get("codec_type") == "video"),
        None,
    )
    try:
        duration = float(format_info.get("duration") or 0)
    except (TypeError, ValueError):
        duration = 0
    duration_is_finite = math.isfinite(duration)
    if not duration_is_finite:
        duration = 0
    if video is None:
        reasons = ["video stream missing"]
        if not duration_is_finite:
            reasons.insert(0, "video duration is not finite")
        return VideoQualityReport(
            pass_=False,
            duration=duration,
            reasons=reasons,
        )

    width, width_is_integer = _parse_dimension(video.get("width"))
    height, height_is_integer = _parse_dimension(video.get("height"))
    dimensions_are_integer = width_is_integer and height_is_integer
    fps = _parse_rate(video.get("avg_frame_rate"))
    fps_is_finite = math.isfinite(fps)
    if not fps_is_finite:
        fps = 0
    base_reasons: list[str] = []
    if not duration_is_finite:
        base_reasons.append("video duration is not finite")
    elif duration <= 0:
        base_reasons.append("video duration is zero")
    elif duration < policy.min_duration_seconds:
        base_reasons.append(
            f"video duration {duration:.3f}s below {policy.min_duration_seconds:.3f}s"
        )
    if not dimensions_are_integer or width <= 0 or height <= 0:
        base_reasons.append("video dimensions are invalid")
    else:
        if width < policy.min_width:
            base_reasons.append(f"video width {width} below {policy.min_width}")
        if height < policy.min_height:
            base_reasons.append(f"video height {height} below {policy.min_height}")
    if not fps_is_finite:
        base_reasons.append("video fps is not finite")
    elif fps < policy.min_fps:
        base_reasons.append(f"video fps {fps:.3f} below {policy.min_fps:.3f}")

    if not dimensions_are_integer:
        return VideoQualityReport(
            pass_=False,
            duration=duration,
            width=width,
            height=height,
            fps=fps,
            reasons=base_reasons,
        )

    terminal = _run(
        runner,
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-sseof",
            "-0.25",
            "-i",
            str(path),
            "-frames:v",
            "1",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "gray",
            "pipe:1",
        ],
        text=False,
    )
    terminal_output = _result_stdout(terminal)
    terminal_bytes = (
        terminal_output
        if isinstance(terminal_output, bytes)
        else bytes(terminal_output or b"")
    )
    terminal_frame_size = width * height
    terminal_decodable = (
        int(getattr(terminal, "returncode", 1)) == 0
        and terminal_frame_size > 0
        and len(terminal_bytes) == terminal_frame_size
    )
    if not terminal_decodable:
        base_reasons.append("terminal frame not decodable")

    sampled = _run(
        runner,
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(path),
            "-vf",
            (
                f"fps={policy.sample_fps},scale={policy.sample_width}:{policy.sample_height}:"
                "flags=area,format=gray"
            ),
            "-f",
            "rawvideo",
            "-pix_fmt",
            "gray",
            "pipe:1",
        ],
        text=False,
    )
    frame_size = policy.sample_width * policy.sample_height
    frames: list[bytes] = []
    if int(getattr(sampled, "returncode", 1)) == 0:
        output = _result_stdout(sampled)
        byte_output = output if isinstance(output, bytes) else bytes(output or b"")
        if len(byte_output) % frame_size != 0:
            base_reasons.append("motion sample payload incomplete")
        else:
            for offset in range(0, len(byte_output), frame_size):
                frames.append(byte_output[offset : offset + frame_size])
            expected_samples = max(2, int(duration * policy.sample_fps) - 1)
            if len(frames) < expected_samples:
                base_reasons.append("motion sample coverage incomplete")

    motion = evaluate_motion_frames(frames, policy)
    reasons = [*base_reasons, *motion.reasons]
    return VideoQualityReport(
        pass_=not reasons,
        duration=duration,
        width=width,
        height=height,
        fps=fps,
        terminal_frame_decodable=terminal_decodable,
        frame_count=motion.frame_count,
        mean_motion_delta=motion.mean_motion_delta,
        duplicate_ratio=motion.duplicate_ratio,
        reasons=reasons,
    )


def assert_video_quality(report: VideoQualityReport) -> None:
    if report.pass_:
        return
    reasons = "; ".join(report.reasons) or "generated video quality gate failed"
    raise VideoQualityError(f"generated video rejected: {reasons}")