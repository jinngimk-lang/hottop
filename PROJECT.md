# Hottop — Persistent Project Brief

> Read this file first whenever context is missing or a new session continues the project.

## Mission

Build a durable hot-topic meme production system for marketing **InkClawAgent** and future user-selected products.

The system continuously turns current film, entertainment, AI, technology, internet and culture topics into **four-panel illustrated meme briefs**. Visual characters and scenes may change every time. The stable creative mechanism is the mapping:

- current recognizable topic → recognizable conflict/roles;
- selected product → solver / breaker / winner role;
- optional competitor, popular tool or legacy workflow → obstacle / antagonist / weaker approach role;
- four panels → setup, escalation, reversal, punchline;
- final copy → memorable product comparison without fabricating factual superiority claims.

Example semantic mapping (not a fixed template): a mythic cave monster can represent a competing workflow; the clever escaping hero can represent InkClawAgent; the last panel lands a short product punchline.

## Non-goals

- No permanent calf/cow mascot requirement.
- No requirement that all four panels share exactly the same composition or character pose.
- No direct copying of film stills, actor likenesses, official posters, logos or other protected visual assets.
- No unsupported factual claim that Product A is objectively faster/better than Product B. If there is no benchmark evidence, comparisons remain satire, metaphor, opinion or workflow framing.

## Core pipeline

1. **Discover** — collect fresh candidate topics from public web/RSS/news/video/social sources.
2. **Enrich** — fetch source pages and supporting context.
3. **Normalize** — turn heterogeneous source records into one `TrendCandidate` schema.
4. **Rank** — score recency, recognizability, conflict clarity, visual potential, product fit and evidence quality.
5. **Map** — identify recognizable roles/conflicts and map product + optional comparison target onto those roles.
6. **Write** — generate a four-panel beat sheet, captions, punchlines and image prompts.
7. **Guardrail** — mark copyright/likeness/trademark and unsupported-comparison risks; rewrite toward original visual treatment.
8. **Archive** — store trend brief, sources, prompts and outcome notes so successful patterns can be reused.

## Upstream integrations

### Agent-Reach

Use as an optional multi-platform acquisition layer rather than vendoring its whole repository. Pin the tested upstream commit in configuration. It can provide web, YouTube, RSS, GitHub and—when the operator explicitly configures authenticated channels—additional social/community sources.

### Crawl4AI

Use as an optional deep-page/browser acquisition layer. Prefer its Docker/MCP service for dynamic pages, clean Markdown, screenshots and multi-page crawling. Keep its service isolated from the core pipeline.

## Repository operating rules

- Work on feature branches and merge through PRs.
- Keep `PROJECT.md`, `STATUS.md` and implementation docs current so work survives context loss.
- Prefer adapters/interfaces around upstream projects; do not fork huge third-party code into this repo unless there is a concrete need.
- Keep credentials, cookies and API keys out of Git and CI logs.
- Public-source collection must respect site terms, robots/rate limits where applicable, authentication boundaries and account safety.
- Third-party authenticated channels are opt-in and should use dedicated/secondary accounts when practical.
- Image-generation output must be original enough to avoid direct replication of protected characters, actor likenesses, exact costumes, official poster composition or recognizable frames.
- Factual comparative claims require evidence records; otherwise phrase them as satire/metaphor/creative opinion.

## Durable output contract

Every generated meme concept should be serializable as a `MemeBrief` containing:

- topic + timestamp;
- source URLs/evidence notes;
- recognizable conflict summary;
- product name and product role;
- optional comparison target and comparison role;
- four panel descriptions;
- four panel captions;
- punchline options;
- image-generation prompt;
- negative prompt / visual exclusions;
- risk flags;
- factual-claim status (`satire`, `supported`, `needs_evidence`).

## Current milestone

**Foundation v0.1**

Build the schemas, ranking/mapping engine, RSS/public-web collector interfaces, Agent-Reach and Crawl4AI adapters/configuration, CLI, reusable agent skill, tests and GitHub Actions. Then run the first real trend batch and archive generated meme briefs.

## Session recovery

When resuming:

1. Read `PROJECT.md`.
2. Read `STATUS.md`.
3. Read the newest file in `docs/superpowers/specs/` and `docs/superpowers/plans/` relevant to the active milestone.
4. Inspect open PRs / failing CI.
5. Continue from `Next actions` in `STATUS.md` without asking for routine approval.
