from pathlib import Path

from hottop.video_production import load_video_production_config


def test_checked_in_lightx2v_profile_preserves_operator_owned_zero_cost_boundary():
    config = load_video_production_config(
        Path("config/video/cinematic-lightx2v-wan22-i2v.yml")
    )

    assert config.generation_backend == "lightx2v-operator"
    assert config.lightx2v is not None
    assert config.lightx2v.model_cls == "wan2.2_moe"
    assert config.lightx2v.task == "i2v"
    assert config.lightx2v.code_license == "Apache-2.0"
    assert config.lightx2v.weights_license == "Apache-2.0"
    assert config.lightx2v.cost_per_unit == 0
    assert config.lightx2v.operator_managed is True
    assert config.lightx2v.auto_install is False
    assert config.lightx2v.auto_download_models is False
    assert config.lightx2v.root == "integrations/LightX2V"
    assert config.lightx2v.config_json.endswith("configs/wan22/wan_moe_i2v.json")
