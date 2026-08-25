from __future__ import annotations

import json
from pathlib import Path

import pytest

from hottop.rendering import CreativeRenderRequest
from hottop.video_production import build_video_production_plan, load_video_production_config
from hottop.video_software3d_production import (
    COW_STORY_PROFILE,
    ODYSSEY_STORY_PROFILE,
    build_story_scene,
    story_profile_for_topic,
)

ROOT = Path(__file__).resolve().parents[1]


def _plan(render_name: str, config_name: str):
    render = CreativeRenderRequest.model_validate(
        json.loads((ROOT / "examples" / "video" / render_name).read_text(encoding="utf-8"))
    )
    config = load_video_production_config(ROOT / "config" / "video" / config_name)
    return build_video_production_plan(render, config)


def test_odyssey_plan_carries_explicit_story_profile_into_every_shot_command() -> None:
    plan = _plan("inkclaw-odyssey-witch-pigs.render.json", "cinematic-software3d.yml")

    assert plan.topic_id == ODYSSEY_STORY_PROFILE
    assert len(plan.generation_command_specs) == 5
    for spec in plan.generation_command_specs:
        profile_index = spec.args.index("--story-profile")
        assert spec.args[profile_index + 1] == ODYSSEY_STORY_PROFILE


def test_cow_plan_carries_explicit_story_profile_into_every_shot_command() -> None:
    plan = _plan("inkclaw-cow-snake.render.json", "anti-polish-software3d.yml")

    assert story_profile_for_topic(plan.topic_id) == COW_STORY_PROFILE
    for spec in plan.generation_command_specs:
        profile_index = spec.args.index("--story-profile")
        assert spec.args[profile_index + 1] == COW_STORY_PROFILE


def test_unknown_software3d_topic_fails_closed() -> None:
    with pytest.raises(ValueError, match="unsupported software 3d story topic"):
        story_profile_for_topic("future-story-without-renderer")


def test_story_profiles_build_materially_distinct_worlds() -> None:
    cow = build_story_scene(
        shot_index=2,
        progress=0.5,
        width=160,
        height=90,
        story_profile=COW_STORY_PROFILE,
    )
    odyssey = build_story_scene(
        shot_index=2,
        progress=0.5,
        width=160,
        height=90,
        story_profile=ODYSSEY_STORY_PROFILE,
    )

    cow_names = {mesh.name for mesh in cow.meshes}
    odyssey_names = {mesh.name for mesh in odyssey.meshes}
    assert "young-cow-body" in cow_names
    assert "hall-floor" in odyssey_names
    assert any(name.startswith("pig-") for name in odyssey_names)
    assert "young-cow-body" not in odyssey_names
