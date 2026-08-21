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
