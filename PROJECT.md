# Hottop — Persistent Project Brief

> Read this file first whenever context is missing or a new session continues the project. `PROJECT.md` is durable doctrine; `STATUS.md` is the short-lived execution snapshot.

## Mission

Build a durable **hot-topic brand creative system** for marketing any user-selected brand, product, service, feature, campaign, person, idea, keyword, or tool. InkClawAgent is one example, not a permanent assumption.

Hottop turns current film, entertainment, animation, technology, internet and culture into original promotional concepts that make a product's value visually memorable. Output format is flexible: a single visual metaphor, `swipe-reveal`, four-panel meme, faux still/poster, split old-vs-new comparison, short cinematic video, GIF/animation or another compact social form. **Not every concept must be four-panel.** Not every output is Anti-Polish, and the promoted subject does not have to be a hero character.

The durable creative goal is not `hot character + logo`. Find a natural bridge between the promoted subject and a recognizable cultural mechanism, then make the subject itself part of the action, prop, transformation, role, material, route, environment or reveal.

## Mandatory fresh-generation entry gate

Every new image or video generation request is a fresh creative run, including Chat generation.

Before any final image/video generation:

1. recover current Hottop truth from `PROJECT.md`, `STATUS.md` and relevant checked-in skills/configs;
2. resolve the promoted subject from the current request/current facts rather than silently inheriting a prior campaign;
3. perform live current-hotspot research for that request unless the user supplied the hotspot, in which case freshly verify the supplied source/context when needed;
4. retain source provenance plus observation/publication timing;
5. choose style, medium and format from the current product↔hotspot bridge and source-medium grammar, not from a historical template;
6. construct `hottop.generation-preflight.v1` and require `evaluate_generation_preflight(...)` or `hottop generation-preflight` to return `ready=true` before final generation.

Default freshness is fail-closed: live research should have been observed within **6 hours**; when a trustworthy publication timestamp exists, the selected hotspot should be within **7 days**. Unknown publication time can pass only with fresh observation evidence and no invented recency claims.

**Historical examples are not defaults.** Historical cow/snake/Odyssey stories, four-panel layouts, Anti-Polish, low-poly 3D, cinematic realism and other successful artifacts teach reusable grammar only. They are not automatic defaults for the next request.

## Creative doctrine

### 1. Semantics before jokes

Resolve the promoted subject before choosing a gag:

- subject type/category;
- job-to-be-done and outcome;
- pain points/tradeoffs;
- differentiators;
- physical/sensory properties when relevant;
- usage ritual/emotional payoff;
- competitors, incumbents, substitutes, legacy/manual workarounds when useful.

The product can be a prop, material, gesture, route, transformation, tool, environment, consequence or final reveal rather than a mascot.

### 2. Reframe before optimize

Identify the **category default** competitors are optimizing, then test constraint deletion:

1. Why must the assumption exist?
2. What if it disappears?
3. What user outcome remains?
4. What new competition axis matters?

Prefer `old premise → deleted constraint → new axis` when it is more truthful, surprising and ownable than incremental feature comparison. Strategic hypotheses stay hypotheses until evidence supports them.

### Cultural mechanism mapping

**Borrow the mechanism, not the skin.** A hotspot is useful because audiences already understand a relationship, causal chain, ritual, transformation, conflict, reversal, chase, rescue, delivery grammar or other mechanism—not because it supplies a costume, famous-looking character, palette or catchphrase to paste around an ad.

For each selected hotspot extract:

1. recognition hook;
2. causal/relationship mechanism;
3. native visual grammar;
4. native dialogue/language rhythm;
5. for motion, native audio grammar.

Then map a real product pain point/differentiator into a functional role: route, key, antidote, obstruction-breaker, transformation, rule deletion, rescue action, tool, material, consequence or reveal. Every retained hotspot element must have a job in the causal chain.

The **product must change the story outcome** through a product truth or defensible metaphor. If another unrelated brand can replace it without changing the story logic, rebuild the concept. Prefer audience decoding order: **hotspot recognition → mapping → product consequence → punchline**.

### 4. Bridge search

Search bridges across shape/material, action/motion, role, function, emotion/ritual and language/symbol. The linkage should be understandable before explanation. A product becoming the action is stronger than a logo sitting beside the reference.

### 5. Format follows the idea

Choose the smallest form that makes the bridge land. Four-panel is only one option. Swipe reveal must add information frame by frame. Narrative video must preserve scene geography, identity and action continuity rather than substituting unrelated stills/hard cuts.

