from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_project_requires_mechanism_mapping_not_hotspot_skin() -> None:
    project = _text("PROJECT.md")

    assert "### Cultural mechanism mapping" in project
    assert "Borrow the mechanism, not the skin" in project
    assert "product must change the story outcome" in project
    assert "hotspot recognition → mapping → product consequence → punchline" in project
    assert "Every retained hotspot element must have a job" in project


def test_creative_skill_routes_user_supplied_and_unspecified_hotspots_differently() -> None:
    skill = _text("skills/brand-metaphor-creative/SKILL.md")

    assert "## Cultural mechanism mapping" in skill
    assert "If the user supplies a hotspot" in skill
    assert "If the user does not supply a hotspot" in skill
    assert "causal/relationship mechanism" in skill
    assert "native visual grammar" in skill
    assert "native dialogue/language rhythm" in skill
    assert "native audio grammar" in skill
    assert "product must change the story outcome" in skill


def test_video_quality_can_route_through_image_first_reference_conditioning() -> None:
    project = _text("PROJECT.md")
    skill = _text("skills/brand-metaphor-creative/SKILL.md")

    for text in (project, skill):
        assert "Image-first quality recovery" in text
        assert "reference-conditioned I2V" in text
        assert "not a slideshow" in text
        assert "direct video" in text


def test_hotspot_skill_preserves_a_user_supplied_topic_and_analyzes_it_first() -> None:
    skill = _text("skills/hottop-meme/SKILL.md")

    assert "When the user supplies the hotspot" in skill
    assert "analyze that supplied hotspot first" in skill
    assert "When no hotspot is supplied" in skill
