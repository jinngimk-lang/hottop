# Hottop — Persistent Project Brief

> Read this file first whenever context is missing or a new session continues the project.

## Mission

Build a durable **hot-topic brand creative system** for marketing any user-selected brand, product, service, feature, campaign, person, idea, keyword, or tool. InkClawAgent is one example, not a permanent assumption.

The system turns current film, entertainment, animation, technology, internet and culture into original promotional concepts that make a product's value visually memorable. It may produce a four-panel meme, a single visual metaphor, a swipe-reveal carousel, a faux film still/poster, a split old-vs-new comparison, or another compact social format. **Not every concept must be four-panel.**

The durable goal is not “attach a logo to a hot character.” It is to find a natural bridge between the promoted subject and a recognizable cultural idea, then make the subject itself part of the action, object, transformation, role, material, environment, or reveal.

## Creative doctrine

### 1. Semantics before jokes

Resolve the promoted subject before choosing a trend or gag:

- subject type and category;
- job-to-be-done and user outcome;
- pain points and tradeoffs;
- differentiators;
- physical/sensory properties where relevant;
- usage ritual and emotional payoff;
- direct competitors, incumbents, substitutes, legacy workflows and manual workarounds.

The promoted subject does not always need to be a hero character. It can be a decisive prop, material, gesture, route, transformation, tool, environment, or final reveal.

### 2. Reframe before optimize

Hottop must deliberately search beyond incremental category competition. Identify the **category default**: the assumption that most competitors are optimizing. Then apply **constraint deletion**:

1. Why must this assumption exist?
2. What happens if it disappears entirely?
3. What user outcome remains?
4. What new competition axis becomes important?

The canonical mental model is the shift from competing on “better keyboards / better hinges” to questioning whether the interaction needs that physical constraint at all. This is a thinking pattern, not a requirement to imitate any historical product.

Prefer `old premise → deleted constraint → new axis` when it produces a more truthful, surprising and ownable concept than “our feature is slightly better.”

### 3. Bridge search

A strong crossover needs a concrete **visual metaphor** or semantic bridge. Search across:

- shape/material: length, stretch, texture, color, liquid, transparency, weight;
- action/motion: pull, shoot, wrap, snap, transform, connect, launch, escape;
- role: guide, key, shield, director, breaker, fuel, shortcut;
- function: coordinate, unlock, cool, protect, energize, simplify;
- emotion/ritual: relief, indulgence, speed, confidence, habit, celebration;
- language/symbol: phrase, gesture, visual grammar, recognizable narrative structure.

The linkage should be understandable before explanation. A food ribbon becoming the visual action in a cultural reference is stronger than simply putting the food beside a famous costume. A workflow product becoming the escape route is stronger than placing its logo on a hero.

### 4. Format follows the idea

Choose the smallest expression form that makes the bridge land:

- `single-visual-metaphor` — one instantly legible fusion;
- `swipe-reveal` — tease the cultural cue, extend the transformation, then reveal the product/brand;
- `four-panel` — setup → escalation → reversal → punchline;
- `faux-film-still` / poster — cinematic role, emotion or spectacle;
- `split-old-vs-new` — category reframing / constraint deletion;
- `product-as-prop` — the product itself performs the culturally recognizable action.

For swipe-reveal, each frame must add information; do not reveal the full answer in the first frame.

### 5. Medium follows the hotspot

- Film/live action → highly photorealistic, original cinematic treatment in the relevant broad genre.
- Animation → original animation-native medium matching the recognizable 2D/3D/low-poly grammar.
- Internet personalities / social phenomena → real-world documentary/social-native realism with anonymous people unless user-supplied rights-cleared assets are available.
- Technology/software → realistic contemporary tech imagery with light cinematic polish.
- Food/consumer goods → polished commercial product photography or product-led visual metaphor when appropriate.
- Native internet memes → format-matched distribution grammar rebuilt with original assets.

Match the medium and recognition cues, not protected production assets.

### 6. Comparison is optional; truth is not

Research direct competitors, recognizable defaults, substitutes and old workflows. Select the clearest pain-point contrast, not automatically the most famous rival.

A named competitor may appear only when the negative side is a supported factual limitation, accurate design/category tradeoff, a job it is not designed to solve, or clearly subjective satire. Never invent benchmarks, outages, prices, quality defects, safety failures or customer sentiment. When evidence is weak, use a generic category proxy or make the old assumption itself the antagonist.

### 7. References teach grammar, not pixels

Hottop may research public advertising, cultural and visual examples when composition, reveal pacing, social distribution grammar, product photography or source-medium cues would improve the concept. The durable output of this research is an **abstract reference manifest**, not a copied image.

