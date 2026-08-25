import math

import pytest

from hottop.video_software3d import project_point
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
