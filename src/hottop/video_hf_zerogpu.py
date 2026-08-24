from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import httpx
from pydantic import BaseModel, Field

from .video_production import ZeroCostCandidateConfig


class ZeroGpuError(RuntimeError):
    """Raised when a free Hugging Face ZeroGPU request cannot complete safely."""

    def __init__(self, message: str, *, code: str, retryable: bool) -> None:
        super().__init__(message)
        self.code = code
        self.retryable = retryable


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


def _build_generation_data(request: HfZeroGpuRequest) -> list[Any]:
    candidate = request.candidate
    if candidate.profile == "ltx23":
        return [
            None,
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
        response = http.post(
            submit_url,
            headers=_headers(request.token),
            json={"data": _build_generation_data(request)},
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
        response = http.get(resolved_url, headers=_headers(request.token))
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
