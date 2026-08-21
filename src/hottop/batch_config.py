from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field


class BatchSourceConfig(BaseModel):
    type: Literal["dailyhot", "newsnow", "rss"]
    key: str = Field(min_length=1)
    limit: int = Field(default=30, ge=1, le=100)
    preset: str | None = None

    @property
    def spec(self) -> str:
        return f"{self.type}:{self.key}"


class BatchConfig(BaseModel):
    name: str = Field(min_length=1)
    sources: list[BatchSourceConfig] = Field(min_length=1)
    top: int = Field(default=5, ge=1, le=50)
    comparison_target: str | None = None


def load_batch_config(path: Path) -> BatchConfig:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return BatchConfig.model_validate(raw)
