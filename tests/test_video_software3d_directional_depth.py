from hottop.video_software3d_odyssey import build_odyssey_story_scene
from hottop.video_software3d_production import build_story_scene


def test_lower_roughness_odyssey_enables_directional_depth_without_changing_anti_polish_baseline():
    cow = build_story_scene(shot_index=1, progress=0.5, width=160, height=90)
    odyssey = build_odyssey_story_scene(shot_index=1, progress=0.5, width=160, height=90)

    assert cow.directional_shading_strength == 0.0
    assert odyssey.directional_shading_strength >= 0.3


def test_odyssey_directional_depth_uses_explicit_light_direction():
    odyssey = build_odyssey_story_scene(shot_index=2, progress=0.5, width=160, height=90)

    assert odyssey.light_direction.z < 0
    assert odyssey.light_direction.y > 0
