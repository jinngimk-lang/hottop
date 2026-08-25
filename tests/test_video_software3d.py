from pathlib import Path

import pytest

from hottop.video_software3d import (
    Camera3D,
    Mesh3D,
    Scene3D,
    Vec3,
    project_point,
    render_scene_frame,
)


def test_project_point_uses_perspective_depth():
    camera = Camera3D(width=320, height=180, focal_length=220.0, position=Vec3(0, 0, 0))

    near = project_point(Vec3(1, 0, 2), camera)
    far = project_point(Vec3(1, 0, 4), camera)

    assert near is not None and far is not None
    cx = camera.width / 2
    assert abs(near[0] - cx) > abs(far[0] - cx)


def test_render_scene_frame_changes_when_mesh_moves(tmp_path: Path):
    camera = Camera3D(width=160, height=90, focal_length=120.0, position=Vec3(0, 0, 0))
    mesh = Mesh3D.box(name="hero", center=Vec3(0, 0, 4), size=Vec3(1, 1, 1))
    scene = Scene3D(camera=camera, meshes=[mesh])

    first = tmp_path / "first.png"
    second = tmp_path / "second.png"
    render_scene_frame(scene, first)
    mesh.translate(Vec3(0.6, 0, 0))
    render_scene_frame(scene, second)

    assert first.read_bytes() != second.read_bytes()


def test_mesh_identity_is_stable_across_transforms():
    mesh = Mesh3D.box(name="odysseus", center=Vec3(0, 0, 4), size=Vec3(1, 2, 1))
    identity = mesh.identity_signature()

    mesh.translate(Vec3(1, 0.25, -0.5))
    mesh.rotate_y(0.4)

    assert mesh.identity_signature() == identity


def test_scene_rejects_duplicate_mesh_identity():
    camera = Camera3D(width=160, height=90, focal_length=120.0, position=Vec3(0, 0, 0))
    a = Mesh3D.box(name="hero", center=Vec3(0, 0, 4), size=Vec3(1, 1, 1))
    b = Mesh3D.box(name="hero", center=Vec3(2, 0, 4), size=Vec3(1, 1, 1))

    with pytest.raises(ValueError, match="duplicate mesh identity"):
        Scene3D(camera=camera, meshes=[a, b])
