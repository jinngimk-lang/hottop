from datetime import UTC, datetime

import pytest

from hottop.models import ReferenceRightsMode, VisualReference


def test_visual_reference_manifest_keeps_provenance_and_abstract_grammar() -> None:
    reference = VisualReference(
        source_url="https://example.com/campaign",
        source_title="Example campaign",
        source_type="public-web",
        observed_at=datetime.now(UTC),
        visual_medium="commercial-product",
        expression_form="swipe-reveal",
        bridge_type="shape-material",
        composition_grammar=["single dominant object", "large negative space"],
        reveal_pattern="tease -> extend -> reveal",
        text_grammar="one short line after the reveal",
        why_effective="the viewer completes the visual association before the product name appears",
        what_not_to_copy=["exact layout", "logo lockup", "distinctive packaging"],
        rights_mode="analysis-only",
        provenance_note="Observed on the public campaign page; screenshot used only for analysis.",
    )

    assert reference.rights_mode == "analysis-only"
    assert reference.composition_grammar == ["single dominant object", "large negative space"]
    assert reference.observed_at.tzinfo is not None
    assert reference.what_not_to_copy


def test_visual_reference_rejects_naive_timestamps() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        VisualReference(
            source_url="https://example.com/a",
            source_title="Example",
            source_type="public-web",
            observed_at=datetime(2026, 8, 21, 12, 0),
            rights_mode="unknown",
            provenance_note="Direct public observation.",
        )


def test_reference_rights_modes_are_explicit() -> None:
    allowed: tuple[ReferenceRightsMode, ...] = (
        "analysis-only",
        "public-domain",
        "rights-cleared",
        "unknown",
    )

    for rights_mode in allowed:
        reference = VisualReference(
            source_url="https://example.com/a",
            source_title="Example",
            source_type="public-web",
            rights_mode=rights_mode,
            provenance_note="Recorded for provenance.",
        )
        assert reference.rights_mode == rights_mode


def test_visual_reference_provenance_identity_is_canonical() -> None:
    reference = VisualReference(
        source_url="https://example.com/a",
        source_title="  Example campaign  ",
        source_type="  public-web  ",
        rights_mode="analysis-only",
        provenance_note="  Direct public observation.  ",
    )

    assert reference.source_title == "Example campaign"
    assert reference.source_type == "public-web"
    assert reference.provenance_note == "Direct public observation."


@pytest.mark.parametrize("field", ["source_title", "source_type", "provenance_note"])
def test_visual_reference_rejects_blank_provenance_identity(field: str) -> None:
    payload = {
        "source_url": "https://example.com/a",
        "source_title": "Example",
        "source_type": "public-web",
        "rights_mode": "analysis-only",
        "provenance_note": "Direct public observation.",
    }
    payload[field] = "   "

    with pytest.raises(ValueError, match="must not be blank"):
        VisualReference.model_validate(payload)


def test_visual_reference_exclusions_are_canonical() -> None:
    reference = VisualReference(
        source_url="https://example.com/a",
        source_title="Example",
        source_type="public-web",
        rights_mode="analysis-only",
        provenance_note="Direct public observation.",
        what_not_to_copy=["  exact layout  ", "  logo lockup  "],
    )

    assert reference.what_not_to_copy == ["exact layout", "logo lockup"]


def test_visual_reference_rejects_blank_exclusions() -> None:
    with pytest.raises(ValueError, match="what not to copy must not contain blank text"):
        VisualReference(
            source_url="https://example.com/a",
            source_title="Example",
            source_type="public-web",
            rights_mode="analysis-only",
            provenance_note="Direct public observation.",
            what_not_to_copy=["exact layout", "   "],
        )


def test_visual_reference_abstract_grammar_is_canonical() -> None:
    reference = VisualReference(
        source_url="https://example.com/a",
        source_title="Example",
        source_type="public-web",
        rights_mode="analysis-only",
        provenance_note="Direct public observation.",
        composition_grammar=["  single dominant object  ", "  large negative space  "],
        reveal_pattern="  tease -> extend -> reveal  ",
        text_grammar="  one short line after the reveal  ",
        why_effective="  the viewer completes the association first  ",
    )

    assert reference.composition_grammar == ["single dominant object", "large negative space"]
    assert reference.reveal_pattern == "tease -> extend -> reveal"
    assert reference.text_grammar == "one short line after the reveal"
    assert reference.why_effective == "the viewer completes the association first"


def test_visual_reference_rejects_blank_composition_grammar() -> None:
    with pytest.raises(ValueError, match="composition grammar must not contain blank text"):
        VisualReference(
            source_url="https://example.com/a",
            source_title="Example",
            source_type="public-web",
            rights_mode="analysis-only",
            provenance_note="Direct public observation.",
            composition_grammar=["single dominant object", "   "],
        )


@pytest.mark.parametrize("field", ["reveal_pattern", "text_grammar", "why_effective"])
def test_visual_reference_rejects_blank_optional_grammar(field: str) -> None:
    payload = {
        "source_url": "https://example.com/a",
        "source_title": "Example",
        "source_type": "public-web",
        "rights_mode": "analysis-only",
        "provenance_note": "Direct public observation.",
        field: "   ",
    }

    with pytest.raises(ValueError, match="must not be blank"):
        VisualReference.model_validate(payload)


def test_visual_reference_artifact_hash_is_canonical_when_present() -> None:
    reference = VisualReference(
        source_url="https://example.com/a",
        source_title="Example",
        source_type="public-web",
        rights_mode="analysis-only",
        provenance_note="Direct public observation.",
        artifact_hash="  sha256:abc123  ",
    )

    assert reference.artifact_hash == "sha256:abc123"


def test_visual_reference_rejects_blank_artifact_hash() -> None:
    with pytest.raises(ValueError, match="artifact hash must not be blank"):
        VisualReference(
            source_url="https://example.com/a",
            source_title="Example",
            source_type="public-web",
            rights_mode="analysis-only",
            provenance_note="Direct public observation.",
            artifact_hash="   ",
        )
