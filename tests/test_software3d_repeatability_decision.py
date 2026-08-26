from pathlib import Path

DECISION = Path("docs/decisions/2026-08-26-software3d-repeatability.md")


def test_repeatability_decision_prioritizes_quality_contracts_over_universal_byte_identity():
    text = DECISION.read_text(encoding="utf-8")

    assert "repeatability is defined first" in text
    assert "not by universal byte equality" in text
    assert "byte-identical outputs remain useful additional evidence" in text
    assert "#31 is a counterexample" in text


def test_repeatability_decision_records_cpu_provenance_without_claiming_causality():
    text = DECISION.read_text(encoding="utf-8")

    assert "AMD EPYC 7763 64-Core Processor" in text
    assert "e8c8a04bfd1dcda906a9b8e1116f3db8b87b00df7e0265072c3b0083a62a37d3" in text
    assert "does **not** prove CPU differences caused #31" in text
