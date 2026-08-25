# Hottop — Persistent Project Brief

> Read this file first whenever context is missing or a new session continues the project. `PROJECT.md` is durable doctrine; `STATUS.md` is the short-lived execution snapshot.

## Mission

Build a durable **hot-topic brand creative system** for marketing any user-selected brand, product, service, feature, campaign, person, idea, keyword, or tool. InkClawAgent is one example, not a permanent assumption.

Hottop turns current film, entertainment, animation, technology, internet and culture into original promotional concepts that make a product's value visually memorable. It may produce a four-panel meme, a single visual metaphor, a swipe-reveal carousel, a faux film still/poster, a split old-vs-new comparison, a short cinematic video, or another compact social format. **Not every concept must be four-panel**, not every output is Anti-Polish, and not every promoted subject must be personified as a hero.

The durable goal is not “attach a logo to a hot character.” Find a natural bridge between the promoted subject and a recognizable cultural idea, then make the subject itself part of the action, prop, transformation, role, material, route, environment, or reveal.

## Creative doctrine

## Mandatory fresh-generation entry gate

Every new image or video generation request is a fresh creative run, including requests made directly in Chat. Before invoking an image/video generation tool, renderer, or production backend:

1. recover current Hottop truth from `PROJECT.md`, `STATUS.md`, and the relevant checked-in creative skill/config when the request is Hottop-related;
2. resolve the promoted product/subject from the current request and current facts rather than silently inheriting a prior campaign subject;
3. **re-explore current news, culture, entertainment, technology and internet hotspots with live public research for that request**, even when a previous asset was generated recently;
4. retain source/provenance plus fresh observation/publication timing for the selected hotspot;
5. choose the visual style/medium and output format from the current product-to-hotspot bridge and source-medium grammar, not from a historical template;
6. construct `hottop.generation-preflight.v1` and require `evaluate_generation_preflight(...)` or `hottop generation-preflight` to return `ready=true` before final asset generation.

Default freshness is fail-closed: live research must have been observed within **6 hours**; when a trustworthy publication timestamp exists, the selected hotspot must have been published within **7 days**. A source with unknown publication time may pass only when fresh observation evidence exists, and copy must not invent publication recency. Missing/stale evidence means research again or select another hotspot; it does not mean generate anyway.

**Historical examples are not defaults.** Previous products, hotspots, characters, cow/snake/Odyssey stories, four-panel layouts, Anti-Polish, low-poly 3D, cinematic realism, or any other successful treatment teach reusable grammar only. Product, hotspot, visual style/medium, and output format are re-resolved per request. A stable product understanding may be reused only when the current request still promotes that same product and the facts remain current; the hotspot/style/format still require a fresh decision.

This entry gate is provider-neutral. Live Chat/web research or configured collectors acquire evidence; the runtime preflight validates that evidence and the dynamic creative selections before generation. It does not silently browse, install dependencies, or substitute a stale trend.

### 1. Semantics before jokes

Resolve the promoted subject before choosing a trend or gag:

- subject type and category;
- job-to-be-done and user outcome;
- pain points and tradeoffs;
- differentiators;
- physical/sensory properties where relevant;
- usage ritual and emotional payoff;
- direct competitors, incumbents, substitutes, legacy workflows and manual workarounds.

The promoted subject can be a decisive prop, material, gesture, route, transformation, tool, environment, or final reveal instead of a mascot.

### 2. Reframe before optimize

Identify the **category default** — the assumption most competitors optimize — before accepting the current competition axis. Apply constraint deletion:

1. Why must this assumption exist?
2. What happens if it disappears entirely?
3. What user outcome remains?
4. What new competition axis becomes important?

Prefer `old premise → deleted constraint → new axis` when it is more truthful, surprising and ownable than “our feature is slightly better.” Strategic hypotheses remain hypotheses until evidence supports them.

### 3. Bridge search

Search for concrete product/hotspot bridges across:

- shape/material — length, stretch, texture, color, liquid, transparency, weight;
- action/motion — pull, shoot, wrap, snap, transform, connect, launch, escape;
- role — guide, key, shield, director, breaker, fuel, shortcut;
- function — coordinate, unlock, cool, protect, energize, simplify;
- emotion/ritual — relief, indulgence, speed, confidence, habit, celebration;
- language/symbol — phrase, gesture, visual grammar, recognizable narrative structure.

