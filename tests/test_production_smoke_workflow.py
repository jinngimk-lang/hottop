from pathlib import Path

import yaml


def test_production_smoke_workflow_executes_checked_in_software3d_stories():
    path = Path(".github/workflows/production-smoke.yml")
    assert path.is_file()

    workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
    jobs = workflow["jobs"]
    job = jobs["software3d-production-smoke"]
    steps = job["steps"]
    rendered = "\n".join(str(step) for step in steps)

    assert ".[dev,video]" in rendered
    assert "ffmpeg" in rendered
    assert "espeak" in rendered
    assert "examples/video/inkclaw-cow-snake.render.json" in rendered
    assert "config/video/anti-polish-software3d.yml" in rendered
    assert "examples/video/inkclaw-odyssey-witch-pigs.render.json" in rendered
    assert "config/video/cinematic-software3d.yml" in rendered
    assert "hottop video-run" in rendered
    assert rendered.count("--execute") >= 2
    assert "hottop-output.mp4" in rendered
    assert "cow" in rendered
    assert "odyssey" in rendered
    assert "sha256.txt" in rendered
    assert "upload-artifact" in rendered
    assert "*.artifact.json" in rendered
