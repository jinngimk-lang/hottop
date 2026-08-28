from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_unityvideo_is_motion_control_benchmark_candidate_only() -> None:
    registry = yaml.safe_load((ROOT / "integrations/model-hub.yml").read_text(encoding="utf-8"))
    models = {model["id"]: model for model in registry["models"]}

    candidate = models["unityvideo-wan22-ti2v-5b"]

    assert candidate["repository"] == "https://github.com/JIA-Lab-research/UnityVideo"
    assert candidate["source_revision_reviewed"] == "e79e9b6bd1c498dd919dceb4cdea47e20417bf70"
    assert candidate["weights"] == "KlingTeam/UnityVideo"
    assert candidate["code_license"] == "MIT"
    assert candidate["weights_license"] == "Apache-2.0-model-card-base-Wan2.2-separate"
    assert candidate["status"] == "benchmark_candidate"
    assert candidate["integration_ready"] is False
    assert candidate["runtime_status"] == "unprobed"
    assert candidate["cost_class"] == "self_owned_compute"
    assert "auto-download" in candidate["runtime_boundary"]
    assert "256 x 256" in candidate["runtime_boundary"]
    assert "motion" in " ".join(candidate["capabilities"])


def test_unityvideo_admission_record_persists_rights_runtime_and_benchmark_gates() -> None:
    record = (ROOT / "docs/research/2026-08-28-unityvideo-admission.md").read_text(
        encoding="utf-8"
    )

    assert "e79e9b6bd1c498dd919dceb4cdea47e20417bf70" in record
    assert "MIT" in record
    assert "Apache-2.0" in record
    assert "10,020,954,352" in record
    assert "0df3909e312526c46f68097958afa055868f73354fe4276d693f7ebc398e6a39" in record
    assert "auto-download" in record
    assert "256 x 256" in record
    assert "33 frames" in record
    assert "motion fidelity" in record
    assert "benchmark candidate" in record