### 6. Medium follows the hotspot

- film/live action → original photorealistic cinematic grammar;
- animation → original animation-native 2D/3D/low-poly grammar;
- internet personalities/social phenomena → documentary/social-native realism with anonymous people unless rights-cleared assets exist;
- technology/software → contemporary tech/professional grammar;
- food/consumer goods → commercial product imagery or product-led metaphor;
- native memes → distribution grammar rebuilt with original assets.

Match medium and recognition cues, not protected production assets.

### 7. Distribution-native restraint

For hotspot/meme/brand-memory work, audience experience comes before landing-page mechanics.

- no in-asset URL/QR/app-store badge by default;
- benefits appear as story consequences before feature labels;
- final attribution stays light enough to remain a meme/scene rather than poster-shaped landing-page UI;
- motion-native ideas stay motion-native when action, dialogue, sound or timing carries recognition.

### 8. Anti-Polish / Controlled Badness

Hottop supports **low production feel + high comedy control** when roughness strengthens the native grammar. Cheap low-poly surfaces, stiff motion, blunt Foley, simple lighting/instrumentation and deadpan acting can be deliberate.

**Do not polish the badness away; make the badness precise.** Roughness never relaxes character continuity, scene geography, cause/effect, subtitle correctness, Mandarin intelligibility, comedy timing, product semantics, evidence/claim safety, rights safety or encoding integrity. Low production feel can be intentional; random failure cannot.

`roughness_score` is a routing variable, not product identity. Cinematic/premium/social-native/serious hotspots require presentable execution.

### 9. Comparison is optional; truth is not

Named competitor negatives must be evidence-backed limitations/tradeoffs, accurately scoped facts or unmistakably subjective satire. Never invent benchmarks, outages, prices, safety failures, quality defects or customer sentiment. When evidence is weak, use a generic proxy or attack the old assumption rather than a named rival.

### 10. References teach grammar, not pixels

Visual references are for composition, pacing, camera, reveal, product-photography and source-medium grammar—not pixel reproduction.

- provenance-rich public HTTP(S) first;
- ordinary third-party screenshots are analysis-only unless rights-cleared/public-domain;
- retain source/time/rights mode, abstract grammar and `what_not_to_copy`;
- do not use exact film frames, actor likenesses, official posters/characters, proprietary UI/trade dress, source footage or copyrighted soundtracks as generation targets without rights-cleared input.

Semantic visual memory is added only after a rights-aware corpus and retrieval benchmark justify it.

## Creative review gate

A concept is ready only if it passes:

1. instant comprehension;
2. natural linkage;
3. product centrality;
4. surprise/reframe;
5. ownability;
6. evidence safety;
7. original execution.

Contextual review (platform/style/goal/ambition/project-shape/hotspot-native/humor fit) ranks only concepts that already pass the hard gate. It cannot rescue a generic or unsafe concept.

## Adaptive guided intake

Hottop behaves like a creative director, not a configuration form. Resolve what the user already said, infer conservative defaults with provenance/confidence, and ask only unresolved questions that materially change the result. Typical budget: **0–3 questions**, usually zero or one.

Durable controls include campaign goal, platform, style, creative ambition, product visibility and optional audience. Output should be **platform-native** before rendering. Explicit user choices override inference. Project shape is a routing signal: consumer/food emphasizes sensory bridges; software/B2B emphasizes workflow pain/category-default deletion; entertainment follows source-medium grammar; fashion/beauty emphasizes form/material/style; services emphasize ritual/outcome/emotion; campaigns/ideas emphasize symbol/semantic bridges.

Revision controls should mutate only relevant dimensions instead of restarting product understanding.

## Core pipeline

1. Resolve interaction intent.
2. Resolve promotion semantics.
3. Discover comparisons when useful.
4. Analyze the supplied hotspot or discover fresh hotspots.
5. Extract recognition hook + causal/visual/dialogue/audio grammar.
6. Research visual references when useful, grammar-only.
7. Normalize evidence/reference records.
8. Reframe category defaults/deleted constraints.
9. Search bridges and assign the product a role that changes outcome.
10. Rank trend/mechanism/bridge quality.
11. Select form/platform/style/roughness dynamically.
12. Write beats, captions, dialogue, audio cues and punchlines.
13. Hard review then contextual ranking.
14. Guardrail claims/copyright/likeness/trademark/competitor framing.
15. Run fresh-generation preflight.
16. For motion choose the strongest admissible route, including image-first reference-conditioned recovery when justified, then `hottop.render.v2 → VideoProductionConfig → hottop.video-plan.v1 → generation → audio → compositor → encoder → media verification`.
17. Archive intent, provenance, evidence, hotspot mechanism, references, rejected assumptions, selected bridge, product role/outcome, format, reviews, prompts, risks and outcome evidence.

