from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import hottop.video_software3d_production as production


def _mesh_names(scene) -> set[str]:
    return {mesh.name for mesh in scene.meshes}


def test_sequence_mode_routes_odyssey_source_to_odyssey_geometry(monkeypatch, tmp_path):
    captured = []
    monkeypatch.setattr(production, "render_scene_frame", lambda scene, _path: captured.append(scene))

    production.render_story_frame_sequence(
        render_source=Path("examples/video/inkclaw-odyssey-witch-pigs.render.json"),
        output_dir=tmp_path / "frames",
        width=180,
        height=320,
        fps=1,
        seconds_per_shot=1.0,
    )

    assert len(captured) == 5
    first_names = _mesh_names(captured[0])
    second_names = _mesh_names(captured[1])
    fourth_names = _mesh_names(captured[3])
    assert "witch-body" in first_names
    assert any(name.startswith("sailor-") for name in first_names)
    assert any(name.startswith("pig-") for name in second_names)
    assert "hero-body" in fourth_names
    assert "young-cow-body" not in first_names


def test_shot_mode_reads_workspace_plan_topic_for_story_routing(monkeypatch, tmp_path):
    plan = {
        "schema_version": "hottop.video-plan.v1",
        "topic_id": "odyssey-witch-pigs",
        "shots": [{"index": 1}],
    }
    (tmp_path / "hottop-video-plan.json").write_text(json.dumps(plan), encoding="utf-8")
    captured = []
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(production, "render_scene_frame", lambda scene, _path: captured.append(scene))

    def fake_runner(args, **_kwargs):
        Path(args[-1]).write_bytes(b"fake-mp4")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    output = tmp_path / "shots" / "shot-001.mp4"
    production.render_story_shot_video(
        shot_index=1,
        output=output,
        duration_seconds=1.0,
        width=180,
        height=320,
        fps=2,
        runner=fake_runner,
    )

    assert output.is_file()
    assert captured
    names = _mesh_names(captured[0])
    assert "witch-body" in names
    assert any(name.startswith("sailor-") for name in names)
    assert "young-cow-body" not in names


def test_unknown_topic_falls_back_to_existing_cow_story(monkeypatch, tmp_path):
    plan = {
        "schema_version": "hottop.video-plan.v1",
        "topic_id": "unknown-generic-topic",
        "shots": [{"index": 1}],
    }
    (tmp_path / "hottop-video-plan.json").write_text(json.dumps(plan), encoding="utf-8")
    captured = []
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(production, "render_scene_frame", lambda scene, _path: captured.append(scene))

    def fake_runner(args, **_kwargs):
        Path(args[-1]).write_bytes(b"fake-mp4")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    production.render_story_shot_video(
        shot_index=1,
        output=tmp_path / "shot.mp4",
        duration_seconds=1.0,
        width=180,
        height=320,
        fps=2,
        runner=fake_runner,
    )

    names = _mesh_names(captured[0])
    assert "young-cow-body" in names
    assert "witch-body" not in names
