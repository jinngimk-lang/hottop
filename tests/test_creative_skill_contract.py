from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "PROJECT.md"
CREATIVE_SKILL = ROOT / "skills" / "brand-metaphor-creative" / "SKILL.md"
HOTTOP_SKILL = ROOT / "skills" / "hottop-meme" / "SKILL.md"


def test_project_persists_broader_creative_direction() -> None:
    text = PROJECT.read_text(encoding="utf-8")
    assert "constraint deletion" in text.lower()
    assert "swipe-reveal" in text.lower()
    assert "visual metaphor" in text.lower()
    assert "not every concept must be four-panel" in text.lower()


def test_brand_metaphor_skill_captures_creative_method() -> None:
    text = CREATIVE_SKILL.read_text(encoding="utf-8")
    required = [
        "category default",
        "constraint deletion",
        "bridge search",
        "format selection",
        "swipe-reveal",
        "creative review gate",
        "named competitor",
    ]
    for phrase in required:
        assert phrase in text.lower()


def test_hottop_meme_skill_routes_to_brand_metaphor_skill() -> None:
    text = HOTTOP_SKILL.read_text(encoding="utf-8")
    assert "brand-metaphor-creative" in text
