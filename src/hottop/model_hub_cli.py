from __future__ import annotations

import json
from pathlib import Path

import typer

from .model_hub import load_model_hub, select_models

app = typer.Typer(no_args_is_help=False, add_completion=False)
DEFAULT_HUB = Path("integrations/model-hub.yml")


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


if __name__ == "__main__":
    app()
