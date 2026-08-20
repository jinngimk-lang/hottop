from hottop.briefing import build_brief
from hottop.models import ProductProfile, TrendCandidate


def test_build_brief_creates_four_panel_hot_topic_meme_with_original_visual_guardrails():
    candidate = TrendCandidate(
        id="film:odyssey",
        title="奥德赛：独眼巨人洞穴冲突成为热议画面",
        summary="史诗冒险中，英雄靠策略突破独眼巨人把守的洞穴。",
        url="https://example.com/odyssey",
        source="movie-trend",
        tags=["film", "myth", "visual"],
        metrics={"recognizability": 0.95, "conflict_clarity": 0.95},
    )
    product = ProductProfile(
        name="InkClawAgent",
        url="https://inkclawagent.com/home",
        strengths=["multi-agent collaboration", "review-edit-revise workflow"],
    )

    brief = build_brief(candidate, product, comparison_target="work巴迪")

    assert len(brief.panels) == 4
    assert brief.panels[0].intent == "setup"
    assert brief.panels[1].intent == "escalation"
    assert brief.panels[2].intent == "reversal"
    assert brief.panels[3].intent == "punchline"
    assert "work巴迪" in brief.panels[1].caption
    assert "InkClawAgent" in brief.panels[2].caption
    assert any("InkClawAgent" in line for line in brief.punchlines)
    assert "actor likeness" in brief.negative_prompt.lower()
    assert "exact film frame" in brief.negative_prompt.lower()
    assert brief.claim_status == "satire"


def test_brief_flags_objective_punchline_when_evidence_is_missing():
    candidate = TrendCandidate(
        id="tech:1",
        title="手动流程太慢",
        url="https://example.com/slow",
        source="tech",
    )
    product = ProductProfile(name="ToolX")

    brief = build_brief(
        candidate,
        product,
        comparison_target="ToolY",
        punchlines=["ToolX 比 ToolY 快 10 倍"],
    )

    assert brief.claim_status == "needs_evidence"
    assert "unsupported-comparison" in brief.risk_flags
