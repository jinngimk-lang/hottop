# Hottop Status

Last updated: 2026-08-21 08:12 +08:00
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
- Added named source presets (`film-entertainment`, `ai-tech`, `zh-internet-culture`) and direct-publisher quality resolution.
- Added `EnrichmentPipeline` with deterministic provider ordering and failure provenance.
- Added `PlainHttpAdapter` as the no-JavaScript, no-auth final public-web fallback for HTML, Markdown and text pages.
- Root-caused CI run 135 failure to whitespace inserted before punctuation across inline HTML tags; parser fix commit `62e651412932417a78bdcd766f8ab5f9268dce9d` passed CI run 139.
- Added `build_default_enrichment_pipeline()` so the normal order is Crawl4AI → Firecrawl when configured → plain HTTP; commit `d67b504c7b932ea905cd8657ebdab2abaa6f317e` passed CI run 145.
- Added typed YAML batch configuration (`BatchConfig` / `BatchSourceConfig`) and loader; implementation commit `a5a0e8195324c47302ce437d32d79cf049eca678` passed CI run 149.
- Added `config/batches/ai-tech-daily.yml` as a repeatable batch example.
- Archived live research batches through `examples/runs/2026-08-21-0800-briefs.json`.
- The 08:00 batch adds: `Hot Spot` release-day monolithic-AI ruler → orchestration satire; robotics `ChatGPT moment` anticipation → do-today's-work-now workflow metaphor; generic dinosaur box-office showdown → flashy tool rivalry versus quiet delivery.

## In progress

- CI run 151 is validating the newest sample-batch-config head.
- Wiring `BatchConfig` into `hottop batch --config` so stored YAML can drive live fan-in without repeating CLI flags.
- Applying per-source `preset` values from batch config to collector/source-quality behavior.
- Connecting approved `RenderRequest` JSON to future image-generation providers without coupling the core package to any single vendor.

## Next actions

1. Confirm CI run 151/newest head; repair immediately if red.
2. Add `hottop batch --config <yaml>` using per-source limits, stored `top`, comparison target, and source list.
3. Make batch-config `preset` explicit in collector/source-quality resolution instead of metadata-only.
4. Continue live research batches, prioritizing highly visual conflicts and culturally recognizable roles over generic news summaries.
5. Inspect Foundation v0.1 diff/reviews and, once remaining contracts are green, mark PR #1 ready and merge.

## Latest live creative signals

- **Hot Spot release day (AP, 2026-08-21):** broad sentient-AI-ruler premise is useful for monolithic万能AI versus coordinated specialist workflow. Never reproduce actor likenesses, film sets, costumes, posters, title treatment or frames. Claim mode: satire.
- **Robotics `ChatGPT moment` discussion (Reuters, 2026-08-20):** useful for `waiting for the next breakthrough vs finishing today's work with orchestration`. Use fictional robots only; never copy Unitree or other product designs. Claim mode: workflow metaphor.
- **Dinosaur box-office showdown (AP, 2026-08-17):** two dinosaur-themed releases competing for attention provides a generic `two flashy tools fighting while the project waits` structure. Use only original generic dinosaur designs; never reproduce franchise creatures, actors, posters or film frames. Claim mode: satire.
- **Humanoid robot commercial test (Reuters, 2026-08-18/20):** strong `backflips vs useful work` metaphor. Use fictional robots only; never copy Unitree/UBTECH/etc. product designs. Claim mode: workflow metaphor.
- **China rocket-launch tourism (Reuters, 2026-08-19):** strong `ignition vs mission-control delivery` structure. Use fictional unbranded spacecraft and generic control-room imagery; no real launch hardware/site replica. Claim mode: satire.
- **Niu Lai viral animation phenomenon (FT, 2026-08-20):** useful for shipped-first-draft versus planning-theater framing. Never use the film's characters, title treatment, poster, frames or identifiable character design. Claim mode: satire/workflow metaphor.
- **The Odyssey summer visibility:** strong cave/giant/escape structure. Use only public-domain Homeric archetypes; never reproduce current actors, costumes, sets, posters or film frames. Claim mode: satire.
- **AI-agent safety/control:** useful for raw autonomy versus controlled orchestration. Use only high-level safety context; never include exploit steps, hacking commands or operational cybersecurity detail.
- **Gemini 3.7 Flash agent-workflow race:** useful for `single fast leg vs full relay` category framing. Never claim InkClawAgent is faster or benchmark-superior; the comparison is workflow scope/orchestration only.

## Constraints

- No credentials/cookies/browser profiles in Git.
- Authenticated social channels are optional and never required for CI.
- Comparisons without benchmarks remain satire/metaphor/opinion; factual superiority claims need evidence.
- Do not reproduce actor likenesses, official posters, exact film frames, copyrighted character designs, identifiable proprietary robot designs, or copied platform UIs in generated prompts.
