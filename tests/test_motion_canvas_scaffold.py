from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "video" / "motion-canvas"


def test_motion_canvas_scaffold_is_pinned_and_plan_driven() -> None:
    package = json.loads((PROJECT / "package.json").read_text(encoding="utf-8"))

    assert package["private"] is True
    assert package["scripts"]["render"] == "node scripts/render.mjs"
    assert package["dependencies"]["@motion-canvas/2d"] == "3.17.2"
    assert package["dependencies"]["@motion-canvas/core"] == "3.17.2"
    assert package["devDependencies"]["@motion-canvas/vite-plugin"] == "3.17.2"
    assert package["devDependencies"]["vite"]

    render_script = (PROJECT / "scripts" / "render.mjs").read_text(encoding="utf-8")
    assert "--plan" in render_script
    assert "hottop.video-plan.v1" in render_script
    assert "src/generated-plan.ts" in render_script


def test_motion_canvas_scene_preserves_one_continuous_plan_timeline() -> None:
    project_source = (PROJECT / "src" / "project.ts").read_text(encoding="utf-8")
    scene_source = (PROJECT / "src" / "scenes" / "hottop.tsx").read_text(encoding="utf-8")

    assert "makeProject" in project_source
    assert "hottop" in project_source
    assert "plan.shots" in scene_source
    assert "start_seconds" in scene_source
    assert "duration_seconds" in scene_source
    assert "plan.audio_cues" in scene_source
    assert "caption" in scene_source
    assert "waitFor" in scene_source
