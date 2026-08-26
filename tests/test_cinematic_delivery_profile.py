from pathlib import Path

import yaml


def test_cinematic_software3d_delivery_profile_is_presentable_and_zero_cost():
    profile_path = Path("config/video/cinematic-software3d-delivery.yml")
    assert profile_path.is_file()

    profile = yaml.safe_load(profile_path.read_text(encoding="utf-8"))

    assert profile["style_profile"] == "cinematic"
    assert profile["generation_backend"] == "software3d"
    assert profile["compositor_backend"] == "moviepy"
    assert profile["encoder_backend"] == "ffmpeg"
    assert profile["width"] >= 720
    assert profile["height"] >= 1280
    assert profile["fps"] >= 24
    assert profile["anti_polish"]["enabled"] is False
    assert profile["audio"]["original_music_only"] is True
    assert profile["text"]["allow_url"] is False
    assert profile["text"]["allow_qr"] is False


def test_ci_smoke_profile_remains_lightweight_and_separate():
    smoke = yaml.safe_load(
        Path("config/video/cinematic-software3d.yml").read_text(encoding="utf-8")
    )

    assert smoke["width"] == 360
    assert smoke["height"] == 640
    assert smoke["fps"] == 12
