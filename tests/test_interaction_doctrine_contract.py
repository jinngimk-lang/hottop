from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_project_charter_persists_adaptive_interaction_doctrine():
    project = (ROOT / "PROJECT.md").read_text(encoding="utf-8").lower()

    for phrase in (
        "adaptive guided intake",
        "0–3 questions",
        "creative ambition",
        "product visibility",
        "platform-native",
        "project-shape",
        "contextual review",
    ):
        assert phrase in project


def test_brand_metaphor_skill_includes_interaction_routing_rules():
    skill = (ROOT / "skills/brand-metaphor-creative/SKILL.md").read_text(encoding="utf-8").lower()

    for phrase in (
        "ask only high-impact questions",
        "creative ambition",
        "platform",
        "product visibility",
        "project shape",
    ):
        assert phrase in skill
