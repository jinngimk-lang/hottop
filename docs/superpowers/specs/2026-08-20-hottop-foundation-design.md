# Hottop Foundation Design

## 1. Goal

Build `hottop` into a durable hot-topic meme research and creative-brief pipeline for InkClawAgent and future user-selected products.

The creative unit is not a fixed mascot. Each run may use different characters, worlds, genres and four-panel compositions. The stable mechanism is semantic mapping:

1. discover a current recognizable topic;
2. identify its memorable conflict, roles and visual grammar;
3. map the promoted product to the solver/breaker/winner role;
4. optionally map a competitor, popular tool or legacy workflow to the obstacle/antagonist/weaker-role metaphor;
5. produce four-panel beats, captions, punchlines and image prompts;
6. preserve evidence and risk flags.

## 2. Safety and claim posture

The system separates **creative comparison** from **factual comparison**.

- `satire`: subjective/metaphorical punchline; no objective benchmark claim.
- `supported`: factual claim with evidence records attached.
- `needs_evidence`: a draft that contains an objective comparison and must not ship until supported or rewritten.

Visual prompts must use original reinterpretation rather than actor likenesses, official posters, exact film frames, exact costume replication, title treatments or protected character designs. A topic may provide narrative semantics (for example, “cyclops-like cave guardian versus clever seafaring hero”) while the rendered characters remain original.

## 3. Architecture

### 3.1 Acquisition layer

All sources normalize into `TrendCandidate`.

**Core public sources**

- `DailyHotApiCollector`: fast Chinese hot-list discovery across Bilibili, Weibo, Zhihu, Baidu, Douyin, movie/news/tech sources and more.
- `NewsNowCollector`: alternate real-time/hot-news aggregation source.
- `RSSCollector`: arbitrary RSS/Atom feeds and RSSHub routes.

**Optional rich acquisition**

- `AgentReachAdapter`: invokes installed Agent-Reach/upstream CLIs for public web, YouTube, RSS, GitHub and operator-configured social/community channels.
- `Crawl4AIAdapter`: calls a local/remote Crawl4AI service for dynamic pages, clean Markdown, screenshots and multi-page enrichment.

**Reference/optional deployment**

- TrendRadar can be deployed separately when a prebuilt monitoring/notification layer is useful. Hottop should consume its outputs through generic RSS/JSON rather than coupling core logic to its internals.

### 3.2 Normalization layer

`TrendCandidate` fields:

- `id: str`
- `title: str`
- `url: str`
- `source: str`
- `source_rank: int | None`
- `published_at: datetime | None`
- `summary: str | None`
- `tags: list[str]`
- `metrics: dict[str, float]`
- `evidence: list[Evidence]`

Duplicates are keyed by canonical URL first, normalized title fingerprint second.

### 3.3 Ranking layer

`TrendScore` is deterministic and inspectable. Default weighted dimensions:

- recency: 0.25
- cross-source presence: 0.20
- recognizability: 0.15
- conflict clarity: 0.15
- visual potential: 0.10
- product-fit: 0.10
- evidence quality: 0.05

Scores are 0–100. Source-specific popularity values are normalized before entering the scorer.

### 3.4 Semantic mapping layer

`RoleMap` captures:

- `topic_world`
- `conflict`
- `promoted_product`
- `product_role`
- `comparison_target | None`
- `comparison_role | None`
- `archetype`
- `why_it_maps`

Initial archetypes:

- monster-vs-clever-hero
- maze-vs-guide
- siege-vs-breaker
- overloaded-team-vs-orchestrator
- slow-manual-process-vs-automation
- fragmented-tools-vs-coordinator
- gatekeeper-vs-bypass

The mapper can be rule-based in v0.1 and later expose an LLM strategy behind the same interface.

### 3.5 Brief generation layer

`MemeBrief` contains:

- topic metadata and evidence;
- `RoleMap`;
- four `Panel` objects (scene, caption, intent);
- 1–3 punchline candidates;
- master image prompt;
- negative prompt / exclusions;
- risk flags;
- factual claim status.

Panels follow setup → escalation → reversal → punchline, but each panel may use a visually distinct composition.

### 3.6 Persistence

Foundation v0.1 stores JSON/Markdown run artifacts under `examples/runs/YYYY-MM-DD/`. The schema remains portable to SQLite/Postgres later.

## 4. CLI

Commands:

- `hottop discover --source dailyhot --limit 50`
- `hottop rank input.json --top 10`
- `hottop brief input.json --product inkclawagent --compare "work巴迪"`
- `hottop doctor`

`doctor` reports core Python health plus optional Agent-Reach/Crawl4AI availability without failing when optional integrations are absent.

## 5. Upstream integration strategy

### Agent-Reach

Pin a tested upstream commit in `integrations/versions.yml`. Provide an install/check script that installs into the operator environment, never into the repository. Never commit cookies or tokens. CI only validates adapter command construction and parsing using fixtures.

### Crawl4AI

Pin a tested version/commit. Provide `docker-compose.integrations.yml` for a local service and document MCP endpoints. Core Python calls the HTTP API; an MCP config file is included for agent clients. CI uses a fake HTTP transport/fixtures and does not launch browsers.

### DailyHotApi / NewsNow / RSSHub

Treat as swappable JSON/RSS discovery sources. Hottop owns the normalized schema and does not depend on a single aggregator remaining online.

## 6. Failure handling

- Collector timeout/error: return a typed source failure and continue other sources.
- Malformed records: skip record, record parse warning.
- Duplicate topics: merge evidence/source presence.
- Optional integration missing: `doctor` warning, not core failure.
- Objective comparison without evidence: `needs_evidence` and block “publish-ready” status.

## 7. Testing

- Unit tests for models, scorer, dedupe, mapping and guardrails.
- Fixture tests for each collector.
- Adapter tests assert exact CLI/HTTP request construction without requiring authenticated accounts.
- CLI smoke tests.
- GitHub Actions on Python 3.11 and 3.12.

## 8. Foundation deliverable

Foundation v0.1 is complete when:

1. CI is green;
2. at least two zero-auth discovery sources work;
3. Agent-Reach and Crawl4AI adapters pass fixture tests;
4. `hottop discover | rank | brief` works locally;
5. one real trend batch is archived with at least three meme briefs;
6. project state is recoverable from `PROJECT.md` + `STATUS.md`.
