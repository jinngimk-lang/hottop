from __future__ import annotations

import math

from .video_software3d import Camera3D, Mesh3D, Scene3D, Vec3


def _box(
    name: str,
    center: Vec3,
    size: Vec3,
    color: tuple[int, int, int],
) -> Mesh3D:
    return Mesh3D.box(name=name, center=center, size=size, base_color=color)


def _person_parts(
    prefix: str,
    *,
    x: float,
    y: float,
    z: float,
    body_color: tuple[int, int, int],
    head_color: tuple[int, int, int] = (184, 139, 103),
    scale: float = 1.0,
) -> list[Mesh3D]:
    return [
        _box(
            f"{prefix}-body",
            Vec3(x, y, z),
            Vec3(0.62 * scale, 1.05 * scale, 0.46 * scale),
            body_color,
        ),
        _box(
            f"{prefix}-head",
            Vec3(x, y + 0.82 * scale, z - 0.04 * scale),
            Vec3(0.48 * scale, 0.48 * scale, 0.44 * scale),
            head_color,
        ),
    ]


def _pig_parts(prefix: str, *, x: float, y: float, z: float, scale: float = 1.0) -> list[Mesh3D]:
    pink = (212, 142, 138)
    return [
        _box(
            f"{prefix}-body",
            Vec3(x, y - 0.12 * scale, z),
            Vec3(0.88 * scale, 0.72 * scale, 0.62 * scale),
            pink,
        ),
        _box(
            f"{prefix}-head",
            Vec3(x, y + 0.46 * scale, z - 0.08 * scale),
            Vec3(0.62 * scale, 0.56 * scale, 0.55 * scale),
            pink,
        ),
        _box(
            f"{prefix}-snout",
            Vec3(x, y + 0.34 * scale, z - 0.42 * scale),
            Vec3(0.38 * scale, 0.22 * scale, 0.18 * scale),
            (232, 174, 164),
        ),
    ]


def _hall_geometry(progress: float) -> list[Mesh3D]:
    meshes = [
        _box("hall-floor", Vec3(0, -1.72, 7.2), Vec3(7.4, 0.24, 8.5), (84, 62, 48)),
        _box("hall-back-wall", Vec3(0, 1.0, 10.0), Vec3(7.4, 5.6, 0.24), (103, 78, 60)),
        _box("long-table", Vec3(-0.15, -0.72, 6.2), Vec3(4.8, 0.28, 1.20), (126, 85, 55)),
        _box("hall-door", Vec3(2.75, 0.15, 9.62), Vec3(1.35, 3.7, 0.18), (62, 48, 40)),
    ]
    for index, x in enumerate((-1.55, -0.15, 1.25)):
        meshes.extend(
            [
                _box(
                    f"laptop-{index}-base",
                    Vec3(x, -0.45, 5.72),
                    Vec3(0.82, 0.08, 0.48),
                    (69, 73, 72),
                ),
                _box(
                    f"laptop-{index}-screen",
                    Vec3(x, -0.07, 5.98),
                    Vec3(0.82, 0.60, 0.08),
                    (56, 105, 96),
                ),
                _box(
                    f"clay-bowl-{index}",
                    Vec3(x + 0.42, -0.43, 5.55),
                    Vec3(0.34, 0.12, 0.34),
                    (150, 99, 66),
                ),
            ]
        )
    for index, x in enumerate((-2.75, 2.35)):
        flame = 0.10 + 0.03 * math.sin(progress * math.pi * 2 + index)
        meshes.extend(
            [
                _box(
                    f"candle-{index}",
                    Vec3(x, -0.12, 7.95),
                    Vec3(0.12, 0.76, 0.12),
                    (198, 169, 112),
                ),
                _box(
                    f"candle-flame-{index}",
                    Vec3(x, 0.34 + flame, 7.92),
                    Vec3(0.18, 0.28, 0.12),
                    (244, 170, 76),
                ),
            ]
        )
    return meshes


def _witch(progress: float, *, foreground: bool) -> list[Mesh3D]:
    x = 1.95 if not foreground else 1.45 - progress * 0.20
    y = 0.10 if not foreground else 0.05
    z = 7.55 if not foreground else 6.45
    parts = _person_parts(
        "witch",
        x=x,
        y=y,
        z=z,
        body_color=(92, 58, 96),
        head_color=(174, 124, 98),
        scale=1.06,
    )
    parts.append(
        _box(
            "witch-cloak",
            Vec3(x, y - 0.58, z + 0.08),
            Vec3(0.92, 0.75, 0.58),
            (76, 48, 80),
        )
    )
    if foreground:
        parts.append(
            _box(
                "witch-raised-hand",
                Vec3(x - 0.42, y + 0.60 + 0.15 * math.sin(progress * math.pi), z - 0.05),
                Vec3(0.18, 0.52, 0.18),
                (174, 124, 98),
            )
        )
    return parts


