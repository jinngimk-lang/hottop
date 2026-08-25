from __future__ import annotations

import json
import mimetypes
import time
from pathlib import Path
from typing import Any, Literal
from urllib.parse import urljoin, urlsplit

import httpx
from pydantic import BaseModel, Field, model_validator

from .video_production import ZeroCostCandidateConfig


class ZeroGpuError(RuntimeError):
    """Raised when a free Hugging Face ZeroGPU request cannot complete safely."""

    def __init__(self, message: str, *, code: str, retryable: bool) -> None:
        super().__init__(message)
        self.code = code
        self.retryable = retryable


ReferenceRights = Literal["generated-original", "user-provided-rights-cleared"]


class HfZeroGpuRequest(BaseModel):
    candidate: ZeroCostCandidateConfig
    prompt: str = Field(min_length=1)
    duration_seconds: float = Field(gt=0, le=12)
    output: Path
    token: str | None = Field(default=None, repr=False)
    negative_prompt: str = "worst quality, inconsistent motion, blurry, jittery, distorted"
    seed: int = 42
    poll_interval_seconds: float = Field(default=2.0, gt=0)
    timeout_seconds: float = Field(default=900.0, gt=0)
    reference_image: Path | None = None
    reference_rights: ReferenceRights | None = None

    @model_validator(mode="after")
    def validate_reference_image(self) -> HfZeroGpuRequest:
        if self.reference_image is None:
            if self.reference_rights is not None:
                raise ValueError("reference_rights requires reference_image")
            return self
        if self.reference_rights is None:
            raise ValueError("reference_image requires an explicit rights-cleared reference_rights mode")
        if not self.reference_image.is_file():
            raise ValueError(f"reference_image does not exist: {self.reference_image}")
        if self.candidate.profile != "ltx23":
            raise ValueError(
                "reference-image ZeroGPU generation is currently validated only for the ltx23 profile"
            )
        return self


def _headers(token: str | None, *, accept: str | None = None) -> dict[str, str]:
    headers: dict[str, str] = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if accept:
        headers["accept"] = accept
    return headers


def _response_text(response: Any) -> str:
    text = getattr(response, "text", "")
    return text if isinstance(text, str) else ""


def _response_json(response: Any) -> Any:
    try:
        return response.json()
    except (ValueError, TypeError, AttributeError):
        text = _response_text(response)
        try:
            return json.loads(text)
        except (ValueError, TypeError):
            return None


def _raise_for_http(response: Any, *, operation: str) -> None:
    status = int(getattr(response, "status_code", 0) or 0)
    if 200 <= status < 300:
        return
    retryable = status in {408, 409, 425, 429} or status >= 500
    raise ZeroGpuError(
        f"Hugging Face ZeroGPU {operation} failed with HTTP {status}",
        code=f"hf_zerogpu_http_{status}",
        retryable=retryable,
    )


def _build_generation_data(
    request: HfZeroGpuRequest,
    *,
    image_input: dict[str, Any] | None = None,
) -> list[Any]:
    candidate = request.candidate
    if candidate.profile == "ltx23":
        return [
            image_input,
            request.prompt,
            request.duration_seconds,
            False,
            request.seed,
            False,
            candidate.height,
            candidate.width,
        ]
    if candidate.profile == "ltx-fast":
        return [
            request.prompt,
            request.negative_prompt,
            None,
            None,
            candidate.height,
            candidate.width,
            "text-to-video",
            request.duration_seconds,
            9,
            request.seed,
            False,
            3,
            False,
        ]
    raise ZeroGpuError(
        f"Unsupported Hugging Face ZeroGPU profile: {candidate.profile}",
        code="hf_zerogpu_unsupported_profile",
        retryable=False,
    )


def _parse_sse(text: str) -> list[tuple[str, str]]:
    events: list[tuple[str, str]] = []
    event_name = "message"
    data: list[str] = []
    for line in text.splitlines():
        if not line:
            if data:
                events.append((event_name, "\n".join(data)))
            event_name = "message"
            data = []
            continue
        if line.startswith("event:"):
            event_name = line[6:].strip()
        elif line.startswith("data:"):
            data.append(line[5:].strip())
    if data:
        events.append((event_name, "\n".join(data)))
    return events


def _parse_event_data(value: str) -> Any:
    try:
        return json.loads(value)
    except (ValueError, TypeError):
        return value


def _find_url(value: Any) -> str | None:
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith(("https://", "http://")):
            return stripped
        return None
    if isinstance(value, list):
        for item in value:
            found = _find_url(item)
            if found:
                return found
        return None
    if isinstance(value, dict):
        for key in ("url", "video", "path", "name"):
            if key in value:
                found = _find_url(value[key])
                if found:
                    return found
        for item in value.values():
            found = _find_url(item)
            if found:
                return found
    return None


def _url_origin(value: str) -> tuple[str, str, int] | None:
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError:
        return None
    scheme = parsed.scheme.lower()
    host = (parsed.hostname or "").lower()
    if scheme not in {"http", "https"} or not host:
        return None
    if port is None:
        port = 443 if scheme == "https" else 80
    return scheme, host, port