## Motion production doctrine

### Zero-cost first

`ZERO_COST_MODE=true` is the unattended target.

- no paid fallback, credits, overage, card enrollment or hidden billing;
- free capacity exhaustion bounded-retries, waits, fails or degrades to an explicitly deterministic route;
- multi-GB model downloads, GPU provisioning and large optional runtimes are operator-controlled;
- generated/deterministic shots pass quality + byte/provenance gates before composition;
- quality failure is never rebranded as Anti-Polish.

### Guaranteed software 3D baseline

Production v0.2 includes pure software low-poly 3D as a guaranteed zero-cost baseline when no GPU/model is available. It uses actual 3D geometry/projection/animation, emits playable MP4 shots, writes byte-bound provenance and is continuously production-smoke tested through dialogue/music/SFX → MoviePy → FFmpeg → final media verification.

This baseline is intentionally suitable for Controlled Badness and reproducible evidence. It is **not** the cinematic quality ceiling.

**Deterministic fallback must be story-explicit.** A software3d renderer may claim only story profiles it actually implements. Shot-mode rendering must derive story identity from the output workspace plan or an explicit supported profile, never from an unrelated current working directory. Unknown, blank or unsupported story topics and missing workspace plans fail closed; they must never silently reuse the cow template or another historical story merely to produce a playable MP4. Distinct checked-in story proofs must produce materially distinct world/character/prop staging, not only different captions.

### Generated-video routes

- **HF ZeroGPU** — optional free shared-GPU transport; bounded, quality-gated, never guaranteed.
- **Wan2.2** — permissive operator-owned local generation candidate where suitable hardware/models are supplied.
- **LightX2V** — maintained Apache-2.0 operator-owned inference framework for tested Wan2.2/local paths; Hottop requires local checkout/model/config preflight, offline execution, no auto-provisioning, shared quality gates and artifact provenance.
- **WanGP** — operator-managed interop route under its own license restrictions; do not vendor, auto-install or auto-download models.
- **Comfy API v2** — explicitly configured self-hosted/remote adapter with environment-only credentials, HTTPS/loopback boundaries, no token on output download and redirects disabled.
- **FramePack / FastVideo / LTX / H3 / SCAIL / LongCat / other candidates** — admission only after separate code/weights license, hardware, security, cost and measurable-quality review.

A permissive code repository does not automatically authorize its weights/model/data or hosted endpoint.

### Artifact and provenance integrity

Generated/deterministic footage is not trusted merely because a backend returned an MP4.

- validate decodability, duration/stream structure, motion/duplicate ratio and final codec/media constraints as relevant;
- bind accepted shot bytes to SHA-256 + size and re-verify immediately before composition;
- delete partial/rejected/failed outputs;
- bind benchmarked generated artifacts to the **actual generator candidate/source revision** when the runtime can prove it;
- **generator source revision, model/checkpoint revision, evaluator revision and output artifact bytes are separate provenance dimensions**;
- never substitute a reviewed registry pin for the source revision actually executed;
- never infer model/weights revision from framework source revision;
- bind model/checkpoint provenance only when the operator runtime exposes independently verifiable local metadata.

For LightX2V, evaluated artifacts record the actual local generator source revision: git HEAD for a real checkout, otherwise a source SHA-256 identity of the local inference entrypoint. Continuity evidence must match that artifact candidate/source provenance exactly.

### Character/reference continuity

Reference-conditioned generation uses local rights-safe inputs only (`generated-original` or `user-provided-rights-cleared`). Repeated subjects carry stable `subject_id`, role and identity-lock semantics; conflicts fail before GPU work.

Output-side continuity claims must bind evaluator evidence to:

1. exact planned reference bytes;
2. exact byte-bound plan shots carrying the same `reference.subject_id`;
3. **all** subject-bearing plan shots for every evaluated subject;
4. generated-artifact candidate/source provenance when available;
5. explicit evaluator identity/revision and fail-closed thresholds.

Partial cherry-picked shot coverage fails closed. Benchmark scope remains explicit: incidental/single-shot subjects are not automatically forced into cross-shot evaluation.