The linkage should be understandable before explanation. A product becoming the culturally recognizable action is stronger than a logo placed beside the reference.

### Cultural mechanism mapping

**Borrow the mechanism, not the skin.** A hotspot is valuable because audiences already understand a relationship, causal chain, ritual, transformation, conflict, reversal or delivery grammar—not because it supplies a costume, famous-looking character, location, palette or catchphrase to paste around an ad.

If the user supplies a hotspot, scene, meme, news item, image, phrase or cultural point, analyze that supplied source first and use fresh public research to verify factual/current context when needed. Do not silently replace a user-selected source merely because another topic is larger. If the user supplies no hotspot, run the mandatory live discovery pass and select a current candidate before mechanism mapping.

For every selected hotspot, extract:

1. the **recognition hook** — what people immediately remember/repeat;
2. the **causal/relationship mechanism** — roles, desire, obstacle/transformation, escalation, reversal and resolution;
3. the **native visual grammar** — the medium, camera/staging, polish/roughness and distribution cues that make it feel native;
4. the **native dialogue/language rhythm** — role relationship, sentence shape, pause, deadpan/seriousness, escalation and punchline timing;
5. for motion, the **native audio grammar** — voice delivery, music energy/texture, silence and Foley/SFX timing that materially carries recognition or comedy.

Then map a real product pain point/differentiator into a functional role inside that mechanism: route, key, antidote, obstruction-breaker, transformation, rule deletion, rescue action, tool, material, consequence or reveal. **Every retained hotspot element must have a job** in the causal chain; decorative references are removed.

The **product must change the story outcome** through a product truth or defensible metaphor. If another unrelated brand can replace it without changing the story logic, reject or rebuild the concept. Prefer the audience decoding order **hotspot recognition → mapping → product consequence → punchline**. Benefits should be understood from the changed outcome before they are stated as feature copy.

Mythic transformation/rescue, cave-blocking obstruction/breakout, crude-family/deadpan 3D, chase/escape, looping failure, boss fight and similar patterns are examples of reusable analytical primitives only. They are not templates. The current hotspot decides the mechanism, humor, medium, dialogue and audio treatment every time.

### 4. Format follows the idea

Choose the smallest expression form that makes the bridge land:

- `single-visual-metaphor` — one instantly legible fusion;
- `swipe-reveal` — tease, extend, then reveal;
- `four-panel` — setup → escalation → reversal → punchline;
- `faux-film-still` / poster — cinematic role, emotion or spectacle;
- `split-old-vs-new` — category reframing / constraint deletion;
- `product-as-prop` — the product performs the culturally recognizable action;
- short video / GIF — when motion, dialogue, reaction timing, transformation or sound carries the idea.

For swipe-reveal, each frame must add information. For narrative video, preserve scene geography, character identity and action continuity rather than using unrelated stills with hard cuts.

### 5. Medium follows the hotspot

- Film/live action → original photorealistic cinematic treatment in the relevant broad genre.
- Animation → original animation-native 2D/3D/low-poly grammar.
- Internet personalities / social phenomena → documentary/social-native realism with anonymous people unless rights-cleared user assets exist.
- Technology/software → realistic contemporary tech imagery with appropriate polish.
- Food/consumer goods → commercial product photography or product-led visual metaphor when useful.
- Native internet memes → distribution grammar rebuilt with original assets.

Match the medium and recognition cues, not protected production assets.

### 6. Distribution-native restraint

For hotspot participation, meme reach and brand-memory work, audience experience comes before landing-page mechanics.

- **No in-asset destination by default:** omit URLs, QR codes, app-store badges and commands such as `立即体验` unless conversion creative explicitly requires them.
- **Benefits as consequences:** show value through what happens — the obstruction disappears, the task starts, the ritual shortens — before adding benefit labels.
- **Light payoff:** final attribution stays compact enough that the audience still experiences a meme/scene rather than an ad poster.

### 7. Anti-Polish / Controlled Badness

Hottop supports a deliberate inverse competition axis for some motion creative: **low production feel + high comedy control**.

