from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from collections.abc import Mapping
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from .video_production import VideoProductionPlan

_DEFAULT_CJK_FONT_CANDIDATES = (
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.otf"),
    Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"),
    Path("/System/Library/Fonts/PingFang.ttc"),
    Path("C:/Windows/Fonts/msyh.ttc"),
    Path("C:/Windows/Fonts/simhei.ttf"),
)
_DIALOGUE_DURATION_TOLERANCE_SECONDS = 0.25


class MoviePyTimelineShot(BaseModel):
    index: int = Field(ge=1)
    source: str
    start_seconds: float = Field(ge=0)
    duration_seconds: float = Field(gt=0)


class MoviePyTimelineCaption(BaseModel):
    text: str
    start_seconds: float = Field(ge=0)
    duration_seconds: float = Field(gt=0)


class MoviePyTimelineDialogueTrack(BaseModel):
    source: str
    start_seconds: float = Field(ge=0)
    duration_seconds: float | None = Field(default=None, gt=0)
    character: str | None = None
    delivery: str | None = None
    duck_bgm_db: float | None = None


class MoviePyTimelineSfxCue(BaseModel):
    start_seconds: float = Field(ge=0)
    duration_seconds: float | None = Field(default=None, gt=0)
    description: str


class MoviePyTimeline(BaseModel):
    schema_version: Literal["hottop.moviepy-timeline.v1"] = "hottop.moviepy-timeline.v1"
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    fps: int = Field(gt=0)
    duration_seconds: float = Field(gt=0)
    shots: list[MoviePyTimelineShot] = Field(min_length=1)
    captions: list[MoviePyTimelineCaption] = Field(default_factory=list)
    dialogue_tracks: list[MoviePyTimelineDialogueTrack] = Field(default_factory=list)
    sfx_cues: list[MoviePyTimelineSfxCue] = Field(default_factory=list)
    bgm_description: str
    generate_synthetic_bgm: bool = True
    generate_procedural_sfx: bool = True


