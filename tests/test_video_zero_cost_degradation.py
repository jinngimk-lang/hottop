import json
from pathlib import Path

import pytest

from hottop.video_hf_zerogpu import ZeroGpuError
from hottop.video_zero_cost import ZeroCostRoutesExhaustedError, run_zero_cost_shot


def _runtime_config(path: Path) -> Path:
    path.write_text(
        json.dumps(
            {
                "enabled": True,
                "allow_paid_fallback": False,
                "max_attempts_per_shot": 1,
                "quality_gate": {"min_motion_delta": 2, "max_duplicate_ratio": 0.6},
                "candidates": [
                    {
                        "id": "hf-public",
                        "kind": "hf-zerogpu",
                        "profile": "ltx23",
                        "space_url": "https://example.hf.space",
                        "api_name": "generate_video",
                        "allow_anonymous": True,
                        "cost_per_unit": 0,
                        "weights_license_review": "required",
                        "width": 768,
                        "height": 512,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return path


def test_zero_cost_exhaustion_degrades_reference_shot_with_explicit_artifact_provenance(
    monkeypatch, tmp_path: Path
):
    config = _runtime_config(tmp_path / "zero-cost.json")
    reference = tmp_path / "reference.png"
    reference.write_bytes(b"rights-cleared-original-image")
    output = tmp_path / "shot-002.mp4"
    artifact_manifest = tmp_path / "shot-002.artifact.json"
    fallback_calls: list[tuple[Path, Path, float]] = []

    def fail_free_route(*args, **kwargs):
        raise ZeroGpuError("free capacity exhausted", code="busy", retryable=True)

    def render_fallback(reference_image: Path, target: Path, duration_seconds: float) -> Path:
        fallback_calls.append((reference_image, target, duration_seconds))
        target.write_bytes(b"deterministic-reference-motion")
        return target

    monkeypatch.setattr("hottop.video_zero_cost.execute_hf_zerogpu", fail_free_route)

    result = run_zero_cost_shot(
        config,
        prompt="keep the original reference identity and add restrained camera motion",
        duration_seconds=2.0,
        output=output,
        reference_image=reference,
        reference_rights="generated-original",
        shot_index=2,
        artifact_manifest_path=artifact_manifest,
        allow_deterministic_fallback=True,
        fallback_renderer=render_fallback,
    )

    assert result == output
    assert fallback_calls == [(reference, output, 2.0)]
    artifact = json.loads(artifact_manifest.read_text(encoding="utf-8"))
    assert artifact["schema_version"] == "hottop.video-artifacts.v1"
    assert artifact["planned_generation_backend"] == "zero-cost-router"
    assert artifact["shots"] == [
        {
            "shot_index": 2,
            "path": str(output),
            "artifact_kind": "deterministic-non-generative",
            "backend": "deterministic-reference-motion",
            "degraded_from": "zero-cost-router",
            "degradation_reason": "zero_cost_routes_exhausted",
        }
    ]


def test_zero_cost_reference_fallback_is_not_implicit(monkeypatch, tmp_path: Path):
    config = _runtime_config(tmp_path / "zero-cost.json")
    reference = tmp_path / "reference.png"
    reference.write_bytes(b"rights-cleared-original-image")

    def fail_free_route(*args, **kwargs):
        raise ZeroGpuError("free capacity exhausted", code="busy", retryable=True)

    monkeypatch.setattr("hottop.video_zero_cost.execute_hf_zerogpu", fail_free_route)

    with pytest.raises(ZeroCostRoutesExhaustedError):
        run_zero_cost_shot(
            config,
            prompt="keep the original reference identity",
            duration_seconds=2.0,
            output=tmp_path / "shot-002.mp4",
            reference_image=reference,
            reference_rights="generated-original",
        )


def test_zero_cost_exhaustion_without_reference_does_not_create_placeholder(
    monkeypatch, tmp_path: Path
):
    config = _runtime_config(tmp_path / "zero-cost.json")
    output = tmp_path / "shot-001.mp4"
    artifact_manifest = tmp_path / "shot-001.artifact.json"

    def fail_free_route(*args, **kwargs):
        raise ZeroGpuError("free capacity exhausted", code="busy", retryable=True)

    monkeypatch.setattr("hottop.video_zero_cost.execute_hf_zerogpu", fail_free_route)

    with pytest.raises(ZeroCostRoutesExhaustedError):
        run_zero_cost_shot(
            config,
            prompt="original cinematic shot",
            duration_seconds=2.0,
            output=output,
            shot_index=1,
            artifact_manifest_path=artifact_manifest,
            allow_deterministic_fallback=True,
        )

    assert not output.exists()
    assert not artifact_manifest.exists()
