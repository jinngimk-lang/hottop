from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any

import typer
import yaml

from .batch_config import BatchConfig, load_batch_config
from .briefing import build_brief
from .collectors.dailyhot import DailyHotApiCollector
from .collectors.newsnow import NewsNowCollector
from .collectors.rss import RSSCollector
from .collectors.rsshub import RSSHubCollector
from .comparison_research import (
    ComparisonResearchResult,
    adapt_comparison_research_results,
)
from .creative_package import CreativePackageInput, build_creative_package
from .doctor import local_doctor
from .integrations.playwright_cli import PlaywrightCliAdapter
from .intake import CreativeIntent, next_question, resolve_intent
from .models import ComparisonCandidate, CreativeConcept, ProductProfile, TrendCandidate
from .orchestrator import OrchestrationInput, orchestrate
from .pipeline import build_batch
from .positioning import (
    build_comparison_research_queries,
    choose_comparison_target,
    infer_promotion_context,
    normalize_comparison_candidates,
)
from .rendering import build_creative_render_request, build_render_request
from .scoring import score_candidate

app = typer.Typer(no_args_is_help=True, add_completion=False)


def _json_dump(value: Any) -> str:
    if hasattr(value, "model_dump"):
        value = value.model_dump(mode="json")
    return json.dumps(value, ensure_ascii=False, indent=2)


def _write_or_echo(value: Any, output: Path | None) -> None:
    text = _json_dump(value)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    else:
        typer.echo(text)


def _load_candidates(path: Path) -> list[TrendCandidate]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    records = raw if isinstance(raw, list) else [raw]
    return [TrendCandidate.model_validate(record) for record in records]


def _load_comparison_candidates(path: Path) -> list[ComparisonCandidate]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, dict):
        if "comparison_candidates" in raw:
            records = raw["comparison_candidates"]
            candidate_kind = "comparison"
        elif "research_results" in raw:
            records = raw["research_results"]
            candidate_kind = "research"
        else:
            raise typer.BadParameter(
                "comparison JSON objects must contain `comparison_candidates` or `research_results`"
            )
    else:
        records = raw
        candidate_kind = "comparison"
    if not isinstance(records, list):
        raise typer.BadParameter("comparison input must contain a JSON array")
    if candidate_kind == "research":
        research_results = [ComparisonResearchResult.model_validate(record) for record in records]
        candidates = adapt_comparison_research_results(research_results)
    else:
        candidates = [ComparisonCandidate.model_validate(record) for record in records]
    return normalize_comparison_candidates(candidates)


def _load_concept(path: Path) -> CreativeConcept:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return CreativeConcept.model_validate(raw)


def _load_intent(path: Path) -> CreativeIntent:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return CreativeIntent.model_validate(raw)


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
    if source == "rsshub":
        return await RSSHubCollector(route=key).collect(limit=limit)
    raise typer.BadParameter("source must be one of: dailyhot, newsnow, rss, rsshub")


def _parse_source_spec(spec: str) -> tuple[str, str]:
    source, separator, key = spec.partition(":")
    if not separator or not source.strip() or not key.strip():
        raise typer.BadParameter("source specs must use TYPE:KEY, for example dailyhot:zhihu")
    return source.strip(), key.strip()


async def _discover_many(specs: list[str], limit: int) -> list[TrendCandidate]:
    parsed = [_parse_source_spec(spec) for spec in specs]
    batches = await asyncio.gather(*(_discover(source, key, limit) for source, key in parsed))
    return [candidate for batch in batches for candidate in batch]


async def _discover_configured(config: BatchConfig) -> list[TrendCandidate]:
    batches = await asyncio.gather(
        *(_discover(source.type, source.key, source.limit) for source in config.sources)
    )
    return [candidate for batch in batches for candidate in batch]


@app.command()
def intent(
    request: str = typer.Argument(..., help="Natural-language creative request"),
    output: Path | None = typer.Option(None, "--output"),
) -> None:
    """Resolve a natural-language request into transparent creative intent."""
    _write_or_echo(resolve_intent(request), output)


@app.command(name="next-question")
def next_question_command(
    intent_path: Path = typer.Argument(..., exists=True, dir_okay=False),
    output: Path | None = typer.Option(None, "--output"),
) -> None:
    """Return one high-impact guided question, or a ready-to-create state."""
    _write_or_echo(next_question(_load_intent(intent_path)), output)


@app.command()
def position(
    term: str | None = typer.Argument(
        None, help="Promoted brand/product/keyword when no YAML profile is supplied"
    ),
    product: Path | None = typer.Option(None, "--product", exists=True, dir_okay=False),
    comparisons: Path | None = typer.Option(
        None,
        "--comparisons",
        exists=True,
        dir_okay=False,
        help="Optional researched comparison candidates or public research-result JSON",
    ),
    output: Path | None = typer.Option(None, "--output"),
) -> None:
    """Resolve promotion semantics and optionally select from researched comparison evidence."""
    if product is not None:
        profile = _load_product(product)
    elif term and term.strip():
        profile = ProductProfile(name=term.strip(), subject_type="keyword")
    else:
        raise typer.BadParameter("provide a promoted term or --product YAML profile")

    comparison_candidates = _load_comparison_candidates(comparisons) if comparisons else []
    selected_comparison = choose_comparison_target(profile, comparison_candidates)
    payload = {
        "schema_version": "hottop.position.v1",
        "profile": profile.model_dump(mode="json"),
        "context": infer_promotion_context(profile).model_dump(mode="json"),
        "research_queries": build_comparison_research_queries(profile),
        "comparison_candidates": [
            candidate.model_dump(mode="json") for candidate in comparison_candidates
        ],
        "selected_comparison": (
            selected_comparison.model_dump(mode="json") if selected_comparison else None
        ),
    }
    _write_or_echo(payload, output)