Input locks are constraints, not proof of generated visual identity. A route becomes identity-preserving only after real generated output passes the evidence contract.

### Image-first quality recovery

Image-first quality recovery is optional, not universal. Use it when direct video misses the chosen style/identity quality bar and a rights-safe approved keyframe/reference is likely to improve the route.

When supported by the selected backend, use the existing **reference-conditioned I2V** path rather than inventing a duplicate backend. The final result is still video, not a slideshow: meaningful motion, geography/identity/action, timing, audio, motion/duplicate gates, provenance and final media verification remain mandatory.

### Audio is first-class

Preserve `speaker` + `delivery`, `voice_profile`, `music_profile`, `sfx_profile` through render → plan → execution.

- guaranteed fallback: eSpeak Mandarin + original synthetic music + procedural Foley;
- CosyVoice3 and Qwen3-TTS CustomVoice are reviewed operator-owned local quality/benchmark candidates;
- cloning/reference-audio routes are rights-gated;
- never imitate copyrighted commercial soundtracks or clone a real person without rights-cleared authority;
- future adapters must preserve zero-cost, license and provenance boundaries.

### Composition/finalization

MoviePy is the default deterministic unattended compositor. Motion Canvas remains optional for advanced vector/interactive work. FFmpeg finalizes H.264/AAC/yuv420p/fast-start output and final-media verification. `video-run` is dry-run by default; only explicit `--execute` may spawn trusted configured stages after readiness passes.

**Mandarin/CJK subtitle readability is a fail-closed delivery boundary.** CJK captions must resolve a real locally available CJK-capable font before MoviePy composition. `HOTTOP_CAPTION_FONT` may point to an operator-provided local font; known installed system CJK fonts may be auto-detected. If no suitable local font exists, composition fails instead of rendering tofu/replacement glyphs. Normal `video-run` never auto-installs or vendors fonts; CI/production-smoke may explicitly provision a reviewed system font package.

## Autonomous operating mandate

Routine safe/reversible/evidence-backed repository decisions proceed without repetitive approval. The operator may research, branch, test, implement, update configs/docs/examples/skills, repair regressions/security issues, run CI, create/review/merge PRs, select zero-cost/open alternatives, and add missing skills/MCPs/plugins when materially useful and safely admitted.

Do not treat an hourly/scheduled run boundary as a work boundary. Continue through all currently unblocked safe work that materially advances the active milestone.

Pause only for materially higher-risk boundaries: destructive/irreversible actions, secret/credential changes/disclosure, paid actions/credits, legal commitments, sensitive external publication or similarly uncontainable consequences.

Autonomy never weakens evidence standards.

## Continuous ecosystem radar

Hottop is a living system. Every production cycle performs targeted freshness checks against the **current measured gap**, not generic popularity.

Track T2V/I2V/reference consistency, low-VRAM/local inference, verified free routes, image-first/reference conditioning, interpolation/restoration/upscaling, temporal consistency, Mandarin/multilingual TTS, original audio, orchestration/composition, QA, licenses and breaking security/runtime changes.

Current watchlist includes Wan2.2/WanGP, ModelTC/LightX2V, FramePack, FastVideo, LTX, MiniMax H3, SCAIL, LongCat, ComfyUI/Diffusers, RIFE, Real-ESRGAN, InfiniteTalk, CosyVoice, Qwen TTS and later measurably stronger candidates.

### Admission gate

Integrate only when applicable checks pass:

1. exact source/project identity and tested revision;
2. code license and model/weights/data license reviewed separately;
3. commercial/geographic/use restrictions understood;
4. true zero-cost or operator-owned execution, no hidden paid fallback;
5. practical hardware/runtime profile;
6. acceptable install/runtime/network/security behavior;
7. concrete measured Hottop gap;
8. testable/reversible narrow integration;
9. benchmark or production evidence showing value.

AGPL/incompatible code may teach architecture/behavior but is not copied into Hottop. Prefer narrow adapters over vendoring huge repositories. No auto-install of unreviewed code or hidden multi-GB download in CI/normal `video-run`.

When a candidate clears the gate, integrate the smallest useful registry/config/adapter/test/benchmark rather than stopping at a research note.

## Persistent project memory protocol

Long-running work must not depend on chat memory alone. `PROJECT.md` is the **living project charter** and `STATUS.md` is the short-lived execution snapshot.

### Context recovery

Recovery order:

1. `PROJECT.md`;
2. `STATUS.md`;
3. active reusable skills;
4. newest relevant spec/plan/decision/research record;
5. current `main`, open PRs, exact-head CI/production evidence;
6. targeted ecosystem freshness check for the current gap.

Do not ask the user to repeat stable direction that the repository can recover.

### Living updates

A **material direction change** must be challenged against current doctrine/evidence and classified as durable or experiment-specific. If durable, **update the charter** (`PROJECT.md`) and the relevant skill/spec in the same workstream, note the stale assumption it supersedes when useful, then update `STATUS.md`. Do not silently stack contradictory doctrine. Periodically compact stale duplication while preserving current canonical rules and the decision log.

### Chat generation source of truth

For Hottop-related generation in Chat, current GitHub state—not stale chat memory—is the source of truth. Recover current project/status/skills/examples/config/rights/provenance rules, then perform the mandatory fresh hotspot pass/preflight for the new asset.

## Repository operating rules

- feature branches + PRs for normal changes;
- safe routine work proceeds autonomously;
- keep `PROJECT.md`, `STATUS.md`, relevant specs/plans/skills current;
- existing-skill first: do not add duplicate capability when an installed skill/MCP/plugin already covers the task;
- prefer narrow adapters over vendoring large upstreams;
- keep credentials/cookies/API keys out of Git/CI logs;
- respect site terms/access/rate limits;
- factual comparisons require evidence;
- visual references are analysis evidence, not automatic generation source material;
- record external capability provenance/license/runtime/cost in durable repository state when practical.

## Non-goals

- no permanent InkClawAgent/AI-tool/mascot/character/four-panel requirement;
- no requirement that the product is personified as winner;
- no copying protected film frames, actor likenesses, official characters/posters, logos/trade dress, proprietary UI, source footage/soundtrack or finished ads without rights-cleared input;
- no unsupported superiority claims;
- no mandatory vector DB/browser-agent/GPU stack before a measured need;
- no static mandatory questionnaire;
- no assumption that more polish is always better;
- no assumption Anti-Polish fits every hotspot;
- no dependency/model integration merely because it is popular/open;
- no identity-preservation claim from prompt/reference locks alone.

## Durable output contract

A mature package/archive should preserve enough to reproduce and audit the creative/production decision:

- intent + inference provenance;
- promotion semantics/comparison context;
- hotspot + timestamp + evidence;
- recognition/causal/visual/dialogue/audio grammar;
- product role + story-outcome change;
- reference manifest + rights/provenance where used;
- category default/deleted constraint/new axis;
- bridge + expression/platform/style/roughness;
- motion/continuity/CTA policy;
- beats/captions/dialogue/punchlines;
- hard/contextual reviews;
- prompts/exclusions/risk flags/claim status;
- `hottop.render.v2`;
- for motion: route choice + `hottop.video-plan.v1`, ordered shots, identity/reference data, role-aware audio, backend specs, **generator source provenance, model provenance when independently verifiable, evaluator provenance, artifact hashes**, final encoding/media verification and outcome evidence.

## Decision log

