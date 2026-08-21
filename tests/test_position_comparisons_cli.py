import json

from typer.testing import CliRunner

from hottop.cli import app

runner = CliRunner()


def test_position_ingests_comparison_candidates_and_selects_best_target(tmp_path):
    product_path = tmp_path / "product.yml"
    product_path.write_text(
        """
name: Example Coffee
subject_type: brand
category: ready-to-drink coffee
jobs_to_be_done:
  - quick caffeine before commuting
pain_points_solved:
  - no time to brew coffee
""".strip()
        + "\n",
        encoding="utf-8",
    )
    comparisons_path = tmp_path / "comparisons.json"
    comparisons_path.write_text(
        json.dumps(
            [
                {
                    "name": "Generic Energy Drink",
                    "category": "energy drinks",
                    "relation": "adjacent-substitute",
                    "recognizability": 0.8,
                    "category_overlap": 0.4,
                    "pain_point_contrast": 0.5,
                    "evidence_quality": 0.7,
                    "claim_posture": "satire",
                },
                {
                    "name": "Popular Bottled Coffee",
                    "category": "ready-to-drink coffee",
                    "relation": "direct-competitor",
                    "recognizability": 0.95,
                    "category_overlap": 1.0,
                    "pain_point_contrast": 0.8,
                    "evidence_quality": 0.9,
                    "claim_posture": "supported",
                    "evidence": [
                        {
                            "url": "https://example.com/bottled-coffee",
                            "source": "brand product page",
                            "source_quality": 0.9,
                            "note": "Evidence supports category/positioning only; no invented defect claim.",
                        }
                    ],
                },
            ]
        ),
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "position",
            "--product",
            str(product_path),
            "--comparisons",
            str(comparisons_path),
        ],
    )

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert len(payload["comparison_candidates"]) == 2
    assert payload["selected_comparison"]["name"] == "Popular Bottled Coffee"
    assert payload["selected_comparison"]["claim_posture"] == "supported"
    assert len(payload["selected_comparison"]["evidence"]) == 1


def test_position_downgrades_unsupported_supported_posture(tmp_path):
    product_path = tmp_path / "product.yml"
    product_path.write_text(
        "name: Example Product\ncategory: consumer product\n",
        encoding="utf-8",
    )
    comparisons_path = tmp_path / "comparisons.json"
    comparisons_path.write_text(
        json.dumps(
            [
                {
                    "name": "Known Alternative",
                    "category": "consumer product",
                    "relation": "direct-competitor",
                    "recognizability": 0.9,
                    "category_overlap": 1.0,
                    "pain_point_contrast": 0.8,
                    "evidence_quality": 0.0,
                    "claim_posture": "supported",
                    "evidence": [],
                }
            ]
        ),
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "position",
            "--product",
            str(product_path),
            "--comparisons",
            str(comparisons_path),
        ],
    )

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["comparison_candidates"][0]["claim_posture"] == "satire"
    assert payload["selected_comparison"]["claim_posture"] == "satire"
