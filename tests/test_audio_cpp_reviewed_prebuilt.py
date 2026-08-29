from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_audio_cpp_manifest_binds_reviewed_v070_linux_prebuilt_provenance() -> None:
    manifest = yaml.safe_load(
        (ROOT / "integrations/audio-cpp-qwen3-tts-benchmark.yml").read_text(encoding="utf-8")
    )

    release = manifest["reviewed_prebuilt_release"]
    assert release["tag"] == "v0.7.0"
    assert release["commit"] == "d2ff37009c69d464bcab6aa4a44a13746e84a914"
    assert release["auto_download_allowed"] is False

    assets = {asset["name"]: asset for asset in release["assets"]}
    assert assets["audio-v0.7.0-bin-ubuntu-x64-cpu.tar.gz"]["sha256"] == (
        "400774c3f92f3da4c5fedfa2e43d50482e951ec288eb39e66c10e63fb46de47d"
    )
    assert assets["audio-v0.7.0-bin-ubuntu-x64-vulkan.tar.gz"]["sha256"] == (
        "e49676f1da28df0d2a6ca2073118964e91f3d14aa3c2ca3ad984e3d09b96932d"
    )
