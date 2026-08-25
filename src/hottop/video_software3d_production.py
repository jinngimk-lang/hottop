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
from .video_software3d_odyssey import build_odyssey_story_scene

Runner = Callable[..., subprocess.CompletedProcess[str]]

COW_STORY_PROFILE = "cow-snake"
ODYSSEY_STORY_PROFILE = "odyssey-witch-pigs"
COW_STORY_TOPICS = frozenset({COW_STORY_PROFILE, "inkclaw-anti-polish-cow-snake"})


def _box(
    name: str,
    center: Vec3,
    size: Vec3,
    color: tuple[int, int, int],
) -> Mesh3D:
    return Mesh3D.box(name=name, center=center, size=size, base_color=color)


def _cow_parts(prefix: str, x: float, y: float, z: float, scale: float, mother: bool = False) -> list[Mesh3D]:
    body_color = (165, 92, 42) if not mother else (128, 79, 48)
    muzzle_color = (128, 116, 112)
    parts = [
        _box(f"{prefix}-body", Vec3(x, y, z), Vec3(1.2 * scale, 1.6 * scale, 0.8 * scale), body_color),
        _box(
            f"{prefix}-head",
            Vec3(x, y + 1.15 * scale, z - 0.05 * scale),
            Vec3(1.0 * scale, 0.9 * scale, 0.78 * scale),
            body_color,
        ),
        _box(
            f"{prefix}-muzzle",
            Vec3(x, y + 0.98 * scale, z - 0.48 * scale),
            Vec3(0.78 * scale, 0.38 * scale, 0.28 * scale),
            muzzle_color,
        ),
        _box(
            f"{prefix}-horn-left",
            Vec3(x - 0.42 * scale, y + 1.72 * scale, z),
            Vec3(0.18 * scale, 0.45 * scale, 0.18 * scale),
            (50, 44, 40),
        ),
        _box(
            f"{prefix}-horn-right",
            Vec3(x + 0.42 * scale, y + 1.72 * scale, z),
            Vec3(0.18 * scale, 0.45 * scale, 0.18 * scale),
            (50, 44, 40),
        ),
    ]
    return parts


def _snake_parts(progress: float, shot_index: int) -> list[Mesh3D]:
    parts: list[Mesh3D] = []
    retreat = max(0.0, (shot_index - 3) * 0.75 + progress * (0.8 if shot_index >= 4 else 0.1))
    for index in range(7):
        phase = progress * 2.0 + index * 0.55
        x = -0.9 + index * 0.32 + math.sin(phase) * 0.14 + retreat
        y = -0.85 + math.sin(phase * 0.7) * 0.08
        z = 4.6 + index * 0.08
        parts.append(
            _box(
                f"snake-segment-{index}",
                Vec3(x, y, z),
                Vec3(0.42, 0.20, 0.30),
                (55, 115, 58),
            )
        )
    return parts


def _build_cow_story_scene(*, shot_index: int, progress: float, width: int, height: int) -> Scene3D:
    if shot_index < 1 or shot_index > 5:
        raise ValueError("software 3d flagship story expects shot_index 1..5")
    progress = min(1.0, max(0.0, progress))
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
            meshes.append(
                _box(
                    f"agent-{label.lower()}",
                    Vec3(-0.75 + index * 0.32, 0.25 + 0.18 * math.sin(progress * math.pi + index), 4.42),
                    Vec3(0.22, 0.22, 0.22),
                    (85 + index * 20, 115 + index * 10, 95),
                )
            )

    if shot_index == 5:
        deploy_box = _box(
            "deploy-box",
            Vec3(0.75 + progress * 2.2, -0.75 + progress * 0.55, 4.1 - progress * 0.2),
            Vec3(0.75, 0.58, 0.55),
            (150, 116, 70),
        )
        deploy_box.rotate_y(progress * 1.2)
        meshes.append(deploy_box)

    return Scene3D(camera=camera, meshes=meshes, background=(31, 24, 22))


def story_profile_for_topic(topic_id: object) -> str:
    if not isinstance(topic_id, str):
        raise ValueError(f"unsupported software 3d story topic: {topic_id!r}")
    normalized = topic_id.strip()
    if normalized in COW_STORY_TOPICS:
        return COW_STORY_PROFILE
    if normalized == ODYSSEY_STORY_PROFILE:
        return ODYSSEY_STORY_PROFILE
    raise ValueError(f"unsupported software 3d story topic: {normalized or '<blank>'}")


def build_story_scene(
    *,
    shot_index: int,
    progress: float,
    width: int,
    height: int,
    story_profile: str = COW_STORY_PROFILE,
) -> Scene3D:
    if story_profile == ODYSSEY_STORY_PROFILE:
        return build_odyssey_story_scene(
            shot_index=shot_index,
            progress=progress,
            width=width,
            height=height,
        )
    if story_profile != COW_STORY_PROFILE:
        raise ValueError(f"unsupported software 3d story profile: {story_profile}")
    return _build_cow_story_scene(
        shot_index=shot_index,
        progress=progress,
        width=width,
        height=height,
    )


