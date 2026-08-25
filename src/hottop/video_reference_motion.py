from __future__ import annotations

import subprocess
from collections.abc import Callable
from pathlib import Path

Runner = Callable[..., subprocess.CompletedProcess[str]]


def render_reference_motion(
    reference_image: Path,
    output: Path,
    duration_seconds: float,
    *,
    width: int = 720,
    height: int = 1280,
    fps: int = 24,
    runner: Runner = subprocess.run,
) -> Path:
    """Animate a rights-cleared local image with deterministic FFmpeg camera motion."""

    if not reference_image.is_file():
        raise FileNotFoundError(f"reference image does not exist: {reference_image}")
    if duration_seconds <= 0:
        raise ValueError("duration_seconds must be positive")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.unlink(missing_ok=True)
    zoom_frames = max(1, round(duration_seconds * fps))
    vf = (
        f"scale={width}:{height}:force_original_aspect_ratio=increase,"
        f"crop={width}:{height},"
        f"zoompan=z='min(zoom+0.0008,1.08)':d={zoom_frames}:s={width}x{height}:fps={fps},"
        "format=yuv420p"
    )
    completed = runner(
        [
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-i",
            str(reference_image),
            "-vf",
            vf,
            "-t",
            str(duration_seconds),
            "-an",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(output),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        output.unlink(missing_ok=True)
        raise RuntimeError(
            f"deterministic reference motion failed with return code {completed.returncode}"
        )
    if not output.is_file() or output.stat().st_size <= 0:
        raise RuntimeError("deterministic reference motion produced no output")
    return output