Intentionally permit cheap-looking low-poly/rough 3D, simple materials, imperfect lighting, slightly stiff motion, blunt Foley, cheap instrumentation, deadpan acting and absurd events treated seriously. These are controlled aesthetic choices, not permission for random failure.

**Do not polish the badness away; make the badness precise.** Even the roughest output must preserve character continuity, scene geography, cause/effect, subtitle correctness, dialogue intelligibility, comedy timing, product semantics, claim safety, rights safety and compatible encoding.

The product should remain native to the crude world rather than suddenly becoming a glossy blue-purple AI hologram or feature-card UI unless that contrast is itself the concept.

**Roughness is a routing variable, not the product identity.** Video profiles carry `roughness_score` 0–100. Film-like, premium, social-native or emotionally serious hotspots should use lower roughness and credible faces, costumes, lighting and camera work. Surface polish varies; directing precision does not.

### 8. Comparison is optional; truth is not

Research competitors, defaults, substitutes and old workflows when useful. A named competitor may appear negatively only when the limitation/tradeoff is evidence-backed, accurately scoped, or unmistakably subjective satire. Never invent benchmarks, outages, prices, quality defects, safety failures or customer sentiment. When evidence is weak, use a generic category proxy or make the old assumption itself the antagonist.

### 9. References teach grammar, not pixels

Public visual references are for composition, pacing, camera, product-photography and source-medium grammar — not pixel copying.

- public HTTP(S) and provenance-rich sources first;
- Playwright CLI is the preferred optional coding-loop visual inspector; Playwright MCP is an escalation for stateful exploratory browser work;
- ordinary third-party screenshots are `analysis-only` unless public-domain or rights-cleared;
- retain source URL/time/rights mode plus abstract grammar notes and `what_not_to_copy`;
- never use exact film frames, actor likenesses, official posters, protected character designs, proprietary UI, distinctive trade dress, source footage or copyrighted soundtrack as generation targets without rights-cleared input.

Semantic visual memory such as OpenCLIP + Qdrant is added only after a rights-aware corpus and retrieval benchmark justify the dependency.

## Creative review gate

A concept is ready only if it passes:

1. **Instant comprehension** — roughly 1–3 seconds.
2. **Natural linkage** — product and hotspot connect through a real bridge.
3. **Product centrality** — removing the promoted subject breaks the idea.
4. **Surprise** — non-obvious jump or category reframe.
5. **Ownability** — cannot be swapped to any competitor unchanged.
6. **Evidence safety** — factual comparisons are supported; otherwise satire/metaphor.
7. **Original execution** — culturally recognizable without reproducing protected production assets.

Reject `hot character + logo`, feature lists wearing costumes, forced references requiring a paragraph of explanation, and concepts that advertise any brand equally well.

## Adaptive guided intake and orchestration

Hottop should feel like a creative director, not a configuration form. Resolve what the user already said, infer conservative defaults with provenance/confidence, and ask only unresolved questions that materially change the result. The default interaction budget is **0–3 questions**, usually zero or one.

Durable controls:

- **campaign goal** — awareness, pain contrast, launch, conversion, brand memory, hotspot participation, category reframe;
- **platform** — creative input, not only export size; output should be **platform-native** before rendering;
- **style** — creative grammar, not prompt adjectives only;
- **creative ambition** — `safe`, `witty`, `breakout`, `category-breaking`;
- **product visibility** — `metaphor-first`, `balanced`, `product-first`;
- **audience** — optional unless it materially changes tone/risk/decoding.

Question priority is promotion target → campaign goal → platform → style → creative ambition → product visibility. Explicit user choices override inference. When the question budget is exhausted, proceed with transparent defaults.

**Project-shape** is a routing signal: food/consumer emphasizes sensory/physical bridges; software/AI/B2B emphasizes workflow pain and category-default deletion; entertainment follows source-medium grammar; fashion/beauty emphasizes form/material/style; services/local emphasize ritual/outcome/emotion; campaigns/ideas emphasize semantic/symbol bridges.

The seven-part Creative Review remains the hard gate. **Contextual review** — platform/style/goal/ambition/project-shape/hotspot-native/humor fit — ranks only concepts that already pass the hard gate.

