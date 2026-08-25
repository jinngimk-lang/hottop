from pathlib import Path

import pytest

from hottop.video_external import ExternalVideoCommand, build_external_video_command


def test_external_video_command_expands_only_declared_placeholders() -> None:
    spec = ExternalVideoCommand(
        program="wangp",
        args=(
            "--prompt",
            "{prompt}",
            "--duration",
            "{duration_seconds}",
            "--output",
            "{output}",
        ),
        cwd=Path("/opt/wangp"),
    )

    command = build_external_video_command(
        spec,
        prompt="a cinematic mythic scene",
        duration_seconds=2.5,
        output=Path("/tmp/shot-001.mp4"),
    )

    assert command.argv == [
        "wangp",
        "--prompt",
        "a cinematic mythic scene",
        "--duration",
        "2.5",
        "--output",
        "/tmp/shot-001.mp4",
    ]
    assert command.cwd == Path("/opt/wangp")


def test_external_video_command_rejects_unknown_placeholder() -> None:
    spec = ExternalVideoCommand(program="wangp", args=("--token", "{token}"))

    with pytest.raises(ValueError, match="unsupported placeholder"):
        build_external_video_command(
            spec,
            prompt="scene",
            duration_seconds=2,
            output=Path("shot.mp4"),
        )


def test_external_video_command_rejects_shell_metacharacters_in_program() -> None:
    spec = ExternalVideoCommand(program="wangp;rm", args=("--prompt", "{prompt}"))

    with pytest.raises(ValueError, match="program must be a single executable name"):
        build_external_video_command(
            spec,
            prompt="scene",
            duration_seconds=2,
            output=Path("shot.mp4"),
        )
