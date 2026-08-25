from pathlib import Path

import yaml


def test_software3d_production_smoke_runs_real_full_pipeline():
    workflow_path = Path(".github/workflows/software3d-production-smoke.yml")
    assert workflow_path.is_file(), "software3d production smoke workflow must be checked in"

    raw = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    jobs = raw["jobs"]
    job = jobs["production-smoke"]
    steps = job["steps"]
    commands = "\n".join(str(step.get("run", "")) for step in steps)
    uses = [str(step.get("uses", "")) for step in steps]

    assert 'pip install -e ".[video]"' in commands
    assert "hottop video-doctor" in commands
    assert "config/video/anti-polish-software3d.yml" in commands
    assert "hottop video-run" in commands
    assert "--execute" in commands
    assert "examples/video/inkclaw-cow-snake.render.json" in commands
    assert "ffprobe" in commands
    assert any(value.startswith("actions/upload-artifact@") for value in uses)
