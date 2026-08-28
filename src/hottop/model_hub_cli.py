from __future__ import annotations

import json
from pathlib import Path

import typer

from .model_hub import load_model_hub, select_models
from .qwentts_cpp_preflight import inspect_qwentts_cpp_inputs

app = typer.Typer(no_args_is_help=False, add_completion=False)
DEFAULT_HUB = Path("integrations/model-hub.yml")


@app.callback()
def main() -> None:
    """Inspect Hottop's safe local multimodal model registry."""


@app.command()
def list(
    hub_path: Path = typer.Option(DEFAULT_HUB, "--hub", exists=True, dir_okay=False),
    capability: str | None = typer.Option(None, "--capability"),
    modality: str | None = typer.Option(None, "--modality"),
    operator_profile: str | None = typer.Option("dgx-spark-dual", "--operator-profile"),
    include_unintegrated: bool = typer.Option(False, "--include-unintegrated"),
    runtime_ready_only: bool = typer.Option(False, "--runtime-ready-only"),
    include_paid: bool = typer.Option(False, "--include-paid"),
) -> None:
    """List safe model-hub candidates; this never installs, downloads or executes models."""

    hub = load_model_hub(hub_path)
    entries = select_models(
        hub,
        capability=capability,
        modality=modality,
        operator_profile=operator_profile,
        zero_cost_only=not include_paid,
        integration_ready_only=not include_unintegrated,
        runtime_ready_only=runtime_ready_only,
    )
    typer.echo(
        json.dumps(
            [entry.model_dump(mode="json") for entry in entries],
            ensure_ascii=False,
            indent=2,
        )
    )


@app.command("probe-qwentts-cpp")
def probe_qwentts_cpp(
    executable: Path = typer.Option(..., "--executable", dir_okay=False),
    talker_gguf: Path = typer.Option(..., "--talker-gguf", dir_okay=False),
    tokenizer_gguf: Path = typer.Option(..., "--tokenizer-gguf", dir_okay=False),
) -> None:
    """Bind local qwentts.cpp benchmark inputs without executing or downloading anything."""

    result = inspect_qwentts_cpp_inputs(
        executable=executable,
        talker_gguf=talker_gguf,
        tokenizer_gguf=tokenizer_gguf,
    )
    typer.echo(json.dumps(result.model_dump(mode="json"), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    app()