@app.command(name="reference-plan")
def reference_plan(
    url: str = typer.Argument(..., help="Public HTTP(S) page to inspect as a visual reference"),
    question: str = typer.Option(..., "--question", help="Specific visual/creative uncertainty to study"),
    mobile: bool = typer.Option(False, "--mobile", help="Plan capture using a mobile viewport"),
    output: Path | None = typer.Option(None, "--output"),
) -> None:
    """Emit a safe visual-reference acquisition plan without executing a browser."""
    adapter = PlaywrightCliAdapter()
    open_command = adapter.open_command(url, mobile=mobile)
    payload = {
        "schema_version": "hottop.reference-plan.v1",
        "url": url,
        "question": question.strip(),
        "rights_mode": "analysis-only",
        "execute": False,
        "persistent_profile": False,
        "session": adapter.session,
        "commands": [
            open_command,
            adapter.screenshot_command("artifacts/reference.png", hires=True),
            adapter.close_command(),
        ],
        "research_output": {
            "composition_grammar": [],
            "reveal_pattern": None,
            "text_grammar": None,
            "bridge_type": None,
            "why_effective": None,
            "what_not_to_copy": [],
            "provenance_note": "",
        },
    }
    _write_or_echo(payload, output)


@app.command()
def discover(
    source: str = typer.Option("dailyhot", "--source"),
    key: str = typer.Option(
        "zhihu", "--key", help="DailyHot route, NewsNow source id, RSS URL, or RSSHub route"
    ),
    limit: int = typer.Option(30, "--limit", min=1, max=100),
    output: Path | None = typer.Option(None, "--output"),
) -> None:
    """Fetch and normalize one trend source."""
    items = asyncio.run(_discover(source, key, limit))
    _write_or_echo([item.model_dump(mode="json") for item in items], output)


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
    """Build the backward-compatible four-panel renderer handoff."""
    candidates = _load_candidates(input_path)
    if index >= len(candidates):
        raise typer.BadParameter(f"index {index} is outside {len(candidates)} candidates")
    profile = _load_product(product)
    brief_result = build_brief(candidates[index], profile, comparison_target=compare)
    _write_or_echo(build_render_request(brief_result), output)


@app.command(name="render-concept")
def render_concept(
    concept_path: Path = typer.Argument(..., exists=True, dir_okay=False),
    output: Path | None = typer.Option(None, "--output"),
) -> None:
    """Validate a flexible CreativeConcept and emit provider-neutral `hottop.render.v2`."""
    _write_or_echo(build_creative_render_request(_load_concept(concept_path)), output)


@app.command(name="package-concepts")
def package_concepts(
    package_path: Path = typer.Argument(..., exists=True, dir_okay=False),
    output: Path | None = typer.Option(None, "--output"),
) -> None:
    """Validate reviewed creative alternatives, select the strongest, and emit render v2."""
    raw = json.loads(package_path.read_text(encoding="utf-8"))
    _write_or_echo(build_creative_package(CreativePackageInput.model_validate(raw)), output)


@app.command(name="orchestrate")
def orchestrate_command(
    orchestration_path: Path = typer.Argument(..., exists=True, dir_okay=False),
    output: Path | None = typer.Option(None, "--output"),
) -> None:
    """Rank reviewed creative directions for the resolved request and emit render v2."""
    raw = json.loads(orchestration_path.read_text(encoding="utf-8"))
    _write_or_echo(orchestrate(OrchestrationInput.model_validate(raw)), output)


@app.command()
def batch(
    input_path: Path | None = typer.Argument(None, exists=True, dir_okay=False),
    product: Path = typer.Option(..., "--product", exists=True, dir_okay=False),
    config: Path | None = typer.Option(None, "--config", exists=True, dir_okay=False),
    compare: str | None = typer.Option(None, "--compare"),
    top: int | None = typer.Option(None, "--top", min=1, max=50),
    source: list[str] | None = typer.Option(
        None,
        "--source",
        help=(
            "Repeatable TYPE:KEY collector spec, e.g. dailyhot:zhihu, "
            "rss:https://example.com/feed.xml, or rsshub:bilibili/ranking/0"
        ),
    ),
    limit_per_source: int = typer.Option(30, "--limit-per-source", min=1, max=100),
    output: Path | None = typer.Option(None, "--output"),
) -> None:
    """Dedupe, rank and build briefs from files, stored config, live collectors, or a mix."""
    candidates = _load_candidates(input_path) if input_path else []
    batch_config = load_batch_config(config) if config else None
    if batch_config:
        candidates.extend(asyncio.run(_discover_configured(batch_config)))
    if source:
        candidates.extend(asyncio.run(_discover_many(source, limit_per_source)))
    if not candidates:
        raise typer.BadParameter(
            "provide an input JSON file, --config YAML, and/or at least one --source TYPE:KEY"
        )

    effective_top = top if top is not None else (batch_config.top if batch_config else 5)
    effective_compare = (
        compare
        if compare is not None
        else (batch_config.comparison_target if batch_config else None)
    )
    result = build_batch(
        candidates,
        _load_product(product),
        comparison_target=effective_compare,
        top=effective_top,
    )
    _write_or_echo(result, output)


@app.command(name="doctor")
def doctor_command() -> None:
    """Report core health and optional integration availability without failing."""
    typer.echo(_json_dump(local_doctor()))


if __name__ == "__main__":
    app()
