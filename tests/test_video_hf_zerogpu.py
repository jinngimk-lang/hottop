from pathlib import Path

import pytest

from hottop.video_hf_zerogpu import HfZeroGpuRequest, ZeroGpuError, execute_hf_zerogpu
from hottop.video_production import ZeroCostCandidateConfig


class FakeResponse:
    def __init__(self, *, status_code: int = 200, json_data=None, text: str = "", content: bytes = b""):
        self.status_code = status_code
        self._json_data = json_data
        self.text = text
        self.content = content

    def json(self):
        return self._json_data


class FakeClient:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def post(self, url, **kwargs):
        self.calls.append(("POST", url, kwargs))
        return self.responses.pop(0)

    def get(self, url, **kwargs):
        self.calls.append(("GET", url, kwargs))
        return self.responses.pop(0)


def _candidate() -> ZeroCostCandidateConfig:
    return ZeroCostCandidateConfig(
        id="hf-ltx23-public",
        profile="ltx23",
        space_url="https://example.hf.space",
        api_name="generate_video",
        token_env="HF_TOKEN",
        allow_anonymous=True,
        cost_per_unit=0,
        weights_license_review="required",
        width=768,
        height=512,
    )


def test_execute_hf_zerogpu_submits_polls_and_writes_atomically(tmp_path: Path):
    output = tmp_path / "shot.mp4"
    client = FakeClient(
        [
            FakeResponse(json_data={"event_id": "evt-1"}),
            FakeResponse(
                text=(
                    'event: complete\ndata: '
                    '["https://example.hf.space/gradio_api/file=video.mp4"]\n\n'
                )
            ),
            FakeResponse(content=b"video-bytes"),
        ]
    )
    request = HfZeroGpuRequest(
        candidate=_candidate(),
        prompt="original cinematic shot",
        duration_seconds=2.0,
        output=output,
        token="top-secret-token",
    )

    result = execute_hf_zerogpu(request, client=client)

    assert result == output
    assert output.read_bytes() == b"video-bytes"
    assert not output.with_suffix(".mp4.part").exists()
    assert "top-secret-token" not in repr(request)
    assert client.calls[0][2]["headers"]["Authorization"] == "Bearer top-secret-token"
    assert client.calls[0][2]["json"]["data"]
    assert client.calls[-1][1].startswith("https://example.hf.space/")


def test_execute_hf_zerogpu_rejects_cross_origin_output_before_download(tmp_path: Path):
    client = FakeClient(
        [
            FakeResponse(json_data={"event_id": "evt-1"}),
            FakeResponse(
                text='event: complete\ndata: ["https://evil.example/steal-token.mp4"]\n\n'
            ),
        ]
    )
    request = HfZeroGpuRequest(
        candidate=_candidate(),
        prompt="original cinematic shot",
        duration_seconds=2.0,
        output=tmp_path / "shot.mp4",
        token="top-secret-token",
    )

    with pytest.raises(ZeroGpuError) as exc_info:
        execute_hf_zerogpu(request, client=client)

    assert exc_info.value.code == "hf_zerogpu_cross_origin_output"
    assert exc_info.value.retryable is False
    assert len(client.calls) == 2
    assert all("evil.example" not in call[1] for call in client.calls)
    assert not request.output.exists()


def test_execute_hf_zerogpu_marks_rate_limit_retryable(tmp_path: Path):
    client = FakeClient([FakeResponse(status_code=429, text="quota exceeded")])
    request = HfZeroGpuRequest(
        candidate=_candidate(),
        prompt="shot",
        duration_seconds=2,
        output=tmp_path / "shot.mp4",
        token=None,
    )

    with pytest.raises(ZeroGpuError) as exc_info:
        execute_hf_zerogpu(request, client=client)

    assert exc_info.value.retryable is True
    assert exc_info.value.code == "hf_zerogpu_http_429"


def test_execute_hf_zerogpu_rejects_missing_event_id_as_nonretryable(tmp_path: Path):
    client = FakeClient([FakeResponse(json_data={"unexpected": True})])
    request = HfZeroGpuRequest(
        candidate=_candidate(),
        prompt="shot",
        duration_seconds=2,
        output=tmp_path / "shot.mp4",
        token=None,
    )

    with pytest.raises(ZeroGpuError) as exc_info:
        execute_hf_zerogpu(request, client=client)

    assert exc_info.value.retryable is False
    assert exc_info.value.code == "hf_zerogpu_missing_event_id"
