# Hottop Status

Last updated: 2026-08-21 11:00 +08:00
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
- Added `config/batches/ai-tech-daily.yml` as a repeatable batch example; CI run 151 passed.
- Added `hottop batch --config <yaml>` support with per-source limits plus stored `top` and comparison target; implementation commit `84fab9605511e97a9414278ada343c554f886986` passed CI run 157.
- Added a default **visual medium router** to `skills/hottop-meme/SKILL.md`: film/live-action → high photorealistic cinematic treatment; animation → animation-native rendering; internet personalities/social phenomena → real-world documentary/social-video realism; AI/technology → realistic contemporary tech imagery; native internet memes → format-matched distribution grammar.
- Generalized the project mission beyond InkClawAgent/AI. The promoted term may now represent a brand, product, service, feature, campaign, person, idea, keyword, or tool.
- Extended `ProductProfile` (kept for backward compatibility) with `subject_type`, `category`, `keywords`, `jobs_to_be_done`, `pain_points_solved`, `differentiators`, and `known_alternatives`.
- Added `PromotionContext` and `ComparisonCandidate` schemas plus `src/hottop/positioning.py`.
- Added deterministic promotion-context inference, research-query planning (`<subject> competitors`, alternatives, category/job and pain-point queries), and evidence-aware comparison-target selection.
- Comparison selection now scores recognizability, category overlap, pain-point contrast, evidence quality and relation type; it never upgrades an unevidenced named competitor to a supported factual claim.
- Updated briefing so the promoted subject's real pain point/differentiator drives the reversal rather than assuming an Agent workflow. Competitor scenes explicitly forbid inventing defects.
- Updated the reusable skill with automatic competitor/substitute/incumbent/manual-workaround discovery and a rule to prefer the clearest pain-point contrast rather than the most famous rival.
- RED contract commit `08b5cf532b368db07c6cad414457f1ccc3fb7eef` failed CI run 169 as expected; generalized implementation/skill/project commits passed through CI run 179.
- Archived live research batches through `examples/runs/2026-08-21-1100-briefs.json`.

## In progress

- Applying per-source `preset` values from batch config to collector/source-quality behavior.
- Connecting approved `RenderRequest` JSON to future image-generation providers without coupling the core package to any single vendor.
- Turning comparison research queries into an explicit CLI/agent handoff so a supplied marketing term can trigger competitor research before meme construction.
- Continuing live research and meme-brief archives while Foundation v0.1 closes out.
- Verifying CI on the newest 11:00 archive/status head; the latest confirmed green implementation is CI run 179.

## Next actions

1. Confirm CI on the newest status/head; repair immediately if red.
2. Add a `position` / comparison-research handoff command that emits resolved promotion context plus current competitor-search queries from a YAML profile or supplied term.
3. Add a structured researched-comparison input/output path so web/Agent-Reach results can become `ComparisonCandidate` records with evidence instead of only a free-text `--compare` name.
4. Make batch-config `preset` explicit in collector/source-quality resolution instead of metadata-only.
5. Add an enrichment command/path that can enrich selected candidates through the default fallback chain before briefing.
6. Extend renderer handoff so `visual_medium` / `genre_treatment` and promotion context are first-class serialized fields rather than prompt-only convention.
7. Continue live research batches, prioritizing highly visual conflicts and culturally recognizable roles over generic news summaries.
8. Inspect Foundation v0.1 diff/reviews and, once remaining contracts are green, mark PR #1 ready and merge.

## Latest live creative signals

- **Humanoid robots move from spectacle toward useful work (Reuters, 2026-08-18/20):** strong `single tricks vs useful coordinated outcome` structure. The 11:00 archive uses a fictional demo-first comparison proxy rather than inventing a defect about a named competitor. Render as photorealistic contemporary robotics/editorial imagery with original unbranded robots. Claim mode: satire/workflow metaphor.
- **Niu Lai viral animation phenomenon (FT, 2026-08-20):** strong `shipped imperfect first version vs endless perfection-before-feedback` structure. Render as original deliberately rough low-poly animation; never use the film's characters, title treatment, poster, frames or identifiable character design. Claim mode: satire/workflow metaphor.
- **The Odyssey summer visibility (AP, 2026-08-16):** strong cave/giant/escape structure. Use only public-domain Homeric archetypes. Default visual medium is photorealistic epic live-action with original casting, costumes, set design and camera composition; never reproduce current actors, costumes, sets, posters or film frames. A real named competitor should only replace the generic cyclops proxy after category/alternative research. Claim mode: satire.
- **Robocops on traffic duty (Reuters, 2026-08-20):** excellent real-world `many specialist lanes vs one orchestrated route` metaphor. Render as photorealistic contemporary street/editorial imagery; use original unbranded robots and no real police insignia. Claim mode: satire/workflow metaphor.
- **Robotics `ChatGPT moment` discussion (Reuters, 2026-08-20):** useful for `waiting for the next breakthrough vs finishing today's work with orchestration`. Render as realistic robotics-expo/project-room imagery with fictional robots only. Claim mode: workflow metaphor.
- **Hot Spot release day (AP, 2026-08-21):** broad sentient-AI-ruler premise is useful for monolithic万能AI versus coordinated specialist workflow. Film-adjacent concepts default to photorealistic cinematic live-action language, but never reproduce actor likenesses, film sets, costumes, posters, title treatment or frames. Claim mode: satire.
- **China rocket-launch tourism (Reuters, 2026-08-19):** strong `ignition vs mission-control delivery` structure. Use fictional unbranded spacecraft and generic control-room imagery; no real launch hardware/site replica. Claim mode: satire.

## Constraints

- No credentials/cookies/browser profiles in Git.
- Authenticated social channels are optional and never required for CI.
- Comparisons without evidence remain satire/metaphor/opinion/category tradeoff; factual superiority claims need evidence.
- A named competitor may be used only for a supported limitation, accurate category tradeoff, specific unmet job/pain point, or clearly subjective satire. Otherwise prefer a fictional category proxy, incumbent habit, legacy workflow or manual workaround.
- Medium and genre should remain highly recognizable, but do not reproduce actor likenesses, official posters, exact film frames, copyrighted character designs, identifiable proprietary robot designs, copied platform UIs, or competitor packaging trade dress.
