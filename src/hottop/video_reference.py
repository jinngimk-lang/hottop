from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

ReferenceRights = Literal["generated-original", "user-provided-rights-cleared"]


class VideoReference(BaseModel):
    """A local rights-cleared image locator for provider-neutral shot continuity."""

    image_path: str = Field(min_length=1)
    rights: ReferenceRights

    @field_validator("image_path")
    @classmethod
    def validate_local_image_path(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("video reference image_path must not be blank")
        lowered = normalized.lower()
        if lowered.startswith(("http://", "https://", "data:")):
            raise ValueError(
                "video reference image_path must be a local locator; remote URLs and inline pixels are forbidden"
            )
        return normalized
