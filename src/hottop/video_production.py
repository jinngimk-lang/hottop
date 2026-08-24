from __future__ import annotations

import shlex
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field

from .rendering import CreativeRenderRequest

VideoStyleProfile = Literal["anti-polish", "cinematic", "social-native"]
GenerationBackend = Literal["wan22-ti2v-5b", "wan22-i2v-a14b", "external"]
CompositorBackend = Literal["motion-canvas", "moviepy", "external"]
EncoderBackend = Literal["ffmpeg", "external"]
OutputFormat = Literal["mp4", "webm", "gif"]
AudioCueKind = Literal["dialogue", "foley", "sfx", "bgm"]
VoiceBackend = Literal["none", "espeak", "external"]
MusicBackend = Literal["none", "synthetic", "external"]
SfxBackend = Literal["none", "procedural", "external"]
CommandStage = Literal["generation", "audio", "compositor", "finalization"]


class ShotPolicy(BaseModel):
    min_shot_seconds: float = Field(gt=0)
    max_shot_seconds: float = Field(gt=0)
    transition_bias: list[str] = Field(default_factory=list)


class AudioConfig(BaseModel):
    bgm_style: str
    dialogue_duck_db: float = -8
    foley_style: str
    voice_backend: VoiceBackend = "none"
    voice_profile: str = "natural-dialogue"
    voice_language: str = "zh"
    voice_rate_wpm: int = Field(default=155, ge=80, le=320)
    music_backend: MusicBackend = "synthetic"
    music_profile: str | None = None
    sfx_backend: SfxBackend = "procedural"
    sfx_profile: str | None = None
    original_music_only: bool = True


class AudioProductionProfile(BaseModel):
    voice_backend: VoiceBackend
    voice_profile: str
    voice_language: str
    voice_rate_wpm: int
    music_backend: MusicBackend
    music_profile: str
    sfx_backend: SfxBackend
    sfx_profile: str
    original_music_only: bool
    dialogue_duck_db: float


class TextConfig(BaseModel):
    subtitle_mode: str = "dialogue-first"
    max_end_card_seconds: float = Field(default=0.8, ge=0)
    allow_url: bool = False
    allow_qr: bool = False


class AntiPolishConfig(BaseModel):
    enabled: bool = False
    rough_3d: bool = False
    low_poly_bias: bool = False
    awkward_motion: bool = False
    deadpan_acting: bool = False
    cheap_instrumentation: bool = False
    forbid_glossy_ai_ad_defaults: bool = False
    precision_must_remain: list[str] = Field(default_factory=list)


class Wan22Config(BaseModel):
    task: str
    size: str
    model_dir: str
    offload_model: bool = True
    convert_model_dtype: bool = True


class MotionCanvasConfig(BaseModel):
    project_dir: str
    manifest_name: str = "hottop-video-plan.json"


class MoviePyConfig(BaseModel):
    shot_dir: str = "shots"
    composite_name: str = "hottop-composite.mp4"


class FFmpegConfig(BaseModel):
    video_codec: str = "libx264"
    audio_codec: str = "aac"
    pixel_format: str = "yuv420p"
    movflags: str = "+faststart"


class VideoProductionConfig(BaseModel):
    schema_version: Literal["hottop.video-config.v1"] = "hottop.video-config.v1"
    name: str
    style_profile: VideoStyleProfile
    generation_backend: GenerationBackend
    compositor_backend: CompositorBackend
    encoder_backend: EncoderBackend
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    fps: int = Field(gt=0)
    duration_seconds: float = Field(gt=0)
    output_format: OutputFormat = "mp4"
    shot_policy: ShotPolicy
    audio: AudioConfig
    text: TextConfig
    anti_polish: AntiPolishConfig = Field(default_factory=AntiPolishConfig)
    wan22: Wan22Config | None = None
    motion_canvas: MotionCanvasConfig | None = None
    moviepy: MoviePyConfig | None = None
    ffmpeg: FFmpegConfig | None = None


