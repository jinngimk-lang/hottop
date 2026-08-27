from pathlib import Path

import yaml

from hottop.creative_memory import load_creative_library, retrieve_references

ROOT = Path(__file__).resolve().parents[1]
LIBRARY_PATH = ROOT / "integrations/creative-reference-library.yml"


def test_library_captures_positive_negative_and_packaging_memory() -> None:
    library = load_creative_library(LIBRARY_PATH)
    ids = {item.id for item in library.references}

    assert {
        "odyssey-witch-pigs-mechanism",
        "niulai-native-rough3d-dialogue",
        "cinematic-slideshow-is-not-video",
        "paired-meme-plus-product-explainer",
        "internal-production-labels-are-not-audience-copy",
    } <= ids

    kinds = {item.learning_kind for item in library.references}
    assert {"positive", "negative", "packaging"} <= kinds


def test_reference_entries_preserve_mechanism_product_role_and_feedback() -> None:
    library = load_creative_library(LIBRARY_PATH)
    odyssey = next(item for item in library.references if item.id == "odyssey-witch-pigs-mechanism")

    assert odyssey.hotspot.mechanism
    assert odyssey.product_bridge
    assert odyssey.product_role
    assert odyssey.story_outcome_change
    assert odyssey.visual_grammar
    assert odyssey.why_it_works
    assert odyssey.user_feedback
    assert "actor_likeness" in odyssey.what_not_to_copy


def test_current_reference_images_are_bound_by_hash_without_committing_binary_assets() -> None:
    raw = yaml.safe_load(LIBRARY_PATH.read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in raw["references"]}

    assert by_id["odyssey-witch-pigs-mechanism"]["assets"][0]["sha256"] == (
        "88f35a35cc36b96bc817df5dbb7a51e2e27a52a518868a5e6a2a8f409d76e32f"
    )
    assert by_id["niulai-native-rough3d-dialogue"]["assets"][0]["sha256"] == (
        "8e44d395234ce40d000037e30e9023bac65df9c8e856eb42b42c93f755958df2"
    )
    assert all(asset["storage"] == "metadata_only" for item in raw["references"] for asset in item.get("assets", []))


def test_retrieval_ranks_mechanism_and_native_grammar_not_old_template() -> None:
    library = load_creative_library(LIBRARY_PATH)

    results = retrieve_references(
        library,
        mechanism_terms=["obstruction", "breakout", "rescue"],
        visual_grammar_terms=["photorealistic", "cinematic", "live-action"],
        product_role_terms=["breakout", "route"],
        limit=3,
    )

    assert results
    assert results[0].reference.id == "odyssey-witch-pigs-mechanism"
    assert all(result.reference.id != "niulai-native-rough3d-dialogue" for result in results[:1])
    assert results[0].matched_dimensions >= 2


def test_negative_patterns_are_returned_as_guardrails_not_generation_templates() -> None:
    library = load_creative_library(LIBRARY_PATH)

    results = retrieve_references(
        library,
        negative_pattern_terms=["slideshow", "pan_zoom", "internal_label"],
        include_negative=True,
        limit=10,
    )
    ids = {result.reference.id for result in results}

    assert "cinematic-slideshow-is-not-video" in ids
    assert "internal-production-labels-are-not-audience-copy" in ids
    assert all(result.reference.reuse_mode != "copy_visual_template" for result in results)


def test_reference_library_is_not_declared_reinforcement_learning() -> None:
    library = load_creative_library(LIBRARY_PATH)

    assert library.learning_mode == "retrieval_plus_few_shot_preference_memory"
    assert library.reinforcement_learning is False
    assert library.policy.store_failures is True
    assert library.policy.store_user_feedback is True
    assert library.policy.store_platform_performance_when_available is True
