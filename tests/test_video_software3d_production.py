import json
import subprocess
from pathlib import Path

import pytest

from hottop.video_software3d_production import (
    build_story_scene,
    render_story_frame_sequence,
    render_story_shot_video,
)


def _render_source(tmp_path: Path) -> Path:
    path = tmp_path / "render.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": "hottop.render.v2",
                "topic_id": "inkclaw-anti-polish-cow-snake",
                "frames": [
                    {"index": 1, "scene": "cow types while snake enters", "caption": "哎呀！"},
                    {"index": 2, "scene": "cow recoils", "caption": "妈——！"},
                    {"index": 3, "scene": "mother cow enters", "caption": "用 InkClawAgent。"},
                    {"index": 4, "scene": "snake loosens", "caption": "这么直接？"},
                    {"index": 5, "scene": "snake retreats", "caption": "别被蛇绊住。"},
                ],
            }
        ),
        encoding="utf-8",
    )
    return path


def _write_workspace_plan(root: Path, topic_id: str = "inkclaw-anti-polish-cow-snake") -> None:
    (root / "hottop-video-plan.json").write_text(
        json.dumps(
            {
                "schema_version": "hottop.video-plan.v1",
                "topic_id": topic_id,
            }
        ),
        encoding="utf-8",
    )


def test_story_scene_keeps_hero_identity_across_shots():
    first = build_story_scene(shot_index=1, progress=0.2, width=160, height=90)
    last = build_story_scene(shot_index=5, progress=0.8, width=160, height=90)

    first_hero = next(mesh for mesh in first.meshes if mesh.name == "young-cow-body")
    last_hero = next(mesh for mesh in last.meshes if mesh.name == "young-cow-body")

    assert first_hero.identity_signature() == last_hero.identity_signature()


def test_story_scene_changes_action_state_across_shots():
    first = build_story_scene(shot_index=1, progress=0.5, width=160, height=90)
    rescue = build_story_scene(shot_index=4, progress=0.5, width=160, height=90)

    first_snake = next(mesh for mesh in first.meshes if mesh.name == "snake-segment-0")
    rescue_snake = next(mesh for mesh in rescue.meshes if mesh.name == "snake-segment-0")

    assert first_snake.position != rescue_snake.position


def test_render_story_frame_sequence_writes_real_png_frames(tmp_path: Path):
    frames = render_story_frame_sequence(
        render_source=_render_source(tmp_path),
        output_dir=tmp_path / "frames",
        width=160,
        height=90,
        fps=4,
        seconds_per_shot=0.5,
    )

    assert len(frames) == 10
    assert all(path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n") for path in frames)
    assert len({path.read_bytes() for path in frames}) > 5


def test_render_story_shot_video_encodes_real_frame_sequence_and_cleans_workspace(tmp_path: Path):
    _write_workspace_plan(tmp_path)
    output = tmp_path / "shots" / "shot-001.mp4"
    calls: list[list[str]] = []

    def runner(argv, **kwargs):
        calls.append(list(argv))
        Path(argv[-1]).write_bytes(b"fake-mp4")
        return subprocess.CompletedProcess(argv, 0, "", "")

    result = render_story_shot_video(
        shot_index=1,
        output=output,
        duration_seconds=0.5,
        width=160,
        height=90,
        fps=4,
        runner=runner,
    )

    assert result == output
    assert output.read_bytes() == b"fake-mp4"
    assert calls and calls[0][0] == "ffmpeg"
    assert "libx264" in calls[0]
    assert "yuv420p" in calls[0]
    assert "+faststart" in calls[0]
    assert not output.with_suffix(".frames").exists()


def test_render_story_shot_video_fails_closed_without_workspace_plan(tmp_path: Path):
    output = tmp_path / "run" / "shots" / "shot-001.mp4"

    def runner(argv, **kwargs):
        Path(argv[-1]).write_bytes(b"fake-mp4")
        return subprocess.CompletedProcess(argv, 0, "", "")

    with pytest.raises(ValueError, match="workspace plan"):
        render_story_shot_video(
            shot_index=1,
            output=output,
            duration_seconds=0.5,
            width=160,
            height=90,
            fps=4,
            runner=runner,
        )
