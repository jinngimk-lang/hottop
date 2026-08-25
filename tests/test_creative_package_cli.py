import json

from typer.testing import CliRunner

from hottop.cli import app

runner = CliRunner()


def test_package_concepts_selects_and_emits_render_v2(tmp_path):
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
    assert payload["selected_index"] == 0
    assert payload["selected_concept"]["strategy"]["expression_form"] == "swipe-reveal"
    assert payload["selected_render"]["schema_version"] == "hottop.render.v2"
    assert len(payload["selected_render"]["frames"]) == 3