class VideoShot(BaseModel):
    index: int = Field(ge=1)
    start_seconds: float = Field(ge=0)
    end_seconds: float = Field(gt=0)
    duration_seconds: float = Field(gt=0)
    scene: str
    caption: str | None = None
    intent: str
    continuity_instruction: str
    generation_prompt: str
    negative_prompt: str


class AudioCue(BaseModel):
    kind: AudioCueKind
    start_seconds: float = Field(ge=0)
    duration_seconds: float | None = Field(default=None, gt=0)
    text: str
    character: str | None = None
    delivery: str | None = None
    voice_profile: str | None = None
    duck_bgm_db: float | None = None


class ExternalCommandSpec(BaseModel):
    program: str
    args: list[str] = Field(default_factory=list)
    cwd: str | None = None
    stage: CommandStage


class VideoProductionPlan(BaseModel):
    schema_version: Literal["hottop.video-plan.v1"] = "hottop.video-plan.v1"
    config_name: str
    topic_id: str
    topic_title: str
    subject_name: str
    style_profile: VideoStyleProfile
    generation_backend: GenerationBackend
    compositor_backend: CompositorBackend
    encoder_backend: EncoderBackend
    width: int
    height: int
    fps: int
    duration_seconds: float
    output_format: OutputFormat
    in_asset_cta_policy: str
    shots: list[VideoShot] = Field(min_length=1)
    audio_profile: AudioProductionProfile | None = None
    audio_cues: list[AudioCue] = Field(default_factory=list)
    generation_commands: list[str] = Field(default_factory=list)
    generation_command_specs: list[ExternalCommandSpec] = Field(default_factory=list)
    compositor_manifest: dict[str, object] = Field(default_factory=dict)
    compositor_command_spec: ExternalCommandSpec | None = None
    finalization_command: list[str] = Field(default_factory=list)
    finalization_command_spec: ExternalCommandSpec | None = None
    execution_notes: list[str] = Field(default_factory=list)


def load_video_production_config(path: Path) -> VideoProductionConfig:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return VideoProductionConfig.model_validate(raw)


def _shot_duration(config: VideoProductionConfig, shot_count: int) -> float:
    equal_share = config.duration_seconds / shot_count
    duration = min(config.shot_policy.max_shot_seconds, equal_share)
    if duration < config.shot_policy.min_shot_seconds:
        return equal_share
    return duration


def _continuity_instruction(config: VideoProductionConfig, index: int) -> str:
    if index == 1:
        return (
            "Establish one continuous location, lighting setup, character identity and object state; "
            "carry them into the next shot."
        )
    transitions = config.shot_policy.transition_bias or ["match-action"]
    transition = transitions[(index - 2) % len(transitions)]
    return (
        "Preserve the same characters, scene geography, lighting and object state from the prior shot; "
        f"bridge the action with a {transition} transition rather than an unrelated still cut."
    )


def _generation_prompt(
    render_request: CreativeRenderRequest,
    config: VideoProductionConfig,
    scene: str,
) -> str:
    parts = [render_request.master_prompt, scene]
    if config.anti_polish.enabled:
        parts.append(
            "Intentional rough cheap low-budget 3D: simple geometry and materials, slightly awkward "
            "motion, deadpan acting, crude but purposeful staging; preserve character continuity."
        )
    return " ".join(part.strip() for part in parts if part.strip())


def _negative_prompt(render_request: CreativeRenderRequest, config: VideoProductionConfig) -> str:
    parts = [render_request.negative_prompt]
    if config.anti_polish.forbid_glossy_ai_ad_defaults:
        parts.append(
            "glossy AI ad, blue-purple hologram, polished mascot team, luxury sci-fi interface, "
            "feature-card UI, unrelated slideshow stills"
        )
    return ", ".join(part.strip() for part in parts if part.strip())


def _wan22_command_spec(
    config: VideoProductionConfig,
    prompt: str,
) -> ExternalCommandSpec | None:
    if not config.generation_backend.startswith("wan22") or config.wan22 is None:
        return None
    args = [
        "generate.py",
        "--task",
        config.wan22.task,
        "--size",
        config.wan22.size,
        "--ckpt_dir",
        config.wan22.model_dir,
    ]
    if config.wan22.offload_model:
        args.extend(["--offload_model", "True"])
    if config.wan22.convert_model_dtype:
        args.append("--convert_model_dtype")
    args.extend(["--prompt", prompt])
    return ExternalCommandSpec(
        program="python",
        args=args,
        cwd="integrations/Wan2.2",
        stage="generation",
    )


