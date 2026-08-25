from __future__ import annotations

from pathlib import Path

import pytest

from hottop.video_moviepy import MoviePyTimelineCaption, _resolve_caption_font


def _caption(text: str) -> MoviePyTimelineCaption:
    return MoviePyTimelineCaption(text=text, start_seconds=0, duration_seconds=1)


def test_cjk_caption_prefers_explicit_local_font(tmp_path: Path) -> None:
    font = tmp_path / "NotoSansCJK-Regular.ttc"
    font.write_bytes(b"local-font-placeholder")

    resolved = _resolve_caption_font(
        [_caption("妈——！")],
        environ={"HOTTOP_CAPTION_FONT": str(font)},
        candidates=(),
    )

    assert resolved == str(font.resolve())


def test_cjk_caption_fails_closed_when_no_local_font_exists(tmp_path: Path) -> None:
    missing = tmp_path / "missing.ttc"

    with pytest.raises(RuntimeError, match="CJK caption font"):
        _resolve_caption_font(
            [_caption("傻孩子，用 InkClawAgent。")],
            environ={"HOTTOP_CAPTION_FONT": str(missing)},
            candidates=(),
        )


def test_ascii_only_caption_can_use_moviepy_default_font() -> None:
    assert _resolve_caption_font(
        [_caption("InkClawAgent")],
        environ={},
        candidates=(),
    ) is None