- use public HTTP(S) and provenance-rich sources;
- prefer Playwright CLI for token-efficient, coding-loop visual inspection and screenshot capture; use ephemeral sessions by default;
- use Playwright MCP only when persistent state or rich exploratory DOM reasoning materially helps;
- treat ordinary third-party screenshots as `analysis-only` unless public-domain or rights-cleared;
- retain source URL/time/rights mode plus abstract composition/reveal/bridge notes;
- do not commit protected screenshots merely to build a moodboard;
- do not use a reference as a pixel-level target or reproduction recipe.

Semantic visual-memory infrastructure such as OpenCLIP + Qdrant should be added only after the reference corpus is large enough that retrieval quality justifies the dependency. Start with transparent local manifests and measure the need first.

## Creative review gate

A concept is ready only if it passes:

1. **Instant comprehension** — lands in roughly 1–3 seconds.
2. **Natural linkage** — product and hotspot connect through a real bridge.
3. **Product centrality** — removing the promoted subject breaks the idea.
4. **Surprise** — includes a non-obvious jump or reframe.
5. **Ownability** — cannot be swapped to any competitor unchanged.
6. **Evidence safety** — factual comparisons are supported; otherwise satire/metaphor.
7. **Original execution** — culturally recognizable without reproducing protected production assets.

Reject `hot character + logo`, feature lists wearing costumes, forced references that need a paragraph of explanation, and concepts that advertise any brand equally well.

## Adaptive guided intake and creative orchestration

Hottop should feel like a creative director, not a configuration form. The default front door is **adaptive guided intake**: resolve what the user already said, infer conservative defaults with provenance/confidence, and ask only unresolved questions that materially change the output. The default interaction budget is **0–3 questions**; most requests should need zero or one. Never repeat platform, style, product, goal or direction that the request already made clear, and never dump a full questionnaire when one compact choice is enough.

The durable interaction controls are:

- **campaign goal** — awareness, pain-point contrast, launch, conversion, brand memory, hotspot participation or category reframe;
- **platform** — a creative input, not merely an export size; output should be **platform-native** before rendering;
- **style** — changes creative grammar, such as reversal/punchline, negative space, cinematic world-building, documentary realism or product texture, not only prompt adjectives;
- **creative ambition** — `safe`, `witty`, `breakout`, `category-breaking`; the last level explicitly raises constraint-deletion/category-reframing pressure;
- **product visibility** — `metaphor-first`, `balanced`, `product-first`, controlling reveal timing and brand attribution;
- **audience** — optional by default and asked only when it materially changes tone, risk or decoding.

Question priority is promotion target → campaign goal → platform → style → creative ambition → product visibility. Audience is not a routine question. Explicit user choices always override inference. When the question budget is exhausted, Hottop proceeds with transparent defaults rather than blocking production.

### Project-shape adaptation

Do not apply one meme grammar to every category. **Project-shape** is a routing signal:

- food/consumer → physical/sensory bridge, product texture, commercial-product/social-native treatment, reveal when useful;
- software/AI/B2B → workflow pain, category-default deletion, evidence-aware comparison and technology/professional grammar;
- entertainment/culture → source-medium cinematic/animation/native-meme grammar;
- fashion/beauty/retail → form/material/style bridge and visual ownership;
- services/local → ritual/outcome/emotion bridge and credible real-world scenario;
- campaigns/ideas/keywords → semantic/symbol bridge and clear decoding.

### Contextual review

The seven-part Creative Review remains the hard quality gate. **Contextual review** adds platform fit, style fit, campaign-goal fit, ambition fit, project-shape fit, hotspot-native fit and humor/delight when humor is expected. Contextual scores may rank concepts that already pass the hard gate; they can never rescue a weak, generic or unsafe concept.

A conversational or future Studio front end may generate multiple internal directions—at minimum pain contrast, natural bridge-led metaphor and constraint-deletion reframe when feasible—then pass them through this gate. The stable handoff is a Creative Package/Orchestration result containing intent provenance, candidate reviews, selected concept, concise rationale, alternates for revisions, references and `hottop.render.v2`.

Revision controls such as `换方向`, `更有梗`, `更大胆`, `产品更明显`, `更高级` and `换平台` should mutate only the relevant intent dimension and rerun the minimum necessary stages rather than restarting product understanding from scratch.

## Core pipeline

