from pathlib import Path

import pytest
from pydantic import ValidationError

from hottop.video_hf_zerogpu import HfZeroGpuRequest, execute_hf_zerogpu
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
        allow_anonymous=True,
        cost_per_unit=0,
        weights_license_review="required",
        width=768,
        height=512,
    )


def test_reference_image_requires_explicit_rights_mode(tmp_path: Path):
    reference = tmp_path / "character.png"
    reference.write_bytes(b"png-bytes")

    with pytest.raises(ValidationError):
        HfZeroGpuRequest(
            candidate=_candidate(),
            prompt="same original character walks through the market",
            duration_seconds=2,
            output=tmp_path / "shot.mp4",
            reference_image=reference,
        )


def test_execute_hf_zerogpu_uploads_rights_cleared_reference_before_generation(tmp_path: Path):
    reference = tmp_path / "character.png"
    reference.write_bytes(b"png-bytes")
    output = tmp_path / "shot.mp4"
    client = FakeClient(
        [
            FakeResponse(json_data=["/tmp/gradio/reference.png"]),
            FakeResponse(json_data={"event_id": "evt-i2v"}),
            FakeResponse(text='event: complete\ndata: ["https://cdn.example/i2v.mp4"]\n\n'),
            FakeResponse(content=b"video-bytes"),
        ]
    )
    request = HfZeroGpuRequest(
        candidate=_candidate(),
        prompt="same original character walks through the market",
        duration_seconds=2,
        output=output,
        reference_image=reference,
        reference_rights="generated-original",
    )

    result = execute_hf_zerogpu(request, client=client)

    assert result == output
    assert client.calls[0][0:2] == (
        "POST",
        "https://example.hf.space/gradio_api/upload",
    )
    assert client.calls[0][2]["files"]["files"][0] == "character.png"
    generation_call = client.calls[1]
    assert generation_call[0:2] == (
        "POST",
        "https://example.hf.space/gradio_api/call/generate_video",
    )
    image_input = generation_call[2]["json"]["data"][0]
    assert image_input["path"] == "/tmp/gradio/reference.png"
    assert image_input["meta"]["_type"] == "gradio.FileData"