def _load_render_source(render_source: Path) -> tuple[list[dict[str, object]], str]:
    raw = json.loads(render_source.read_text(encoding="utf-8"))
    if raw.get("schema_version") != "hottop.render.v2":
        raise ValueError("software 3d production requires hottop.render.v2")
    frames = raw.get("frames")
    if not isinstance(frames, list) or len(frames) != 5:
        raise ValueError("software 3d flagship source requires exactly five frames")
    return frames, story_profile_for_topic(raw.get("topic_id"))


def _story_profile_from_workspace_plan(path: Path) -> str:
    if not path.is_file():
        raise ValueError(f"software 3d workspace plan is missing: {path}")
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("software 3d workspace plan is unreadable") from exc
    if raw.get("schema_version") != "hottop.video-plan.v1":
        raise ValueError("software 3d workspace requires hottop.video-plan.v1")
    return story_profile_for_topic(raw.get("topic_id"))


def render_story_frame_sequence(
    *,
    render_source: Path,
    output_dir: Path,
    width: int = 360,
    height: int = 640,
    fps: int = 12,
    seconds_per_shot: float = 2.4,
) -> list[Path]:
    frames, story_profile = _load_render_source(render_source)
    if fps <= 0 or seconds_per_shot <= 0:
        raise ValueError("fps and seconds_per_shot must be positive")
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    count_per_shot = max(1, round(fps * seconds_per_shot))
    for shot_position, _ in enumerate(frames, start=1):
        for frame_index in range(count_per_shot):
            progress = frame_index / max(1, count_per_shot - 1)
            scene = build_story_scene(
                shot_index=shot_position,
                progress=progress,
                width=width,
                height=height,
                story_profile=story_profile,
            )
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
        shots=[
            VideoShotArtifact(
                shot_index=shot_index,
                path=str(resolved_output),
                artifact_kind="deterministic-generated",
                backend="software3d",
                sha256=hashlib.sha256(payload).hexdigest(),
                size_bytes=len(payload),
            )
        ],
    )
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        temporary.write_text(
            manifest.model_dump_json(indent=2) + "\n",
            encoding="utf-8",
        )
        temporary.replace(manifest_path)
    finally:
        temporary.unlink(missing_ok=True)
    return manifest_path


def render_story_shot_video(
    *,
    shot_index: int,
    output: Path,
    duration_seconds: float,
    width: int = 360,
    height: int = 640,
    fps: int = 12,
    story_profile: str | None = None,
    runner: Runner = subprocess.run,
) -> Path:
    if shot_index < 1 or shot_index > 5:
        raise ValueError("software 3d flagship story expects shot_index 1..5")
    if duration_seconds <= 0 or fps <= 0:
        raise ValueError("duration_seconds and fps must be positive")

    resolved_output = output.resolve()
    if story_profile is None:
        workspace_plan = resolved_output.parent.parent / "hottop-video-plan.json"
        story_profile = _story_profile_from_workspace_plan(workspace_plan)
    elif story_profile not in {COW_STORY_PROFILE, ODYSSEY_STORY_PROFILE}:
        raise ValueError(f"unsupported software 3d story profile: {story_profile}")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.unlink(missing_ok=True)
    manifest_path = resolved_output.with_suffix(".artifact.json")
    manifest_path.unlink(missing_ok=True)
    frames_dir = output.with_suffix(".frames")
    shutil.rmtree(frames_dir, ignore_errors=True)
    frames_dir.mkdir(parents=True, exist_ok=True)
    frame_count = max(2, round(duration_seconds * fps))
    try:
        for frame_index in range(frame_count):
            progress = frame_index / max(1, frame_count - 1)
            scene = build_story_scene(
                shot_index=shot_index,
                progress=progress,
                width=width,
                height=height,
                story_profile=story_profile,
            )
            render_scene_frame(scene, frames_dir / f"frame-{frame_index:05d}.png")

        completed = runner(
            [
                "ffmpeg",
                "-y",
                "-framerate",
                str(fps),
                "-i",
                str(frames_dir / "frame-%05d.png"),
                "-t",
                f"{duration_seconds:g}",
                "-an",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                str(output),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            output.unlink(missing_ok=True)
            raise RuntimeError(
                f"software 3d shot encoding failed with return code {completed.returncode}"
            )
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
    parser.add_argument("--story-profile")
    parser.add_argument("--width", type=int, default=360)
    parser.add_argument("--height", type=int, default=640)
    parser.add_argument("--fps", type=int, default=12)
    parser.add_argument("--seconds-per-shot", type=float, default=2.4)
    parser.add_argument("--duration-seconds", type=float)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if args.shot_index is not None or args.output is not None:
        if args.shot_index is None or args.output is None or args.duration_seconds is None:
            raise SystemExit("shot mode requires --shot-index, --duration-seconds and --output")
        render_story_shot_video(
            shot_index=args.shot_index,
            output=Path(args.output),
            duration_seconds=args.duration_seconds,
            width=args.width,
            height=args.height,
            fps=args.fps,
            story_profile=args.story_profile,
        )
        return
    if not args.render or not args.output_dir:
        raise SystemExit("sequence mode requires --render and --output-dir")
    render_story_frame_sequence(
        render_source=Path(args.render),
        output_dir=Path(args.output_dir),
        width=args.width,
        height=args.height,
        fps=args.fps,
        seconds_per_shot=args.seconds_per_shot,
    )


if __name__ == "__main__":
    main()
