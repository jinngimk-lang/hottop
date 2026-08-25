from __future__ import annotations

from hottop import video_moviepy


class _FakeTextClip:
    created: list[_FakeTextClip] = []

    def __init__(self, **kwargs: object) -> None:
        self.text = str(kwargs["text"])
        self.font_size = int(kwargs["font_size"])
        method = str(kwargs["method"])
        self.w = 250 if method == "label" and len(self.text) <= 8 else 400
        if len(self.text) <= 8:
            self.h = 48
        else:
            self.h = 145 if self.font_size >= 38 else 110
        self.closed = False
        self.created.append(self)

    def close(self) -> None:
        self.closed = True


def test_multiline_caption_bottom_stays_inside_vertical_safe_area() -> None:
    frame_height = 640
    text_height = 150

    y = video_moviepy._caption_bottom_y(frame_height=frame_height, text_height=text_height)

    assert y >= 0
    assert y + text_height <= frame_height - 24


def test_short_caption_is_bottom_anchored_with_margin() -> None:
    frame_height = 640
    text_height = 48
    expected_margin = max(24, round(frame_height * 0.06))

    y = video_moviepy._caption_bottom_y(frame_height=frame_height, text_height=text_height)

    assert y == frame_height - text_height - expected_margin
    assert y > int(frame_height * 0.78)


def test_caption_taller_than_frame_clamps_to_top() -> None:
    assert video_moviepy._caption_bottom_y(frame_height=100, text_height=200) == 0


def _caption_fitter():
    fitter = getattr(video_moviepy, "_fit_caption_text_clip", None)
    assert fitter is not None, "MoviePy compositor must adapt tall mobile captions"
    return fitter


def test_tall_mobile_caption_shrinks_until_it_stays_out_of_subject_area() -> None:
    _FakeTextClip.created.clear()

    clip = _caption_fitter()(
        _FakeTextClip,
        text="先把环境、依赖、部署、Token 配好再说。",
        font=None,
        frame_width=360,
        frame_height=640,
    )

    assert clip.font_size < 38
    assert clip.h <= round(640 * 0.18)
    assert _FakeTextClip.created[0].closed is True


def test_short_mobile_caption_keeps_default_readable_size() -> None:
    _FakeTextClip.created.clear()

    clip = _caption_fitter()(
        _FakeTextClip,
        text="不用。直接干活。",
        font=None,
        frame_width=360,
        frame_height=640,
    )

    assert clip.font_size == 38
    assert len(_FakeTextClip.created) == 1
    assert clip.closed is False
