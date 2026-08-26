import json

EVIDENCE_PATH = "examples/runs/odyssey-cinematic-software3d-delivery.evidence.json"


def _load_evidence() -> dict[str, object]:
    with open(EVIDENCE_PATH, encoding="utf-8") as handle:
        return json.load(handle)


def test_cinematic_delivery_evidence_archive_binds_real_run_and_media() -> None:
    evidence = _load_evidence()

    assert evidence["schema_version"] == "hottop.production-evidence.v1"
    assert evidence["source"]["render"] == "examples/video/inkclaw-odyssey-witch-pigs.render.json"
    assert evidence["source"]["config"] == "config/video/cinematic-software3d-delivery.yml"

    run = evidence["workflow_run"]
    assert run["name"] == "cinematic-delivery-smoke"
    assert run["run_id"] == 32937393633
    assert run["head_sha"] == "1cab4dfb4afb6b2611235025fd0cc04b7e2ab0ec"
    assert run["conclusion"] == "success"
    assert run["artifact_id"] == 9595569148
    assert run["artifact_digest"] == (
        "sha256:eb5c67f3d6c0cf3e88d52045e9e3ef60492fbbe395f5ebc9fb1590faf54d55b4"
    )
    assert run["artifact_is_ephemeral"] is True

    final = evidence["final_media"]
    assert final["sha256"] == "a22fc5bb03bee2815d2dca532c123ac6de1454e737719b3e702f1e35189f8fa6"
    assert final["size_bytes"] == 596237
    assert final["duration_seconds"] == 15.0
    assert final["video"] == {
        "codec": "h264",
        "width": 720,
        "height": 1280,
        "pixel_format": "yuv420p",
        "fps": 24.0,
    }
    assert final["audio"]["codec"] == "aac"
    assert final["audio"]["duration_seconds"] == 15.0

    shots = evidence["shots"]
    assert len(shots) == 5
    assert [shot["shot_index"] for shot in shots] == [1, 2, 3, 4, 5]
    assert all(shot["planned_generation_backend"] == "software3d" for shot in shots)
    assert all(shot["artifact_kind"] == "deterministic-generated" for shot in shots)
    assert all(len(shot["sha256"]) == 64 and shot["size_bytes"] > 0 for shot in shots)


def test_cinematic_delivery_evidence_archive_keeps_observation_scope_explicit() -> None:
    evidence = _load_evidence()

    inspection = evidence["inspection"]
    assert inspection["sample_timestamps_seconds"] == [1, 4, 7, 10, 13]
    assert inspection["motion_sample"]["sample_fps"] == 4
    assert inspection["motion_sample"]["duplicate_ratio_below_delta_0_25"] == 0.0
    assert inspection["audio_sample"]["integrated_lufs"] == -20.0
    assert inspection["audio_sample"]["silence_segments_ge_0_5s_at_minus_35db"] == 0
    assert inspection["claim_scope"] == "deterministic software3d delivery evidence only"
    assert inspection["generated_identity_claim"] is False


def test_historical_delivery_evidence_is_explicit_about_missing_runtime_identity() -> None:
    evidence = _load_evidence()

    runtime = evidence["runtime_provenance"]
    assert runtime["status"] == "not_captured_in_archived_run"
    assert runtime["required_schema"] == "hottop.runtime-provenance.v1"
    assert runtime["backfill_allowed"] is False
