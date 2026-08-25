import json
from pathlib import Path

from hottop.video_quality import VideoQualityReport
from hottop.video_zero_cost import run_zero_cost_shot


def _runtime_config(path: Path) -> Path:
    path.write_text(
        json.dumps(
            {
                "enabled": True,
                "allow_paid_fallback": False,
                "max_attempts_per_shot": 2,
                "quality_gate": {
                    "min_motion_delta": 2.0,
                    "max_duplicate_ratio": 0.6,
                    "sample_fps": 4,
                    "sample_width": 96,
                    "sample_height": 54,
                },
                "candidates": [
                    {
                        "id": "first",
                        "kind": "hf-zerogpu",
                        "profile": "ltx23",
                        "space_url": "https://first.hf.space",
                        "api_name": "generate_video",
                        "allow_anonymous": True,
                        "cost_per_unit": 0,
                        "weights_license_review": "required",
                        "width": 768,
                        "height": 512,
                    },
                    {
                        "id": "second",
                        "kind": "hf-zerogpu",
                        "profile": "ltx23",
                        "space_url": "https://second.hf.space",
                        "api_name": "generate_video",
                        "allow_anonymous": True,
                        "cost_per_unit": 0,
                        "weights_license_review": "required",
                        "width": 768,
                        "height": 512,
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    return path


def test_zero_cost_shot_rejects_bad_video_and_tries_next_free_candidate(
    tmp_path: Path,
    monkeypatch,
):
    config_path = _runtime_config(tmp_path / "zero-cost-runtime.json")
    output = tmp_path / "shot.mp4"
    generated: list[str] = []
    inspected: list[str] = []

    def fake_generate(request):
        candidate_id = request.candidate.id
        generated.append(candidate_id)
        request.output.write_text(candidate_id, encoding="utf-8")
        return request.output

    def fake_inspect(path, policy):
        candidate_id = path.read_text(encoding="utf-8")
        inspected.append(candidate_id)
        if candidate_id == "first":
            return VideoQualityReport(
                pass_=False,
                terminal_frame_decodable=True,
                frame_count=4,
                mean_motion_delta=0.2,
                duplicate_ratio=1.0,
                reasons=["motion delta below policy"],
            )
        return VideoQualityReport(
            pass_=True,
            terminal_frame_decodable=True,
            frame_count=4,
            mean_motion_delta=4.0,
            duplicate_ratio=0.0,
        )

    monkeypatch.setattr("hottop.video_zero_cost.execute_hf_zerogpu", fake_generate)
    monkeypatch.setattr("hottop.video_zero_cost.inspect_video_quality", fake_inspect, raising=False)

    result = run_zero_cost_shot(
        config_path,
        prompt="original cinematic motion",
        duration_seconds=2.0,
        output=output,
        env={},
    )

    assert result == output
    assert output.read_text(encoding="utf-8") == "second"
    assert generated == ["first", "second"]
    assert inspected == ["first", "second"]
