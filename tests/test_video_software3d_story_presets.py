from __future__ import annotations

import json
from pathlib import Path

from hottop.rendering import CreativeRenderFrame, CreativeRenderRequest
from hottop.video_production import (
    VideoProductionConfig,
    build_video_production_plan,
    load_video_production_config,
)
from hottop.video_software3d_production import (
    ODYSSEY_PRESET,
    build_story_scene,
    resolve_story_preset_for_output,
)


def _odyssey_request() -> CreativeRenderRequest:
    frames = [
        ("Sailors eat at an original mythic witch banquet while manually coding at crude laptops.", "这活得干多久？", "crew"),
        ("The anonymous witch raises a cup; the sailors transform into blocky pigs but keep typing.", "手动流程？那你们慢慢干。", "witch"),
        ("An original returning sailor hero enters and sees pig-coders at the same banquet table.", "怎么全成同事了？", "hero"),
        ("The hero opens InkClawAgent and four crude agent blocks split Research, Write, Review and Code.", "算了，InkClawAgent。", "hero"),
        ("The pigs stop typing as the completed work appears; one pig looks confused.", "那我变猪的意义是？", "pig"),
        ("The hero deadpans while everyone remains in the same room.", "剧情需要。", "hero"),
    ]
    return CreativeRenderRequest(
        topic_id=ODYSSEY_PRESET,
        topic_title="original mythic witch pigs workflow meme",
        subject_name="InkClawAgent",
        expression_form="faux-film-still",
        visual_medium="animation-low-poly",
        genre_treatment="original low-budget mythic 3D comedy",
        distribution_mode="motion",
        in_asset_cta_policy="no-destination",
        motion_continuity_required=True,
        category_default="manual serial workflow",
        deleted_constraint="one person manually performs every stage",
        new_competition_axis="time to coordinated useful work",
        bridge_type="action-motion",
        bridge="manual repetitive work literally turns the crew into pigs until multi-agent delegation breaks the spell",
        frames=[
            CreativeRenderFrame(
                index=index,
                scene=scene,
                caption=caption,
                intent="story",
                speaker=speaker,
                delivery="deadpan Mandarin",
            )
            for index, (scene, caption, speaker) in enumerate(frames, start=1)
        ],
        master_prompt="original public-domain mythic voyage grammar, anonymous characters, low-poly cinematic meme",
        negative_prompt="actor likeness, copied movie frame, official costume, official production design, copyrighted soundtrack",
        punchlines=["剧情需要。", "多 Agent 协作，先把活干完。"],
        risk_flags=["public-domain myth motif only", "original staging and character geometry"],
        claim_status="satire",
    )


def _odyssey_config() -> VideoProductionConfig:
    return VideoProductionConfig.model_validate(
        {
            "name": "odyssey-software3d",
            "style_profile": "anti-polish",
            "roughness_score": 62,
            "generation_backend": "software3d",
            "compositor_backend": "moviepy",
            "encoder_backend": "ffmpeg",
            "width": 360,
            "height": 640,
            "fps": 12,
            "duration_seconds": 12,
            "shot_policy": {"min_shot_seconds": 1, "max_shot_seconds": 2},
            "audio": {"bgm_style": "original cheap mythic comedy", "foley_style": "blunt transformation Foley"},
            "text": {},
            "moviepy": {"shot_dir": "shots", "composite_name": "composite.mp4"},
            "ffmpeg": {
                "video_codec": "libx264",
                "audio_codec": "aac",
                "pixel_format": "yuv420p",
                "movflags": "+faststart",
            },
        }
    )


def test_software3d_resolves_story_preset_from_render_topic_in_materialized_plan(tmp_path):
    plan = build_video_production_plan(_odyssey_request(), _odyssey_config())
    plan_path = tmp_path / "hottop-video-plan.json"
    plan_path.write_text(plan.model_dump_json(indent=2) + "\n", encoding="utf-8")
    output = tmp_path / "shots" / "shot-001.mp4"

    assert resolve_story_preset_for_output(output) == ODYSSEY_PRESET


def test_odyssey_story_preset_changes_geometry_across_transformation():
    before = build_story_scene(
        preset=ODYSSEY_PRESET,
        shot_index=1,
        progress=0.5,
        width=180,
        height=320,
    )
    after = build_story_scene(
        preset=ODYSSEY_PRESET,
        shot_index=2,
        progress=0.9,
        width=180,
        height=320,
    )

    before_names = {mesh.name for mesh in before.meshes}
    after_names = {mesh.name for mesh in after.meshes}
    assert any(name.startswith("crew-") for name in before_names)
    assert any(name.startswith("pig-") for name in after_names)
    assert "banquet-table" in before_names & after_names
    assert "witch-body" in before_names & after_names


def test_cow_snake_story_remains_default_for_backward_compatibility():
    scene = build_story_scene(shot_index=1, progress=0.5, width=180, height=320)
    names = {mesh.name for mesh in scene.meshes}
    assert "young-cow-body" in names
    assert "laptop-screen" in names


def test_checked_in_odyssey_software3d_assets_build_full_audio_video_plan():
    root = Path(__file__).resolve().parents[1]
    render_path = root / "examples/video/inkclaw-odyssey-witch-pigs-software3d.render.json"
    config_path = root / "config/video/odyssey-software3d.yml"

    raw_render = json.loads(render_path.read_text(encoding="utf-8"))
    request = CreativeRenderRequest.model_validate(raw_render)
    config = load_video_production_config(config_path)
    plan = build_video_production_plan(request, config)

    assert request.topic_id == ODYSSEY_PRESET
    assert len(plan.shots) == 6
    assert plan.duration_seconds == 12
    assert plan.generation_backend == "software3d"
    assert plan.audio_profile is not None
    assert plan.audio_profile.voice_backend == "espeak"
    assert plan.audio_profile.music_backend == "synthetic"
    assert plan.audio_profile.sfx_backend == "procedural"
    dialogue = [cue for cue in plan.audio_cues if cue.kind == "dialogue"]
    assert len(dialogue) == 6
    assert {cue.character for cue in dialogue} >= {"crew", "witch", "hero", "pig"}
