from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_project_charter_requires_fresh_research_for_every_new_asset_request() -> None:
    project = _text("PROJECT.md")

    assert "## Mandatory fresh-generation entry gate" in project
    assert "Every new image or video generation request" in project
    assert "Historical examples are not defaults" in project
    assert "`hottop generation-preflight`" in project
    assert "6 hours" in project
    assert "7 days" in project


def test_general_creative_skill_binds_chat_to_repo_truth_and_dynamic_choices() -> None:
    skill = _text("skills/brand-metaphor-creative/SKILL.md")

    assert "### Mandatory fresh-generation preflight" in skill
    assert "reread `PROJECT.md` and `STATUS.md`" in skill
    assert "re-explore current news, culture, and internet hotspots" in skill
    assert "product, hotspot, visual style/medium, and output format" in skill
    assert "`generation-preflight`" in skill


def test_hottop_meme_skill_cannot_reuse_a_previous_hotspot_as_default() -> None:
    skill = _text("skills/hottop-meme/SKILL.md")

    assert "### Mandatory fresh-generation preflight" in skill
    assert "Never reuse a previous hotspot, product, character, style, or panel format as an implicit default" in skill
    assert "fresh hotspot evidence" in skill
    assert "`generation-preflight`" in skill
