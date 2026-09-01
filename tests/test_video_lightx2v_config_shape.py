from __future__ import annotations

from pathlib import Path

import pytest

from hottop.video_lightx2v import LightX2VAdapterConfig, LightX2VError, run_lightx2v_shot


def test_lightx2v_fails_closed_before_gpu_when_config_json_is_not_an_object(tmp_path: Path):
    root = tmp_path / "LightX2V"
    (root / "lightx2v").mkdir(parents=True)
    (root / "lightx2v" / "infer.py").write_text("# operator checkout\n", encoding="utf-8")
    config_json = root / "configs" / "wan22" / "wan_moe_i2v.json"
    config_json.parent.mkdir(parents=True)
    config_json.write_text("[]\n", encoding="utf-8")
    model_path = tmp_path / "Wan2.2-I2V-A14B"
    model_path.mkdir()
    (model_path / "weights.bin").write_bytes(b"test-model-bytes")
    config = LightX2VAdapterConfig(
        root=root,
        model_path=model_path,
        config_json=config_json,
        model_cls="wan2.2_moe",
        task="t2v",
        code_license="Apache-2.0",
        weights_license="Apache-2.0",
    )

    def gpu_probe():
        raise AssertionError("GPU probe must not start when config JSON has the wrong shape")

    with pytest.raises(LightX2VError, match="config JSON"):
        run_lightx2v_shot(
            config,
            prompt="test",
            negative_prompt="",
            output=tmp_path / "shot.mp4",
            runner=lambda *_args, **_kwargs: None,
            gpu_probe=gpu_probe,
        )


def test_lightx2v_fails_closed_before_gpu_when_config_json_uses_nonstandard_constants(
    tmp_path: Path,
):
    root = tmp_path / "LightX2V"
    (root / "lightx2v").mkdir(parents=True)
    (root / "lightx2v" / "infer.py").write_text("# operator checkout\n", encoding="utf-8")
    config_json = root / "configs" / "wan22" / "wan_moe_i2v.json"
    config_json.parent.mkdir(parents=True)
    config_json.write_text('{"guidance_scale": NaN}\n', encoding="utf-8")
    model_path = tmp_path / "Wan2.2-I2V-A14B"
    model_path.mkdir()
    (model_path / "weights.bin").write_bytes(b"test-model-bytes")
    config = LightX2VAdapterConfig(
        root=root,
        model_path=model_path,
        config_json=config_json,
        model_cls="wan2.2_moe",
        task="i2v",
        code_license="Apache-2.0",
        weights_license="Apache-2.0",
    )

    def gpu_probe():
        raise AssertionError("GPU probe must not start when config JSON is not strict JSON")

    with pytest.raises(LightX2VError, match="config JSON"):
        run_lightx2v_shot(
            config,
            prompt="test",
            negative_prompt="",
            output=tmp_path / "shot.mp4",
            runner=lambda *_args, **_kwargs: None,
            gpu_probe=gpu_probe,
        )
