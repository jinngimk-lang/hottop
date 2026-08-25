from hottop.creative import CreativeReview
from hottop.creative_package import (
    CreativePackageInput,
    CreativePackageOption,
    build_creative_package,
)
from hottop.models import CreativeConcept


def test_creative_package_preserves_option_label_for_conversational_revisions():
    concept = CreativeConcept.model_validate(
        {
            "topic": {"id": "x", "title": "x", "url": "https://example.com/x", "source": "test"},
            "promotion": {"subject_name": "Thing", "subject_type": "product", "category": "consumer"},
            "strategy": {
                "bridge_type": "function",
                "bridge": "thing becomes action",
                "expression_form": "single-visual-metaphor",
            },
            "beats": [
                {"scene": "Thing performs the action.", "caption": "Done.", "intent": "reveal"}
            ],
            "visual_medium": "commercial-product",
            "genre_treatment": "original product advertising",
            "punchlines": ["Done."],
            "image_prompt": "Original product metaphor.",
            "negative_prompt": "No copied assets.",
            "claim_status": "satire",
        }
    )
    package = CreativePackageInput(
        options=[
            CreativePackageOption(
                label="bridge-led",
                concept=concept,
                review=CreativeReview(
                    name="bridge-led",
                    instant_comprehension=0.9,
                    natural_linkage=0.9,
                    product_centrality=0.9,
                    surprise=0.8,
                    ownability=0.9,
                    evidence_safety=0.95,
                    original_execution=0.95,
                ),
            )
        ],
        references=[],
    )

    result = build_creative_package(package)

    assert result.option_diagnostics[0].label == "bridge-led"
