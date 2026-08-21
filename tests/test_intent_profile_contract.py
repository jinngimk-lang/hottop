from hottop.intake import CreativeIntent, IntentValue


def test_intent_fields_expose_provenance_and_confidence():
    intent = CreativeIntent.model_validate(
        {
            "request": "launch",
            "promotion_target": {"value": "Thing", "source": "explicit", "confidence": 1.0},
            "campaign_goal": {"value": "product-launch", "source": "inferred", "confidence": 0.8},
            "platform": {"value": "auto", "source": "defaulted", "confidence": 0.0},
            "style": {"value": "auto", "source": "defaulted", "confidence": 0.0},
            "creative_ambition": {"value": "witty", "source": "defaulted", "confidence": 0.0},
            "product_visibility": {"value": "balanced", "source": "defaulted", "confidence": 0.0},
            "audience": {"value": None, "source": "defaulted", "confidence": 0.0},
            "hotspot_preference": {"value": "auto", "source": "defaulted", "confidence": 0.0},
            "constraints": [],
        }
    )

    assert isinstance(intent.platform, IntentValue)
    assert intent.promotion_target.source == "explicit"
    assert intent.campaign_goal.confidence == 0.8
