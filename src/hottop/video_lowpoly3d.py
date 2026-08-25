from __future__ import annotations

import argparse
import math
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias

Point3: TypeAlias = tuple[float, float, float]
Point2: TypeAlias = tuple[float, float]
Color: TypeAlias = tuple[int, int, int]


@dataclass(frozen=True)
class _Face:
    points: tuple[Point3, ...]
    color: Color


_PRESETS = {"cow-snake-workshop-v1"}


def project_point(
    point: Point3,
    *,
    width: int,
    height: int,
    focal_length: float = 1.15,
) -> tuple[float, float, float]:
    """Project a camera-space 3D point with a deterministic pinhole camera."""

    x, y, z = point
    if z <= 0.05:
        raise ValueError("3D points must be in front of the camera")
    scale = focal_length * min(width, height) / z
    return width / 2 + x * scale, height * 0.56 - y * scale, z


def _shade(color: Color, factor: float) -> Color:
    return tuple(max(0, min(255, round(channel * factor))) for channel in color)  # type: ignore[return-value]


def _cuboid(
    center: Point3,
    size: Point3,
    color: Color,
    *,
    yaw: float = 0.0,
) -> list[_Face]:
    cx, cy, cz = center
    sx, sy, sz = (value / 2 for value in size)
    corners: list[Point3] = []
    cos_yaw = math.cos(yaw)
    sin_yaw = math.sin(yaw)
    for x, y, z in (
        (-sx, -sy, -sz),
        (sx, -sy, -sz),
        (sx, sy, -sz),
        (-sx, sy, -sz),
        (-sx, -sy, sz),
        (sx, -sy, sz),
        (sx, sy, sz),
        (-sx, sy, sz),
    ):
        rx = x * cos_yaw - z * sin_yaw
        rz = x * sin_yaw + z * cos_yaw
        corners.append((cx + rx, cy + y, cz + rz))
    specs = (
        ((0, 1, 2, 3), 0.68),
        ((4, 7, 6, 5), 1.0),
        ((0, 4, 5, 1), 0.56),
        ((3, 2, 6, 7), 1.12),
        ((1, 5, 6, 2), 0.86),
        ((0, 3, 7, 4), 0.76),
    )
    return [
        _Face(tuple(corners[index] for index in indices), _shade(color, factor))
        for indices, factor in specs
    ]


def _triangle(center: Point3, scale: Point3, color: Color) -> _Face:
    cx, cy, cz = center
    sx, sy, sz = scale
    return _Face(
        (
            (cx - sx, cy - sy, cz + sz),
            (cx + sx, cy - sy, cz - sz),
            (cx, cy + sy, cz),
        ),
        color,
    )


def _world_to_camera(point: Point3, camera_x: float, camera_y: float) -> Point3:
    x, y, z = point
    return x - camera_x, y - camera_y, z


def _fill_polygon(buffer: bytearray, width: int, height: int, points: list[Point2], color: Color) -> None:
    if len(points) < 3:
        return
    min_y = max(0, math.floor(min(point[1] for point in points)))
    max_y = min(height - 1, math.ceil(max(point[1] for point in points)))
    pixel = bytes(color)
    count = len(points)
    for y in range(min_y, max_y + 1):
        scan_y = y + 0.5
        intersections: list[float] = []
        for index in range(count):
            x1, y1 = points[index]
            x2, y2 = points[(index + 1) % count]
            if y1 == y2:
                continue
            if scan_y < min(y1, y2) or scan_y >= max(y1, y2):
                continue
            ratio = (scan_y - y1) / (y2 - y1)
            intersections.append(x1 + (x2 - x1) * ratio)
        intersections.sort()
        for left, right in zip(intersections[::2], intersections[1::2], strict=False):
            start = max(0, math.ceil(left))
            end = min(width - 1, math.floor(right))
            if end < start:
                continue
            offset = (y * width + start) * 3
            buffer[offset : offset + (end - start + 1) * 3] = pixel * (end - start + 1)