Revision controls such as `换方向`, `更有梗`, `更大胆`, `产品更明显`, `更高级`, `换平台` should mutate only the relevant dimensions rather than restarting product understanding.

## Core pipeline

1. Resolve interaction intent.
2. Resolve promotion semantics.
3. Discover competitors/substitutes/legacy workflows when useful.
4. If the user supplied a hotspot, analyze and freshly verify that source first; otherwise discover current hotspots with fresh live evidence for the current generation request.
5. Extract hotspot recognition hook, causal/relationship mechanism, native visual/dialogue/audio grammar and source context.
6. Research visual references when useful, abstracting grammar only.
7. Normalize evidence/reference records.
8. Reframe category defaults and deleted constraints.
9. Search semantic/visual bridges and assign the product a functional role that changes the story outcome.
10. Rank trend, mechanism and bridge quality.
11. Select expression form, platform treatment, style and roughness dynamically for this request.
12. Write beats, captions, reveal order, dialogue, audio cues and punchlines.
13. Run hard Creative Review and contextual ranking.
14. Guardrail claims, copyright/likeness/trademark and competitor framing.
15. Run the mandatory fresh-generation preflight; blocked inputs do not proceed to asset generation.
16. For motion: choose the strongest quality route, including image-first reference-conditioned recovery when direct generation misses the quality bar, then `hottop.render.v2 → VideoProductionConfig → hottop.video-plan.v1 → generation → audio → compositor → encoder → media verification`.
17. Archive intent, provenance, evidence, hotspot mechanism, reference manifest, rejected assumptions, selected bridge, product role/outcome change, format, reviews, prompts, risks and outcome evidence.

## Motion production doctrine

### Zero-cost first

For unattended generation, **`ZERO_COST_MODE=true` is the preferred default policy**. Hottop may spend free shared GPU capacity only on high-value generative shots while UI/product footage, captions, deterministic camera work, audio, compositing and final encoding remain CPU/operator-owned whenever possible.

- no paid fallback, credits, overage, card enrollment or hidden billing;
- free capacity exhaustion waits, bounded-retries, fails, or degrades to an explicitly deterministic path;
- model downloads, GPU provisioning and large optional runtimes remain operator-controlled;
- every generated/deterministic shot must pass the appropriate quality and byte/provenance gate before composition;
- quality failures are not rebranded as “Anti-Polish”.

### Deterministic software 3D baseline

Production v0.2 includes a **pure software low-poly 3D path** as a guaranteed zero-cost baseline when no GPU/model is available. It uses real 3D geometry/projection/animation rather than slideshow zooms, emits playable MP4 shots through FFmpeg, and writes byte-bound provenance sidecars consumed before MoviePy composition. This path is intentionally suitable for Controlled Badness and testable production evidence; it is not the visual ceiling for cinematic profiles.

### Generated-video routes

- **HF ZeroGPU** — optional free shared-GPU transport with bounded free-only routing, quality gates and strict download/token boundaries. Availability is never guaranteed.
- **Wan2.2** — primary permissive local/open generation candidate where suitable hardware is operator-provided.
- **WanGP** — operator-managed low-VRAM interop route through its supported headless/API boundary; Hottop does not vendor it, auto-install it or auto-download models. Its own license is evaluated separately from the models it runs.
- **Comfy API v2** — optional explicitly configured self-hosted/remote orchestration adapter; credentials are environment-only, remote endpoints/outputs are HTTPS-gated, local HTTP is loopback-only, output download redirects are disabled and API tokens are not attached to output downloads.
- **FramePack / FastVideo / LTX / H3 / SCAIL / LongCat / other candidates** — tracked in a reviewed candidate registry and enabled only after code-license, weights-license, hardware, security, zero-cost and measurable-quality checks. A permissive code repository does not automatically authorize its weights or hosted endpoint.

### Artifact integrity

Generated or deterministic footage is not trusted merely because a provider returned an MP4. Validate decodability, duration/stream structure, frame motion/duplicate ratio and final codec/media constraints as relevant. Bind accepted shot artifacts to SHA-256 and byte size and re-verify immediately before composition. Partial/rejected artifacts are deleted.

### Character/reference continuity

