from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import subprocess
from collections.abc import Callable
from pathlib import Path

from .video_artifacts import VideoArtifactManifest, VideoShotArtifact
from .video_software3d import Camera3D, Mesh3D, Scene3D, Vec3, render_scene_frame

Runner = Callable[..., subprocess.CompletedProcess[str]]
DEFAULT_PRESET = "cow-snake-workshop-v1"
ODYSSEY_PRESET = "odyssey-witch-pigs-v1"
STORY_SHOT_COUNTS = {DEFAULT_PRESET: 5, ODYSSEY_PRESET: 6}


def _box(name: str, center: Vec3, size: Vec3, color: tuple[int, int, int]) -> Mesh3D:
    return Mesh3D.box(name=name, center=center, size=size, base_color=color)


def _cow_parts(prefix: str, x: float, y: float, z: float, scale: float, mother: bool = False) -> list[Mesh3D]:
    body_color = (165, 92, 42) if not mother else (128, 79, 48)
    muzzle_color = (128, 116, 112)
    return [
        _box(f"{prefix}-body", Vec3(x, y, z), Vec3(1.2 * scale, 1.6 * scale, 0.8 * scale), body_color),
        _box(f"{prefix}-head", Vec3(x, y + 1.15 * scale, z - 0.05 * scale), Vec3(1.0 * scale, 0.9 * scale, 0.78 * scale), body_color),
        _box(f"{prefix}-muzzle", Vec3(x, y + 0.98 * scale, z - 0.48 * scale), Vec3(0.78 * scale, 0.38 * scale, 0.28 * scale), muzzle_color),
        _box(f"{prefix}-horn-left", Vec3(x - 0.42 * scale, y + 1.72 * scale, z), Vec3(0.18 * scale, 0.45 * scale, 0.18 * scale), (50, 44, 40)),
        _box(f"{prefix}-horn-right", Vec3(x + 0.42 * scale, y + 1.72 * scale, z), Vec3(0.18 * scale, 0.45 * scale, 0.18 * scale), (50, 44, 40)),
    ]


def _snake_parts(progress: float, shot_index: int) -> list[Mesh3D]:
    parts: list[Mesh3D] = []
    retreat = max(0.0, (shot_index - 3) * 0.75 + progress * (0.8 if shot_index >= 4 else 0.1))
    for index in range(7):
        phase = progress * 2.0 + index * 0.55
        x = -0.9 + index * 0.32 + math.sin(phase) * 0.14 + retreat
        y = -0.85 + math.sin(phase * 0.7) * 0.08
        z = 4.6 + index * 0.08
        parts.append(_box(f"snake-segment-{index}", Vec3(x, y, z), Vec3(0.42, 0.20, 0.30), (55, 115, 58)))
    return parts


def _build_cow_snake_scene(*, shot_index: int, progress: float, width: int, height: int) -> Scene3D:
    if shot_index < 1 or shot_index > STORY_SHOT_COUNTS[DEFAULT_PRESET]:
        raise ValueError("cow-snake-workshop-v1 expects shot_index 1..5")
    camera = Camera3D(width=width, height=height, focal_length=width * 0.9, position=Vec3(0, 0.2, 0))
    meshes: list[Mesh3D] = [
        _box("floor", Vec3(0, -1.7, 6.5), Vec3(7.0, 0.25, 8.0), (77, 54, 38)),
        _box("back-wall", Vec3(0, 1.0, 9.0), Vec3(7.0, 5.5, 0.25), (88, 62, 44)),
        _box("desk", Vec3(-0.35, -0.75, 5.0), Vec3(2.8, 0.25, 1.25), (103, 68, 43)),
        _box("laptop-base", Vec3(-0.3, -0.48, 4.7), Vec3(1.1, 0.10, 0.65), (55, 57, 56)),
        _box("laptop-screen", Vec3(-0.3, 0.03, 5.05), Vec3(1.15, 0.82, 0.10), (45, 70, 64)),
        _box("doorway", Vec3(2.35, 0.4, 8.65), Vec3(1.5, 3.9, 0.20), (47, 35, 28)),
    ]
    hero_x = -1.15
    hero_y = 0.0
    if shot_index == 2:
        hero_x -= 0.3 + progress * 0.28
        hero_y += 0.08 * math.sin(progress * math.pi)
    elif shot_index >= 4:
        hero_x += 0.16
    hero_parts = _cow_parts("young-cow", hero_x, hero_y, 5.6, 0.82)
    if shot_index == 2:
        for part in hero_parts:
            part.rotate_y(-0.28 - progress * 0.18)
    meshes.extend(hero_parts)
    if shot_index >= 3:
        mother_x = 2.7 - min(1.0, progress + (shot_index - 3) * 0.7) * 1.15
        mother = _cow_parts("mother-cow", mother_x, 0.12, 6.9, 1.02, mother=True)
        for part in mother:
            part.rotate_y(-0.18)
        meshes.extend(mother)
    meshes.extend(_snake_parts(progress, shot_index))
    if shot_index >= 4:
        for index, label in enumerate(("Research", "Write", "Review", "Code")):
            meshes.append(_box(f"agent-{label.lower()}", Vec3(-0.75 + index * 0.32, 0.25 + 0.18 * math.sin(progress * math.pi + index), 4.42), Vec3(0.22, 0.22, 0.22), (85 + index * 20, 115 + index * 10, 95)))
    if shot_index == 5:
        deploy_box = _box("deploy-box", Vec3(0.75 + progress * 2.2, -0.75 + progress * 0.55, 4.1 - progress * 0.2), Vec3(0.75, 0.58, 0.55), (150, 116, 70))
        deploy_box.rotate_y(progress * 1.2)
        meshes.append(deploy_box)
    return Scene3D(camera=camera, meshes=meshes, background=(31, 24, 22))