1. **Resolve interaction intent** — promotion target, campaign goal, platform, style, creative ambition, product visibility and only the high-impact missing questions.
2. **Resolve promotion semantics** — category, job, pain point, differentiator, physical/sensory properties, ritual and alternatives.
3. **Discover comparisons** — competitors, incumbents, substitutes, legacy/manual options with fresh evidence.
4. **Discover hotspots** — public web/RSS/news/video/social sources.
5. **Enrich** — source pages, context and useful visual/cultural cues.
6. **Research references when useful** — capture provenance and abstract composition/reveal/medium grammar, not source pixels.
7. **Normalize** — structured trend, comparison and optional visual-reference records.
8. **Reframe** — identify category default, candidate deleted constraints and new competition axes.
9. **Bridge** — generate shape/action/role/function/emotion/symbol links between subject and hotspot.
10. **Rank** — score trend quality, comparison fit and creative bridge strength.
11. **Select format and project/platform treatment** — single metaphor, swipe-reveal, four-panel, faux still/poster, split comparison or product-as-prop with platform/style/project-shape routing.
12. **Write** — beats, captions, reveal order, punchlines and medium-matched prompts.
13. **Review and select** — hard creative gate first, contextual review second; regenerate rather than force a winner if all fail.
14. **Guardrail** — claims, copyright/likeness/trademark, misleading competitor framing.
15. **Archive** — intent/provenance, evidence, reference manifests, rejected assumptions, selected bridge, format, reviews, prompts and outcome notes.

## Persistent project memory protocol

Long-running work must not depend on chat memory alone. Every new multi-session project should create a **living project charter** before substantial implementation or repeated production. In Hottop, `PROJECT.md` is that durable charter and `STATUS.md` is the short-lived execution snapshot.

### What belongs in the living project charter

Keep only durable information that future sessions must recover accurately:

- mission, audience, success criteria and non-goals;
- canonical creative doctrine and product/brand semantics;
- architecture, major integrations and operating boundaries;
- accepted constraints and evidence/claim rules;
- stable workflow and output contracts;
- active reusable skills and recovery order;
- major strategic decisions and a compact **decision log** when rationale would otherwise be lost.

Keep transient CI run IDs, hourly research notes and short-lived tasks in `STATUS.md` or archives instead of bloating the charter.

### Context recovery

Treat repository documents as the source of truth when there is **context pressure**: a long conversation, a new session, uncertainty about prior decisions, a handoff between agents, or a return after time away. Recovery order is:

1. `PROJECT.md` — durable direction and canonical decisions;
2. `STATUS.md` — current branch, CI, in-progress work and next actions;
3. active reusable skill(s);
4. newest relevant spec/plan/decision record;
5. PR/CI state and current evidence as needed.

Do not ask the user to repeat stable project direction that the repository can recover.

### Living updates

A **material direction change** must be persisted before future work relies on it. Examples include a new creative principle, newly preferred expression form, category-reframing rule, integration strategy, safety boundary, architecture change, recurring user instruction, or a repeated pattern proven useful across runs.

When one appears:

1. challenge it against the current doctrine and evidence;
2. decide whether it is durable or merely experiment-specific;
3. if durable, **update the charter** and the relevant skill/spec in the same workstream;
4. record why it changed, what assumption it replaces, and any migration/compatibility effect in the decision log when useful;
5. update `STATUS.md` so the next recovery reads the new direction immediately.

Do not silently accumulate contradictory instructions. Supersede stale rules explicitly and keep one canonical current interpretation.

### Stability review

After meaningful doctrine or architecture updates, reread the charter with fresh eyes and check for contradictions, stale assumptions, duplicated rules, missing recovery steps and overly narrow examples. The goal is a project that becomes **more precise and more interesting as it learns**, not a longer document that preserves every historical thought.

## Non-goals

- No permanent InkClawAgent, AI-tool, mascot or character requirement.
- No permanent four-panel requirement.
- No rule that the product must always be personified as the winner.
- No direct copying of film stills, actor likenesses, official posters, protected character designs, logos, packaging trade dress, proprietary UI, distinctive production assets or finished advertising compositions.
- No unsupported factual claim that Subject A is objectively faster/better/cheaper/safer than Subject B.
- No assumption that creativity means staying inside the current category's accepted competition axis.
- No requirement to deploy a vector database, browser agent or GPU render stack before a measured use case exists.
- No static mandatory intake questionnaire; the interaction must stop asking once the remaining uncertainty no longer justifies interruption.

## Upstream integrations

### Agent-Reach

Use as an optional multi-platform acquisition layer rather than vendoring its whole repository. Pin the tested upstream commit in configuration. Authenticated channels are operator opt-in.

### Crawl4AI

Use as the preferred optional deep-page/browser acquisition layer for dynamic pages, clean Markdown, screenshots and multi-page crawling. Keep the service isolated from the core package.