Reference-conditioned generation uses local, rights-safe inputs only (`generated-original` or `user-provided-rights-cleared`). Repeated subjects carry stable `subject_id`, role and identity-lock semantics; conflicts fail before GPU work. Provider-specific image fields are isolated behind adapters rather than guessed in the creative contract.

### Image-first quality recovery

**Image-first quality recovery** is an optional quality route, not a universal pipeline. Use it when the concept calls for motion but the available **direct video** path fails the chosen style's visual-quality, identity or consistency bar and the existing reference-conditioned path is likely to improve it.

Generate or select high-quality rights-safe keyframe/reference images first, and require them to pass the same hotspot-mechanism, product-role, visual-style and identity review expected of the final piece. Bind their provenance, SHA-256 and stable subject/role/identity-lock data, then use the repository's existing **reference-conditioned I2V** adapters when the chosen backend supports them. Do not add a duplicate video backend merely to implement this routing rule. When direct video already meets or exceeds the target, keep the direct route.

The final asset is **not a slideshow**. Static stills, pan/zoom-only motion, unrelated hard-cut images or an MP4 container without meaningful action do not count as successful video. Reference-conditioned I2V must still show meaningful motion, preserve geography/identity/action, follow the hotspot's native timing and pass motion/duplicate, audio, artifact, codec and final media verification. Reject, retry or reroute when the generated motion is worse than the approved keyframe or breaks continuity.

### Audio is first-class

Role-aware dialogue (`speaker`, `delivery`, voice profile), original music and SFX/Foley are preserved from `render.v2` into `video-plan.v1` and the execution timeline.

- free fallback: eSpeak Mandarin + Hottop original synthetic music + procedural Foley;
- **CosyVoice3** is a reviewed operator-owned local quality upgrade with explicit rights gating for reference voice audio and no silent model download;
- **Qwen3-TTS** is a high-priority permissive local benchmark candidate; voice-cloning capability remains rights-gated and is not enabled merely because the model is open;
- future TTS/music adapters must preserve zero-cost policy, license provenance and voice/music rights boundaries;
- never imitate copyrighted commercial soundtracks or clone a real person's voice without rights-cleared source and intended-use authority.

### Composition/finalization

- MoviePy is the default deterministic unattended headless compositor.
- Motion Canvas remains optional for richer custom vector motion / interactive preview.
- FFmpeg finalizes H.264/AAC/yuv420p/fast-start output and media verification.
- Remotion remains optional/license-reviewed rather than a silent default dependency.

`hottop video-plan ...` is planning-only. `hottop video-run ...` is dry-run by default; only explicit `--execute` may spawn trusted configured stages after readiness passes.

## Autonomous operating mandate

The project is operated with broad repository autonomy. Routine, reversible, evidence-backed decisions are delegated to the project operator/agent and **must not stop for repetitive approval**.

Without asking again, the operator may:

- research and choose implementation approaches;
- create/update feature branches, tests, code, configs, docs, examples and CI;
- fix regressions and security findings;
- create, review, update and merge PRs when repository gates are satisfied;
- select among zero-cost/open alternatives;
- add or update reusable skills, MCP/plugin/tool integrations when they materially improve the project and their permissions/security are understood;
- update `PROJECT.md`, skills/specs and `STATUS.md` when durable direction changes;
- continue useful work across phase boundaries rather than waiting for the next scheduled loop.

Pause only for materially higher-risk boundaries: destructive/irreversible operations, secrets/credential changes or disclosure, paid actions/credits, legal commitments, sensitive external publication, or another action whose consequences cannot reasonably be contained/reversed.

Autonomy does not weaken evidence standards. A new dependency, model, plugin, MCP or upstream project is admitted only after its actual value and boundary are understood.

## Continuous ecosystem radar

Hottop is a **living system**, not a fixed stack. Production work includes continuous targeted research for materially better GitHub/open-source projects, models, runtimes and current technical developments.

### Radar scope

Track developments relevant to concrete Hottop gaps, especially:

- T2V/I2V and reference/character-consistent video generation;
- low-VRAM and CPU/operator-owned inference;
- verified free shared-GPU routes;
- keyframe/image generation and reference conditioning;
- interpolation, restoration/upscaling and temporal consistency;
- Mandarin/multilingual expressive TTS and safe voice design;
- original music/SFX generation;
- headless orchestration/composition;
- video/audio/media quality assurance;
- licensing, security and breaking runtime/API changes.

