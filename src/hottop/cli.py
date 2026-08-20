from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any

import typer
import yaml

from .briefing import build_brief
from .collectors.dailyhot import DailyHotApiCollector
from .collectors.newsnow import NewsNowCollector
from .collectors.rss import RSSCollector
from .doctor import local_doctor
from .models import ProductProfile, TrendCandidate
from .pipeline import build_batch
from .rendering import build_render_request
from .scoring import score_candidate

app = typer.Typer(no_args_is_help=True, add_completion=False)


def _json_dump(value: Any) -> str:
    if hasattr(value, "model_dump"):
        value = value.model_dump(mode="json")
    return json.dumps(value, ensure_ascii=False, indent=2)


def _load_candidates(path: Path) -> list[TrendCandidate]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    records = raw if isinstance(raw, list) else [raw]
    return [TrendCandidate.model_validate(record) for record in records]


def _load_product(path: Path) -> ProductProfile:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return ProductProfile.model_validate(raw)


async def _discover(source: str, key: str, limit: int) -> list[TrendCandidate]:
    if source == "dailyhot":
        return await DailyHotApiCollector(route=key).collect(limit=limit)
    if source == "newsnow":
        return await NewsNowCollector(source_id=key).collect(limit=limit)
    if source == "rss":
        return await RSSCollector(feed_url=key, source_name="rss:custom").collect(limit=limit)
    raise typer.BadParameter("source must be one of: dailyhot, newsnow, rss")


@app.command()
def discover(
    source: str = typer.Option("dailyhot", "--source"),
    key: str = typer.Option("zhihu", "--key", help="DailyHot route, NewsNow source id, or RSS URL"),
    limit: int = typer.Option(30, "--limit", min=1, max=100),
    output: Path | None = typer.Option(None, "--output"),
) -> None:
    """Fetch and normalize one trend source."""
    items = asyncio.run(_discover(source, key, limit))
    text = _json_dump([item.model_dump(mode="json") for item in items])
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    else:
        typer.echo(text)


@app.command()
def rank(
    input_path: Path = typer.Argument(..., exists=True, dir_okay=False),
    top: int = typer.Option(10, "--top", min=1),
) -> None:
    """Rank normalized candidates using the deterministic foundation scorer."""
    ranked = [
        {"candidate": candidate.model_dump(mode="json"), "score": score_candidate(candidate).model_dump()}
        for candidate in _load_candidates(input_path)
    ]
    ranked.sort(key=lambda item: item["score"]["total"], reverse=True)
    typer.echo(_json_dump(ranked[:top]))


@app.command()
def brief(
    input_path: Path = typer.Argument(..., exists=True, dir_okay=False),
    product: Path = typer.Option(..., "--product", exists=True, dir_okay=False),
    compare: str | None = typer.Option(None, "--compare"),
    index: int = typer.Option(0, "--index", min=0),
) -> None:
    """Build a four-panel meme brief from a normalized trend candidate."""
    candidates = _load_candidates(input_path)
    if index >= len(candidates):
        raise typer.BadParameter(f"index {index} is outside {len(candidates)} candidates")
    profile = _load_product(product)
    result = build_brief(candidates[index], profile, comparison_target=compare)
    typer.echo(_json_dump(result))


@app.command()
def render(
    input_path: Path = typer.Argument(..., exists=True, dir_okay=False),
    product: Path = typer.Option(..., "--product", exists=True, dir_okay=False),
    compare: str | None = typer.Option(None, "--compare"),
    index: int = typer.Option(0, "--index", min=0),
    output: Path | None = typer.Option(None, "--output"),
) -> None:
    """Build a provider-neutral image-generation handoff from one trend candidate."""
    candidates = _load_candidates(input_path)
    if index >= len(candidates):
        raise typer.BadParameter(f"index {index} is outside {len(candidates)} candidates")
    profile = _load_product(product)
    brief_result = build_brief(candidates[index], profile, comparison_target=compare)
    render_request = build_render_request(brief_result)
    text = _json_dump(render_request)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    else:
        typer.echo(text)


@app.command()
def batch(
    input_path: Path = typer.Argument(..., exists=True, dir_okay=False),
    product: Path = typer.Option(..., "--product", exists=True, dir_okay=False),
    compare: str | None = typer.Option(None, "--compare"),
    top: int = typer.Option(5, "--top", min=1, max=50),
    output: Path | None = typer.Option(None, "--output"),
) -> None:
    """Dedupe, rank and build multiple four-panel briefs in one command."""
    result = build_batch(
        _load_candidates(input_path),
        _load_product(product),
        comparison_target=compare,
        top=top,
    )
    text = _json_dump(result)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    else:
        typer.echo(text)


@app.command(name="doctor")
def doctor_command() -> None:
    """Report core health and optional integration availability without failing."""
    typer.echo(_json_dump(local_doctor()))


if __name__ == "__main__":
    app()
