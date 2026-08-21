# Hottop — Persistent Project Brief

> Read this file first whenever context is missing or a new session continues the project.

## Mission

Build a durable hot-topic meme production system for marketing **any user-selected brand, product, service, feature, campaign, person, idea, keyword, or tool**. InkClawAgent is one current example, not a permanent assumption.

The system continuously turns current film, entertainment, AI, technology, internet and culture topics into **four-panel illustrated meme briefs**. Visual characters and scenes may change every time. The stable creative mechanism is the mapping:

- user-supplied promoted term → resolve its subject type, category, job-to-be-done, pain point and differentiator;
- current recognizable topic → recognizable conflict/roles;
- promoted subject → solver / breaker / winner / desired-outcome role appropriate to its real category;
- automatically researched direct competitor, adjacent substitute, incumbent default, legacy workflow or manual workaround → obstacle / antagonist / mismatched approach role;
- four panels → setup, escalation, reversal, punchline;
- final copy → memorable comparison without fabricating factual superiority claims.

Example semantic mapping (not a fixed template): a mythic cave monster can represent a competing workflow; a clever escaping hero can represent the promoted subject. For a non-software product, the same hotspot may map to a completely different pain point and victory condition.

## Non-goals

- No permanent InkClawAgent or AI-tool requirement.
- No permanent calf/cow mascot requirement.
- No requirement that all four panels share exactly the same composition or character pose.
- No direct copying of film stills, actor likenesses, official posters, logos, packaging trade dress or other protected visual assets.
- No unsupported factual claim that Subject A is objectively faster/better/cheaper/safer than Subject B. If there is no evidence, comparisons remain satire, metaphor, opinion, category tradeoff or workflow framing.

## Core pipeline

1. **Resolve promotion semantics** — understand the supplied term: subject type, category, job, pain point, differentiator and known alternatives.
2. **Discover comparisons** — research direct competitors, incumbents, substitutes and legacy/manual alternatives using fresh public sources.
3. **Discover hotspots** — collect fresh candidate topics from public web/RSS/news/video/social sources.
4. **Enrich** — fetch source pages and supporting context.
5. **Normalize** — turn heterogeneous source records into one `TrendCandidate` schema and comparison candidates into structured records.
6. **Rank** — score hotspot recency/recognizability/visual potential and comparison recognizability/category overlap/pain-point contrast/evidence quality.
7. **Map** — identify recognizable roles/conflicts and map the promoted subject + selected comparison target onto those roles.
8. **Write** — generate a four-panel beat sheet, captions, punchlines and medium-matched image prompts.
9. **Guardrail** — mark copyright/likeness/trademark and unsupported-comparison risks; rewrite toward original visual treatment.
10. **Archive** — store promotion context, trend brief, sources, comparison rationale, prompts and outcome notes so successful patterns can be reused.

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
- Image-generation output must be original enough to avoid direct replication of protected characters, actor likenesses, exact costumes, official poster composition, recognizable frames, proprietary UI or distinctive competitor trade dress.
- Factual comparative claims require evidence records; otherwise phrase them as satire/metaphor/creative opinion or use a category/legacy proxy instead of inventing a defect.

## Durable output contract

Every generated meme concept should be serializable with:

- promotion context: subject name/type/category/job/pain point/differentiator;
- topic + timestamp;
- source URLs/evidence notes;
- researched comparison candidates + selected target + selection rationale;
- recognizable conflict summary;
- promoted-subject role;
- comparison role;
- visual medium + genre treatment;
- four panel descriptions;
- four panel captions;
- punchline options;
- image-generation prompt;
- negative prompt / visual exclusions;
- risk flags;
- factual-claim status (`satire`, `supported`, `needs_evidence`).

## Current milestone

**Foundation v0.1**

Build the schemas, ranking/mapping engine, RSS/public-web collector interfaces, Agent-Reach and Crawl4AI adapters/configuration, CLI, reusable agent skill, tests and GitHub Actions. Close the milestone with arbitrary-promotion semantics, evidence-aware comparison discovery, medium routing and real trend archives.

## Session recovery

When resuming:

1. Read `PROJECT.md`.
2. Read `STATUS.md`.
3. Read the newest file in `docs/superpowers/specs/` and `docs/superpowers/plans/` relevant to the active milestone.
4. Inspect open PRs / failing CI.
5. Continue from `Next actions` in `STATUS.md` without asking for routine approval.