Current watchlist includes Wan2.2/WanGP, FramePack, FastVideo, LTX, MiniMax H3, SCAIL, LongCat, ComfyUI/Diffusers, RIFE, Real-ESRGAN, InfiniteTalk, CosyVoice, Qwen TTS and any later project that is measurably stronger.

### Admission gate

A candidate may be integrated when all applicable checks pass:

1. source/project identity and exact tested revision are verifiable;
2. **code license and model/weights license are reviewed separately**;
3. intended commercial/geographic/use restrictions are understood;
4. zero-cost or operator-owned execution is real, with no hidden paid fallback;
5. hardware/runtime requirements are practical for a defined profile;
6. install/runtime/network behavior is acceptably isolated and secure;
7. it addresses a concrete measured Hottop gap;
8. integration is testable, reversible and preferably adapter-based;
9. a benchmark or production case can show why it improves on the current route.

If code is AGPL or otherwise incompatible with Hottop's intended distribution, learn from the architecture but do not copy incompatible implementation into Hottop. Prefer a clean reimplementation of the useful behavior.

### Integration behavior

When a candidate clears the gate, **do not stop at a research note**: add the needed registry entry, config, adapter, test, benchmark or selectively ported permissive file/behavior into Hottop. Avoid vendoring huge repositories when a narrow adapter is enough. Do not auto-install unreviewed code or silently download multi-gigabyte models in CI/normal `video-run`.

Freshness checks are targeted, not noisy. If nothing material changed, continue the active Production milestone rather than producing empty radar reports.

## Persistent project memory protocol

Long-running work must not depend on chat memory alone. `PROJECT.md` is the **living project charter** and `STATUS.md` the current branch/CI/work/next-action snapshot.

### Context recovery

Context recovery order:

1. `PROJECT.md`.
2. `STATUS.md`.
3. Active reusable skill(s).
4. Newest relevant spec/plan/decision record.
5. Current main/open PR/exact-head CI and current public evidence as needed.

Do not ask the user to repeat stable project direction that the repository can recover.

### Chat generation source of truth

When the user asks in a ChatGPT conversation to create or revise a Hottop-related image, meme, storyboard, video, prompt package or production asset, the **current GitHub repository is the project source of truth**, not stale chat memory.

Before generation, recover the minimum relevant current state from the repository:

1. current `PROJECT.md` and `STATUS.md`;
2. the relevant checked-in reusable skill(s);
3. the relevant current example/render source, style/config profile, creative directive, rights/provenance rule and production constraint;
4. current `main` / active PR state when it changes the generation contract;
5. fresh hotspot/public evidence for the new asset request.

A new explicit user instruction in the current conversation may evolve the project, but durable changes must be reconciled back into the repository. Do not generate from an old remembered style/config when the repository has a newer one. The mandatory fresh-generation entry gate applies even when the prior Chat turn used the same product: re-research the hotspot and re-select style/format before a new image/video asset.

When the user names or supplies the hotspot, analyze that hotspot's mechanism and native visual/dialogue/audio grammar first; when no hotspot is supplied, discover fresh candidates first. In both cases the current repository skill—not an old uploaded or remembered copy—is the canonical Chat creative method.

### Living updates

A **material direction change** must be challenged against current doctrine/evidence and classified as durable or experiment-specific. If durable, **update the charter** (`PROJECT.md`) and the relevant skill/spec in the same workstream, explicitly state what stale assumption it supersedes when useful, then update `STATUS.md` so the next recovery immediately sees the new state.

Do not silently stack contradictory instructions. After meaningful doctrine/architecture changes, reread the charter for stale milestones, duplication and contradictions.

## Repository operating rules

