from __future__ import annotations

from pathlib import Path

from hottop.video_lightx2v import _offline_environment


def test_lightx2v_offline_environment_does_not_forward_network_credentials(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "must-not-reach-operator-runtime")
    monkeypatch.setenv("HF_TOKEN", "must-not-reach-operator-runtime")
    monkeypatch.setenv("HTTPS_PROXY", "http://proxy.example.invalid:8080")
    monkeypatch.setenv("ALL_PROXY", "socks5://proxy.example.invalid:1080")
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "0")

    env = _offline_environment(Path("/operator/LightX2V"))

    assert "OPENAI_API_KEY" not in env
    assert "HF_TOKEN" not in env
    assert "HTTPS_PROXY" not in env
    assert "ALL_PROXY" not in env
    assert env["CUDA_VISIBLE_DEVICES"] == "0"
    assert env["HF_HUB_OFFLINE"] == "1"
    assert env["TRANSFORMERS_OFFLINE"] == "1"
    assert env["HF_DATASETS_OFFLINE"] == "1"
