from __future__ import annotations

import json
from pathlib import Path

import typer

from .creative_memory import load_creative_library, retrieve_references

app = typer.Typer(no_args_is_help=False, add_completion=False)
DEFAULT_LIBRARY = Path("integrations/creative-reference-library.yml")


def _split(values: list[str] | None) -> list[str]:
    result: list[str] = []
    for value in values or []:
        result.extend(part.strip() for part in value.split(",") if part.strip())
    return result


@app.command()
def search(
    library_path: Path = typer.Option(DEFAULT_LIBRARY, "--library", exists=True, dir_okay=False),
    mechanism: list[str] | None = typer.Option(None, "--mechanism"),
    visual: list[str] | None = typer.Option(None, "--visual"),
    product_role: list[str] | None = typer.Option(None, "--product-role"),
    tag: list[str] | None = typer.Option(None, "--tag"),
    negative_pattern: list[str] | None = typer.Option(None, "--negative-pattern"),
    include_negative: bool = typer.Option(False, "--include-negative"),
    limit: int = typer.Option(5, "--limit", min=1, max=50),
) -> None:
    """Retrieve mechanism/grammar memory and guardrails; never copy old visual templates."""

    library = load_creative_library(library_path)
    matches = retrieve_references(
        library,
        mechanism_terms=_split(mechanism),
        visual_grammar_terms=_split(visual),
        product_role_terms=_split(product_role),
        tag_terms=_split(tag),
        negative_pattern_terms=_split(negative_pattern),
        include_negative=include_negative,
        limit=limit,
    )
    payload = [
        {
            "id": match.reference.id,
            "title": match.reference.title,
            "learning_kind": match.reference.learning_kind,
            "reuse_mode": match.reference.reuse_mode,
            "score": match.score,
            "matched_dimensions": match.matched_dimensions,
            "matched_terms": match.matched_terms,
            "mechanism": match.reference.hotspot.mechanism,
            "product_bridge": match.reference.product_bridge,
            "promotion_lessons": match.reference.promotion_lessons,
            "negative_patterns": match.reference.negative_patterns,
        }
        for match in matches
    ]
    typer.echo(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    app()