def build_moviepy_timeline(
    plan: VideoProductionPlan,
    *,
    shots_dir: Path,
    audio_dir: Path | None = None,
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
    resolved_audio_dir = audio_dir if audio_dir is not None else shots_dir.parent / "audio"
    dialogue_cues = [cue for cue in plan.audio_cues if cue.kind == "dialogue"]
    voice_enabled = plan.audio_profile is not None and plan.audio_profile.voice_backend != "none"
    dialogue_tracks = (
        [
            MoviePyTimelineDialogueTrack(
                source=str(resolved_audio_dir / f"dialogue-{index:03d}.wav"),
                start_seconds=cue.start_seconds,
                duration_seconds=cue.duration_seconds,
                character=cue.character,
                delivery=cue.delivery,
                duck_bgm_db=cue.duck_bgm_db,
            )
            for index, cue in enumerate(dialogue_cues, start=1)
        ]
        if voice_enabled
        else []
    )
    sfx_cues = [
        MoviePyTimelineSfxCue(
            start_seconds=cue.start_seconds,
            duration_seconds=cue.duration_seconds,
            description=cue.text,
        )
        for cue in plan.audio_cues
        if cue.kind in {"foley", "sfx"}
    ]
    generate_synthetic_bgm = (
        plan.audio_profile is None or plan.audio_profile.music_backend == "synthetic"
    )
    generate_procedural_sfx = (
        plan.audio_profile is None or plan.audio_profile.sfx_backend == "procedural"
    )
    return MoviePyTimeline(
        width=plan.width,
        height=plan.height,
        fps=plan.fps,
        duration_seconds=plan.duration_seconds,
        shots=shots,
        captions=captions,
        dialogue_tracks=dialogue_tracks,
        sfx_cues=sfx_cues,
        bgm_description=bgm_description,
        generate_synthetic_bgm=generate_synthetic_bgm,
        generate_procedural_sfx=generate_procedural_sfx,
    )


def verify_moviepy_shot_artifacts(timeline: MoviePyTimeline) -> None:
    """Reverify generated shot bytes immediately before the compositor consumes them."""

    for shot in timeline.shots:
        source = Path(shot.source)
        manifest_path = source.with_suffix(".artifact.json")
        if not manifest_path.is_file():
            raise ValueError(f"Missing artifact manifest for MoviePy shot {shot.index}: {manifest_path}")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        records = manifest.get("shots")
        if not isinstance(records, list):
            raise ValueError(f"Invalid artifact manifest for MoviePy shot {shot.index}")
        record = next(
            (
                item
                for item in records
                if isinstance(item, dict)
                and item.get("shot_index") == shot.index
                and item.get("path") == str(source)
            ),
            None,
        )
        if record is None:
            raise ValueError(f"Artifact manifest does not bind MoviePy shot {shot.index} to {source}")
        if not source.is_file():
            raise ValueError(f"MoviePy shot {shot.index} content mismatch: source file is missing")
        content = source.read_bytes()
        expected_size = record.get("size_bytes")
        expected_sha256 = record.get("sha256")
        actual_sha256 = hashlib.sha256(content).hexdigest()
        if expected_size != len(content) or expected_sha256 != actual_sha256:
            raise ValueError(f"MoviePy shot {shot.index} content mismatch with artifact provenance")


def _contains_cjk(text: str) -> bool:
    return any(
        0x3400 <= ord(character) <= 0x4DBF
        or 0x4E00 <= ord(character) <= 0x9FFF
        or 0xF900 <= ord(character) <= 0xFAFF
        for character in text
    )


def _resolve_caption_font(
    captions: list[MoviePyTimelineCaption],
    *,
    environ: Mapping[str, str] | None = None,
    candidates: tuple[Path, ...] = _DEFAULT_CJK_FONT_CANDIDATES,
) -> str | None:
    """Resolve a local CJK-capable caption font or fail closed before composition."""

    if not any(_contains_cjk(caption.text) for caption in captions):
        return None

    environment = os.environ if environ is None else environ
    explicit = environment.get("HOTTOP_CAPTION_FONT")
    if explicit:
        font_path = Path(explicit).expanduser().resolve()
        if font_path.is_file():
            return str(font_path)
        raise RuntimeError(f"CJK caption font is not available locally: {font_path}")

    for candidate in candidates:
        font_path = candidate.expanduser().resolve()
        if font_path.is_file():
            return str(font_path)

    raise RuntimeError(
        "CJK caption font is required for Mandarin/CJK captions; "
        "set HOTTOP_CAPTION_FONT to a local CJK-capable font file"
    )


def _caption_bottom_y(*, frame_height: int, text_height: int) -> int:
    """Bottom-anchor a rendered caption while preserving a visible vertical safe margin."""

    margin = max(24, round(frame_height * 0.06))
    return max(0, frame_height - text_height - margin)


def _fit_caption_text_clip(
    text_clip_factory,
    *,
    text: str,
    font: str | None,
    frame_width: int,
    frame_height: int,
):
    """Fit a full mobile caption without letting long copy dominate the subject area."""

    font_size = max(38, frame_width // 14)
    minimum_font_size = max(28, frame_width // 24)
    maximum_text_height = max(72, round(frame_height * 0.18))

    while True:
        clip = text_clip_factory(
            text=text,
            font=font,
            font_size=font_size,
            color="white",
            stroke_color="black",
            stroke_width=3,
            method="caption",
            size=(int(frame_width * 0.88), None),
            text_align="center",
        )
        if clip.h <= maximum_text_height or font_size <= minimum_font_size:
            return clip

        scale = maximum_text_height / clip.h
        next_font_size = max(
            minimum_font_size,
            min(font_size - 2, math.floor(font_size * scale)),
        )
        clip.close()
        font_size = next_font_size


def _synthetic_bgm_array(
    duration_seconds: float,
    description: str = "",
    sample_rate: int = 44100,
):
    """Build an original low-cost music bed; style words affect tempo/register, not source audio."""

    try:
        import numpy as np
    except ImportError as exc:  # pragma: no cover - execution-environment guard
        raise RuntimeError("MoviePy video execution requires the optional `video` dependencies") from exc

    sample_count = max(1, int(duration_seconds * sample_rate))
    audio = np.zeros(sample_count, dtype=float)
    lowered = description.lower()
    epic = any(token in lowered for token in ("epic", "myth", "史诗", "dark"))
    notes = (73.42, 98.0, 110.0, 82.41) if epic else (110.0, 146.83, 164.81, 130.81)
    beat_seconds = 0.65 if epic else 0.5
    beat_count = int(math.ceil(duration_seconds / beat_seconds))
    for beat in range(beat_count):
        start_seconds = beat * beat_seconds
        start = int(start_seconds * sample_rate)
        end = min(sample_count, start + int((0.34 if epic else 0.24) * sample_rate))
        if end <= start:
            continue
        local = np.arange(end - start, dtype=float) / sample_rate
        frequency = notes[beat % len(notes)]
        envelope = np.exp((-8.0 if epic else -12.0) * local)
        pluck = np.sin(2 * math.pi * frequency * local) * envelope
        if beat % 4 == 0:
            pluck += 0.35 * np.sin(2 * math.pi * (frequency / 2) * local) * np.exp(-15.0 * local)
        audio[start:end] += (0.09 if epic else 0.12) * pluck
    stereo = np.column_stack((audio, audio))
    return stereo, sample_rate


def _apply_dialogue_ducking(
    audio,
    *,
    sample_rate: int,
    dialogue_tracks: list[MoviePyTimelineDialogueTrack],
):
    """Attenuate a BGM copy only inside dialogue windows using the strongest configured duck."""

    try:
        import numpy as np
    except ImportError as exc:  # pragma: no cover - execution-environment guard
        raise RuntimeError("MoviePy video execution requires the optional `video` dependencies") from exc

    ducked = np.array(audio, dtype=float, copy=True)
    if ducked.ndim == 0 or ducked.shape[0] == 0:
        return ducked

    sample_count = ducked.shape[0]
    gains = np.ones(sample_count, dtype=float)
    for track in dialogue_tracks:
        if track.duck_bgm_db is None or track.duration_seconds is None:
            continue
        start = max(0, min(sample_count, int(round(track.start_seconds * sample_rate))))
        end = max(
            start,
            min(
                sample_count,
                int(round((track.start_seconds + track.duration_seconds) * sample_rate)),
            ),
        )
        if end <= start:
            continue
        track_gain = 10 ** (track.duck_bgm_db / 20)
        gains[start:end] = np.minimum(gains[start:end], track_gain)

    if ducked.ndim == 1:
        return ducked * gains
    return ducked * gains.reshape((-1,) + (1,) * (ducked.ndim - 1))


def _validate_dialogue_track_duration(
    *,
    actual_duration_seconds: float,
    track: MoviePyTimelineDialogueTrack,
) -> None:
    """Fail closed instead of silently truncating materially overlong dialogue."""

    if track.duration_seconds is None:
        return
    if actual_duration_seconds - track.duration_seconds > _DIALOGUE_DURATION_TOLERANCE_SECONDS:
        raise RuntimeError(
            "dialogue audio exceeds its planned window: "
            f"{track.source} is {actual_duration_seconds:.3f}s for "
            f"{track.duration_seconds:.3f}s"
        )


def _effective_dialogue_duck_track(
    track: MoviePyTimelineDialogueTrack,
    *,
    actual_duration_seconds: float,
) -> MoviePyTimelineDialogueTrack:
    """Bind BGM attenuation to validated audible voice length, not the whole planned shot."""

    duration = actual_duration_seconds
    if track.duration_seconds is not None:
        duration = min(duration, track.duration_seconds)
    return track.model_copy(update={"duration_seconds": duration})


def _procedural_sfx_array(
    duration_seconds: float,
    cues: list[MoviePyTimelineSfxCue],
    sample_rate: int = 44100,
):
    """Create small original Foley hits so the baseline pipeline has SFX without a stock library."""

    try:
        import numpy as np
    except ImportError as exc:  # pragma: no cover - execution-environment guard
        raise RuntimeError("MoviePy video execution requires the optional `video` dependencies") from exc

    sample_count = max(1, int(duration_seconds * sample_rate))
    audio = np.zeros(sample_count, dtype=float)
    for index, cue in enumerate(cues):
        start = min(sample_count - 1, int(cue.start_seconds * sample_rate))
        hit_length = min(sample_count - start, int(0.16 * sample_rate))
        if hit_length <= 0:
            continue
        local = np.arange(hit_length, dtype=float) / sample_rate
        rng = np.random.default_rng(index + 104729)
        noise = rng.normal(0.0, 1.0, hit_length)
        envelope = np.exp(-22.0 * local)
        tonal = np.sin(2 * math.pi * (145.0 + 37.0 * (index % 5)) * local)
        audio[start : start + hit_length] += 0.035 * noise * envelope + 0.055 * tonal * envelope
    stereo = np.column_stack((audio, audio))
    return stereo, sample_rate


def render_moviepy_timeline(
    timeline: MoviePyTimeline,
    *,
    output: Path,
) -> None:
    """Render shots with captions, dialogue, original music and procedural Foley/SFX."""

    verify_moviepy_shot_artifacts(timeline)
    caption_font = _resolve_caption_font(timeline.captions)

    try:
        from moviepy import (
            AudioArrayClip,
            AudioFileClip,
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

    missing_shots = [shot.source for shot in timeline.shots if not Path(shot.source).is_file()]
    if missing_shots:
        raise FileNotFoundError("Missing generated video shots: " + ", ".join(missing_shots))
    missing_dialogue = [
        track.source for track in timeline.dialogue_tracks if not Path(track.source).is_file()
    ]
    if missing_dialogue:
        raise FileNotFoundError("Missing dialogue audio tracks: " + ", ".join(missing_dialogue))

    clips = []
    opened_video = []
    opened_audio = []
    composite = None
    try:
        for shot in timeline.shots:
            clip = VideoFileClip(shot.source)
            opened_video.append(clip)
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
            text = _fit_caption_text_clip(
                TextClip,
                text=caption.text,
                font=caption_font,
                frame_width=timeline.width,
                frame_height=timeline.height,
            )
            caption_y = _caption_bottom_y(
                frame_height=timeline.height,
                text_height=text.h,
            )
            text = (
                text.with_start(caption.start_seconds)
                .with_duration(caption.duration_seconds)
                .with_position(("center", caption_y))
            )
            layers.append(text)

        composite = CompositeVideoClip(layers, size=(timeline.width, timeline.height))
        duration = min(composite.duration, timeline.duration_seconds)
        audio_layers = []
        if composite.audio is not None:
            audio_layers.append(composite.audio)

        prepared_dialogue = []
        effective_duck_tracks = []
        for track in timeline.dialogue_tracks:
            voice = AudioFileClip(track.source)
            opened_audio.append(voice)
            _validate_dialogue_track_duration(
                actual_duration_seconds=voice.duration,
                track=track,
            )
            effective_duck_tracks.append(
                _effective_dialogue_duck_track(
                    track,
                    actual_duration_seconds=voice.duration,
                )
            )
            if track.duration_seconds is not None and voice.duration > track.duration_seconds:
                voice = voice.subclipped(0, track.duration_seconds)
            prepared_dialogue.append((track, voice))

        if timeline.generate_synthetic_bgm:
            audio_array, sample_rate = _synthetic_bgm_array(
                duration,
                timeline.bgm_description,
            )
            audio_array = _apply_dialogue_ducking(
                audio_array,
                sample_rate=sample_rate,
                dialogue_tracks=effective_duck_tracks,
            )
            bgm = AudioArrayClip(audio_array, fps=sample_rate).with_duration(duration)
            audio_layers.append(bgm)

        if timeline.generate_procedural_sfx and timeline.sfx_cues:
            sfx_array, sample_rate = _procedural_sfx_array(duration, timeline.sfx_cues)
            sfx = AudioArrayClip(sfx_array, fps=sample_rate).with_duration(duration)
            audio_layers.append(sfx)

        for track, voice in prepared_dialogue:
            voice = voice.with_start(track.start_seconds)
            audio_layers.append(voice)

        if audio_layers:
            composite = composite.with_audio(CompositeAudioClip(audio_layers))

        output.parent.mkdir(parents=True, exist_ok=True)
        composite.write_videofile(
            str(output),
            fps=timeline.fps,
            codec="libx264",
            audio_codec="aac",
            preset="medium",
            logger=None,
        )
    finally:
        if composite is not None:
            composite.close()
        for clip in opened_video:
            clip.close()
        for clip in opened_audio:
            clip.close()


def _load_plan(path: Path) -> VideoProductionPlan:
    return VideoProductionPlan.model_validate(json.loads(path.read_text(encoding="utf-8")))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compose a Hottop video plan headlessly with MoviePy")
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--shots-dir", type=Path, required=True)
    parser.add_argument("--audio-dir", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)

    timeline = build_moviepy_timeline(
        _load_plan(args.plan),
        shots_dir=args.shots_dir,
        audio_dir=args.audio_dir,
    )
    render_moviepy_timeline(timeline, output=args.output)
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())
