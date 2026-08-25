from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import hottop.video_software3d_production as production
from hottop.video_software3d_production import (
    COW_STORY_PROFILE,
    ODYSSEY_STORY_PROFILE,
    build_story_scene,
    story_profile_for_topic,
)


def _mesh_names(scene) -> set[str]:
    return {mesh.name for mesh in scene.meshes}


def test_known_topics_resolve_to_supported_story_profiles() -> None:
    assert story_profile_for_topic("inkclaw-anti-polish-cow-snake") == COW_STORY_PROFILE
    assert story_profile_for_topic("odyssey-witch-pigs") == ODYSSEY_STORY_PROFILE


def test_unknown_software3d_topic_fails_closed() -> None:
    with pytest.raises(ValueError, match="unsupported software 3d story topic"):
        story_profile_for_topic("future-story-without-renderer")


def test_shot_mode_reads_plan_from_output_workspace_not_current_working_directory(
    monkeypatch,
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "odyssey-workspace"
    shots = workspace / "shots"
    shots.mkdir(parents=True)
    (workspace / "hottop-video-plan.json").write_text(
        json.dumps(
            {
                "schema_version": "hottop.video-plan.v1",
                "topic_id": "odyssey-witch-pigs",
            }
        ),
        encoding="utf-8",
    )
    unrelated_cwd = tmp_path / "project-root"
    unrelated_cwd.mkdir()
    monkeypatch.chdir(unrelated_cwd)

    captured = []
    monkeypatch.setattr(production, "render_scene_frame", lambda scene, _path: captured.append(scene))

    def fake_runner(args, **_kwargs):
        Path(args[-1]).write_bytes(b"fake-mp4")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    production.render_story_shot_video(
        shot_index=2,
        output=shots / "shot-002.mp4",
        duration_seconds=1.0,
        width=180,
        height=320,
        fps=2,
        runner=fake_runner,
    )

    assert captured
    names = _mesh_names(captured[0])
    assert "hall-floor" in names
    assert any(name.startswith("pig-") for name in names)
    assert "young-cow-body" not in names


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

    cow_names = _mesh_names(cow)
    odyssey_names = _mesh_names(odyssey)
    assert "young-cow-body" in cow_names
    assert "hall-floor" in odyssey_names
    assert any(name.startswith("pig-") for name in odyssey_names)
    assert "young-cow-body" not in odyssey_names
