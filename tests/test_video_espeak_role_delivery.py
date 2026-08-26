from pathlib import Path

from hottop.rendering import CreativeRenderRequest
from hottop.video_execution import run_video_production
from hottop.video_production import load_video_production_config


def _only_espeak_ng(name: str) -> str | None:
    binaries = {
        "espeak-ng": "/usr/bin/espeak-ng",
        "ffmpeg": "/usr/bin/ffmpeg",
    }
    return binaries.get(name)


def _flag_value(args: list[str], flag: str) -> int:
    return int(args[args.index(flag) + 1])


def test_espeak_fallback_reflects_character_and_delivery_without_external_models(
    monkeypatch, tmp_path
):
    request = CreativeRenderRequest.model_validate_json(
        Path("examples/video/inkclaw-cow-snake.render.json").read_text(encoding="utf-8")
    )
    config = load_video_production_config(Path("config/video/anti-polish-software3d.yml"))
    monkeypatch.setattr("hottop.video_execution.shutil.which", _only_espeak_ng)

    result = run_video_production(
        request,
        config,
        output_dir=tmp_path / "run",
        project_root=Path("."),
        execute=False,
    )

    audio_commands = [command for command in result.runtime_commands if command.stage == "audio"]
    dialogue_frames = [frame for frame in request.frames if frame.speaker]
    assert len(audio_commands) == len(dialogue_frames)
    assert all(command.program == "/usr/bin/espeak-ng" for command in audio_commands)
    assert all("-p" in command.args for command in audio_commands)

    pitches_by_speaker: dict[str, set[int]] = {}
    speeds_by_speaker: dict[str, set[int]] = {}
    for frame, command in zip(dialogue_frames, audio_commands, strict=True):
        speaker = frame.speaker or ""
        pitches_by_speaker.setdefault(speaker, set()).add(_flag_value(command.args, "-p"))
        speeds_by_speaker.setdefault(speaker, set()).add(_flag_value(command.args, "-s"))

    # Character identity should remain stable across shots while distinct roles stay audible.
    assert len(pitches_by_speaker["young-cow"]) == 1
    assert len(pitches_by_speaker["mother-cow"]) == 1
    young_pitch = next(iter(pitches_by_speaker["young-cow"]))
    mother_pitch = next(iter(pitches_by_speaker["mother-cow"]))
    assert abs(young_pitch - mother_pitch) >= 6

    # Delivery metadata should affect cadence instead of being silently discarded.
    assert len(speeds_by_speaker["young-cow"]) >= 2
