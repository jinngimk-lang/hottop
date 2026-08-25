from __future__ import annotations

from dataclasses import dataclass

from hottop.video_moviepy import _fit_caption_text_clip


@dataclass
class FakeTextClip:
    w: int
    h: int
    closed: bool = False

    def close(self) -> None:
        self.closed = True


def test_short_mixed_cjk_latin_caption_prefers_single_line_label_when_it_fits():
    calls: list[dict[str, object]] = []

    def factory(**kwargs):
        calls.append(kwargs)
        if kwargs["method"] == "label":
            return FakeTextClip(w=520, h=58)
        return FakeTextClip(w=633, h=118)

    clip = _fit_caption_text_clip(
        factory,
        text="用 InkClawAgent。",
        font="/tmp/noto-cjk.ttf",
        frame_width=720,
        frame_height=1280,
    )

    assert clip.h == 58
    assert calls[0]["method"] == "label"
    assert calls[0]["size"] == (None, None)
    assert len(calls) == 1


def test_short_mixed_caption_shrinks_single_line_before_falling_back_to_wrap():
    calls: list[dict[str, object]] = []

    def factory(**kwargs):
        calls.append(kwargs)
        font_size = int(kwargs["font_size"])
        if kwargs["method"] == "label":
            width = 680 if font_size >= 51 else 620
            return FakeTextClip(w=width, h=font_size + 7)
        return FakeTextClip(w=633, h=118)

    clip = _fit_caption_text_clip(
        factory,
        text="用 InkClawAgent。",
        font="/tmp/noto-cjk.ttf",
        frame_width=720,
        frame_height=1280,
    )

    assert clip.w == 620
    assert [call["method"] for call in calls] == ["label", "label"]
    assert int(calls[1]["font_size"]) < int(calls[0]["font_size"])
    assert all(call["size"] == (None, None) for call in calls)