def _human_parts(prefix: str, x: float, y: float, z: float, scale: float, color: tuple[int, int, int]) -> list[Mesh3D]:
    skin = (151, 112, 86)
    return [
        _box(f"{prefix}-body", Vec3(x, y, z), Vec3(0.72 * scale, 1.15 * scale, 0.48 * scale), color),
        _box(f"{prefix}-head", Vec3(x, y + 0.88 * scale, z - 0.04 * scale), Vec3(0.52 * scale, 0.52 * scale, 0.46 * scale), skin),
        _box(f"{prefix}-arm-left", Vec3(x - 0.48 * scale, y + 0.05 * scale, z), Vec3(0.20 * scale, 0.86 * scale, 0.20 * scale), skin),
        _box(f"{prefix}-arm-right", Vec3(x + 0.48 * scale, y + 0.05 * scale, z), Vec3(0.20 * scale, 0.86 * scale, 0.20 * scale), skin),
    ]


def _pig_parts(prefix: str, x: float, y: float, z: float, scale: float) -> list[Mesh3D]:
    pink = (177, 112, 112)
    dark = (92, 66, 62)
    return [
        _box(f"{prefix}-body", Vec3(x, y, z), Vec3(1.05 * scale, 0.72 * scale, 0.72 * scale), pink),
        _box(f"{prefix}-head", Vec3(x, y + 0.42 * scale, z - 0.42 * scale), Vec3(0.72 * scale, 0.62 * scale, 0.58 * scale), pink),
        _box(f"{prefix}-snout", Vec3(x, y + 0.30 * scale, z - 0.78 * scale), Vec3(0.48 * scale, 0.28 * scale, 0.22 * scale), dark),
        _box(f"{prefix}-ear-left", Vec3(x - 0.25 * scale, y + 0.82 * scale, z - 0.38 * scale), Vec3(0.18 * scale, 0.28 * scale, 0.12 * scale), pink),
        _box(f"{prefix}-ear-right", Vec3(x + 0.25 * scale, y + 0.82 * scale, z - 0.38 * scale), Vec3(0.18 * scale, 0.28 * scale, 0.12 * scale), pink),
    ]


def _banquet_laptop(prefix: str, x: float, z: float) -> list[Mesh3D]:
    return [
        _box(f"{prefix}-laptop-base", Vec3(x, -0.43, z), Vec3(0.62, 0.08, 0.48), (50, 49, 46)),
        _box(f"{prefix}-laptop-screen", Vec3(x, -0.08, z + 0.18), Vec3(0.64, 0.54, 0.08), (47, 73, 66)),
    ]


