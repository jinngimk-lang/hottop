import json

from typer.testing import CliRunner
from hottop.cli import app

runner = CliRunner()


def test_creative_directive_command_emits_generation_guidance(tmp_path):
    payload_path = tmp_path / "directive-input.json"
    payload_path.write_text(
        json.dumps(
            {
                "intent": {
                    "request": "给云朵拉面做小红书出圈有梗广告，最后再揭示产品",
                    "promotion_target": {"value": "云朵拉面", "source": "explicit", "confidence": 1.0},
                    "campaign_goal": {"value": "hotspot-participation", "source": "explicit", "confidence": 1.0},
                    "platform": {"value": "xiaohongshu", "source": "explicit", "confidence": 1.0},
                    "style": {"value": "funny-meme", "source": "explicit", "confidence": 1.0},
                    "creative_ambition": {"value": "breakout", "source": "explicit", "confidence": 1.0},
                    "product_visibility": {"value": "metaphor-first", "source": "explicit", "confidence": 1.0},
                    "audience": {"value": None, "source": "defaulted", "confidence": 0.0},
                    "hotspot_preference": {"value": "current-best", "source": "explicit", "confidence": 1.0},
                    "constraints": [],
                },
                "promotion_context": {
                    "subject_name": "云朵拉面",
                    "subject_type": "product",
                    "category": "food consumer",
                    "primary_job": "make a memorable quick meal",
                    "primary_pain_point": "food ads look interchangeable",
                    "primary_differentiator": "long elastic ribbon-like noodles",
                    "semantic_terms": ["long", "elastic", "ribbon"],
                },
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    result = runner.invoke(app, ["creative-directive", str(payload_path)])

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["schema_version"] == "hottop.creative-directive.v1"
    assert payload["direction_lanes"][0] == "bridge-led-metaphor"
    assert payload["preferred_forms"][0] == "swipe-reveal"
    assert "misdirection-reveal" in payload["joke_mechanics"]
