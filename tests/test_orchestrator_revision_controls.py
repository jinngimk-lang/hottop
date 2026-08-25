from hottop.intake import resolve_intent
from hottop.orchestrator import revision_overrides


def test_revision_controls_mutate_only_relevant_intent_dimensions():
    intent = resolve_intent(
        "给咖啡新品做一个小红书出圈高级广告，最后揭示产品",
        overrides={"promotion_target": "Coffee Drop"},
    )

    bolder = revision_overrides(intent, "更大胆")
    funnier = revision_overrides(intent, "更有梗")
    clearer = revision_overrides(intent, "产品更明显")

    assert bolder["creative_ambition"] == "category-breaking"
    assert "style" not in bolder
    assert funnier["style"] == "funny-meme"
    assert clearer["product_visibility"] == "product-first"
