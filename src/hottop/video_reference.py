from __future__ import annotations

from collections.abc import Iterable
from typing import Literal

from pydantic import BaseModel, Field, field_validator

ReferenceRights = Literal["generated-original", "user-provided-rights-cleared"]


class VideoReference(BaseModel):
    """A local rights-cleared image locator and optional subject identity anchor."""

    image_path: str = Field(min_length=1)
    rights: ReferenceRights
    subject_id: str | None = Field(default=None, exclude_if=lambda value: value is None)
    role: str | None = Field(default=None, exclude_if=lambda value: value is None)
    identity_lock: list[str] = Field(default_factory=list, exclude_if=lambda value: not value)

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

    @field_validator("subject_id", "role")
    @classmethod
    def normalize_optional_label(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        if not normalized:
            raise ValueError("video reference identity labels must not be blank")
        return normalized

    @field_validator("identity_lock")
    @classmethod
    def normalize_identity_lock(cls, value: list[str]) -> list[str]:
        normalized: list[str] = []
        for item in value:
            cleaned = item.strip()
            if not cleaned:
                raise ValueError("video reference identity_lock entries must not be blank")
            if cleaned not in normalized:
                normalized.append(cleaned)
        return normalized

    def identity_prompt(self) -> str | None:
        if self.subject_id is None:
            return None
        parts = [f"Identity anchor {self.subject_id}"]
        if self.role:
            parts.append(f"role: {self.role}")
        if self.identity_lock:
            parts.append("preserve exactly: " + ", ".join(self.identity_lock))
        parts.append(
            "keep the same recognizable person/character identity across shots while allowing pose, expression and camera angle to change"
        )
        return "; ".join(parts) + "."


def validate_reference_identity_consistency(references: Iterable[VideoReference]) -> None:
    """Reject identity drift encoded in configuration before any provider receives a prompt."""

    seen: dict[str, VideoReference] = {}
    for reference in references:
        if reference.subject_id is None:
            continue
        prior = seen.get(reference.subject_id)
        if prior is None:
            seen[reference.subject_id] = reference
            continue
        if prior.image_path != reference.image_path or prior.rights != reference.rights:
            raise ValueError(
                f"subject {reference.subject_id!r} has a conflicting reference image or rights mode"
            )
        if prior.identity_lock != reference.identity_lock or prior.role != reference.role:
            raise ValueError(f"subject {reference.subject_id!r} has a conflicting identity lock")