def _gradient_background(width: int, height: int) -> bytearray:
    buffer = bytearray(width * height * 3)
    horizon = int(height * 0.58)
    for y in range(height):
        if y < horizon:
            ratio = y / max(1, horizon)
            color = (
                round(62 + 46 * ratio),
                round(43 + 24 * ratio),
                round(34 + 17 * ratio),
            )
        else:
            ratio = (y - horizon) / max(1, height - horizon)
            color = (
                round(74 - 28 * ratio),
                round(51 - 19 * ratio),
                round(36 - 14 * ratio),
            )
        row = bytes(color) * width
        start = y * width * 3
        buffer[start : start + width * 3] = row
    return buffer


def _scene_faces(shot_index: int, time_seconds: float) -> tuple[list[_Face], float, float]:
    phase = time_seconds * 2 * math.pi
    bob = math.sin(phase * 1.4) * 0.035
    recoil = 0.0
    if shot_index % 4 == 2:
        recoil = min(0.42, time_seconds * 0.85)
    camera_x = math.sin(time_seconds * 0.8 + shot_index * 0.37) * 0.055
    camera_y = 0.05 + math.sin(time_seconds * 0.63) * 0.015

    faces: list[_Face] = []
    # Workshop floor props and back wall geometry establish persistent perspective.
    faces.extend(_cuboid((-1.55, -0.55, 6.9), (0.42, 1.15, 0.55), (92, 61, 42)))
    faces.extend(_cuboid((1.48, -0.48, 7.6), (0.5, 1.3, 0.6), (81, 55, 39)))
    faces.extend(_cuboid((0.0, -0.72, 5.4), (2.95, 0.18, 1.15), (104, 69, 42)))
    faces.extend(_cuboid((-1.12, -1.35, 5.35), (0.18, 1.25, 0.18), (70, 45, 30)))
    faces.extend(_cuboid((1.12, -1.35, 5.35), (0.18, 1.25, 0.18), (70, 45, 30)))

    # Laptop: base + upright screen, deliberately blocky.
    faces.extend(_cuboid((0.32, -0.5, 4.82), (0.95, 0.09, 0.68), (45, 49, 47), yaw=-0.08))
    faces.extend(_cuboid((0.34, -0.05, 5.18), (0.92, 0.74, 0.09), (38, 44, 42), yaw=-0.08))
    faces.extend(_cuboid((0.34, -0.05, 5.12), (0.72, 0.54, 0.035), (92, 121, 91), yaw=-0.08))

    # Original bovine programmer. Identity is encoded as stable geometry and palette across shots.
    cow_x = -0.72 - recoil
    cow_z = 4.45 + math.sin(phase * 0.45) * 0.025
    faces.extend(_cuboid((cow_x, -0.48 + bob, cow_z), (0.72, 1.0, 0.62), (205, 118, 48), yaw=0.12))
    faces.extend(_cuboid((cow_x + 0.02, 0.25 + bob, cow_z - 0.02), (0.66, 0.58, 0.58), (222, 135, 57), yaw=0.1))
    faces.extend(_cuboid((cow_x + 0.01, 0.12 + bob, cow_z - 0.34), (0.46, 0.24, 0.18), (145, 96, 82), yaw=0.1))
    # short horns + ears: original simple wedges, not a protected character model
    faces.append(_triangle((cow_x - 0.29, 0.58 + bob, cow_z - 0.02), (0.16, 0.2, 0.08), (75, 62, 49)))
    faces.append(_triangle((cow_x + 0.31, 0.58 + bob, cow_z - 0.02), (0.16, 0.2, -0.08), (75, 62, 49)))
    faces.extend(_cuboid((cow_x - 0.25, -1.17, cow_z), (0.22, 0.55, 0.22), (166, 91, 39)))
    faces.extend(_cuboid((cow_x + 0.25, -1.17, cow_z), (0.22, 0.55, 0.22), (166, 91, 39)))

    # Cable-snake: segmented cuboids create depth and real parallax as it crosses the desk.
    snake_phase = time_seconds * 2.6 + shot_index * 0.45
    for segment in range(8):
        u = segment / 7
        x = -0.1 + u * 1.8 + math.sin(snake_phase + segment * 0.75) * 0.11
        y = -1.34 + math.sin(snake_phase * 1.2 + segment * 0.5) * 0.06
        z = 4.0 + u * 0.8 + math.cos(snake_phase + segment * 0.55) * 0.09
        size = 0.25 if segment < 7 else 0.33
        faces.extend(_cuboid((x, y, z), (size, size, size), (70, 142, 71), yaw=snake_phase * 0.08))

    # A moving foreground crate gives obvious occlusion/parallax without a fake Ken Burns move.
    crate_x = 1.35 - ((time_seconds * 0.18 + shot_index * 0.07) % 0.35)
    faces.extend(_cuboid((crate_x, -1.45, 3.65), (0.52, 0.52, 0.52), (126, 79, 42), yaw=0.16))
    return faces, camera_x, camera_y


