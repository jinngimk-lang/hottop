import json

from typer.testing import CliRunner

from hottop.cli import app

runner = CliRunner()


def test_intent_command_resolves_natural_request():
    result = runner.invoke(
        app,
        [
            "intent",
            "给这个咖啡新品做一个小红书出圈高级广告，产品最后再揭示",
        ],
    )

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["platform"]["value"] == "xiaohongshu"
    assert payload["creative_ambition"]["value"] == "breakout"
    assert payload["product_visibility"]["value"] == "metaphor-first"


def test_next_question_command_emits_ready_state_for_complete_intent(tmp_path):
    intent_path = tmp_path / "intent.json"
    result = runner.invoke(
        app,
        [
            "intent",
            "给这个咖啡新品做一个小红书出圈高级广告，产品最后再揭示",
            "--output",
            str(intent_path),
        ],
    )
    assert result.exit_code == 0, result.stdout

    result = runner.invoke(app, ["next-question", str(intent_path)])

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["ready_to_create"] is True
    assert payload["question"] is None


def test_package_concepts_command_selects_candidate(tmp_path):
    package_path = tmp_path / "package.json"
    package_path.write_text(
        json.dumps(
            {
                "options": [
                    {
                        "label": "bridge-led-reveal",
                        "concept": {
                            "topic": {
                                "id": "consumer:reveal",
                                "title": "Fictional product reveal format",
                                "url": "https://example.com/trend",
                                "source": "test",
                                "tags": ["culture", "food"],
                            },
                            "promotion": {
                                "subject_name": "Ribbon Lunch",
                                "subject_type": "product",
                                "category": "food",
                                "primary_job": "memorable quick lunch",
                                "primary_pain_point": "generic food ads look interchangeable",
                                "primary_differentiator": "long elastic ribbon texture",
                                "semantic_terms": ["long", "elastic", "ribbon"],
                            },
                            "strategy": {
                                "category_default": "show the bowl immediately",
                                "deleted_constraint": "full product reveal in frame one",
                                "new_competition_axis": "curiosity before reveal",
                                "bridge_type": "shape-material",
                                "bridge": "the food ribbon becomes the visual action",
                                "expression_form": "swipe-reveal",
                            },
                            "beats": [
                                {
                                    "scene": "A mysterious ribbon crosses a clean frame.",
                                    "caption": None,
                                    "intent": "tease",
                                },
                                {
                                    "scene": "Texture reveals that the ribbon is food.",
                                    "caption": "Wait for it.",
                                    "intent": "material clue",
                                },
                                {
                                    "scene": "The ribbon lands in the fictional product bowl.",
                                    "caption": "The reveal is the product.",
                                    "intent": "reveal",
                                },
                            ],
                            "visual_medium": "commercial-product",
                            "genre_treatment": "minimal premium food photography",
                            "punchlines": ["The reveal is the product."],
                            "image_prompt": "Original three-frame food reveal with a ribbon-like product action.",
                            "negative_prompt": "No copied layout, protected character, logo, or trade dress.",
                            "risk_flags": [],
                            "claim_status": "satire",
                        },
                        "review": {
                            "name": "bridge-led-reveal",
                            "instant_comprehension": 0.92,
                            "natural_linkage": 0.95,
                            "product_centrality": 0.97,
                            "surprise": 0.88,
                            "ownability": 0.93,
                            "evidence_safety": 0.95,
                            "original_execution": 0.95,
                        },
                    }
                ],
                "references": [],
            }
        ),
        encoding="utf-8",
    )

    result = runner.invoke(app, ["package-concepts", str(package_path)])

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["schema_version"] == "hottop.creative-package.v1"
    assert payload["selected_render"]["schema_version"] == "hottop.render.v2"


def test_orchestrate_command_emits_selected_render(tmp_path):
    orchestration_path = tmp_path / "orchestration.json"
    orchestration_path.write_text(
        json.dumps(
            {
                "intent": {
                    "request": "给 Ribbon Lunch 做小红书出圈高级广告，最后揭示产品",
                    "promotion_target": {"value": "Ribbon Lunch", "source": "explicit", "confidence": 1.0},
                    "campaign_goal": {"value": "hotspot-participation", "source": "inferred", "confidence": 0.8},
                    "platform": {"value": "xiaohongshu", "source": "inferred", "confidence": 0.98},
                    "style": {"value": "minimal-premium", "source": "inferred", "confidence": 0.86},
                    "creative_ambition": {"value": "breakout", "source": "inferred", "confidence": 0.92},
                    "product_visibility": {"value": "metaphor-first", "source": "inferred", "confidence": 0.93},
                    "audience": {"value": None, "source": "defaulted", "confidence": 0.0},
                    "hotspot_preference": {"value": "auto", "source": "defaulted", "confidence": 0.0},
                    "constraints": [],
                },
                "promotion_context": {
                    "subject_name": "Ribbon Lunch",
                    "subject_type": "product",
                    "category": "food",
                    "primary_job": "memorable quick lunch",
                    "primary_pain_point": "generic food ads look interchangeable",
                    "primary_differentiator": "long elastic ribbon texture",
                    "semantic_terms": ["long", "elastic", "ribbon"],
                },
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
                            "promotion": {
                                "subject_name": "Ribbon Lunch",
                                "subject_type": "product",
                                "category": "food",
                                "primary_job": "memorable quick lunch",
                                "primary_pain_point": "generic food ads look interchangeable",
                                "primary_differentiator": "long elastic ribbon texture",
                                "semantic_terms": ["long", "elastic", "ribbon"],
                            },
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
                                {"scene": "Product reveal.", "caption": "There it is.", "intent": "reveal"},
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
        ),
        encoding="utf-8",
    )

    result = runner.invoke(app, ["orchestrate", str(orchestration_path)])

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["schema_version"] == "hottop.orchestration.v1"
    assert payload["selected_render"]["schema_version"] == "hottop.render.v2"
