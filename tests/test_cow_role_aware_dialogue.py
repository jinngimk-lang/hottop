from pathlib import Path

from hottop.rendering import CreativeRenderRequest
from hottop.video_production import build_video_production_plan, load_video_production_config


def test_cow_flagship_preserves_speaker_and_delivery_through_video_plan() -> None:
    request = CreativeRenderRequest.model_validate_json(
        Path("examples/video/inkclaw-cow-snake.render.json").read_text(encoding="utf-8")
    )
    config = load_video_production_config(Path("config/video/anti-polish-software3d.yml"))

    assert [frame.speaker for frame in request.frames] == [
        "young-cow",
        "young-cow",
        "mother-cow",
        "young-cow",
        "mother-cow",
    ]
    assert all(frame.delivery for frame in request.frames)

    plan = build_video_production_plan(request, config)
    dialogue = [cue for cue in plan.audio_cues if cue.kind == "dialogue"]

    assert [cue.character for cue in dialogue] == [
        "young-cow",
        "young-cow",
        "mother-cow",
        "young-cow",
        "mother-cow",
    ]
    assert all(cue.delivery for cue in dialogue)