def render_lowpoly_frame(
    *,
    preset: str,
    shot_index: int,
    time_seconds: float,
    width: int,
    height: int,
) -> bytes:
    """Render one deterministic PPM frame from original low-poly 3D geometry."""

    if preset not in _PRESETS:
        raise ValueError(f"unknown software low-poly preset: {preset}")
    if shot_index < 1 or time_seconds < 0 or width < 16 or height < 16:
        raise ValueError("invalid software low-poly frame arguments")

    buffer = _gradient_background(width, height)
    faces, camera_x, camera_y = _scene_faces(shot_index, time_seconds)
    visible: list[tuple[float, list[Point2], Color]] = []
    for face in faces:
        camera_points = [_world_to_camera(point, camera_x, camera_y) for point in face.points]
        if any(point[2] <= 0.05 for point in camera_points):
            continue
        projected = [
            project_point(point, width=width, height=height, focal_length=1.32)
            for point in camera_points
        ]
        depth = sum(point[2] for point in projected) / len(projected)
        visible.append((depth, [(point[0], point[1]) for point in projected], face.color))

    for _, points, color in sorted(visible, key=lambda item: item[0], reverse=True):
        _fill_polygon(buffer, width, height, points, color)

    header = f"P6\n{width} {height}\n255\n".encode("ascii")
    return header + bytes(buffer)


def render_lowpoly_shot(
    *,
    preset: str,
    shot_index: int,
    duration_seconds: float,
    width: int,
    height: int,
    fps: int,
    output: Path,
) -> Path:
    """Encode a deterministic software-rendered 3D shot as H.264 MP4."""

    if duration_seconds <= 0 or fps <= 0:
        raise ValueError("duration and fps must be positive")
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise RuntimeError("ffmpeg is required for software low-poly shot encoding")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.unlink(missing_ok=True)
    frames = max(2, math.ceil(duration_seconds * fps))
    process = subprocess.Popen(
        [
            ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "image2pipe",
            "-vcodec",
            "ppm",
            "-framerate",
            str(fps),
            "-i",
            "pipe:0",
            "-an",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(output),
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdin is not None
    try:
        for frame_index in range(frames):
            frame_time = min(duration_seconds, frame_index / fps)
            process.stdin.write(
                render_lowpoly_frame(
                    preset=preset,
                    shot_index=shot_index,
                    time_seconds=frame_time,
                    width=width,
                    height=height,
                )
            )
        process.stdin.close()
        stderr = process.stderr.read() if process.stderr is not None else b""
        return_code = process.wait()
    except Exception:
        process.kill()
        process.wait()
        output.unlink(missing_ok=True)
        raise
    if return_code != 0:
        output.unlink(missing_ok=True)
        message = stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"software low-poly ffmpeg encoding failed: {message}")
    if not output.is_file() or output.stat().st_size <= 0:
        raise RuntimeError("software low-poly renderer produced no output")
    return output


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render one Hottop software low-poly 3D shot")
    parser.add_argument("--preset", required=True)
    parser.add_argument("--shot-index", type=int, required=True)
    parser.add_argument("--duration-seconds", type=float, required=True)
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--height", type=int, required=True)
    parser.add_argument("--fps", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    render_lowpoly_shot(
        preset=args.preset,
        shot_index=args.shot_index,
        duration_seconds=args.duration_seconds,
        width=args.width,
        height=args.height,
        fps=args.fps,
        output=args.output,
    )


if __name__ == "__main__":
    main()
