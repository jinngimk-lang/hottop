from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from .video_production import VideoProductionPlan


class MoviePyTimelineShot(BaseModel):
    index: int = Field(ge=1)
    source: str
    start_seconds: float = Field(ge=0)
    duration_seconds: float = Field(gt=0)


class MoviePyTimelineCaption(BaseModel):
    text: str
    start_seconds: float = Field(ge=0)
    duration_seconds: float = Field(gt=0)


class MoviePyTimeline(BaseModel):
    schema_version: Literal["hottop.moviepy-timeline.v1"] = "hottop.moviepy-timeline.v1"
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    fps: int = Field(gt=0)
    duration_seconds: float = Field(gt=0)
    shots: list[MoviePyTimelineShot] = Field(min_length=1)
    captions: list[MoviePyTimelineCaption] = Field(default_factory=list)
    bgm_description: str
    generate_synthetic_bgm: bool = True


def build_moviepy_timeline(
    plan: VideoProductionPlan,
    *,
    shots_dir: Path,
) -> MoviePyTimeline:
    """Map a trusted Hottop video plan into deterministic headless compositor inputs."""

    shots = [
        MoviePyTimelineShot(
            index=shot.index,
            source=str(shots_dir / f"shot-{shot.index:03d}.mp4"),
            start_seconds=shot.start_seconds,
            duration_seconds=shot.duration_seconds,
        )
        for shot in plan.shots
    ]
    captions = [
        MoviePyTimelineCaption(
            text=shot.caption.strip(),
            start_seconds=shot.start_seconds,
            duration_seconds=shot.duration_seconds,
        )
        for shot in plan.shots
        if shot.caption and shot.caption.strip()
    ]
    bgm_description = next(
        (cue.text for cue in plan.audio_cues if cue.kind == "bgm" and cue.text.strip()),
        "cheap comedic plucks and crude percussion",
    )
    return MoviePyTimeline(
        width=plan.width,
        height=plan.height,
        fps=plan.fps,
        duration_seconds=plan.duration_seconds,
        shots=shots,
        captions=captions,
        bgm_description=bgm_description,
    )


def _synthetic_bgm_array(duration_seconds: float, sample_rate: int = 44100):
    """Build deliberately cheap original plucks without shipping copyrighted music."""

    try:
        import numpy as np
    except ImportError as exc:  # pragma: no cover - execution-environment guard
        raise RuntimeError("MoviePy video execution requires the optional `video` dependencies") from exc

    sample_count = max(1, int(duration_seconds * sample_rate))
    audio = np.zeros(sample_count, dtype=float)
    notes = (110.0, 146.83, 164.81, 130.81)
    beat_seconds = 0.5
    beat_count = int(math.ceil(duration_seconds / beat_seconds))
    for beat in range(beat_count):
        start_seconds = beat * beat_seconds
        start = int(start_seconds * sample_rate)
        end = min(sample_count, start + int(0.24 * sample_rate))
        if end <= start:
            continue
        local = np.arange(end - start, dtype=float) / sample_rate
        frequency = notes[beat % len(notes)]
        envelope = np.exp(-12.0 * local)
        pluck = np.sin(2 * math.pi * frequency * local) * envelope
        if beat % 4 == 0:
            pluck += 0.35 * np.sin(2 * math.pi * 55.0 * local) * np.exp(-18.0 * local)
        audio[start:end] += 0.12 * pluck
    stereo = np.column_stack((audio, audio))
    return stereo, sample_rate


def render_moviepy_timeline(
    timeline: MoviePyTimeline,
    *,
    output: Path,
) -> None:
    """Render generated shot files with captions and an original synthetic rough-comedy bed."""

    try:
        from moviepy import (
            AudioArrayClip,
            CompositeAudioClip,
            CompositeVideoClip,
            TextClip,
            VideoFileClip,
            concatenate_videoclips,
        )
    except ImportError as exc:  # pragma: no cover - execution-environment guard
        raise RuntimeError(
            "MoviePy compositor is not installed. Install the optional Hottop video dependencies."
        ) from exc

    missing = [shot.source for shot in timeline.shots if not Path(shot.source).is_file()]
    if missing:
        raise FileNotFoundError("Missing generated video shots: " + ", ".join(missing))

    clips = []
    opened = []
    try:
        for shot in timeline.shots:
            clip = VideoFileClip(shot.source)
            opened.append(clip)
            if clip.duration > shot.duration_seconds:
                clip = clip.subclipped(0, shot.duration_seconds)
            elif clip.duration < shot.duration_seconds:
                clip = clip.with_effects([]).with_duration(shot.duration_seconds)
            clip = clip.resized(new_size=(timeline.width, timeline.height))
            clips.append(clip)

        base = concatenate_videoclips(clips, method="compose")
        if base.duration > timeline.duration_seconds:
            base = base.subclipped(0, timeline.duration_seconds)

        layers = [base]
        for caption in timeline.captions:
            text = TextClip(
                text=caption.text,
                font_size=max(38, timeline.width // 14),
                color="white",
                stroke_color="black",
                stroke_width=3,
                method="caption",
                size=(int(timeline.width * 0.88), None),
                text_align="center",
            )
            text = (
                text.with_start(caption.start_seconds)
                .with_duration(caption.duration_seconds)
                .with_position(("center", int(timeline.height * 0.78)))
            )
            layers.append(text)

        composite = CompositeVideoClip(layers, size=(timeline.width, timeline.height))
        duration = min(composite.duration, timeline.duration_seconds)
        if timeline.generate_synthetic_bgm:
            audio_array, sample_rate = _synthetic_bgm_array(duration)
            bgm = AudioArrayClip(audio_array, fps=sample_rate).with_duration(duration)
            if composite.audio is not None:
                audio = CompositeAudioClip([composite.audio, bgm])
            else:
                audio = bgm
            composite = composite.with_audio(audio)

        output.parent.mkdir(parents=True, exist_ok=True)
        composite.write_videofile(
            str(output),
            fps=timeline.fps,
            codec="libx264",
            audio_codec="aac",
            preset="medium",
            logger=None,
        )
        composite.close()
    finally:
        for clip in opened:
            clip.close()


def _load_plan(path: Path) -> VideoProductionPlan:
    return VideoProductionPlan.model_validate(json.loads(path.read_text(encoding="utf-8")))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compose a Hottop video plan headlessly with MoviePy")
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--shots-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)

    timeline = build_moviepy_timeline(_load_plan(args.plan), shots_dir=args.shots_dir)
    render_moviepy_timeline(timeline, output=args.output)
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
