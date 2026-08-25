from types import SimpleNamespace

import pytest

from hottop.video_quality import VideoQualityReport
from hottop.video_wangp import WanGPAdapterConfig, WanGPError, run_wangp_shot


def _settings(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text(
        '{"model_type":"wan2.2_i2v","prompt":"template"}',
        encoding="utf-8",
    )
    return path


def _session_for(generated):
    class FakeJob:
        def result(self):
            return SimpleNamespace(success=True, generated_files=[str(generated)], errors=[])

    class FakeSession:
        def get_model_availability(self, model_type):
            return {"model_type": model_type, "status": "available", "available": True}

        def submit_task(self, settings):
            return FakeJob()

    return FakeSession()


def test_wangp_quality_policy_defaults_match_shared_generated_video_gate(tmp_path):
    config = WanGPAdapterConfig(root=tmp_path / "WanGP", settings_path=_settings(tmp_path))

    assert config.quality_policy.min_motion_delta == 2.0
    assert config.quality_policy.max_duplicate_ratio == 0.6
    assert config.quality_policy.sample_fps == 4
    assert config.quality_policy.sample_width == 96
    assert config.quality_policy.sample_height == 54


def test_wangp_rejects_and_deletes_generated_video_that_fails_quality_gate(tmp_path):
    generated = tmp_path / "wangp-generated.mp4"
    generated.write_bytes(b"bad-video-bytes")
    output = tmp_path / "shots" / "shot-001.mp4"
    inspected = []

    def inspect(path, policy):
        inspected.append((path, policy))
        return VideoQualityReport(
            pass_=False,
            duration=2.0,
            width=768,
            height=512,
            fps=24,
            terminal_frame_decodable=True,
            frame_count=8,
            mean_motion_delta=0.1,
            duplicate_ratio=0.95,
            reasons=["motion delta 0.100 below 2.000", "duplicate ratio 0.950 above 0.600"],
        )

    config = WanGPAdapterConfig(root=tmp_path / "WanGP", settings_path=_settings(tmp_path))

    with pytest.raises(WanGPError, match="rejected by quality gate"):
        run_wangp_shot(
            config,
            prompt="same hero moves through frame",
            duration_seconds=2.0,
            fps=24,
            output=output,
            session_factory=lambda **_kwargs: _session_for(generated),
            quality_inspector=inspect,
        )

    assert len(inspected) == 1
    assert inspected[0][0] == output.resolve()
    assert not output.exists()


def test_wangp_returns_generated_video_only_after_quality_gate_passes(tmp_path):
    generated = tmp_path / "wangp-generated.mp4"
    generated.write_bytes(b"good-video-bytes")
    output = tmp_path / "shots" / "shot-001.mp4"
    inspected = []

    def inspect(path, policy):
        inspected.append((path, policy))
        return VideoQualityReport(
            pass_=True,
            duration=2.0,
            width=768,
            height=512,
            fps=24,
            terminal_frame_decodable=True,
            frame_count=8,
            mean_motion_delta=8.0,
            duplicate_ratio=0.0,
        )

    config = WanGPAdapterConfig(root=tmp_path / "WanGP", settings_path=_settings(tmp_path))

    result = run_wangp_shot(
        config,
        prompt="same hero moves through frame",
        duration_seconds=2.0,
        fps=24,
        output=output,
        session_factory=lambda **_kwargs: _session_for(generated),
        quality_inspector=inspect,
    )

    assert result == output.resolve()
    assert output.read_bytes() == b"good-video-bytes"
    assert len(inspected) == 1