def _magic(progress: float, strength: float) -> list[Mesh3D]:
    parts: list[Mesh3D] = []
    for index in range(7):
        phase = progress * 2.8 + index * 0.65
        parts.append(
            _box(
                f"magic-{index}",
                Vec3(
                    -1.55 + index * 0.46,
                    -0.22 + math.sin(phase) * 0.25 * strength,
                    5.45 + math.cos(phase * 0.7) * 0.10,
                ),
                Vec3(0.22, 0.12, 0.20),
                (143, 92, 158),
            )
        )
    return parts


def build_odyssey_story_scene(*, shot_index: int, progress: float, width: int, height: int) -> Scene3D:
    if shot_index < 1 or shot_index > 5:
        raise ValueError("software 3d Odyssey story expects shot_index 1..5")
    progress = min(1.0, max(0.0, progress))
    base_camera_x = 0.04 * math.sin((shot_index - 1) * 0.9)
    direction = 1.0 if shot_index in {1, 4, 5} else -1.0
    camera_x = base_camera_x + direction * (progress - 0.5) * 2.8
    camera_y = 0.18 + (progress - 0.5) * 0.8
    camera_z = (progress - 0.5) * 1.3
    focal_length = width * 0.98 * (1.0 + (progress - 0.5) * 0.10)
    camera = Camera3D(
        width=width,
        height=height,
        focal_length=focal_length,
        position=Vec3(camera_x, camera_y, camera_z),
    )
    meshes = _hall_geometry(progress)

    sailor_xs = (-1.55, -0.15, 1.25)
    if shot_index == 1:
        for index, x in enumerate(sailor_xs):
            meshes.extend(
                _person_parts(
                    f"sailor-{index}",
                    x=x,
                    y=0.02 + 0.04 * math.sin(progress * math.pi + index),
                    z=6.65,
                    body_color=(92 + index * 18, 88, 73),
                    scale=0.86,
                )
            )
        meshes.extend(_witch(progress, foreground=False))
    elif shot_index in {2, 3}:
        for index, x in enumerate(sailor_xs):
            pig_y = -0.02 + 0.08 * math.sin(progress * math.pi * 2 + index)
            meshes.extend(_pig_parts(f"pig-{index}", x=x, y=pig_y, z=6.60, scale=0.88))
        meshes.extend(_witch(progress, foreground=True))
        meshes.extend(_magic(progress, 1.0 if shot_index == 2 else 0.65))
    elif shot_index == 4:
        for index, x in enumerate(sailor_xs):
            meshes.extend(_pig_parts(f"pig-{index}", x=x, y=0.0, z=6.62, scale=0.86))
        hero_x = 2.75 - progress * 1.25
        meshes.extend(
            _person_parts(
                "hero",
                x=hero_x,
                y=0.04,
                z=7.25 - progress * 0.70,
                body_color=(105, 119, 94),
                scale=0.98,
            )
        )
        meshes.extend(_witch(progress, foreground=False))
        meshes.extend(_magic(progress, max(0.12, 1.0 - progress)))
        meshes.extend(
            [
                _box("inkclaw-laptop-base", Vec3(0.55, -0.46, 5.55), Vec3(0.88, 0.08, 0.50), (66, 74, 72)),
                _box("inkclaw-screen", Vec3(0.55, -0.03, 5.83), Vec3(0.88, 0.64, 0.08), (42, 132, 96)),
            ]
        )
    else:
        for index, x in enumerate(sailor_xs):
            meshes.extend(
                _person_parts(
                    f"sailor-{index}",
                    x=x,
                    y=0.02 + 0.04 * math.sin(progress * math.pi * 2 + index),
                    z=6.65,
                    body_color=(92 + index * 18, 88, 73),
                    scale=0.86,
                )
            )
        meshes.extend(
            _person_parts(
                "hero",
                x=1.95,
                y=0.04,
                z=7.10,
                body_color=(105, 119, 94),
                scale=0.98,
            )
        )
        meshes.extend(_witch(progress, foreground=False))
        smoke_scale = max(0.10, 1.0 - progress)
        for index in range(4):
            meshes.append(
                _box(
                    f"harmless-smoke-{index}",
                    Vec3(1.55 + index * 0.22, 0.12 + progress * 0.55, 6.1 + index * 0.08),
                    Vec3(0.22 * smoke_scale, 0.22 * smoke_scale, 0.22 * smoke_scale),
                    (142, 130, 145),
                )
            )

    return Scene3D(camera=camera, meshes=meshes, background=(45, 38, 42))
