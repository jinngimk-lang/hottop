from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "PROJECT.md"
CREATIVE_SKILL = ROOT / "skills" / "brand-metaphor-creative" / "SKILL.md"
HOTTOP_SKILL = ROOT / "skills" / "hottop-meme" / "SKILL.md"
REFERENCE_SKILL = ROOT / "skills" / "creative-reference-research" / "SKILL.md"


def test_project_persists_broader_creative_direction() -> None:
    text = PROJECT.read_text(encoding="utf-8")
    assert "constraint deletion" in text.lower()
    assert "swipe-reveal" in text.lower()
    assert "visual metaphor" in text.lower()
    assert "not every concept must be four-panel" in text.lower()


def test_project_persists_continuity_protocol() -> None:
    text = PROJECT.read_text(encoding="utf-8").lower()
    required = [
        "living project charter",
        "context recovery",
        "material direction change",
        "decision log",
        "update the charter",
    ]
    for phrase in required:
        assert phrase in text


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


def test_brand_metaphor_skill_captures_project_memory_loop() -> None:
    text = CREATIVE_SKILL.read_text(encoding="utf-8").lower()
    required = [
        "persistent project protocol",
        "context pressure",
        "recovery order",
        "update the charter",
        "decision log",
    ]
    for phrase in required:
        assert phrase in text


def test_hottop_meme_skill_routes_to_brand_metaphor_skill() -> None:
    text = HOTTOP_SKILL.read_text(encoding="utf-8")
    assert "brand-metaphor-creative" in text


def test_visual_reference_skill_is_provenance_first_and_non_copying() -> None:
    text = REFERENCE_SKILL.read_text(encoding="utf-8").lower()
    required = [
        "visual reference",
        "playwright",
        "provenance",
        "analysis-only",
        "do not copy",
        "composition grammar",
        "reference manifest",
    ]
    for phrase in required:
        assert phrase in text


def test_project_lists_visual_reference_research_as_reusable_skill() -> None:
    text = PROJECT.read_text(encoding="utf-8")
    assert "skills/creative-reference-research/SKILL.md" in text