def _build_odyssey_scene(*, shot_index: int, progress: float, width: int, height: int) -> Scene3D:
    if shot_index < 1 or shot_index > STORY_SHOT_COUNTS[ODYSSEY_PRESET]:
        raise ValueError("odyssey-witch-pigs-v1 expects shot_index 1..6")
    camera = Camera3D(width=width, height=height, focal_length=width * 0.92, position=Vec3(0, 0.25, 0))
    meshes: list[Mesh3D] = [
        _box("stone-floor", Vec3(0, -1.65, 6.6), Vec3(7.2, 0.22, 8.0), (71, 62, 54)),
        _box("banquet-back-wall", Vec3(0, 1.15, 9.0), Vec3(7.2, 5.7, 0.24), (94, 76, 58)),
        _box("banquet-table", Vec3(-0.1, -0.66, 5.55), Vec3(4.6, 0.28, 1.35), (112, 75, 46)),
        _box("witch-body", Vec3(2.15, 0.05, 6.55), Vec3(0.78, 1.55, 0.58), (70, 48, 78)),
        _box("witch-head", Vec3(2.15, 1.18, 6.48), Vec3(0.58, 0.58, 0.52), (146, 111, 91)),
        _box("witch-cup", Vec3(1.72, 0.58 + 0.16 * math.sin(progress * math.pi), 5.78), Vec3(0.25, 0.33, 0.25), (139, 105, 53)),
        _box("doorway", Vec3(-2.65, 0.35, 8.72), Vec3(1.25, 3.9, 0.18), (47, 38, 32)),
    ]
    crew_positions = [(-1.35, 5.05), (-0.15, 5.18), (1.02, 5.08)]
    for index, (x, z) in enumerate(crew_positions, start=1):
        if shot_index == 1:
            meshes.extend(_human_parts(f"crew-{index}", x, -0.05, z, 0.72, (91 + index * 12, 78, 61)))
        else:
            bounce = 0.06 * math.sin(progress * math.pi * 2 + index)
            meshes.extend(_pig_parts(f"pig-{index}", x, -0.40 + bounce, z, 0.72))
        meshes.extend(_banquet_laptop(f"station-{index}", x, z - 0.52))
    if shot_index >= 3:
        hero_x = -2.45 + min(1.0, progress + (shot_index - 3) * 0.45) * 0.9
        hero = _human_parts("hero", hero_x, 0.02, 6.45, 0.88, (76, 83, 93))
        for part in hero:
            part.rotate_y(0.18)
        meshes.extend(hero)
    if shot_index >= 4:
        meshes.extend([
            _box("inkclaw-laptop", Vec3(-0.72, -0.18, 4.25), Vec3(0.86, 0.12, 0.62), (48, 52, 50)),
            _box("inkclaw-screen", Vec3(-0.72, 0.30, 4.52), Vec3(0.90, 0.78, 0.10), (42, 75, 65)),
        ])
        for index, label in enumerate(("research", "write", "review", "code")):
            orbit = progress * 0.9 + index * 0.55
            meshes.append(_box(f"agent-{label}", Vec3(-0.85 + index * 0.42, 0.58 + 0.18 * math.sin(orbit), 4.05 + 0.10 * math.cos(orbit)), Vec3(0.25, 0.25, 0.25), (78 + index * 23, 116, 93 + index * 8)))
    if shot_index >= 5:
        meshes.append(_box("completed-work", Vec3(0.45, 0.58, 4.35), Vec3(1.15, 0.72, 0.08), (74, 121, 89)))
    return Scene3D(camera=camera, meshes=meshes, background=(28, 24, 27))


def build_story_scene(*, shot_index: int, progress: float, width: int, height: int, preset: str = DEFAULT_PRESET) -> Scene3D:
    progress = min(1.0, max(0.0, progress))
    if preset == DEFAULT_PRESET:
        return _build_cow_snake_scene(shot_index=shot_index, progress=progress, width=width, height=height)
    if preset == ODYSSEY_PRESET:
        return _build_odyssey_scene(shot_index=shot_index, progress=progress, width=width, height=height)
    raise ValueError(f"unknown software 3d story preset: {preset}")


