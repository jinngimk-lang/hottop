import json

from typer.testing import CliRunner

from hottop.cli import app

runner = CliRunner()


def _orchestration_item() -> dict[str, object]:
    promotion = {
        "subject_name": "Ribbon Lunch",
        "subject_type": "product",
        "category": "food",
        "primary_job": "memorable quick lunch",
        "primary_pain_point": "generic food ads look interchangeable",
        "primary_differentiator": "long elastic ribbon texture",
        "semantic_terms": ["long", "elastic", "ribbon"],
    }
    return {
        "intent": {
            "request": "给 Ribbon Lunch 做小红书出圈高级广告，最后揭示产品",
            "promotion_target": {
                "value": "Ribbon Lunch",
                "source": "explicit",
                "confidence": 1.0,
            },
            "campaign_goal": {
                "value": "hotspot-participation",
                "source": "inferred",
                "confidence": 0.8,
            },
            "platform": {"value": "xiaohongshu", "source": "inferred", "confidence": 0.98},
            "style": {"value": "minimal-premium", "source": "inferred", "confidence": 0.86},
            "creative_ambition": {"value": "breakout", "source": "inferred", "confidence": 0.92},
            "product_visibility": {
                "value": "metaphor-first",
                "source": "inferred",
                "confidence": 0.93,
            },
            "audience": {"value": None, "source": "defaulted", "confidence": 0.0},
            "hotspot_preference": {"value": "auto", "source": "defaulted", "confidence": 0.0},
            "constraints": [],
        },
        "promotion_context": promotion,
        "options": [
            {
                "label": "bridge-reveal",
                "concept": {
                    "topic": {
                        "id": "bridge",
                        "title": "Fictional culture moment",
                        "url": "https://example.com/bridge",
                        "source": "test",
                        "tags": ["culture", "food"],
                    },
                    "promotion": promotion,
                    "strategy": {
                        "category_default": "show product immediately",
                        "deleted_constraint": "full reveal in frame one",
                        "new_competition_axis": "curiosity",
                        "bridge_type": "shape-material",
                        "bridge": "product ribbon becomes the action",
                        "expression_form": "swipe-reveal",
                    },
                    "beats": [
                        {"scene": "Ribbon crosses frame.", "caption": None, "intent": "tease"},
                        {"scene": "Texture clue.", "caption": "Wait.", "intent": "clue"},
                        {
                            "scene": "Product reveal.",
                            "caption": "There it is.",
                            "intent": "reveal",
                        },
                    ],
                    "visual_medium": "commercial-product",
                    "genre_treatment": "minimal premium food photography",
                    "punchlines": ["There it is."],
                    "image_prompt": "Original product-led reveal.",
                    "negative_prompt": "No copied protected assets.",
                    "risk_flags": [],
                    "claim_status": "satire",
                },
                "review": {
                    "name": "bridge-reveal",
                    "instant_comprehension": 0.9,
                    "natural_linkage": 0.92,
                    "product_centrality": 0.95,
                    "surprise": 0.86,
                    "ownability": 0.9,
                    "evidence_safety": 0.95,
                    "original_execution": 0.95,
                },
                "context_review": {
                    "name": "bridge-reveal",
                    "platform_fit": 0.95,
                    "style_fit": 0.95,
                    "campaign_goal_fit": 0.9,
                    "ambition_fit": 0.9,
                    "project_shape_fit": 0.95,
                    "hotspot_native_fit": 0.9,
                    "humor_or_delight": 0.75,
                    "humor_expected": False,
                },
            }
        ],
        "references": [],
    }


def test_creative_batch_emits_flexible_selected_concepts_and_render_v2(tmp_path):
    batch_path = tmp_path / "creative-batch.json"
    batch_path.write_text(json.dumps({"items": [_orchestration_item()]}), encoding="utf-8")

    result = runner.invoke(app, ["creative-batch", str(batch_path)])

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["schema_version"] == "hottop.creative-batch.v1"
    assert payload["input_count"] == 1
    assert payload["results"][0]["selected_concept"]["strategy"]["expression_form"] == "swipe-reveal"
    assert payload["results"][0]["selected_render"]["schema_version"] == "hottop.render.v2"