def _completed_output(text: str) -> tuple[str, str | None]:
    events = _parse_sse(text)
    for event_name, data in reversed(events):
        if event_name == "error":
            payload = _parse_event_data(data)
            message = payload.get("message") if isinstance(payload, dict) else payload
            return "failed", str(message or "ZeroGPU generation failed")
        if event_name == "complete":
            url = _find_url(_parse_event_data(data))
            return ("complete", url) if url else ("failed", None)
    return "running", None


def _uploaded_path(payload: Any) -> str | None:
    if isinstance(payload, list) and payload:
        first = payload[0]
        if isinstance(first, str) and first.strip():
            return first.strip()
        if isinstance(first, dict):
            for key in ("path", "name"):
                value = first.get(key)
                if isinstance(value, str) and value.strip():
                    return value.strip()
    if isinstance(payload, dict):
        for key in ("path", "name"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        files = payload.get("files")
        if isinstance(files, list) and files:
            return _uploaded_path(files)
    return None


def _upload_reference_image(
    request: HfZeroGpuRequest,
    http: Any,
) -> dict[str, Any] | None:
    if request.reference_image is None:
        return None
    image_path = request.reference_image
    mime_type = mimetypes.guess_type(image_path.name)[0] or "application/octet-stream"
    response = http.post(
        f"{request.candidate.space_url}/gradio_api/upload",
        headers=_headers(request.token),
        files={"files": (image_path.name, image_path.read_bytes(), mime_type)},
    )
    _raise_for_http(response, operation="reference upload")
    uploaded_path = _uploaded_path(_response_json(response))
    if not uploaded_path:
        raise ZeroGpuError(
            "Hugging Face ZeroGPU reference upload returned no file path",
            code="hf_zerogpu_upload_missing_path",
            retryable=False,
        )
    return {"path": uploaded_path, "meta": {"_type": "gradio.FileData"}}


def execute_hf_zerogpu(
    request: HfZeroGpuRequest,
    *,
    client: Any | None = None,
) -> Path:
    """Run one public/free Gradio queue job and atomically persist the returned video."""

    owns_client = client is None
    http = client or httpx.Client(timeout=min(request.timeout_seconds, 60.0), follow_redirects=True)
    candidate = request.candidate
    submit_url = f"{candidate.space_url}/gradio_api/call/{candidate.api_name}"
    try:
        image_input = _upload_reference_image(request, http)
        response = http.post(
            submit_url,
            headers=_headers(request.token),
            json={"data": _build_generation_data(request, image_input=image_input)},
        )
        _raise_for_http(response, operation="submission")
        payload = _response_json(response)
        event_id = payload.get("event_id") if isinstance(payload, dict) else None
        if not isinstance(event_id, str) or not event_id.strip():
            raise ZeroGpuError(
                "Hugging Face ZeroGPU returned no event id",
                code="hf_zerogpu_missing_event_id",
                retryable=False,
            )

        result_url = f"{candidate.space_url}/gradio_api/call/{candidate.api_name}/{event_id}"
        deadline = time.monotonic() + request.timeout_seconds
        output_url: str | None = None
        while time.monotonic() < deadline:
            response = http.get(
                result_url,
                headers=_headers(request.token, accept="text/event-stream"),
            )
            _raise_for_http(response, operation="poll")
            state, value = _completed_output(_response_text(response))
            if state == "complete":
                output_url = value
                break
            if state == "failed":
                raise ZeroGpuError(
                    str(value or "Hugging Face ZeroGPU completed without a video URL"),
                    code="hf_zerogpu_remote_job_failed",
                    retryable=True,
                )
            time.sleep(request.poll_interval_seconds)
        if not output_url:
            raise ZeroGpuError(
                "Hugging Face ZeroGPU generation timed out",
                code="hf_zerogpu_timeout",
                retryable=True,
            )

        resolved_url = urljoin(candidate.space_url.rstrip("/") + "/", output_url)
        candidate_origin = _url_origin(candidate.space_url)
        output_origin = _url_origin(resolved_url)
        if candidate_origin is None or output_origin != candidate_origin:
            raise ZeroGpuError(
                "Hugging Face ZeroGPU returned a cross-origin output URL; refusing external download",
                code="hf_zerogpu_cross_origin_output",
                retryable=False,
            )
        response = http.get(
            resolved_url,
            headers=_headers(request.token),
            follow_redirects=False,
        )
        _raise_for_http(response, operation="download")
        content = bytes(getattr(response, "content", b"") or b"")
        if not content:
            raise ZeroGpuError(
                "Hugging Face ZeroGPU download returned an empty file",
                code="hf_zerogpu_empty_output",
                retryable=True,
            )

        request.output.parent.mkdir(parents=True, exist_ok=True)
        temporary = request.output.with_suffix(request.output.suffix + ".part")
        try:
            temporary.write_bytes(content)
            temporary.replace(request.output)
        finally:
            if temporary.exists():
                temporary.unlink()
        return request.output
    finally:
        if owns_client:
            http.close()
