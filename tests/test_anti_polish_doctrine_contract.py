from pathlib import Path
import tomllib

import yaml


def test_project_and_skill_persist_controlled_badness_doctrine():
    project = Path("PROJECT.md").read_text(encoding="utf-8")
    skill = Path("skills/brand-metaphor-creative/SKILL.md").read_text(encoding="utf-8")
    combined = f"{project}\n{skill}"

    for phrase in (
        "Anti-Polish",
        "Controlled Badness",
        "low production feel",
        "high comedy control",
        "character continuity",
        "subtitle correctness",
        "comedy timing",
        "Wan2.2",
        "MoviePy",
        "headless",
        "Motion Canvas",
        "FFmpeg",
    ):
        assert phrase in combined

    assert "Do not polish the badness away; make the badness precise." in project


def test_video_upstreams_are_pinned_with_safe_roles():
    versions = yaml.safe_load(Path("integrations/versions.yml").read_text(encoding="utf-8"))

    assert versions["wan22"]["repo"] == "Wan-Video/Wan2.2"
    assert versions["wan22"]["license"] == "Apache-2.0"
    assert versions["moviepy"]["repo"] == "Zulko/moviepy"
    assert versions["moviepy"]["version"] == "2.2.0"
    assert versions["moviepy"]["license"] == "MIT"
    assert versions["motion_canvas"]["commit"] == "7b91435c301d530351dcf5ebb91dd139c002e405"
    assert versions["motion_canvas"]["license"] == "MIT"
    assert versions["ffmpeg"]["commit"] == "1019f8f036602a8464185baa4857654337eeca14"
    assert versions["remotion"]["default_enabled"] is False
    assert "license" in versions["remotion"]["notes"].lower()


def test_moviepy_is_an_optional_video_dependency_not_a_core_requirement():
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    dependencies = pyproject["project"]["optional-dependencies"]["video"]

    assert "moviepy>=2.2,<3" in dependencies
    assert all(not dependency.startswith("moviepy") for dependency in pyproject["project"]["dependencies"])
