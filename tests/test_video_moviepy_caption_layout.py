from __future__ import annotations

from hottop.video_moviepy import _caption_bottom_y


def test_multiline_caption_bottom_stays_inside_vertical_safe_area() -> None:
    frame_height = 640
    text_height = 150

    y = _caption_bottom_y(frame_height=frame_height, text_height=text_height)

    assert y >= 0
    assert y + text_height <= frame_height - 24


def test_short_caption_is_bottom_anchored_with_margin() -> None:
    frame_height = 640
    text_height = 48
    expected_margin = max(24, round(frame_height * 0.06))

    y = _caption_bottom_y(frame_height=frame_height, text_height=text_height)

    assert y == frame_height - text_height - expected_margin
    assert y > int(frame_height * 0.78)


def test_caption_taller_than_frame_clamps_to_top() -> None:
    assert _caption_bottom_y(frame_height=100, text_height=200) == 0
