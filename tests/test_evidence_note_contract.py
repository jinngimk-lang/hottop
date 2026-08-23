import pytest

from hottop.models import Evidence


def test_evidence_note_is_canonical_when_present():
    evidence = Evidence(
        url="https://example.com/source",
        source="Primary source",
        note="  factual limitation documented here  ",
    )

    assert evidence.note == "factual limitation documented here"


def test_evidence_note_rejects_blank_text_when_present():
    with pytest.raises(ValueError, match="evidence note must not be blank"):
        Evidence(
            url="https://example.com/source",
            source="Primary source",
            note="   ",
        )
