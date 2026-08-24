import json
from pathlib import Path

import httpx

from hottop.rendering import CreativeRenderFrame, CreativeRenderRequest
from hottop.video_comfy_api import ComfyJobRequest, execute_comfy_job
from hottop.video_execution import inspect_video_environment, run_video_production
from hottop.video_production import VideoProductionConfig


def _request() -> CreativeRenderRequest:
    return CreativeRenderRequest(
        topic_id="cloud-cinematic",
        topic_title="cloud cinematic meme",
        subject_name="InkClawAgent",
        expression_form="faux-film-still",
        visual_medium="live-action-cinematic",
        genre_treatment="original cinematic meme",
        distribution_mode="motion",
        in_asset_cta_policy="no-destination",
        motion_continuity_required=True,
        category_default="setup ceremony",
        deleted_constraint="deployment ceremony",
        new_competition_axis="time to useful work",
        bridge_type="role",
        bridge="product breaks a story obstacle",
        frames=[
            CreativeRenderFrame(
                index=1,
                scene="Original cinematic hero enters one continuous room.",
                caption="打开，直接干活。",
                intent="solution",
                speaker="hero",
                delivery="understated Mandarin",
            )
        ],
        master_prompt="original live-action cinematic meme",
        negative_prompt="actor likeness, copied film frame",
        punchlines=["先把活干完。"],
        risk_flags=["original staging only"],
        claim_status="satire",
    )


def _config(tmp_path: Path) -> VideoProductionConfig:
    workflow = tmp_path / "workflow.api.json"
    workflow.write_text(
        json.dumps(
            {
                "6": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {"text": "PROMPT_PLACEHOLDER"},
                }
            }
        ),
        encoding="utf-8",
    )
    return VideoProductionConfig.model_validate(
        {
            "name": "comfy-cloud-test",
            "style_profile": "cinematic",
            "roughness_score": 25,
            "generation_backend": "comfy-api-v2",
            "compositor_backend": "external",
            "encoder_backend": "external",
            "width": 720,
            "height": 1280,
            "fps": 24,
            "duration_seconds": 5,
            "shot_policy": {"min_shot_seconds": 1, "max_shot_seconds": 5},
            "audio": {
                "bgm_style": "original restrained score",
                "foley_style": "cinematic foley",
                "voice_backend": "none",
                "music_backend": "none",
                "sfx_backend": "none",
            },
            "text": {},
            "comfy_api_v2": {
                "endpoint": "https://cloud.example.test",
                "workflow_path": str(workflow),
                "prompt_node_id": "6",
                "prompt_input_name": "text",
                "token_env": "COMFY_API_TOKEN",
                "poll_interval_seconds": 0.1,
                "timeout_seconds": 30,
            },
        }
    )


def test_comfy_video_run_dry_run_references_token_env_not_secret(monkeypatch, tmp_path):
    config = _config(tmp_path)
    monkeypatch.setenv("COMFY_API_TOKEN", "super-secret-token")

    status = inspect_video_environment(config, project_root=tmp_path)
    assert status.comfy_api is not None
    assert status.comfy_api.ready is True

    result = run_video_production(
        _request(),
        config,
        output_dir=tmp_path / "run",
        project_root=tmp_path,
        execute=False,
    )

    generation = [command for command in result.runtime_commands if command.stage == "generation"]
    assert len(generation) == 1
    command = generation[0]
    assert command.program.endswith("python") or "python" in Path(command.program).name
    assert command.args[:2] == ["-m", "hottop.video_comfy_api"]
    assert "--token-env" in command.args
    assert "COMFY_API_TOKEN" in command.args
    assert "super-secret-token" not in " ".join(command.args)
    assert "--prompt" in command.args
    assert "--output" in command.args


def test_comfy_readiness_fails_closed_without_token(monkeypatch, tmp_path):
    config = _config(tmp_path)
    monkeypatch.delenv("COMFY_API_TOKEN", raising=False)

    status = inspect_video_environment(config, project_root=tmp_path)

    assert status.ready is False
    assert status.comfy_api is not None
    assert "COMFY_API_TOKEN" in " ".join(status.comfy_api.missing)


def test_comfy_api_v2_executes_api_workflow_and_downloads_video(tmp_path):
    workflow = tmp_path / "workflow.json"
    workflow.write_text(
        json.dumps(
            {
                "6": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {"text": "old text"},
                }
            }
        ),
        encoding="utf-8",
    )
    output = tmp_path / "shot.mp4"
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/v2/jobs" and request.method == "POST":
            seen["authorization"] = request.headers.get("authorization")
            payload = json.loads(request.content.decode("utf-8"))
            seen["payload"] = payload
            return httpx.Response(
                201,
                json={
                    "id": "job-1",
                    "status": "queued",
                    "created_at": "2026-08-24T00:00:00Z",
                    "started_at": None,
                    "completed_at": None,
                    "expires_at": None,
                    "queue_position": 1,
                    "progress": None,
                    "outputs": [],
                    "error": None,
                    "urls": {
                        "self": "/api/v2/jobs/job-1",
                        "events": "/api/v2/jobs/job-1/events",
                        "cancel": "/api/v2/jobs/job-1/cancel",
                    },
                },
            )
        if request.url.path == "/api/v2/jobs/job-1" and request.method == "GET":
            return httpx.Response(
                200,
                json={
                    "id": "job-1",
                    "status": "succeeded",
                    "created_at": "2026-08-24T00:00:00Z",
                    "started_at": "2026-08-24T00:00:01Z",
                    "completed_at": "2026-08-24T00:00:10Z",
                    "expires_at": None,
                    "queue_position": None,
                    "progress": {"value": 1, "nodes_done": 10, "nodes_total": 10},
                    "outputs": [
                        {
                            "node_id": "99",
                            "name": "result.mp4",
                            "type": "video",
                            "content_type": "video/mp4",
                            "size_bytes": 7,
                            "id": "asset-1",
                            "hash": None,
                            "url": "https://files.example.test/result.mp4",
                            "url_expires_at": "2026-08-24T01:00:00Z",
                            "job_id": "job-1",
                        }
                    ],
                    "error": None,
                    "urls": {
                        "self": "/api/v2/jobs/job-1",
                        "events": "/api/v2/jobs/job-1/events",
                        "cancel": "/api/v2/jobs/job-1/cancel",
                    },
                },
            )
        if request.url.host == "files.example.test":
            return httpx.Response(200, content=b"MP4DATA")
        raise AssertionError(f"unexpected request: {request.method} {request.url}")

    client = httpx.Client(transport=httpx.MockTransport(handler))
    execute_comfy_job(
        ComfyJobRequest(
            endpoint="https://cloud.example.test",
            workflow_path=workflow,
            prompt_node_id="6",
            prompt_input_name="text",
            prompt="new cinematic prompt",
            output=output,
            token="token-value",
            poll_interval_seconds=0.01,
            timeout_seconds=2,
        ),
        client=client,
    )

    assert output.read_bytes() == b"MP4DATA"
    assert seen["authorization"] == "Bearer token-value"
    payload = seen["payload"]
    assert isinstance(payload, dict)
    assert payload["workflow"]["6"]["inputs"]["text"] == "new cinematic prompt"
