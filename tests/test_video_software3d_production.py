import json
from pathlib import Path

from hottop.video_software3d_production import (
    build_story_scene,
    render_story_frame_sequence,
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