def _wan22_command(config: VideoProductionConfig, prompt: str) -> str | None:
    spec = _wan22_command_spec(config, prompt)
    if spec is None:
        return None
    return " ".join(shlex.quote(value) for value in [spec.program, *spec.args])


def _compositor_command_spec(config: VideoProductionConfig) -> ExternalCommandSpec | None:
    if config.compositor_backend == "motion-canvas" and config.motion_canvas is not None:
        return ExternalCommandSpec(
            program="npm",
            args=[
                "run",
                "render",
                "--",
                "--plan",
                config.motion_canvas.manifest_name,
            ],
            cwd=str(Path(config.motion_canvas.project_dir)),
            stage="compositor",
        )
    if config.compositor_backend == "moviepy" and config.moviepy is not None:
        return ExternalCommandSpec(
            program="python",
            args=[
                "-m",
                "hottop.video_moviepy",
                "--plan",
                "hottop-video-plan.json",
                "--shots-dir",
                config.moviepy.shot_dir,
                "--output",
                config.moviepy.composite_name,
            ],
            cwd=".",
            stage="compositor",
        )
    return None


def _audio_profile(config: VideoProductionConfig) -> AudioProductionProfile:
    return AudioProductionProfile(
        voice_backend=config.audio.voice_backend,
        voice_profile=config.audio.voice_profile,
        voice_language=config.audio.voice_language,
        voice_rate_wpm=config.audio.voice_rate_wpm,
        music_backend=config.audio.music_backend,
        music_profile=config.audio.music_profile or config.audio.bgm_style,
        sfx_backend=config.audio.sfx_backend,
        sfx_profile=config.audio.sfx_profile or config.audio.foley_style,
        original_music_only=config.audio.original_music_only,
        dialogue_duck_db=config.audio.dialogue_duck_db,
    )


def _audio_cues(
    render_request: CreativeRenderRequest,
    config: VideoProductionConfig,
    shots: list[VideoShot],
) -> list[AudioCue]:
    profile = _audio_profile(config)
    cues = [
        AudioCue(
            kind="bgm",
            start_seconds=0,
            duration_seconds=config.duration_seconds,
            text=profile.music_profile,
        )
    ]
    for shot, frame in zip(shots, render_request.frames, strict=True):
        cues.append(
            AudioCue(
                kind="foley",
                start_seconds=shot.start_seconds,
                duration_seconds=shot.duration_seconds,
                text=f"{profile.sfx_profile}; follow the visible action in shot {shot.index}",
            )
        )
        if frame.caption:
            cues.append(
                AudioCue(
                    kind="dialogue",
                    start_seconds=shot.start_seconds,
                    duration_seconds=shot.duration_seconds,
                    text=frame.caption,
                    character=frame.speaker,
                    delivery=frame.delivery,
                    voice_profile=profile.voice_profile,
                    duck_bgm_db=config.audio.dialogue_duck_db,
                )
            )
    return cues


def _composite_input_name(config: VideoProductionConfig) -> str:
    if config.compositor_backend == "moviepy" and config.moviepy is not None:
        return config.moviepy.composite_name
    return "motion-canvas-output.mp4"


def _finalization_command(config: VideoProductionConfig) -> list[str]:
    if config.encoder_backend != "ffmpeg" or config.ffmpeg is None:
        return []
    output_name = f"hottop-output.{config.output_format}"
    return [
        "ffmpeg",
        "-i",
        _composite_input_name(config),
        "-c:v",
        config.ffmpeg.video_codec,
        "-pix_fmt",
        config.ffmpeg.pixel_format,
        "-c:a",
        config.ffmpeg.audio_codec,
        "-movflags",
        config.ffmpeg.movflags,
        output_name,
    ]