- Work on feature branches and merge through PRs unless an explicitly documented exceptional recovery path requires otherwise.
- Continue safe work autonomously; routine design/implementation choices are not approval gates.
- Keep `PROJECT.md`, `STATUS.md`, relevant specs/plans and reusable skills current.
- Prefer narrow adapters/interfaces around upstream projects over vendoring large third-party repositories.
- **Existing-skill first:** inspect already available reusable skills/MCPs/plugins before adding anything. If an existing capability covers the task, use it rather than relearning, reinstalling or introducing a duplicate alternative. Add a new skill/MCP/plugin only for a concrete uncovered capability gap, after permission scope, license, security, cost and reversibility are understood.
- Keep credentials, cookies and API keys out of Git and CI logs.
- Respect site terms, access boundaries, rate limits and account safety.
- Image/video output matches broad genre/medium grammar while remaining original staging.
- Factual comparisons require evidence; otherwise use satire/metaphor/category tradeoff/generic proxies.
- Visual-reference assets are evidence for analysis, not automatic source material for generation.
- New external capabilities must be recorded with provenance/license/runtime/cost status in a machine-readable registry or equivalent durable record when practical.

## Non-goals

- No permanent InkClawAgent, AI-tool, mascot, character or four-panel requirement.
- No rule that the product must always be personified as the winner.
- No direct copying of protected film stills, actor likenesses, official posters/characters, logos, packaging trade dress, proprietary UI, source footage, soundtrack or finished ad composition without rights-cleared input.
- No unsupported factual superiority claims.
- No assumption that creativity means staying inside the current category competition axis.
- No mandatory vector DB/browser-agent/GPU stack before a measured use case exists.
- No static mandatory intake questionnaire.
- No assumption that more polished output is always more effective.
- No assumption that Anti-Polish is correct for every hotspot.
- No dependency/model integration merely because it is popular or open source.

## Durable output contract

A mature creative package should serialize:

- intent and provenance/confidence for inferred values;
- promotion semantics and selected comparison context;
- topic + timestamp + evidence;
- hotspot recognition hook + causal/relationship mechanism;
- native visual grammar + dialogue/language rhythm + motion audio grammar when applicable;
- product role inside the mechanism + story-outcome change;
- optional reference manifest + provenance/rights mode;
- category default, deleted constraint and new competition axis;
- bridge type + bridge sentence;
- selected expression form/platform/style/project-shape treatment;
- static/motion choice, continuity and CTA policy;
- narrative/reveal beats, captions/dialogue/punchlines;
- visual medium + genre treatment;
- hard/contextual reviews, rationale and revision alternates;
- generation prompt, negative prompt, exclusions and risk flags;
- factual-claim status (`satire`, `supported`, `needs_evidence`);
- provider-neutral `hottop.render.v2` handoff;
- when motion is selected: route choice (direct or image-first reference-conditioned recovery when justified) plus `hottop.video-plan.v1` with ordered shots, continuity, `roughness_score`, role-aware dialogue, music/SFX profiles/cues, backend commands/manifests, provenance and final encoding contract.

## Decision log

