import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from hottop.video_quality import VideoQualityPolicy, inspect_video_quality


@pytest.mark.parametrize(
    "metadata",
    [
        [],
        {"format": [], "streams": []},
        {"format": {"duration": "2.0"}, "streams": [None]},
    ],
)
def test_inspect_video_quality_rejects_malformed_metadata_shapes(
    tmp_path: Path,
    metadata: object,
):
    path = tmp_path / "malformed-metadata.mp4"
    path.write_bytes(b"video")

    def runner(args, **kwargs):
        assert args[0] == "ffprobe"
        return SimpleNamespace(
            returncode=0,
            stdout=json.dumps(metadata),
            stderr="",
        )

    report = inspect_video_quality(path, VideoQualityPolicy(), runner=runner)

    assert report.pass_ is False
    assert "ffprobe metadata structure invalid" in report.reasons
