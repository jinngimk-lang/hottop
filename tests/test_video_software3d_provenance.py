import hashlib
import json
import subprocess
from pathlib import Path

from hottop.rendering import CreativeRenderRequest
from hottop.video_execution import _artifact_manifest_path, run_video_production
from hottop.video_production import ExternalCommandSpec, load_video_production_config
from hottop.video_software3d_production import render_story_shot_video


def test_software3d_shot_writes_byte_bound_provenance_manifest(tmp_path: Path):
    (tmp_path / "hottop-video-plan.json").write_text(
        json.dumps(
            {
                "schema_version": "hottop.video-plan.v1",
                "topic_id": "inkclaw-anti-polish-cow-snake",
            }
        ),
        encoding="utf-8",
    )
    output = tmp_path / "shots" / "shot-001.mp4"
    manifest = output.with_suffix(".artifact.json")
    payload = b"software3d-video-bytes"

    def runner(argv, **kwargs):
        Path(argv[-1]).write_bytes(payload)
        return subprocess.CompletedProcess(argv, 0, "", "")

    render_story_shot_video(
        shot_index=1,
        output=output,
        duration_seconds=0.5,
        width=160,
        height=90,
        fps=4,
        runner=runner,
    )

    record = json.loads(manifest.read_text(encoding="utf-8"))
    assert record["planned_generation_backend"] == "software3d"
    assert len(record["shots"]) == 1
    shot = record["shots"][0]
    assert shot["shot_index"] == 1
    assert shot["path"] == str(output.resolve())
    assert shot["artifact_kind"] == "deterministic-generated"
    assert shot["backend"] == "software3d"
    assert shot["sha256"] == hashlib.sha256(payload).hexdigest()
    assert shot["size_bytes"] == len(payload)


def test_video_run_software3d_outputs_follow_moviepy_manifest_convention(tmp_path: Path):
    render = CreativeRenderRequest.model_validate(
        json.loads(Path("examples/video/inkclaw-cow-snake.render.json").read_text(encoding="utf-8"))
    )
    config = load_video_production_config(Path("config/video/anti-polish-software3d.yml"))

    result = run_video_production(
        render,
        config,
        output_dir=tmp_path / "run",
        project_root=Path("."),
        execute=False,
    )

    generation = [command for command in result.runtime_commands if command.stage == "generation"]
    assert len(generation) == 5
    expected_manifests = []
    for index, command in enumerate(generation, start=1):
        output = Path(command.args[command.args.index("--output") + 1])
        assert output == (tmp_path / "run" / "shots" / f"shot-{index:03d}.mp4").resolve()
        expected_manifest = output.with_suffix(".artifact.json")
        assert expected_manifest.name == f"shot-{index:03d}.artifact.json"
        expected_manifests.append(str(expected_manifest))

    assert result.artifact_manifest_paths == expected_manifests


def test_runtime_discovers_software3d_sidecar_from_generation_output(tmp_path: Path):
    output = (tmp_path / "shots" / "shot-001.mp4").resolve()
    command = ExternalCommandSpec(
        program="python",
        args=[
            "-m",
            "hottop.video_software3d_production",
            "--shot-index",
            "1",
            "--output",
            str(output),
        ],
        stage="generation",
    )

    assert _artifact_manifest_path(command) == output.with_suffix(".artifact.json")
