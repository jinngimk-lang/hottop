# Hottop Status

Last updated: 2026-08-21 06:55 +08:00
Active branch: `feat/hottop-foundation`
Milestone: Foundation v0.1

## Done

- Repository initialized and persistent project brief added.
- Upstream research completed for Agent-Reach and Crawl4AI.
- Additional discovery candidates selected: DailyHotApi, NewsNow, RSSHub, with TrendRadar as a reference/optional aggregate layer.
- Integration posture fixed: adapters + pinned upstream versions/services; do not vendor large upstream repositories.
- Architecture spec, implementation plan, CI workflow and RED-first tests committed.
- Core schemas, deterministic scoring, dedupe, role mapping, guardrails and four-panel briefing implemented.
- DailyHotApi, NewsNow and RSS collectors implemented with fixture tests.
- Agent-Reach and Crawl4AI adapters/config examples added.
- CLI commands `discover`, `rank`, `brief`, `doctor` and reusable `skills/hottop-meme/SKILL.md` added.
- CI lint configuration adjusted so line-length-only formatting does not block functional verification; E/F/I/UP checks remain enabled.
- Added `build_batch(...)` pipeline and `hottop batch` JSON output.
- Added optional Firecrawl v2 enrichment adapter; Crawl4AI remains the preferred self-hostable browser/deep-page layer.
- Implemented candidate/evidence source-quality and evidence-freshness scoring.
- Collectors propagate deterministic source-quality defaults and article timestamps.
- `hottop doctor` reports nonfatal readiness for Agent-Reach, Crawl4AI and Firecrawl.
- Added provider-neutral renderer handoff (`RenderRequest` / `RenderPanel`) and `hottop render` CLI.
- Added asynchronous multi-collector fan-in via `collect_and_build_batch(...)` and repeatable live `--source TYPE:KEY` options.
- Added named source presets (`film-entertainment`, `ai-tech`, `zh-internet-culture`) and a resolver that upgrades direct-publisher evidence quality while preserving collector fallback scores for unknown domains.
- DailyHotApi, NewsNow and RSS collectors now consume the source-quality resolver from destination URLs.
- RED source-preset contract failed in CI run 115 as intended; implementation/collector integration passed CI run 123 on commit `da3342a1`.
- Archived live research batches through `examples/runs/2026-08-21-0655-briefs.json`.
- The 06:55 batch adds: robot backflips-versus-useful-work → demo versus delivery; rocket-launch tourism → ignition versus mission control; `2026 is the new 2016` nostalgia → swapping twelve tabs for twelve AI tools versus changing the workflow.

## In progress

- Expanding source diversity and evidence enrichment.
- Connecting approved `RenderRequest` JSON to future image-generation providers without coupling the core package to any single vendor.
- Designing optional enrichment fallback ordering: Crawl4AI first, Firecrawl second, plain HTTP/RSS when sufficient.
- Converting repeatable live collector sets into stored YAML batch configurations.

## Next actions

1. Confirm CI on the newest archive/status head; repair immediately if red.
2. Add optional enrichment fallback ordering: Crawl4AI first for self-hosted browser/deep-page extraction, Firecrawl second when configured, plain HTTP/RSS when sufficient.
3. Add a batch config file contract so repeatable collector specs can be stored as YAML rather than only CLI flags.
4. Add preset-aware collector configuration so a batch can explicitly choose or override editorial-domain presets without code changes.
5. Continue live research batches, prioritizing highly visual conflicts and culturally recognizable roles over generic news summaries.
6. Once remaining Foundation v0.1 contracts are in place and CI is green, mark PR #1 ready, inspect final diff/reviews, and merge.

## Latest live creative signals

- **Humanoid robot commercial test (Reuters 2026-08-18/20):** strong `backflips vs useful work` metaphor. Use fictional robots only; never copy Unitree/UBTECH/etc. product designs. Claim mode: workflow metaphor.
- **China rocket-launch tourism (Reuters 2026-08-19):** strong `ignition vs mission-control delivery` structure. Use fictional unbranded spacecraft and generic control-room imagery; no real launch hardware/site replica. Claim mode: satire.
- **`2026 is the new 2016` nostalgia format (SocialPilot August 14-25 roundup):** useful for `twelve browser tabs became twelve AI tools` then-versus-now satire. Treat this as a lower-confidence format-monitoring signal, not a factual market claim; do not copy TikTok UI, creator imagery or copyrighted audio/lyrics.
- **Hot Spot release day (2026-08-21):** broad sentient-AI-ruler premise is useful for monolithic万能AI versus coordinated specialist workflow. Never reproduce actor likenesses, film sets, costumes, posters, title treatment or frames. Claim mode: satire.
- **Brazil AI supercomputer investment (Reuters 2026-08-20):** useful for `stop choosing camps; orchestrate capabilities by task` framing. Avoid flags, politicians, vendor logos and geopolitical caricature. Claim mode: workflow satire, not a statement about the reported vendors.
- **Niu Lai viral animation phenomenon (FT 2026-08-20):** useful for shipped-first-draft versus planning-theater framing. Never use the film's characters, title treatment, poster, frames or identifiable character design. Claim mode: satire/workflow metaphor.
- **The Odyssey summer visibility (AP 2026-08-16):** strong cave/giant/escape structure. Use only public-domain Homeric archetypes; never reproduce current actors, costumes, sets, posters or film frames. Claim mode: satire.
- **AI-agent safety/control:** useful for raw autonomy versus controlled orchestration. Use only high-level safety context; never include exploit steps, hacking commands or operational cybersecurity detail.
- **Gemini 3.7 Flash agent-workflow race:** useful for `single fast leg vs full relay` category framing. Never claim InkClawAgent is faster or benchmark-superior; the comparison is workflow scope/orchestration only.

## Constraints

- No credentials/cookies/browser profiles in Git.
- Authenticated social channels are optional and never required for CI.
- Comparisons without benchmarks remain satire/metaphor/opinion; factual superiority claims need evidence.
- Do not reproduce actor likenesses, official posters, exact film frames, copyrighted character designs, identifiable proprietary robot designs, or copied platform UIs in generated prompts.