- **2026-08-25 — Deterministic story routing becomes fail-closed.** Artifact inspection proved that a correct Odyssey plan could still render the cow/workroom world because shot-mode software3d inferred story identity from the wrong working directory and silently defaulted to cow. PR #39 fixed the production workspace lookup; the follow-up hardening removes residual `missing/unknown → cow` fallback. Hottop now rejects unsupported deterministic stories rather than producing a valid but semantically false MP4. Distinct story proofs must remain materially distinct visual worlds.
- **2026-08-25 — CJK subtitle rendering becomes fail-closed.** Direct inspection of production-smoke artifacts found Mandarin captions rendered as tofu because MoviePy fell back to a non-CJK Pillow font even though codec/media gates passed. Hottop now requires a real local CJK-capable caption font when CJK text is present; missing font is a production failure, not an acceptable encoding success. Normal execution does not auto-install fonts.
- **2026-08-25 — Generator source provenance becomes part of continuity evidence.** Byte-valid reference/shot evidence is insufficient if a run can be relabelled as another generator candidate/version. Evaluated LightX2V artifacts now bind the actual local generator source revision and continuity evidence must match it. Framework source revision, model/checkpoint revision, evaluator revision and output bytes remain separate provenance dimensions. This supersedes the weaker self-reported benchmark `candidate_revision` interpretation and explicitly forbids treating a reviewed registry pin as proof of what code actually ran.
- **2026-08-25 — Continuity evidence becomes subject-bound and complete within evaluated scope.** Output-side identity claims bind exact reference bytes + byte-bound generated artifacts to the same `subject_id`; every subject-bearing plan shot for an evaluated subject must be covered. This supersedes global-manifest/subset checking while avoiding an overbroad requirement for incidental single-shot subjects.
- **2026-08-25 — Hotspot mechanism mapping becomes canonical; image-first is quality recovery, not a template.** Product must take a functional role that changes the story outcome. Image-first reference conditioning is used only when it improves a weak direct-video route; slideshows/stills do not count as successful video.
- **2026-08-25 — Fresh hotspot research becomes a mandatory generation entry gate.** Every new image/video request re-resolves subject, live hotspot context, style/medium/format and must pass generation preflight; recent historical creative is not silently reused as default.
- **2026-08-25 — GitHub becomes Chat generation source of truth; existing capability wins over duplicate installation.** Recover current repository doctrine/status/skills/configs before Hottop generation; add new skills/MCPs/plugins only for concrete uncovered gaps.
- **2026-08-25 — Autonomous operation + continuous ecosystem radar become canonical.** Routine reversible repository work and evidence-backed integration proceed without repetitive approval; targeted upstream scanning is part of production, not a reporting chore.
- **2026-08-25 — Software 3D becomes the guaranteed zero-cost motion baseline, not the quality ceiling.** Real software 3D motion + audio + composition + verified MP4 stays available without GPU/model download while cinematic routes continue improving.
- **2026-08-24 — Zero-cost hybrid video becomes the unattended default.** Free shared GPU/operator compute for high-value shots, deterministic local work for the rest, bounded retries, quality gates, no paid fallback.
- **2026-08-24 — Video roughness becomes style-routed and audio becomes first-class.** Voice/original music/SFX are production-contract fields; cinematic quality and deliberate roughness are routed separately.
- **2026-08-24 — Anti-Polish / Controlled Badness becomes first-class selectable strategy.** Deliberate roughness is allowed only when it strengthens native grammar and never relaxes continuity/timing/subtitle/claim/rights/media requirements.
- **2026-08-24 — Social creative is ad-light by default; motion-native ideas stay motion-native.** URLs/QR CTAs are omitted by default for hotspot/meme/brand-memory assets, and dynamic ideas are not flattened into static posters for convenience.

## Reusable skills

- `skills/brand-metaphor-creative/SKILL.md` — intent, reframing, mechanism-first hotspot mapping, bridge search, format/medium routing, Controlled Badness, image-first recovery and creative review.
- `skills/creative-reference-research/SKILL.md` — provenance-first grammar-only visual-reference research.
- `skills/hottop-meme/SKILL.md` — supplied/unspecified hotspot acquisition/analysis, evidence-aware comparisons, medium routing and four-panel execution when selected.

Use existing suitable capabilities first; add external/operator skills/MCPs/plugins only after a concrete gap and admission review.

## Current milestone

**Production v0.2 — repeatable real video output**

Acceptance target: playable vertical shorts generated from checked-in Hottop render/config sources with coherent moving imagery, stable original subject identity, continuous geography/action, intelligible Mandarin dialogue, original BGM/SFX, natural transitions, product benefit emerging through story, quality/provenance gates and H.264/AAC-compatible final delivery.

Priority order:

1. produce/verify end-to-end config → moving shots → audio → MoviePy → FFmpeg → final MP4 evidence;
2. keep software3d guaranteed zero-cost while benchmarking stronger operator-owned/open reference-conditioned routes;
3. improve output-side identity/reference evidence and reject failures before composition;
4. improve Mandarin dialogue through reviewed local Qwen3-TTS/CosyVoice routes while preserving rights gates/eSpeak fallback;
5. archive render/config, generator/model/evaluator provenance, artifact hashes and final-media verification;
6. turn successful runs into reusable production baselines instead of accumulating unproven provider abstraction.

## Session recovery

1. Read `PROJECT.md`.
2. Read `STATUS.md`.
3. Read relevant reusable skills.
4. Read newest relevant spec/plan/decision/research record.
5. Inspect current `main`, open PRs and exact-head CI/production-smoke.
6. Perform targeted ecosystem freshness check for the current Production gap.
7. For a new image/video generation, perform the fresh hotspot pass or supplied-hotspot mechanism analysis before generation.
8. Continue the highest-value safe action autonomously; do not stop for routine approval or a scheduled-run boundary.
