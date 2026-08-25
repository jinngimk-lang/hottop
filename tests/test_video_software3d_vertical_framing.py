# ruff: noqa: I001
from hottop.video_software3d import project_point
from hottop.video_software3d_production import build_story_scene


SUBJECT_PREFIXES = {
    "cow-snake": (
        "young-cow-",
        "mother-cow-",
        "snake-segment-",
        "agent-",
        "deploy-box",
    ),
    "odyssey-witch-pigs": (
        "sailor-",
        "pig-",
        "witch-",
        "hero-",
        "magic-",
        "inkclaw-",
        "harmless-smoke-",
    ),
}


def _projected_subject_bounds(
    story_profile: str,
    shot_index: int,
) -> tuple[float, float]:
    height = 640
    scene = build_story_scene(
        shot_index=shot_index,
        progress=0.5,
        width=360,
        height=height,
        story_profile=story_profile,
    )
    prefixes = SUBJECT_PREFIXES[story_profile]
    ys: list[float] = []
    for mesh in scene.meshes:
        if not mesh.name.startswith(prefixes):
            continue
        for vertex in mesh.vertices:
            projected = project_point(mesh.world_vertex(vertex), scene.camera)
            if projected is not None:
                ys.append(projected[1])
    assert ys, f"{story_profile} shot {shot_index} has no projected narrative subject"
    return min(ys) / height, max(ys) / height


def _assert_story_uses_mobile_canvas(story_profile: str) -> None:
    for shot_index in range(1, 6):
        top, bottom = _projected_subject_bounds(story_profile, shot_index)
        assert top <= 0.35, (story_profile, shot_index, top, bottom)
        assert bottom <= 0.72, (story_profile, shot_index, top, bottom)


def test_cow_story_subjects_use_the_mobile_canvas():
    """Anti-Polish narrative subjects should not sit below an empty upper third."""

    _assert_story_uses_mobile_canvas("cow-snake")


def test_odyssey_story_subjects_use_the_mobile_canvas():
    """Cinematic narrative subjects should not sit below an empty upper third."""

    _assert_story_uses_mobile_canvas("odyssey-witch-pigs")
