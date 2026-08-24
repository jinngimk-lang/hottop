from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from hottop.video_production import VideoProductionConfig


def _base_config() -> dict[str, object]:
    raw = yaml.safe_load(Path("config/video/cinematic-meme-direct.yml").read_text(encoding="utf-8"))
    assert isinstance(raw, dict)
    raw.pop("wan22", None)
    return raw


def _candidate(*, cost_per_unit: float = 0) -> dict[str, object]:
    return {
        "id": "hf-ltx23-public",
        "kind": "hf-zerogpu",
        "profile": "ltx23",
        "space_url": "https://example.hf.space",
        "api_name": "generate_video",
        "token_env": "HF_TOKEN",
        "allow_anonymous": True,
        "cost_per_unit": cost_per_unit,
        "weights_license_review": "required",
        "width": 768,
        "height": 512,
    }


def test_zero_cost_router_accepts_only_free_candidates():
    raw = _base_config()
    raw["generation_backend"] = "zero-cost-router"
    raw["zero_cost"] = {
        "enabled": True,
        "allow_paid_fallback": False,
        "max_attempts_per_shot": 2,
        "quality_gate": {
            "min_motion_delta": 2.0,
            "max_duplicate_ratio": 0.6,
        },
        "candidates": [_candidate()],
    }

    config = VideoProductionConfig.model_validate(raw)

    assert config.zero_cost is not None
    assert config.zero_cost.allow_paid_fallback is False
    assert config.zero_cost.max_attempts_per_shot == 2
    assert config.zero_cost.candidates[0].cost_per_unit == 0
    assert config.zero_cost.candidates[0].token_env == "HF_TOKEN"


def test_zero_cost_router_rejects_paid_fallback():
    raw = _base_config()
    raw["generation_backend"] = "zero-cost-router"
    raw["zero_cost"] = {
        "enabled": True,
        "allow_paid_fallback": True,
        "max_attempts_per_shot": 2,
        "candidates": [_candidate()],
    }

    with pytest.raises(ValidationError):
        VideoProductionConfig.model_validate(raw)


def test_zero_cost_router_rejects_nonzero_candidate_cost():
    raw = _base_config()
    raw["generation_backend"] = "zero-cost-router"
    raw["zero_cost"] = {
        "enabled": True,
        "allow_paid_fallback": False,
        "max_attempts_per_shot": 2,
        "candidates": [_candidate(cost_per_unit=0.01)],
    }

    with pytest.raises(ValidationError):
        VideoProductionConfig.model_validate(raw)


def test_zero_cost_router_requires_at_least_one_candidate():
    raw = _base_config()
    raw["generation_backend"] = "zero-cost-router"
    raw["zero_cost"] = {
        "enabled": True,
        "allow_paid_fallback": False,
        "max_attempts_per_shot": 2,
        "candidates": [],
    }

    with pytest.raises(ValidationError):
        VideoProductionConfig.model_validate(raw)
