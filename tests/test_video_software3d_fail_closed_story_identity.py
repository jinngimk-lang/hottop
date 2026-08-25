from __future__ import annotations

import json
from pathlib import Path

import pytest

from hottop.video_software3d_production import (
    COW_STORY_PROFILE,
    ODYSSEY_STORY_PROFILE,
    _story_profile_from_workspace_plan,
    story_profile_for_topic,
)


def test_known_story_topics_resolve_explicitly() -> None:
    assert story_profile_for_topic("inkclaw-anti-polish-cow-snake") == COW_STORY_PROFILE
    assert story_profile_for_topic("odyssey-witch-pigs") == ODYSSEY_STORY_PROFILE


def test_unknown_story_topic_fails_closed() -> None:
    with pytest.raises(ValueError, match="unsupported software 3d story topic"):
        story_profile_for_topic("future-story-without-renderer")


def test_missing_workspace_plan_fails_closed(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="workspace plan is missing"):
        _story_profile_from_workspace_plan(tmp_path / "missing-plan.json")


def test_workspace_plan_with_unknown_topic_fails_closed(tmp_path: Path) -> None:
    plan = tmp_path / "hottop-video-plan.json"
    plan.write_text(
        json.dumps(
            {
                "schema_version": "hottop.video-plan.v1",
                "topic_id": "unsupported-story",
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="unsupported software 3d story topic"):
        _story_profile_from_workspace_plan(plan)
