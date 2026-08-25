from __future__ import annotations

from pathlib import Path
from typing import Final

from pydantic import BaseModel, Field

_ALLOWED_PLACEHOLDERS: Final = frozenset({"prompt", "duration_seconds", "output"})


class ExternalVideoCommand(BaseModel):
    """Operator-provided local video generator command.

    This is intentionally only a command contract. Hottop does not bundle or
    download the upstream application, credentials, models, or GPU runtime.
    """

    program: str = Field(min_length=1)
    args: tuple[str, ...] = ()
    cwd: Path | None = None


class BuiltExternalVideoCommand(BaseModel):
    argv: list[str] = Field(min_length=1)
    cwd: Path | None = None


def _validate_program(program: str) -> str:
    if not program.strip() or program != program.strip():
        raise ValueError("program must be a single executable name")
    if any(char in program for char in ";&|<>\n\r\t"):
        raise ValueError("program must be a single executable name")
    if "/" in program or "\\" in program:
        # Absolute/relative executable paths are deliberately allowed only
        # through a trusted operator environment in a future executor. The
        # command contract itself stays portable and easy to audit.
        raise ValueError("program must be a single executable name")
    return program


def _expand(value: str, values: dict[str, str]) -> str:
    result = value
    start = 0
    while True:
        left = result.find("{", start)
        if left < 0:
            return result
        right = result.find("}", left + 1)
        if right < 0:
            raise ValueError("unclosed placeholder")
        name = result[left + 1 : right]
        if name not in _ALLOWED_PLACEHOLDERS:
            raise ValueError(f"unsupported placeholder: {name}")
        result = result[:left] + values[name] + result[right + 1 :]
        start = left + len(values[name])


def build_external_video_command(
    spec: ExternalVideoCommand,
    *,
    prompt: str,
    duration_seconds: float,
    output: Path,
) -> BuiltExternalVideoCommand:
    """Build an argv-only command for an operator-installed video backend.

    No shell syntax is interpreted. Secrets and arbitrary environment values
    are intentionally unavailable as placeholders.
    """

    program = _validate_program(spec.program)
    values = {
        "prompt": prompt,
        "duration_seconds": str(duration_seconds),
        "output": str(output),
    }
    argv = [program]
    for arg in spec.args:
        argv.append(_expand(arg, values))
    return BuiltExternalVideoCommand(argv=argv, cwd=spec.cwd)