- **2026-08-25 — Hotspot mechanism mapping becomes canonical; image-first is a quality recovery route, not a template.** Hottop now distinguishes user-supplied hotspots from unspecified requests, extracts recognition/causal/visual/dialogue/audio grammar, requires the product to take a functional role that changes the story outcome, and rejects decorative hotspot skins. When direct video misses the selected quality/identity/style bar, already-reviewed keyframes may drive the existing rights-safe reference-conditioned I2V path; motion/audio/media gates remain mandatory and stills/slideshows do not count as successful video. This extends the existing dynamic-hotspot and reference-continuity architecture without adding a duplicate backend or skill.
- **2026-08-25 — Fresh hotspot research becomes a mandatory generation entry gate.** Every new image/video request, including Chat generation, re-resolves the promoted subject, performs live current-hotspot research, chooses style/medium/format dynamically, and must pass `hottop.generation-preflight.v1` before final generation. This supersedes the weaker assumption that a recently used hotspot/style/example can be silently reused as the next request's default.
- **2026-08-25 — GitHub becomes the Chat generation source of truth; existing capability wins over duplicate installation.** Hottop-related image/video generation in Chat must first recover the latest repository doctrine, status, relevant skills, examples/configs and constraints. Existing suitable skills/MCPs/plugins are reused; new capabilities are added only for real gaps after admission checks.
- **2026-08-25 — Autonomous operation + continuous ecosystem radar become canonical.** Routine reversible repository decisions, integrations, tests, CI work, PR lifecycle and durable project-memory updates proceed without repetitive approval. Every production cycle also performs targeted freshness checks for materially stronger open-source/GitHub/model/runtime options; candidates that pass source/license/cost/hardware/security/value gates are integrated rather than merely reported. High-risk destructive, secret, paid, legal and sensitive-publication actions remain explicit stop boundaries.
- **2026-08-25 — Software 3D becomes the guaranteed zero-cost motion baseline, not the quality ceiling.** Hottop can now generate real low-poly 3D geometry/animation and MP4 shots without Blender/GPU/model downloads, with byte-bound provenance before composition. This secures repeatable Anti-Polish production while cinematic styles continue to seek stronger reference-conditioned open models.
- **2026-08-24 — Zero-cost hybrid video becomes the unattended generation default.** `ZERO_COST_MODE=true` means free shared GPU or operator-owned compute for high-value shots, deterministic MoviePy/FFmpeg/audio for the rest, bounded retries, quality gates and no paid fallback.
- **2026-08-24 — Video roughness becomes style-routed and audio becomes first-class.** Voice, original music and SFX/Foley are production-contract fields rather than ad-hoc post work. Cinematic film memes may remain convincing while low-budget absurdity can be deliberately selected.
- **2026-08-24 — Anti-Polish / Controlled Badness becomes a first-class selectable strategy.** Hottop may compete on deliberate roughness when it strengthens native meme grammar, without relaxing continuity/timing/subtitle/claim/rights requirements.
- **2026-08-24 — Social creative is ad-light by default; motion-native ideas stay motion-native.** URLs/QR CTAs are omitted by default for meme/hotspot/brand-memory assets, and dynamic ideas are not flattened into static posters merely for convenience.

## Reusable skills

- `skills/brand-metaphor-creative/SKILL.md` — primary creative method: intent, category reframing, constraint deletion, mechanism-first hotspot mapping, bridge search, format/medium routing, Controlled Badness, image-first reference-conditioned quality recovery and review gates.
- `skills/creative-reference-research/SKILL.md` — provenance-first visual-reference research and grammar-only handoff.
- `skills/hottop-meme/SKILL.md` — supplied-vs-unspecified hotspot acquisition/analysis, evidence-aware comparison, medium routing and four-panel execution when four-panel is selected.
- External/operator skills, MCPs and plugins may be added only when the existing-skill-first rule finds a concrete capability gap and the autonomous admission rule says the addition materially improves that task.

## Current milestone

**Production v0.2 — repeatable real video output**

Move from architecture completeness to reproducible production evidence. The acceptance target is a real playable vertical short generated from checked-in Hottop render/config sources, with coherent moving imagery, stable original subject identity, continuous geography/action, intelligible dialogue, original BGM/SFX, natural transitions, product benefit emerging through story, quality/provenance gates, and final H.264/AAC-compatible delivery.

Priority order:

1. Produce and verify end-to-end config → real moving shots → audio → composite → final MP4 runs.
2. Keep the software3d route as a guaranteed zero-cost baseline while benchmarking stronger free/open reference-conditioned routes for cinematic quality.
3. Improve character/reference consistency and reject identity/quality failures before composition; use approved image-first references when they measurably improve a weak direct-video route.
4. Upgrade Mandarin dialogue quality through reviewed zero-cost/operator-owned TTS (CosyVoice3/Qwen3-TTS or stronger candidates) while preserving voice-rights gates.
5. Archive render source, production profile, candidate/model provenance, artifact hashes and final media verification so runs are reproducible.
6. Turn successful production runs into repeatable hotspot/product baselines instead of accumulating unproven provider abstractions.

## Session recovery

When resuming:

1. Read `PROJECT.md`.
2. Read `STATUS.md`.
3. Read relevant reusable skills.
4. Read newest relevant spec/plan/decision record.
5. Inspect current main, open PRs and exact-head CI.
6. Perform a targeted ecosystem freshness check relevant to the current Production gap.
7. For any new image/video generation request, separately perform live hotspot/news research and pass the mandatory fresh-generation preflight before generating the asset.
8. If a hotspot is supplied, analyze its mechanism before product mapping; if no hotspot is supplied, discover fresh candidates first.
9. Continue the highest-value safe action autonomously; do not stop for routine approval or wait for a scheduled loop boundary.
