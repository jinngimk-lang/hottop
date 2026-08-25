import json

from typer.testing import CliRunner

from hottop.cli import app

runner = CliRunner()


def test_render_concept_exports_flexible_render_v2(tmp_path):
    concept_path = tmp_path / "concept.json"
    concept_path.write_text(
        json.dumps(
            {
                "topic": {
                    "id": "culture:reveal",
                    "title": "A visual reveal trend",
                    "url": "https://example.com/trend",
                    "source": "test",
                    "tags": ["social"],
                },
                "promotion": {
                    "subject_name": "Ribbon Noodles",
                    "subject_type": "product",
                    "category": "food",
                    "primary_job": "quick lunch",
                    "primary_pain_point": "forgettable product advertising",
                    "primary_differentiator": "long elastic ribbon texture",
                    "semantic_terms": ["long", "elastic", "ribbon"],
                },
                "strategy": {
                    "category_default": "show a finished bowl immediately",
                    "deleted_constraint": "the product must be fully revealed in frame one",
                    "new_competition_axis": "curiosity before reveal",
                    "bridge_type": "shape-material",
                    "bridge": "the noodle ribbon becomes the recognizable visual action before the food reveal",
                    "expression_form": "swipe-reveal",
                },
                "comparison_target": None,
                "beats": [
                    {
                        "scene": "A minimal hand gesture launches a mysterious ribbon-like strand.",
                        "caption": None,
                        "intent": "tease",
                    },
                    {
                        "scene": "The strand stretches across the frame with glossy food texture becoming visible.",
                        "caption": "Wait for it.",
                        "intent": "extend curiosity",
                    },
                    {
                        "scene": "The strand lands in the branded bowl and reveals it was the product all along.",
                        "caption": "The reveal is the product.",
                        "intent": "brand reveal",
                    },
                ],
                "visual_medium": "commercial-product",
                "genre_treatment": "minimal premium food photography with playful social-ad timing",
                "punchlines": ["The reveal is the product."],
                "image_prompt": "Original three-frame commercial food carousel; product ribbon is the visual action; clean studio lighting.",
                "negative_prompt": "No copied ad layout, no protected character design, no competitor logo.",
                "risk_flags": [],
                "claim_status": "satire",
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = runner.invoke(app, ["render-concept", str(concept_path)])

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["schema_version"] == "hottop.render.v2"
    assert payload["expression_form"] == "swipe-reveal"
    assert payload["visual_medium"] == "commercial-product"
    assert payload["category_default"] == "show a finished bowl immediately"
    assert payload["deleted_constraint"] == "the product must be fully revealed in frame one"
    assert payload["new_competition_axis"] == "curiosity before reveal"
    assert payload["bridge_type"] == "shape-material"
    assert len(payload["frames"]) == 3
    assert payload["frames"][1]["caption"] == "Wait for it."
