from pathlib import Path

from hottop.rendering import CreativeRenderFrame, CreativeRenderRequest
from hottop.video_execution import inspect_video_environment, run_video_production
from hottop.video_production import load_video_production_config


def _request() -> CreativeRenderRequest:
    return CreativeRenderRequest(
        topic_id="espeak-ng-runtime",
        topic_title="Mandarin fallback runtime",
        subject_name="InkClawAgent",
        expression_form="faux-film-still",
        visual_medium="animation-low-poly",
        genre_treatment="controlled badness rough 3D comedy",
        distribution_mode="motion",
        in_asset_cta_policy="no-destination",
        motion_continuity_required=True,
        bridge_type="role",
        bridge="the local voice backend carries the dialogue",
        frames=[
            CreativeRenderFrame(
                index=1,
                scene="A rough 3D cow speaks in a workshop.",
                caption="妈——！",
                intent="dialogue",
            )
        ],
        master_prompt="original low-poly animation",
        negative_prompt="copied character, glossy ad",
        punchlines=["别被蛇绊住。"],
        risk_flags=["original staging only"],
        claim_status="satire",
    )


def _only_espeak_ng(name: str) -> str | None:
    binaries = {
        "espeak-ng": "/usr/bin/espeak-ng",
        "ffmpeg": "/usr/bin/ffmpeg",
    }
    return binaries.get(name)


def test_espeak_voice_readiness_prefers_native_espeak_ng(monkeypatch):
    config = load_video_production_config(Path("config/video/anti-polish-software3d.yml"))
    monkeypatch.setattr("hottop.video_execution.shutil.which", _only_espeak_ng)

    status = inspect_video_environment(config, project_root=Path("."))

    assert status.voice is not None
    assert status.voice.ready is True
    assert "espeak-ng=/usr/bin/espeak-ng" in status.voice.checks


def test_espeak_runtime_uses_native_espeak_ng_when_available(monkeypatch, tmp_path):
    config = load_video_production_config(Path("config/video/anti-polish-software3d.yml"))
    monkeypatch.setattr("hottop.video_execution.shutil.which", _only_espeak_ng)

    result = run_video_production(
        _request(),
        config,
        output_dir=tmp_path / "run",
        project_root=Path("."),
        execute=False,
    )

    audio_commands = [command for command in result.runtime_commands if command.stage == "audio"]
    assert audio_commands
    assert all(command.program == "/usr/bin/espeak-ng" for command in audio_commands)
