from __future__ import annotations

import argparse
import copy
import json
import os
import time
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlsplit

import httpx
from pydantic import BaseModel, Field, field_validator


class ComfyApiError(RuntimeError):
    """Raised when the configured Comfy API v2 job cannot complete safely."""


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


def _is_loopback_http_endpoint(value: str) -> bool:
    try:
        parsed = urlsplit(value)
    except ValueError:
        return False
    return parsed.scheme.lower() == "http" and (parsed.hostname or "").lower() in {
        "localhost",
        "127.0.0.1",
        "::1",
    }


class ComfyJobRequest(BaseModel):
    endpoint: str
    workflow_path: Path
    prompt_node_id: str
    prompt_input_name: str
    prompt: str
    output: Path
    token: str = Field(min_length=1, repr=False)
    poll_interval_seconds: float = Field(default=2.0, gt=0)
    timeout_seconds: float = Field(default=900.0, gt=0)

    @field_validator("endpoint")
    @classmethod
    def validate_endpoint(cls, value: str) -> str:
        normalized = value.strip().rstrip("/")
        try:
            parsed = urlsplit(normalized)
            _ = parsed.port
        except ValueError as exc:
            raise ValueError("Comfy API endpoint must use HTTPS or an explicit localhost URL") from exc
        scheme = parsed.scheme.lower()
        host = (parsed.hostname or "").lower()
        if parsed.username is not None or parsed.password is not None:
            raise ValueError("Comfy API endpoint must not embed credentials")
        if scheme == "https" and host:
            return normalized
        if scheme == "http" and host in {"localhost", "127.0.0.1", "::1"}:
            return normalized
        raise ValueError("Comfy API endpoint must use HTTPS or an explicit localhost URL")

    @field_validator("prompt_node_id", "prompt_input_name", "prompt")
    @classmethod
    def normalize_required_text(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Comfy API job text fields must not be blank")
        return normalized


def _load_workflow(request: ComfyJobRequest) -> dict[str, Any]:
    if not request.workflow_path.is_file():
        raise ComfyApiError(f"Comfy API workflow not found: {request.workflow_path}")
    try:
        raw = json.loads(request.workflow_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ComfyApiError(f"Comfy API workflow is not valid JSON: {request.workflow_path}") from exc
    if not isinstance(raw, dict):
        raise ComfyApiError("Comfy API workflow root must be a JSON object")
    workflow = copy.deepcopy(raw)
    node = workflow.get(request.prompt_node_id)
    if not isinstance(node, dict):
        raise ComfyApiError(f"Comfy API prompt node not found: {request.prompt_node_id}")
    inputs = node.get("inputs")
    if not isinstance(inputs, dict):
        raise ComfyApiError(f"Comfy API prompt node has no inputs object: {request.prompt_node_id}")
    if request.prompt_input_name not in inputs:
        raise ComfyApiError(
            f"Comfy API prompt input not found: {request.prompt_node_id}.{request.prompt_input_name}"
        )
    inputs[request.prompt_input_name] = request.prompt
    return workflow


def _job_url(endpoint: str, job_id: str) -> str:
    return urljoin(endpoint.rstrip("/") + "/", f"api/v2/jobs/{job_id}")


def _select_video_output(job: dict[str, Any]) -> str:
    outputs = job.get("outputs")
    if not isinstance(outputs, list):
        raise ComfyApiError("Comfy API succeeded without an outputs list")
    for output in outputs:
        if not isinstance(output, dict):
            continue
        output_type = str(output.get("type") or "").lower()
        content_type = str(output.get("content_type") or "").lower()
        url = output.get("url")
        if isinstance(url, str) and url and (output_type == "video" or content_type.startswith("video/")):
            return url
    raise ComfyApiError("Comfy API succeeded without a downloadable video output")


def _safe_output_url(endpoint: str, raw_output_url: str) -> str:
    resolved = urljoin(endpoint.rstrip("/") + "/", raw_output_url)
    origin = _url_origin(resolved)
    if origin is None:
        raise ComfyApiError("Comfy API output URL must use HTTP(S)")
    if origin[0] == "https":
        return resolved
    if _is_loopback_http_endpoint(endpoint) and origin == _url_origin(endpoint):
        return resolved
    raise ComfyApiError(
        "Comfy API remote output URL must use HTTPS; plain HTTP is allowed only for the same localhost endpoint"
    )


def execute_comfy_job(
    request: ComfyJobRequest,
    *,
    client: httpx.Client | None = None,
) -> Path:
    """Submit one configured workflow, poll it, and persist exactly one returned video artifact."""

    workflow = _load_workflow(request)
    headers = {"Authorization": f"Bearer {request.token}"}
    owns_client = client is None
    http = client or httpx.Client(timeout=min(request.timeout_seconds, 60.0), follow_redirects=False)
    try:
        response = http.post(
            f"{request.endpoint}/api/v2/jobs",
            headers=headers,
            json={"workflow": workflow},
        )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise ComfyApiError(f"Comfy API job submission failed with HTTP {response.status_code}") from exc
        payload = response.json()
        if not isinstance(payload, dict) or not isinstance(payload.get("id"), str):
            raise ComfyApiError("Comfy API job submission returned no job id")
        job_id = payload["id"]
        deadline = time.monotonic() + request.timeout_seconds
        job = payload
        while str(job.get("status") or "").lower() not in {"succeeded", "failed", "cancelled"}:
            if time.monotonic() >= deadline:
                raise ComfyApiError(f"Comfy API job timed out: {job_id}")
            time.sleep(request.poll_interval_seconds)
            response = http.get(_job_url(request.endpoint, job_id), headers=headers)
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                raise ComfyApiError(
                    f"Comfy API job polling failed with HTTP {response.status_code}: {job_id}"
                ) from exc
            job = response.json()
            if not isinstance(job, dict):
                raise ComfyApiError(f"Comfy API job polling returned an invalid payload: {job_id}")

        status = str(job.get("status") or "").lower()
        if status != "succeeded":
            error = job.get("error")
            raise ComfyApiError(f"Comfy API job ended with status {status}: {error or 'no details'}")

        output_url = _safe_output_url(request.endpoint, _select_video_output(job))
        download = http.get(output_url, follow_redirects=False)
        try:
            download.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise ComfyApiError(
                f"Comfy API output download failed with HTTP {download.status_code}"
            ) from exc
        if not download.content:
            raise ComfyApiError("Comfy API output download was empty")

        request.output.parent.mkdir(parents=True, exist_ok=True)
        temporary = request.output.with_suffix(request.output.suffix + ".part")
        try:
            temporary.write_bytes(download.content)
            temporary.replace(request.output)
        finally:
            if temporary.exists():
                temporary.unlink()
        return request.output
    finally:
        if owns_client:
            http.close()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute one operator-configured Comfy API v2 video job")
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--prompt-node-id", required=True)
    parser.add_argument("--prompt-input-name", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--token-env", required=True)
    parser.add_argument("--poll-interval-seconds", type=float, default=2.0)
    parser.add_argument("--timeout-seconds", type=float, default=900.0)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    token = os.environ.get(args.token_env)
    if not token:
        raise SystemExit(f"required Comfy API token environment variable is missing: {args.token_env}")
    request = ComfyJobRequest(
        endpoint=args.endpoint,
        workflow_path=Path(args.workflow),
        prompt_node_id=args.prompt_node_id,
        prompt_input_name=args.prompt_input_name,
        prompt=args.prompt,
        output=Path(args.output),
        token=token,
        poll_interval_seconds=args.poll_interval_seconds,
        timeout_seconds=args.timeout_seconds,
    )
    try:
        execute_comfy_job(request)
    except ComfyApiError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
