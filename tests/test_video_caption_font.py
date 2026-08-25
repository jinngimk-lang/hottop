from pathlib import Path

import pytest

from hottop.video_moviepy import select_caption_font


def test_ascii_captions_do_not_require_external_font(tmp_path: Path):
    assert select_caption_font(["InkClawAgent"], candidates=[tmp_path / "missing.ttf"]) is None


def test_unicode_captions_fail_closed_without_compatible_font(tmp_path: Path):
    with pytest.raises(RuntimeError, match="Unicode captions require"):
        select_caption_font(["妈——！", "不用部署"], candidates=[tmp_path / "missing.ttf"])


def test_unicode_captions_select_first_available_font(tmp_path: Path):
    first = tmp_path / "missing.ttf"
    second = tmp_path / "NotoSansCJK-Regular.ttc"
    second.write_bytes(b"font-placeholder")

    assert select_caption_font(["直接干活。"], candidates=[first, second]) == str(second)
