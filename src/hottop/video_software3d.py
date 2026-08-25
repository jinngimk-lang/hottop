from __future__ import annotations

import hashlib
import math
import struct
import zlib
from dataclasses import dataclass, field
from pathlib import Path


PORTRAIT_PRINCIPAL_Y_RATIO = 0.42


@dataclass(frozen=True)
class Vec3:
    x: float
    y: float
    z: float

    def __add__(self, other: Vec3) -> Vec3:
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)


@dataclass(frozen=True)
class Camera3D:
    width: int
    height: int
    focal_length: float
    position: Vec3 = Vec3(0.0, 0.0, 0.0)
    near: float = 0.05

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("camera dimensions must be positive")
        if self.focal_length <= 0 or self.near <= 0:
            raise ValueError("camera focal length and near plane must be positive")


@dataclass
class Mesh3D:
    name: str
    vertices: tuple[Vec3, ...]
    faces: tuple[tuple[int, ...], ...]
    position: Vec3 = Vec3(0.0, 0.0, 0.0)
    yaw_radians: float = 0.0
    base_color: tuple[int, int, int] = (190, 125, 65)
    _identity: str = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("mesh name must not be blank")
        if not self.vertices or not self.faces:
            raise ValueError("mesh requires vertices and faces")
        for face in self.faces:
            if len(face) < 3 or any(index < 0 or index >= len(self.vertices) for index in face):
                raise ValueError("mesh face contains invalid vertex indices")
        payload = repr((self.name, self.vertices, self.faces)).encode("utf-8")
        self._identity = hashlib.sha256(payload).hexdigest()

    @classmethod
    def box(
        cls,
        *,
        name: str,
        center: Vec3,
        size: Vec3,
        base_color: tuple[int, int, int] = (190, 125, 65),
    ) -> Mesh3D:
        hx, hy, hz = size.x / 2, size.y / 2, size.z / 2
        vertices = (
            Vec3(-hx, -hy, -hz),
            Vec3(hx, -hy, -hz),
            Vec3(hx, hy, -hz),
            Vec3(-hx, hy, -hz),
            Vec3(-hx, -hy, hz),
            Vec3(hx, -hy, hz),
            Vec3(hx, hy, hz),
            Vec3(-hx, hy, hz),
        )
        faces = (
            (0, 1, 2, 3),
            (4, 7, 6, 5),
            (0, 4, 5, 1),
            (3, 2, 6, 7),
            (1, 5, 6, 2),
            (0, 3, 7, 4),
        )
        return cls(name=name, vertices=vertices, faces=faces, position=center, base_color=base_color)

    def identity_signature(self) -> str:
        return self._identity

    def translate(self, delta: Vec3) -> None:
        self.position = self.position + delta

    def rotate_y(self, radians: float) -> None:
        self.yaw_radians += radians

    def world_vertex(self, vertex: Vec3) -> Vec3:
        cosine = math.cos(self.yaw_radians)
        sine = math.sin(self.yaw_radians)
        rotated = Vec3(
            vertex.x * cosine + vertex.z * sine,
            vertex.y,
            -vertex.x * sine + vertex.z * cosine,
        )
        return rotated + self.position


@dataclass
class Scene3D:
    camera: Camera3D
    meshes: list[Mesh3D]
    background: tuple[int, int, int] = (44, 31, 25)

    def __post_init__(self) -> None:
        identities = [mesh.name for mesh in self.meshes]
        if len(identities) != len(set(identities)):
            raise ValueError("duplicate mesh identity in scene")


def project_point(point: Vec3, camera: Camera3D) -> tuple[float, float, float] | None:
    relative = Vec3(
        point.x - camera.position.x,
        point.y - camera.position.y,
        point.z - camera.position.z,
    )
    if relative.z <= camera.near:
        return None
    x = camera.width / 2 + camera.focal_length * relative.x / relative.z
    principal_y_ratio = PORTRAIT_PRINCIPAL_Y_RATIO if camera.height > camera.width else 0.5
    y = camera.height * principal_y_ratio - camera.focal_length * relative.y / relative.z
    return x, y, relative.z


def _shade(color: tuple[int, int, int], factor: float) -> tuple[int, int, int]:
    return tuple(max(0, min(255, round(channel * factor))) for channel in color)


def _inside_polygon(x: float, y: float, points: list[tuple[float, float]]) -> bool:
    inside = False
    j = len(points) - 1
    for i, (xi, yi) in enumerate(points):
        xj, yj = points[j]
        intersects = ((yi > y) != (yj > y)) and (
            x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi
        )
        if intersects:
            inside = not inside
        j = i
    return inside


def _fill_polygon(
    pixels: bytearray,
    width: int,
    height: int,
    points: list[tuple[float, float]],
    color: tuple[int, int, int],
) -> None:
    min_x = max(0, math.floor(min(point[0] for point in points)))
    max_x = min(width - 1, math.ceil(max(point[0] for point in points)))
    min_y = max(0, math.floor(min(point[1] for point in points)))
    max_y = min(height - 1, math.ceil(max(point[1] for point in points)))
    for py in range(min_y, max_y + 1):
        for px in range(min_x, max_x + 1):
            if _inside_polygon(px + 0.5, py + 0.5, points):
                offset = (py * width + px) * 3
                pixels[offset : offset + 3] = bytes(color)


def _write_png(path: Path, width: int, height: int, pixels: bytes) -> None:
    def chunk(kind: bytes, data: bytes) -> bytes:
        body = kind + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    raw = b"".join(
        b"\x00" + pixels[row * width * 3 : (row + 1) * width * 3]
        for row in range(height)
    )
    payload = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, level=6))
        + chunk(b"IEND", b"")
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".part")
    try:
        temporary.write_bytes(payload)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def render_scene_frame(scene: Scene3D, output: Path) -> Path:
    camera = scene.camera
    pixels = bytearray(bytes(scene.background) * (camera.width * camera.height))
    draw_faces: list[tuple[float, list[tuple[float, float]], tuple[int, int, int]]] = []

    for mesh in scene.meshes:
        world = [mesh.world_vertex(vertex) for vertex in mesh.vertices]
        for face_index, face in enumerate(mesh.faces):
            projected = [project_point(world[index], camera) for index in face]
            if any(point is None for point in projected):
                continue
            visible = [point for point in projected if point is not None]
            depth = sum(point[2] for point in visible) / len(visible)
            points = [(point[0], point[1]) for point in visible]
            factor = 0.62 + 0.08 * (face_index % 5)
            draw_faces.append((depth, points, _shade(mesh.base_color, factor)))

    for _, points, color in sorted(draw_faces, key=lambda item: item[0], reverse=True):
        _fill_polygon(pixels, camera.width, camera.height, points, color)

    _write_png(output, camera.width, camera.height, bytes(pixels))
    return output
