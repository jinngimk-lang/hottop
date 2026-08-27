from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_domainshuttle_is_registry_only_and_fail_closed() -> None:
    registry = yaml.safe_load((ROOT / "integrations/model-hub.yml").read_text(encoding="utf-8"))
    models = {model["id"]: model for model in registry["models"]}

    candidate = models["domainshuttle-wan22-a14b"]

    assert candidate["repository"] == "https://github.com/HKUST-C4G/DomainShuttle"
    assert candidate["source_revision_reviewed"] == "ba7a7a3b275dcdb9896ca43ede3587b6c1dc6060"
    assert candidate["weights"] == "CNcreator0331/DomainShuttle_weight"
    assert candidate["weights_revision_reviewed"] == "418962e4db32ecce6c1542d536c0ab7326417938"
    assert candidate["code_license"] == "Apache-2.0"
    assert candidate["status"] == "benchmark_candidate"
    assert candidate["integration_ready"] is False
    assert candidate["runtime_status"] == "unprobed"
    assert candidate["cost_class"] == "self_owned_compute"
    assert "auto-download" in candidate["runtime_boundary"]
    assert "license metadata mismatch" in candidate["runtime_boundary"]


def test_domainshuttle_admission_record_persists_license_and_runtime_gates() -> None:
    record = (ROOT / "docs/research/2026-08-28-domainshuttle-admission.md").read_text(
        encoding="utf-8"
    )

    assert "ba7a7a3b275dcdb9896ca43ede3587b6c1dc6060" in record
    assert "418962e4db32ecce6c1542d536c0ab7326417938" in record
    assert "Apache-2.0" in record
    assert "MIT" in record
    assert "70 GB" in record
    assert "126 GB" in record
    assert "benchmark candidate" in record
    assert "no auto-download" in record
