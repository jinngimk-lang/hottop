import math
from pathlib import Path

import pytest
from PIL import Image, ImageChops, ImageStat

from hottop.video_software3d import project_point, render_scene_frame
from hottop.video_software3d_production import build_story_scene


@pytest.mark.parametrize(
    ("story_profile", "anchor_name"),
    [
        ("cow-snake", "laptop-screen"),
        ("odyssey-witch-pigs", "long-table"),
    ],
)
def test_software3d_shots_have_perceptible_camera_motion(story_profile: str, anchor_name: str):
    """The deterministic baseline must read as motion, not five almost-static cards."""

    for shot_index in range(1, 6):
        start = build_story_scene(
            shot_index=shot_index,
            progress=0.0,
            width=360,
            height=640,
            story_profile=story_profile,
        )
        end = build_story_scene(
            shot_index=shot_index,
            progress=1.0,
            width=360,
            height=640,
            story_profile=story_profile,
        )
        start_anchor = next(mesh for mesh in start.meshes if mesh.name == anchor_name)
        end_anchor = next(mesh for mesh in end.meshes if mesh.name == anchor_name)
        start_screen = project_point(start_anchor.position, start.camera)
        end_screen = project_point(end_anchor.position, end.camera)

        assert start_screen is not None
        assert end_screen is not None
        displacement = math.hypot(
            end_screen[0] - start_screen[0],
            end_screen[1] - start_screen[1],
        )
        assert displacement >= 18.0, (
            f"{story_profile} shot {shot_index} only moves a stable scene anchor "
            f"{displacement:.2f}px; the baseline should have clearly perceptible camera motion"
        )


@pytest.mark.parametrize(
    ("story_profile", "minimum_dolly"),
    [
        ("cow-snake", 0.40),
        ("odyssey-witch-pigs", 0.25),
    ],
)
def test_software3d_motion_changes_scene_scale_with_style_routed_dolly(
    story_profile: str,
    minimum_dolly: float,
):
    """Camera motion must affect the whole frame, not only slide it sideways."""

    for shot_index in range(1, 6):
        start = build_story_scene(
            shot_index=shot_index,
            progress=0.0,
            width=360,
            height=640,
            story_profile=story_profile,
        )
        end = build_story_scene(
            shot_index=shot_index,
            progress=1.0,
            width=360,
            height=640,
            story_profile=story_profile,
        )

        assert abs(end.camera.position.z - start.camera.position.z) >= minimum_dolly


def _sample_scene_motion(*, story_profile: str, shot_index: int, output_dir: Path) -> tuple[float, float]:
    sampled: list[Image.Image] = []
    for sample_index in range(9):
        progress = sample_index / 8
        scene = build_story_scene(
            shot_index=shot_index,
            progress=progress,
            width=360,
            height=640,
            story_profile=story_profile,
        )
        path = output_dir / f"{story_profile}-{shot_index}-{sample_index}.png"
        render_scene_frame(scene, path)
        with Image.open(path) as image:
            sampled.append(image.convert("L").resize((96, 54)))

    deltas: list[float] = []
    for previous, current in zip(sampled, sampled[1:], strict=False):
        difference = ImageChops.difference(previous, current)
        deltas.append(ImageStat.Stat(difference).mean[0])
    mean_delta = sum(deltas) / len(deltas)
    duplicate_ratio = sum(delta <= 1.0 for delta in deltas) / len(deltas)
    return mean_delta, duplicate_ratio


@pytest.mark.parametrize("story_profile", ["cow-snake", "odyssey-witch-pigs"])
def test_software3d_rendered_pixels_meet_perceptible_motion_gate(
    story_profile: str,
    tmp_path: Path,
):
    """Rendered pixels must pass the same perceptible-motion policy used for generated video."""

    for shot_index in range(1, 6):
        mean_delta, duplicate_ratio = _sample_scene_motion(
            story_profile=story_profile,
            shot_index=shot_index,
            output_dir=tmp_path,
        )
        assert mean_delta >= 2.0, (
            f"{story_profile} shot {shot_index} mean motion {mean_delta:.3f} is below 2.0"
        )
        assert duplicate_ratio <= 0.60, (
            f"{story_profile} shot {shot_index} duplicate ratio {duplicate_ratio:.3f} exceeds 0.60"
        )
