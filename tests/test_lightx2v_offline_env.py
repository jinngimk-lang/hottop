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


def test_lightx2v_offline_environment_does_not_forward_runtime_injection_controls(monkeypatch):
    monkeypatch.setenv("LD_PRELOAD", "/tmp/unbound-runtime.so")
    monkeypatch.setenv("PYTHONHOME", "/tmp/unbound-python-home")
    monkeypatch.setenv("PYTHONSTARTUP", "/tmp/unbound-startup.py")
    monkeypatch.setenv("PYTHONINSPECT", "1")
    monkeypatch.setenv("LD_LIBRARY_PATH", "/operator/cuda/lib64")

    env = _offline_environment(Path("/operator/LightX2V"))

    assert "LD_PRELOAD" not in env
    assert "PYTHONHOME" not in env
    assert "PYTHONSTARTUP" not in env
    assert "PYTHONINSPECT" not in env
    assert env["LD_LIBRARY_PATH"] == "/operator/cuda/lib64"


def test_lightx2v_offline_environment_disables_unbound_user_site_packages(monkeypatch):
    monkeypatch.setenv("PYTHONUSERBASE", "/tmp/unbound-user-base")
    monkeypatch.delenv("PYTHONNOUSERSITE", raising=False)

    env = _offline_environment(Path("/operator/LightX2V"))

    assert "PYTHONUSERBASE" not in env
    assert env["PYTHONNOUSERSITE"] == "1"


def test_lightx2v_offline_environment_does_not_forward_cloud_credential_handles(monkeypatch):
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "must-not-reach-operator-runtime")
    monkeypatch.setenv("AWS_SHARED_CREDENTIALS_FILE", "/tmp/unbound-aws-credentials")
    monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", "/tmp/unbound-google-credentials.json")
    monkeypatch.setenv("CLOUDSDK_CONFIG", "/tmp/unbound-gcloud-config")
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "0")

    env = _offline_environment(Path("/operator/LightX2V"))

    assert "AWS_ACCESS_KEY_ID" not in env
    assert "AWS_SHARED_CREDENTIALS_FILE" not in env
    assert "GOOGLE_APPLICATION_CREDENTIALS" not in env
    assert "CLOUDSDK_CONFIG" not in env
    assert env["CUDA_VISIBLE_DEVICES"] == "0"
