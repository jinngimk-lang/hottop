from pathlib import Path

import yaml


def test_production_smoke_workflow_executes_checked_in_software3d_stories():
    path = Path(".github/workflows/production-smoke.yml")
    assert path.is_file()

    raw = path.read_text(encoding="utf-8")
    workflow = yaml.safe_load(raw)
    jobs = workflow["jobs"]
    job = jobs["software3d-production-smoke"]
    steps = job["steps"]
    rendered = "\n".join(str(step) for step in steps)

    assert "push:" in raw
    assert "branches:" in raw
    assert "- main" in raw
    assert ".[dev,video]" in rendered
    assert "ffmpeg" in rendered
    assert "espeak-ng-espeak" in rendered
    assert "Full dictionary is not installed for 'zh'" in raw
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
    assert "artifacts/production-smoke/cow/shots/*.artifact.json" in raw
    assert "artifacts/production-smoke/odyssey/shots/*.artifact.json" in raw
    assert "HOTTOP_ESPEAK_NG_ROLE_SEPARATION" in raw
    assert "abs(role_pitches[\"young-cow\"] - role_pitches[\"mother-cow\"]) >= 6" in raw
    assert "HOTTOP_SEAM_QUALITY" in raw
    assert "max_seam_delta <= 8.0" in raw
    assert "max_seam_ratio <= 5.5" in raw
