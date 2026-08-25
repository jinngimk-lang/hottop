import shutil
from pathlib import Path

from hottop.rendering import CreativeRenderFrame, CreativeRenderRequest
from hottop.video_execution import run_video_production
from hottop.video_moviepy import build_moviepy_timeline
from hottop.video_production import build_video_production_plan, load_video_production_config


def _odyssey_request() -> CreativeRenderRequest:
    return CreativeRenderRequest(
        topic_id="odyssey-witch-pigs",
        topic_title="witch turns coding crew into pigs",
        subject_name="InkClawAgent",
        expression_form="faux-film-still",
        visual_medium="live-action-cinematic",
        genre_treatment="original mythic cinematic meme with controlled roughness",
        distribution_mode="motion",
        in_asset_cta_policy="no-destination",
        motion_continuity_required=True,
        category_default="agent work starts with setup ceremony",
        deleted_constraint="remove deployment ceremony before useful work",
        new_competition_axis="time to useful work",
        bridge_type="role",
        bridge="a mythic rescue turns workflow friction into a transformation curse",
        frames=[
            CreativeRenderFrame(
                index=1,
                scene="Sailors code while eating at an original witch's banquet table.",
                caption="这需求再改一下就行……",
                intent="setup",
                speaker="crew",
                delivery="tired, distracted, natural Mandarin",
            ),
            CreativeRenderFrame(
                index=2,
                scene="The witch casts a comic curse and the sailors become pigs around the laptops.",
                caption="先把环境、依赖、部署、Token 配好再说。",
                intent="obstruction",
                speaker="witch",
                delivery="calm, ominous, deadpan Mandarin",
            ),
            CreativeRenderFrame(
                index=3,
                scene="An original returning sailor hero arrives and opens InkClawAgent to break the curse.",
                caption="不用。打开 InkClawAgent，直接干活。",
                intent="solution and punchline",
                speaker="hero",
                delivery="grounded, confident, understated Mandarin",
            ),
        ],
        master_prompt="original mythic Mediterranean cinematic scene, consistent cast and location",
        negative_prompt="copied film frame, actor likeness, official character design, glossy AI feature cards",
        punchlines=["先把活干完，再谈史诗。"],
        risk_flags=["original staging and cast only"],
        claim_status="satire",
    )


def test_video_plan_carries_voice_music_and_sfx_profiles():
    config = load_video_production_config(Path("config/video/anti-polish-direct.yml"))
    plan = build_video_production_plan(_odyssey_request(), config)

    assert config.audio.voice_backend == "espeak"
    assert config.audio.voice_profile == "rough-mandarin-dialogue"
    assert config.audio.music_backend == "synthetic"
    assert config.audio.music_profile == "cheap-comedy-original"
    assert config.audio.sfx_backend == "procedural"
    assert config.audio.sfx_profile == "blunt-comedic-foley"
    assert config.audio.original_music_only is True

    assert plan.audio_profile.voice_backend == "espeak"
    assert plan.audio_profile.music_backend == "synthetic"
    assert plan.audio_profile.sfx_backend == "procedural"
    assert plan.audio_profile.original_music_only is True

    dialogue = [cue for cue in plan.audio_cues if cue.kind == "dialogue"]
    assert [cue.character for cue in dialogue] == ["crew", "witch", "hero"]
    assert all(cue.voice_profile == "rough-mandarin-dialogue" for cue in dialogue)
    assert all(cue.delivery for cue in dialogue)


def _voice_which(real_which, *, espeak_ng: str | None, espeak: str | None):
    def resolve(name: str):
        if name == "espeak-ng":
            return espeak_ng
        if name == "espeak":
            return espeak
        return real_which(name)

    return resolve


def test_video_run_prefers_espeak_ng_cmn_for_mandarin(monkeypatch, tmp_path):
    config = load_video_production_config(Path("config/video/anti-polish-direct.yml"))
    real_which = shutil.which
    monkeypatch.setattr(
        "hottop.video_execution.shutil.which",
        _voice_which(real_which, espeak_ng="/usr/bin/espeak-ng", espeak="/usr/bin/espeak"),
    )

    def forbidden_run(*_args, **_kwargs):
        raise AssertionError("dry-run must not spawn external processes")

    monkeypatch.setattr("hottop.video_execution.subprocess.run", forbidden_run)
    result = run_video_production(
        _odyssey_request(),
        config,
        output_dir=tmp_path / "run",
        project_root=Path("."),
        execute=False,
    )

    audio_commands = [command for command in result.runtime_commands if command.stage == "audio"]
    assert len(audio_commands) == 3
    assert all(command.program == "/usr/bin/espeak-ng" for command in audio_commands)
    assert all(command.args[:2] == ["-v", "cmn"] for command in audio_commands)


def test_video_run_keeps_legacy_espeak_fallback(monkeypatch, tmp_path):
    config = load_video_production_config(Path("config/video/anti-polish-direct.yml"))
    real_which = shutil.which
    monkeypatch.setattr(
        "hottop.video_execution.shutil.which",
        _voice_which(real_which, espeak_ng=None, espeak="/usr/bin/espeak"),
    )

    def forbidden_run(*_args, **_kwargs):
        raise AssertionError("dry-run must not spawn external processes")

    monkeypatch.setattr("hottop.video_execution.subprocess.run", forbidden_run)
    result = run_video_production(
        _odyssey_request(),
        config,
        output_dir=tmp_path / "run",
        project_root=Path("."),
        execute=False,
    )

    audio_commands = [command for command in result.runtime_commands if command.stage == "audio"]
    assert len(audio_commands) == 3
    assert all(command.program == "/usr/bin/espeak" for command in audio_commands)
    assert all(command.args[:2] == ["-v", "zh"] for command in audio_commands)


def test_video_run_materializes_audio_stage_and_moviepy_dialogue_tracks(monkeypatch, tmp_path):
    config = load_video_production_config(Path("config/video/anti-polish-direct.yml"))
    real_which = shutil.which
    monkeypatch.setattr(
        "hottop.video_execution.shutil.which",
        _voice_which(real_which, espeak_ng=None, espeak="/usr/bin/espeak"),
    )

    def forbidden_run(*_args, **_kwargs):
        raise AssertionError("dry-run must not spawn external processes")

    monkeypatch.setattr("hottop.video_execution.subprocess.run", forbidden_run)
    result = run_video_production(
        _odyssey_request(),
        config,
        output_dir=tmp_path / "run",
        project_root=Path("."),
        execute=False,
    )

    assert Path(result.audio_dir).is_dir()
    audio_commands = [command for command in result.runtime_commands if command.stage == "audio"]
    assert len(audio_commands) == 3
    assert all(command.program == "/usr/bin/espeak" for command in audio_commands)
    assert all("-w" in command.args for command in audio_commands)

    plan = build_video_production_plan(_odyssey_request(), config)
    timeline = build_moviepy_timeline(
        plan,
        shots_dir=tmp_path / "shots",
        audio_dir=tmp_path / "audio",
    )
    assert [Path(track.source).name for track in timeline.dialogue_tracks] == [
        "dialogue-001.wav",
        "dialogue-002.wav",
        "dialogue-003.wav",
    ]
    assert [track.character for track in timeline.dialogue_tracks] == ["crew", "witch", "hero"]
    assert timeline.generate_synthetic_bgm is True
    assert timeline.generate_procedural_sfx is True
