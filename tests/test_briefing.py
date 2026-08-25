from hottop.briefing import build_brief
from hottop.mechanism import HotspotMechanism, ProductMechanismMapping
from hottop.models import ProductProfile, TrendCandidate


def _mechanism_mapping() -> ProductMechanismMapping:
    return ProductMechanismMapping(
        mechanism=HotspotMechanism(
            topic_id="film:odyssey",
            source_mode="user-supplied",
            recognition_hook="a giant blocks the only obvious exit until the trapped group changes the rules",
            causal_chain=[
                "the crew enters the cave",
                "the giant seals the exit and traps everyone",
                "a clever route changes the terms of escape",
                "the crew gets back to the voyage",
            ],
            native_visual_grammar="original live-action mythic cave cinema with huge scale contrast",
            native_dialogue_grammar="tense short lines followed by a confident reversal",
            native_audio_grammar="dark cave ambience, restrained mythic score, impact Foley at the reversal",
        ),
        promoted_product="InkClawAgent",
        product_role="the alternate route that breaks the workflow trap",
        product_bridge="remove setup and deployment friction instead of optimizing the blocked path",
        outcome_before="developers are trapped spending effort on setup friction",
        outcome_after="developers return to the actual task",
        punchline="别跟洞口耗，直接换条路。",
        comparison_target="work巴迪",
        comparison_role="the workflow obstruction at the cave exit",
    )


def test_build_brief_creates_mechanism_driven_four_panel_with_original_visual_guardrails():
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

    brief = build_brief(
        candidate,
        product,
        comparison_target="work巴迪",
        mechanism_mapping=_mechanism_mapping(),
    )

    assert len(brief.panels) == 4
    assert [panel.intent for panel in brief.panels] == [
        "setup",
        "escalation",
        "reversal",
        "punchline",
    ]
    assert brief.role_map.product_role == "the alternate route that breaks the workflow trap"
    assert brief.role_map.archetype == "mechanism-driven"
    assert brief.mechanism_mapping.mechanism.native_audio_grammar is not None
    assert "original live-action mythic cave cinema" in brief.image_prompt
    assert "actor likeness" in brief.negative_prompt.lower()
    assert "exact film frame" in brief.negative_prompt.lower()
    assert brief.claim_status == "satire"


def test_brief_flags_objective_punchline_when_evidence_is_missing():
    candidate = TrendCandidate(
        id="film:odyssey",
        title="A supplied cultural scene",
        url="https://example.com/slow",
        source="tech",
    )
    product = ProductProfile(name="InkClawAgent")

    brief = build_brief(
        candidate,
        product,
        comparison_target="work巴迪",
        punchlines=["InkClawAgent 比 work巴迪 快 10 倍"],
        mechanism_mapping=_mechanism_mapping(),
    )

    assert brief.claim_status == "needs_evidence"
    assert "unsupported-comparison" in brief.risk_flags
