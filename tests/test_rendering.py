from hottop.briefing import build_brief
from hottop.models import ProductProfile, TrendCandidate
from hottop.rendering import build_render_request


def test_build_render_request_preserves_four_panels_and_guardrails():
    candidate = TrendCandidate(
        id="film:odyssey",
        title="奥德赛洞穴破局",
        url="https://example.com/odyssey",
        source="movie-trend",
        summary="公共领域史诗原型中的洞穴困局与智取破局。",
    )
    product = ProductProfile(name="InkClawAgent")
    brief = build_brief(candidate, product, comparison_target="work巴迪")

    request = build_render_request(brief)

    assert request.schema_version == "hottop.render.v1"
    assert request.layout == "four-panel-grid"
    assert request.aspect_ratio == "1:1"
    assert len(request.panels) == 4
    assert [panel.caption for panel in request.panels] == [panel.caption for panel in brief.panels]
    assert request.master_prompt == brief.image_prompt
    assert request.negative_prompt == brief.negative_prompt
    assert request.claim_status == "satire"
    assert request.provider is None
    assert "actor likeness" in request.negative_prompt.lower()


def test_render_request_keeps_provider_settings_out_of_core_contract():
    candidate = TrendCandidate(
        id="ai:agents",
        title="多 Agent 工作流热议",
        url="https://example.com/agents",
        source="tech",
    )
    brief = build_brief(candidate, ProductProfile(name="InkClawAgent"))

    request = build_render_request(brief)
    payload = request.model_dump(mode="json")

    assert "api_key" not in payload
    assert "model" not in payload
    assert payload["topic_id"] == "ai:agents"
    assert payload["product_name"] == "InkClawAgent"