def resolve_story_preset_for_output(output: Path) -> str:
    plan_path = output.resolve().parent.parent / "hottop-video-plan.json"
    if not plan_path.is_file():
        return DEFAULT_PRESET
    try:
        raw = json.loads(plan_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return DEFAULT_PRESET
    topic_id = str(raw.get("topic_id") or "").strip()
    return topic_id if topic_id in STORY_SHOT_COUNTS else DEFAULT_PRESET


def _load_render_frames(render_source: Path, *, preset: str = DEFAULT_PRESET) -> list[dict[str, object]]:
    raw = json.loads(render_source.read_text(encoding="utf-8"))
    if raw.get("schema_version") != "hottop.render.v2":
        raise ValueError("software 3d production requires hottop.render.v2")
    frames = raw.get("frames")
    expected = STORY_SHOT_COUNTS.get(preset)
    if expected is None:
        raise ValueError(f"unknown software 3d story preset: {preset}")
    if not isinstance(frames, list) or len(frames) != expected:
        raise ValueError(f"software 3d preset {preset} requires exactly {expected} frames")
    return frames


def render_story_frame_sequence(*, render_source: Path, output_dir: Path, width: int = 360, height: int = 640, fps: int = 12, seconds_per_shot: float = 2.4, preset: str = DEFAULT_PRESET) -> list[Path]:
    frames = _load_render_frames(render_source, preset=preset)
    if fps <= 0 or seconds_per_shot <= 0:
        raise ValueError("fps and seconds_per_shot must be positive")
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    count_per_shot = max(1, round(fps * seconds_per_shot))
    for shot_position, _ in enumerate(frames, start=1):
        for frame_index in range(count_per_shot):
            progress = frame_index / max(1, count_per_shot - 1)
            scene = build_story_scene(shot_index=shot_position, progress=progress, width=width, height=height, preset=preset)
            path = output_dir / f"frame-{len(paths):05d}.png"
            render_scene_frame(scene, path)
            paths.append(path)
    return paths


def _write_shot_manifest(*, shot_index: int, output: Path) -> Path:
    resolved_output = output.resolve()
    payload = resolved_output.read_bytes()
    manifest_path = resolved_output.with_suffix(".artifact.json")
    temporary = manifest_path.with_suffix(manifest_path.suffix + ".part")
    manifest = VideoArtifactManifest(
        planned_generation_backend="software3d",
        shots=[VideoShotArtifact(shot_index=shot_index, path=str(resolved_output), artifact_kind="deterministic-generated", backend="software3d", sha256=hashlib.sha256(payload).hexdigest(), size_bytes=len(payload))],
    )
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        temporary.write_text(manifest.model_dump_json(indent=2) + "\n", encoding="utf-8")
        temporary.replace(manifest_path)
    finally:
        temporary.unlink(missing_ok=True)
    return manifest_path


def render_story_shot_video(*, shot_index: int, output: Path, duration_seconds: float, width: int = 360, height: int = 640, fps: int = 12, preset: str | None = None, runner: Runner = subprocess.run) -> Path:
    selected_preset = preset or resolve_story_preset_for_output(output)
    expected = STORY_SHOT_COUNTS.get(selected_preset)
    if expected is None:
        raise ValueError(f"unknown software 3d story preset: {selected_preset}")
    if shot_index < 1 or shot_index > expected:
        raise ValueError(f"software 3d preset {selected_preset} expects shot_index 1..{expected}")
    if duration_seconds <= 0 or fps <= 0:
        raise ValueError("duration_seconds and fps must be positive")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.unlink(missing_ok=True)
    manifest_path = output.resolve().with_suffix(".artifact.json")
    manifest_path.unlink(missing_ok=True)
    frames_dir = output.with_suffix(".frames")
    shutil.rmtree(frames_dir, ignore_errors=True)
    frames_dir.mkdir(parents=True, exist_ok=True)
    frame_count = max(2, round(duration_seconds * fps))
    try:
        for frame_index in range(frame_count):
            progress = frame_index / max(1, frame_count - 1)
            scene = build_story_scene(shot_index=shot_index, progress=progress, width=width, height=height, preset=selected_preset)
            render_scene_frame(scene, frames_dir / f"frame-{frame_index:05d}.png")
        completed = runner(["ffmpeg", "-y", "-framerate", str(fps), "-i", str(frames_dir / "frame-%05d.png"), "-t", f"{duration_seconds:g}", "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(output)], capture_output=True, text=True, check=False)
        if completed.returncode != 0:
            output.unlink(missing_ok=True)
            raise RuntimeError(f"software 3d shot encoding failed with return code {completed.returncode}")
        if not output.is_file() or output.stat().st_size <= 0:
            raise RuntimeError("software 3d shot encoder produced no output")
        try:
            _write_shot_manifest(shot_index=shot_index, output=output)
        except Exception:
            output.unlink(missing_ok=True)
            manifest_path.unlink(missing_ok=True)
            raise
        return output
    finally:
        shutil.rmtree(frames_dir, ignore_errors=True)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render Hottop deterministic software-3D footage")
    parser.add_argument("--render")
    parser.add_argument("--output-dir")
    parser.add_argument("--shot-index", type=int)
    parser.add_argument("--output")
    parser.add_argument("--width", type=int, default=360)
    parser.add_argument("--height", type=int, default=640)
    parser.add_argument("--fps", type=int, default=12)
    parser.add_argument("--seconds-per-shot", type=float, default=2.4)
    parser.add_argument("--duration-seconds", type=float)
    parser.add_argument("--preset", choices=sorted(STORY_SHOT_COUNTS))
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if args.shot_index is not None or args.output is not None:
        if args.shot_index is None or args.output is None or args.duration_seconds is None:
            raise SystemExit("shot mode requires --shot-index, --duration-seconds and --output")
        render_story_shot_video(shot_index=args.shot_index, output=Path(args.output), duration_seconds=args.duration_seconds, width=args.width, height=args.height, fps=args.fps, preset=args.preset)
        return
    if not args.render or not args.output_dir:
        raise SystemExit("sequence mode requires --render and --output-dir")
    render_story_frame_sequence(render_source=Path(args.render), output_dir=Path(args.output_dir), width=args.width, height=args.height, fps=args.fps, seconds_per_shot=args.seconds_per_shot, preset=args.preset or DEFAULT_PRESET)


if __name__ == "__main__":
    main()