def _finalization_command_spec(config: VideoProductionConfig) -> ExternalCommandSpec | None:
    command = _finalization_command(config)
    if not command:
        return None
    return ExternalCommandSpec(
        program=command[0],
        args=command[1:],
        stage="finalization",
    )


def build_video_production_plan(
    render_request: CreativeRenderRequest,
    config: VideoProductionConfig,
) -> VideoProductionPlan:
    shot_count = len(render_request.frames)
    duration = _shot_duration(config, shot_count)
    shots: list[VideoShot] = []
    commands: list[str] = []
    command_specs: list[ExternalCommandSpec] = []

    for position, frame in enumerate(render_request.frames, start=1):
        start = round((position - 1) * duration, 3)
        end = round(min(position * duration, config.duration_seconds), 3)
        prompt = _generation_prompt(render_request, config, frame.scene)
        shots.append(
            VideoShot(
                index=position,
                start_seconds=start,
                end_seconds=end,
                duration_seconds=round(end - start, 3),
                scene=frame.scene,
                caption=frame.caption,
                intent=frame.intent,
                continuity_instruction=_continuity_instruction(config, position),
                generation_prompt=prompt,
                negative_prompt=_negative_prompt(render_request, config),
            )
        )
        command = _wan22_command(config, prompt)
        if command:
            commands.append(command)
        command_spec = _wan22_command_spec(config, prompt)
        if command_spec:
            command_specs.append(command_spec)

    audio_profile = _audio_profile(config)
    audio_cues = _audio_cues(render_request, config, shots)
    compositor_manifest: dict[str, object] = {
        "backend": config.compositor_backend,
        "project_dir": config.motion_canvas.project_dir if config.motion_canvas else None,
        "manifest_name": (
            config.motion_canvas.manifest_name if config.motion_canvas else "hottop-video-plan.json"
        ),
        "shot_dir": config.moviepy.shot_dir if config.moviepy else None,
        "composite_name": config.moviepy.composite_name if config.moviepy else None,
        "width": config.width,
        "height": config.height,
        "fps": config.fps,
        "shots": [shot.model_dump(mode="json") for shot in shots],
        "audio_profile": audio_profile.model_dump(mode="json"),
        "audio_cues": [cue.model_dump(mode="json") for cue in audio_cues],
    }
    compositor_note = (
        "MoviePy is the headless deterministic compositor for captions, dialogue, original music, procedural SFX and shot assembly."
        if config.compositor_backend == "moviepy"
        else "Motion Canvas is the deterministic compositor for subtitles, SFX/BGM timing and continuity."
    )
    execution_notes = [
        compositor_note,
        (
            "Preserve character continuity, scene geography, cause/effect, subtitle correctness, "
            "dialogue intelligibility and comedy timing even when production looks intentionally rough."
        ),
        "Voice, music and SFX are explicit production profiles; changing audio providers must not change creative semantics.",
        "When original_music_only is true, do not fetch or imitate copyrighted commercial soundtrack audio.",
        "Wan2.2 execution is optional/local and requires operator-controlled model files and GPU resources.",
        "Do not auto-fetch copyrighted film footage, protected character assets or commercial soundtracks.",
    ]
    finalization_command = _finalization_command(config)

    return VideoProductionPlan(
        config_name=config.name,
        topic_id=render_request.topic_id,
        topic_title=render_request.topic_title,
        subject_name=render_request.subject_name,
        style_profile=config.style_profile,
        generation_backend=config.generation_backend,
        compositor_backend=config.compositor_backend,
        encoder_backend=config.encoder_backend,
        width=config.width,
        height=config.height,
        fps=config.fps,
        duration_seconds=config.duration_seconds,
        output_format=config.output_format,
        in_asset_cta_policy=render_request.in_asset_cta_policy,
        shots=shots,
        audio_profile=audio_profile,
        audio_cues=audio_cues,
        generation_commands=commands,
        generation_command_specs=command_specs,
        compositor_manifest=compositor_manifest,
        compositor_command_spec=_compositor_command_spec(config),
        finalization_command=finalization_command,
        finalization_command_spec=_finalization_command_spec(config),
        execution_notes=execution_notes,
    )