### Firecrawl / plain HTTP

Use Firecrawl as an optional hosted fallback and plain HTTP as the final no-JavaScript public-web fallback. Keep credentials out of source control.

### Playwright CLI / Playwright MCP

Use Playwright CLI as the preferred optional visual-reference browser adapter for coding loops because it provides concise, scriptable visual inspection without making browser state a core dependency. Hottop defaults to an ephemeral named session and public HTTP(S) pages. Playwright MCP remains an optional escalation for stateful exploratory browser work, not the default path.

### Future semantic visual memory

When a sufficiently large rights-aware reference corpus exists, evaluate pinned OpenCLIP inference for image/text embeddings and Qdrant/Qdrant MCP for semantic retrieval. Begin with local/read-only operation where practical, keep provenance and rights metadata beside embeddings, and require a retrieval-quality experiment before promoting this stack into the core workflow.

### Future render backends

Keep rendering provider-neutral. ComfyUI is a candidate optional local/offline backend because reusable workflows can be exposed through APIs, but it must remain isolated behind an adapter, pinned to a tested stable release/workflow, and preserve per-model/license provenance. Do not silently enable paid API nodes or make GPU availability a core requirement.

## Repository operating rules

- Work on feature branches and merge through PRs.
- Keep `PROJECT.md`, `STATUS.md`, relevant specs/plans and reusable skills current so work survives context loss.
- On recovery, follow the persistent project memory protocol rather than relying on fuzzy conversation memory.
- Prefer adapters/interfaces around upstream projects; do not fork huge third-party code without a concrete need.
- Keep credentials, cookies and API keys out of Git and CI logs.
- Respect site terms, access boundaries, rate limits and account safety.
- Image output should reproduce the **broad medium/genre grammar** needed for recognition while remaining an original staging.
- Factual comparative claims require evidence records; otherwise use satire/metaphor/category tradeoff or a generic proxy.
- Visual-reference assets are evidence for analysis, not automatic source material for generation.

## Durable output contract

A mature creative concept/package should be serializable with:

- creative intent: request, promotion target, campaign goal, platform, style, creative ambition, product visibility, optional audience/hotspot preference and source/confidence for inferred values;
- questions asked/answers when guided intake was required;
- promotion context: subject/type/category/job/pain point/differentiator plus physical/sensory cues where useful;
- topic + timestamp + evidence;
- researched comparison candidates + selected target/rationale;
- optional visual-reference manifest(s) + provenance/rights mode;
- `category_default`;
- `deleted_constraint` or explicit `none`;
- `new_competition_axis`;
- bridge type + one-sentence bridge;
- selected expression form;
- platform/style/project-shape routing hints when useful;
- reveal/narrative beats;
- visual medium + genre treatment;
- captions/copy/punchlines;
- base creative review + contextual review + selection rationale;
- alternates sufficient for lightweight revision controls;
- master image-generation prompt;
- negative prompt / exclusions;
- risk flags;
- factual-claim status (`satire`, `supported`, `needs_evidence`);
- provider-neutral `hottop.render.v2` handoff.

## Reusable skills

- `skills/brand-metaphor-creative/SKILL.md` — primary creative-thinking method: adaptive intent handling, category reframing, constraint deletion, bridge search, expression-form selection, project/platform routing, creative review gate and persistent project protocol for multi-session creative work.
- `skills/creative-reference-research/SKILL.md` — provenance-first visual-reference research: Playwright-assisted inspection, composition/reveal abstraction, rights modes and explicit non-copying handoff into creative strategy.
- `skills/hottop-meme/SKILL.md` — hotspot acquisition, evidence-aware comparison handling, visual-medium routing and four-panel execution when four-panel is the selected form.

## Current milestone

**Foundation v0.1**

Close the foundation with arbitrary-promotion semantics, adaptive guided intake, platform/style/project-shape routing, evidence-aware comparison discovery, hotspot acquisition/enrichment, creative-doctrine persistence, reference-research contracts, bridge/format contracts, contextual review, provider-neutral renderer handoff, tests, CI and representative live archives.

## Session recovery

When resuming:

1. Read `PROJECT.md`.
2. Read `STATUS.md`.
3. Read `skills/brand-metaphor-creative/SKILL.md`; read `skills/creative-reference-research/SKILL.md` when visual-reference research is relevant; read `skills/hottop-meme/SKILL.md` when hotspot/four-panel execution applies.
4. Read the newest relevant spec/plan or decision record for the active milestone.
5. Inspect open PRs / failing CI.
6. Continue from `Next actions` in `STATUS.md` without asking for routine approval.
