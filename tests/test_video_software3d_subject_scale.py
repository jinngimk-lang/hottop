from __future__ import annotations

from hottop.video_software3d import project_point
from hottop.video_software3d_production import build_story_scene


PRIMARY_SUBJECT_PREFIXES = {
    1: ("witch-",),
    2: ("witch-",),
    3: ("witch-",),
    4: ("hero-",),
    5: ("hero-",),
}


def _primary_subject_height_ratio(shot_index: int) -> float:
    height = 640
    scene = build_story_scene(
        shot_index=shot_index,
        progress=0.5,
        width=360,
        height=height,
        story_profile="odyssey-witch-pigs",
    )
    prefixes = PRIMARY_SUBJECT_PREFIXES[shot_index]
    ys: list[float] = []
    for mesh in scene.meshes:
        if not mesh.name.startswith(prefixes):
            continue
        for vertex in mesh.vertices:
            projected = project_point(mesh.world_vertex(vertex), scene.camera)
            if projected is not None:
                ys.append(projected[1])
    assert ys, f"Odyssey shot {shot_index} has no projected primary subject"
    return (max(ys) - min(ys)) / height


def test_odyssey_primary_subjects_are_readable_on_mobile():
    """Cinematic key characters should not read as tiny figures in the 9:16 canvas."""

    for shot_index in range(1, 6):
        ratio = _primary_subject_height_ratio(shot_index)
        assert ratio >= 0.14, (shot_index, ratio)
