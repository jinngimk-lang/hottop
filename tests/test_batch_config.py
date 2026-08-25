from pathlib import Path

from hottop.batch_config import BatchConfig, load_batch_config


def test_batch_config_loads_repeatable_source_contract(tmp_path: Path):
    path = tmp_path / "batch.yml"
    path.write_text(
        """
name: ai-daily
sources:
  - type: dailyhot
    key: zhihu
    limit: 20
    preset: zh-internet-culture
  - type: newsnow
    key: tech
    preset: ai-tech
top: 6
comparison_target: work巴迪
""",
        encoding="utf-8",
    )

    config = load_batch_config(path)

    assert isinstance(config, BatchConfig)
    assert config.name == "ai-daily"
    assert config.top == 6
    assert config.comparison_target == "work巴迪"
    assert config.sources[0].spec == "dailyhot:zhihu"
    assert config.sources[0].limit == 20
    assert config.sources[1].limit == 30


def test_batch_config_requires_at_least_one_source():
    try:
        BatchConfig(name="empty", sources=[])
    except ValueError as exc:
        assert "at least 1 item" in str(exc)
    else:
        raise AssertionError("empty batch config should fail validation")
