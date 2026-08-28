# Hottop — Persistent Project Brief

> Read this file first whenever context is missing or a new session continues the project. `PROJECT.md` is durable doctrine; `STATUS.md` is the short-lived execution snapshot.

## Mission

Build a durable **hot-topic brand creative system** for marketing any user-selected brand, product, service, feature, campaign, person, idea, keyword or tool. InkClawAgent is one example, not a permanent assumption.

Hottop turns current film, entertainment, animation, technology, internet and culture into original promotional concepts that make a product's value visually memorable. Output format is flexible: single visual metaphor, swipe-reveal, four-panel, faux still/poster, split old-vs-new, short cinematic video, GIF/animation or another compact social form. **Not every concept must be four-panel.** Not every output is Anti-Polish. The promoted subject does not have to be a hero character.

The durable goal is not `hot character + logo`. Find a natural bridge between the promoted subject and a recognizable cultural mechanism, then make the subject part of the action, prop, transformation, role, material, route, environment or reveal.

## Mandatory fresh-generation entry gate

Every new image or video generation request is a fresh creative run, including Chat generation.

Before final generation:

1. recover `PROJECT.md`, `STATUS.md` and relevant checked-in skills/configs;
2. resolve the promoted subject from the current request/current facts;
3. analyze the supplied hotspot, or perform live current-hotspot research if none was supplied;
4. retain source provenance plus observation/publication timing;
5. choose style, medium and format from the current product↔hotspot bridge and source-medium grammar, not a historical template;
6. construct `hottop.generation-preflight.v1` and require `evaluate_generation_preflight(...)` / `hottop generation-preflight` to return `ready=true`.

Default freshness is fail-closed: live research should have been observed within **6 hours**; when a trustworthy publication timestamp exists, the selected hotspot should normally be within **7 days**. Unknown publication time can pass only with fresh observation evidence and no invented recency claim.

**Historical examples are not defaults.** Historical cow/snake/Odyssey stories, four-panel layouts, Anti-Polish, software3d, cinematic realism and prior successful assets teach grammar only. They are not automatic defaults.

## Creative doctrine

### Semantics before jokes

Resolve category, job-to-be-done/outcome, pain/tradeoff, differentiator, physical/sensory properties when relevant, usage ritual/emotional payoff and alternatives before choosing the gag. The product may be a prop, material, gesture, route, transformation, tool, environment, consequence or reveal rather than a mascot.

### Reframe before optimize

Identify the **category default** competitors are optimizing, then test constraint deletion:

1. why must the assumption exist?
2. what if it disappears?
3. what user outcome remains?
4. what new competition axis matters?

Prefer `old premise → deleted constraint → new axis` when it is more truthful, surprising and ownable than incremental comparison. Strategic hypotheses remain hypotheses until evidence supports them.

### Cultural mechanism mapping

**Borrow the mechanism, not the skin.** For each selected hotspot extract:

1. recognition hook;
2. causal/relationship mechanism;
3. native visual grammar;
4. native dialogue/language rhythm;
5. for motion, native audio grammar.

Then map a real product truth into a functional role: route, key, antidote, obstruction-breaker, transformation, rule deletion, rescue action, tool, material, consequence or reveal. Every retained hotspot element must have a job in the causal chain.

The **product must change the story outcome** through a product truth or defensible metaphor. If an unrelated brand can replace it without changing the logic, rebuild the concept. Prefer decoding order: **hotspot recognition → mapping → product consequence → punchline**.

### Bridge search

Search shape/material, action/motion, role, function, emotion/ritual and language/symbol bridges. The link should be understandable before explanation. Product-as-action is stronger than product-beside-reference.

### Format and medium follow the idea

Choose the smallest form that makes the bridge land. Four-panel is one option, not the default. Swipe-reveal must add information frame by frame. Narrative video preserves geography, identity and action continuity rather than substituting unrelated stills/hard cuts.

Medium follows the hotspot:

- film/live action → original cinematic grammar;
- animation → original animation-native grammar;
- internet personalities/social phenomena → documentary/social-native realism with anonymous people unless rights-cleared assets exist;
- technology/software → contemporary tech/professional grammar;
- food/consumer goods → commercial product imagery/product-led metaphor;
- native memes → distribution grammar rebuilt with original assets.

Match medium/recognition cues, not protected production assets.

### Distribution-native restraint

For hotspot/meme/brand-memory work, audience experience comes before landing-page mechanics.

- no in-asset URL/QR/app-store badge by default;
- benefits appear as story consequences before feature labels;
- final attribution stays light enough to remain a meme/scene;
- motion-native ideas stay motion-native when action/dialogue/sound/timing carries recognition.

### Anti-Polish / Controlled Badness

Hottop supports **low production feel + high comedy control** when roughness strengthens native grammar. Cheap low-poly surfaces, stiff motion, blunt Foley, simple lighting/instrumentation and deadpan acting may be deliberate.

**Do not polish the badness away; make the badness precise.** Roughness never relaxes character continuity, geography, cause/effect, subtitle correctness, Mandarin intelligibility, comedy timing, product semantics, evidence/claim safety, rights safety or encoding integrity. Low production feel can be intentional; random failure cannot. `roughness_score` is a routing variable, not product identity.

### Comparison is optional; truth is not

Named competitor negatives must be evidence-backed limitations/tradeoffs, accurately scoped facts or unmistakably subjective satire. Never invent benchmarks, outages, prices, safety failures, quality defects or customer sentiment. When evidence is weak, use a generic proxy or attack the old assumption itself.

### References teach grammar, not pixels

Visual references teach composition, pacing, camera, reveal, product-photography and source-medium grammar—not pixel reproduction.

- provenance-rich public HTTP(S) first;
- ordinary third-party screenshots are analysis-only unless rights-cleared/public-domain;
- retain source/time/rights mode, abstract grammar and `what_not_to_copy`;
- do not use exact film frames, actor likenesses, official posters/characters, proprietary UI/trade dress, source footage or copyrighted soundtracks as generation targets without rights-cleared input.

## Creative reference memory

Hottop learns from prior work through **retrieval + few-shot/preference memory**, not template reuse and not reinforcement learning.

Canonical memory artifacts:

- `integrations/creative-reference-library.yml`;
- `src/hottop/creative_memory.py`;
- `src/hottop/creative_memory_cli.py`;
- `skills/creative-reference-memory/SKILL.md`;
- `docs/creative/creative-reference-memory.md`.

Fresh hotspot evidence remains authoritative. Retrieval happens **after** current hotspot/mechanism analysis and **before** ideation when prior cases can help. Retrieve similar mechanisms, native grammar, product roles and negative patterns; use positive cases as reasoning exemplars and negative cases as guardrails. Never silently reuse a past layout, character, scene, punchline or visual template.

Preserve durable user feedback and real platform-performance signals when available, but never invent ratings or scores. Historical generated/original/user-authorized assets may later use an approved Git LFS/object-store path; ordinary third-party copyrighted media remains metadata/analysis only by default.

Training work (SFT/DPO/reward model/RL) is deferred until the library becomes a sufficiently large, clean, rights-safe, labeled dataset with measured value. The current memory system must not be described as RL.

## Creative review gate

A concept is ready only if it passes:

1. instant comprehension;
2. natural linkage;
3. product centrality;
4. surprise/reframe;
5. ownability;
6. evidence safety;
7. original execution.

**Contextual review** (platform/style/goal/ambition/project-shape/hotspot-native/humor fit) ranks only concepts that already pass the hard gate. It cannot rescue a generic or unsafe concept.

## Adaptive guided intake

Hottop behaves like a creative director, not a static questionnaire. Resolve what the user already said, infer conservative defaults with provenance/confidence and ask only questions that materially change the output. Typical budget: **0–3 questions**, usually zero or one. Explicit user choices override inference.

The durable interaction controls include campaign goal, platform, style, **creative ambition**, **product visibility** and optional audience. Output should be **platform-native** before rendering, and **project-shape** is a routing signal rather than a fixed meme grammar.

## Core pipeline

1. Resolve interaction intent.
2. Resolve promotion semantics.
3. Discover comparisons when useful.
4. Analyze the supplied hotspot or discover fresh hotspots.
5. Extract recognition hook + causal/visual/dialogue/audio grammar.
6. Research visual references when useful, grammar-only.
7. Normalize evidence/reference records.
8. Retrieve relevant creative-memory mechanisms/grammars/guardrails when useful; fresh hotspot evidence stays authoritative.
9. Reframe category defaults/deleted constraints.
10. Search bridges and assign the product a role that changes outcome.
11. Rank trend/mechanism/bridge quality.
12. Select form/platform/style/roughness dynamically.
13. Write beats, captions, dialogue, audio cues and punchlines.
14. Hard review then contextual ranking.
15. Guardrail claims/copyright/likeness/trademark/competitor framing.
16. Run fresh-generation preflight.
17. For motion choose the strongest admissible route, including image-first reference-conditioned recovery when justified, then `hottop.render.v2 → VideoProductionConfig → hottop.video-plan.v1 → generation → audio → compositor → encoder → media verification`.
18. Archive intent, provenance, evidence, hotspot mechanism, references, retrieved-memory influence/guardrails when material, rejected assumptions, selected bridge, product role/outcome, format, reviews, prompts, risks and outcome evidence.

## Motion production doctrine

### Zero-cost first

`ZERO_COST_MODE=true` is the unattended target.

- no paid fallback, credits, overage, card enrollment or hidden billing;
- free capacity exhaustion bounded-retries, waits, fails or degrades to an explicitly deterministic route;
- multi-GB model downloads, GPU provisioning and large optional runtimes are operator-controlled;
- generated/deterministic shots pass a **quality gate** plus byte/provenance gates before composition;
- quality failure is never rebranded as Anti-Polish.

### Guaranteed software 3D baseline

Production v0.2 includes pure software low-poly 3D as a guaranteed zero-cost baseline when no GPU/model is available. It uses actual 3D geometry/projection/animation, emits playable MP4 shots, writes byte-bound provenance and is production-smoke tested through dialogue/music/SFX → MoviePy → FFmpeg → final-media verification. It is suitable for Controlled Badness and reproducible evidence, **not the cinematic quality ceiling**.

**Repeatability is contract-first, not hash-first.** Success means bound source/plan/provenance plus accepted visual/audio/media/integrity gates reproduce. Byte equality is useful scoped evidence only when actually observed under bound runtime identity. Different hashes are not automatically a regression when accepted production contracts still pass.

**Deterministic fallback is story-explicit.** Software3d may claim only implemented story profiles. Shot-mode derives story identity from the output-workspace plan. Missing/blank/unknown/unsupported topics fail closed and never silently reuse another historical story.

**Mobile-first framing includes subject scale and placement.** 9:16 evidence checks readable principal-subject placement/scale while preserving subtitle safe areas and geography; thresholds are measured/style/backend specific.

**Mobile subtitle quality includes line breaks.** CJK captions require a real local CJK-capable font. Short mixed-script captions must not be forced into one-character orphan lines when a readable natural-width line fits. Normal `video-run` never auto-installs or vendors fonts.

### Generated-video routes

- **HF ZeroGPU** — optional free shared-GPU transport; bounded, quality-gated, never guaranteed.
- **Wan2.2** — operator-owned local generation candidate where suitable hardware/models are supplied.
- **LightX2V** — maintained Apache-2.0 operator-owned inference framework for tested Wan2.2/local paths; local checkout/model/config preflight, offline execution, no auto-provisioning, shared quality/provenance gates.
- **WanGP** — operator-managed interop route under its own license restrictions; do not vendor, auto-install or auto-download models.
- **Comfy API v2** — explicitly configured self-hosted/remote adapter with environment-only credentials, HTTPS/loopback boundaries, no token on output download and redirects disabled.
- **FramePack / FastVideo / LTX / H3 / SCAIL / LongCat / Stand-In / Memento / other candidates** — admit only after separate code/weights/data license, hardware, security, cost and measurable-quality review.

A permissive code repository does not automatically authorize its weights/model/data or hosted endpoint.

### Artifact and provenance integrity

Generated/deterministic footage is not trusted merely because a backend returned an MP4.

- validate decodability, duration/stream structure, motion/duplicate ratio and final codec/media constraints as relevant;
- bind accepted shot bytes to SHA-256 + size and re-verify immediately before composition;
- delete partial/rejected/failed outputs;
- bind benchmarked artifacts to the **actual generator candidate/source revision** when runtime can prove it;
- generator source revision, model/checkpoint revision, evaluator revision and output bytes are separate provenance dimensions;
- never substitute a reviewed registry pin for what code actually ran;
- never infer model/weights revision from framework source revision;
- bind model/checkpoint provenance only when independently verifiable local metadata exists.

For LightX2V, evaluated artifacts record actual local generator source identity: git HEAD for a real checkout, otherwise source SHA-256 of the local inference entrypoint. Continuity evidence must match artifact candidate/source provenance exactly.

### Character/reference continuity

Reference-conditioned generation uses local rights-safe inputs only (`generated-original` or `user-provided-rights-cleared`). Repeated subjects carry stable `subject_id`, role and identity-lock semantics; conflicts fail before GPU work.

Output-side continuity claims bind evaluator evidence to:

1. exact planned reference bytes;
2. exact byte-bound plan shots carrying the same `reference.subject_id`;
3. **all** subject-bearing plan shots for every evaluated subject;
4. generated-artifact candidate/source provenance when available;
5. explicit evaluator identity/revision and fail-closed thresholds.

Partial cherry-picked coverage fails closed. Input locks are constraints, not proof of generated identity. A route becomes identity-preserving only after real generated output passes the evidence contract.

**Identity fidelity and motion fidelity are separate evidence dimensions.** A subject can remain recognizable while the requested motion is incorrect, frozen or degenerate; strong motion can also coexist with subject drift. When a route claims to control both, benchmark and persist both dimensions independently before describing the result as successful subject-and-motion continuity.

### Image-first quality recovery

Use image-first recovery only when **direct video** misses the selected style/identity bar and a rights-safe accepted keyframe/reference can improve the route. Reuse existing **reference-conditioned I2V** rather than inventing a duplicate backend. Final output must still contain meaningful motion and pass continuity, audio, motion/duplicate, provenance and final-media gates; it is **not a slideshow**. A still/pan/zoom/slideshow is not successful video.

### Audio is first-class

Preserve `speaker + delivery`, `voice_profile`, `music_profile`, `sfx_profile` through render → plan → execution.

- guaranteed fallback: eSpeak-family Mandarin + original synthetic music + procedural Foley;
- recurring eSpeak-family characters use stable bounded deterministic pitch and `delivery` maps to bounded cadence around configured base rate; this is purposeful low-fidelity differentiation, not neural/natural-acting or collision-free speaker identity;
- **dialogue input integrity fails closed before TTS routing:** `AudioCue.text` is trimmed/nonblank, and `kind=dialogue` must contain at least one Unicode letter or number; punctuation/symbol-only text may remain valid for SFX/Foley descriptions but never consumes speech runtime as dialogue;
- Qwen3-TTS CustomVoice and CosyVoice3 are operator-owned local benchmark candidates;
- neural-TTS integrity is fail-closed against actual serialized audio: model samples must be non-empty and finite, then the exact int16 PCM destined for WAV must contain at least one non-zero sample before any WAV/temp-file creation;
- Qwen role-aware Production is checkpoint-capability gated: current reviewed 0.6B CustomVoice does not preserve `instruct`; current 1.7B is the admitted delivery-controlled candidate;
- bounded Qwen dialogue uses a duration-derived generation token ceiling as resource protection, while exact produced PCM duration remains the authoritative slot-fit gate;
- operator neural-TTS benchmark evidence binds serving topology, execution-shape/cache policy, hardware/runtime identity and cold-vs-warmed repeated trial state; throughput/latency gains never stand in for Mandarin intelligibility, delivery or naturalness evidence;
- preset-speaker/output publication rights are separate from source/model licensing;
- voice cloning/reference-audio is rights-gated;
- never imitate copyrighted commercial soundtracks or clone a real person without rights-cleared authority.

### Composition/finalization

MoviePy is the deterministic unattended **headless** compositor. Motion Canvas remains optional for advanced vector/interactive work. FFmpeg finalizes H.264/AAC/yuv420p/fast-start output and final-media verification. `video-run` is dry-run by default; only explicit `--execute` may spawn trusted configured stages after readiness passes. Runtime never silently installs packages, downloads models, provisions GPU, enables paid services or fetches protected source footage.

## Autonomous operating mandate

Routine safe/reversible/evidence-backed repository decisions proceed without repetitive approval. Research, branches, tests, implementation, configs/docs/examples/skills, regression/security repair, CI, PR lifecycle, zero-cost/open alternative selection and missing capability admission proceed autonomously when safe.

Do not treat an hourly/scheduled run boundary as a work boundary. Continue all currently unblocked safe work that materially advances the milestone.

Pause only for materially higher-risk boundaries: destructive/irreversible action, secret/credential changes/disclosure, paid actions/credits, legal commitments, sensitive external publication or similarly uncontainable consequences. Autonomy never weakens evidence standards.

## Continuous ecosystem radar

Every production cycle performs targeted freshness checks against the **current measured gap**, not generic popularity.

Track T2V/I2V/reference consistency, low-VRAM/local inference, verified free routes, image-first/reference conditioning, interpolation/restoration/upscaling, temporal consistency, Mandarin/multilingual TTS, original audio, orchestration/composition, QA, licenses and breaking security/runtime changes.

Current watchlist includes Wan2.2/WanGP, ModelTC/LightX2V, FramePack, FastVideo, LTX, MiniMax H3, SCAIL, LongCat, Stand-In, Memento, ComfyUI/Diffusers, RIFE, Real-ESRGAN, InfiniteTalk, CosyVoice, Qwen TTS and later measurably stronger candidates.

### Admission gate

Integrate only when applicable checks pass:

1. exact source/project identity and tested revision;
2. code license and model/weights/data license reviewed separately;
3. commercial/geographic/use restrictions understood;
4. true zero-cost/operator-owned execution, no hidden paid fallback;
5. practical hardware/runtime profile;
6. acceptable install/runtime/network/security behavior;
7. concrete measured Hottop gap;
8. testable/reversible narrow integration;
9. benchmark/production evidence showing value.

AGPL/incompatible code may teach architecture/behavior but is not copied into Hottop. Prefer narrow adapters over vendoring huge repositories. No auto-install of unreviewed code or hidden multi-GB downloads in CI/normal `video-run`. When a candidate clears the gate, integrate the smallest useful capability rather than stopping at a research note.

## Persistent project memory protocol

Long-running work must not depend on chat memory. `PROJECT.md` is the **living project charter**; `STATUS.md` is the execution snapshot.

### Context recovery

Recovery order:

1. `PROJECT.md`;
2. `STATUS.md`;
3. active reusable skills;
4. newest relevant spec/plan/decision/research record;
5. current `main`, open PRs and exact-head CI/production evidence;
6. targeted ecosystem freshness check for the current gap.

Do not ask the user to repeat stable direction recoverable from the repository.

A **material direction change** must be challenged against doctrine/evidence and classified durable vs experiment-specific. If durable, **update the charter** and relevant skill/spec in the same workstream, note the stale assumption it supersedes when useful, then update `STATUS.md`. Do not silently stack contradictory doctrine. Periodically compact stale duplication while preserving current canonical rules and decision log.

For Hottop-related generation in Chat, current GitHub state—not stale chat memory—is the source of truth. Recover current doctrine/status/skills/examples/config/rights/provenance, then perform the mandatory fresh hotspot pass/preflight.

## Repository operating rules

- feature branches + PRs for normal changes;
- keep `PROJECT.md`, `STATUS.md`, relevant specs/plans/skills current;
- existing suitable capability wins over duplicate installation;
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
- no mandatory vector DB/browser-agent/GPU stack before measured need;
- no static mandatory questionnaire;
- no assumption more polish is always better;
- no assumption Anti-Polish fits every hotspot;
- no dependency/model integration merely because it is popular/open;
- no identity-preservation claim from prompt/reference locks alone;
- no claim that creative reference retrieval is RL or permission to reuse prior visual templates.

## Durable output contract

A mature package/archive preserves enough to reproduce/audit the creative and production decision:

- intent + inference provenance;
- promotion semantics/comparison context;
- hotspot + timestamp + evidence;
- recognition/causal/visual/dialogue/audio grammar;
- product role + story-outcome change;
- reference manifest + rights/provenance;
- retrieved creative-memory mechanisms/guardrails when material, without copied templates;
- category default/deleted constraint/new axis;
- bridge + expression/platform/style/roughness;
- motion/continuity/CTA policy;
- beats/captions/dialogue/punchlines;
- hard/contextual reviews;
- prompts/exclusions/risk flags/claim status;
- `hottop.render.v2`;
- for motion: route choice + `hottop.video-plan.v1`, ordered shots, identity/reference data, role-aware audio, backend specs, generator/model/evaluator provenance, artifact hashes, final encoding/media verification and outcome evidence.

## Decision log

- **2026-08-28 — Dialogue TTS input integrity is semantic and fail-closed before runtime.** Audio cue text is normalized/nonblank at the plan boundary; dialogue additionally requires at least one Unicode letter or number so punctuation/symbol-only requests never consume eSpeak/Qwen/CosyVoice speech runtime. This input gate is independent of, and does not replace, Qwen token ceilings, produced-PCM duration checks or final audio integrity gates.
- **2026-08-28 — Operator neural-TTS benchmark provenance binds topology, execution shape and trial state.** Same model/checkpoint can show materially different throughput under single-instance versus same-card multi-replica/MPS topology, and cache/kernel execution shape can produce different same-seed waveforms. Future operator Qwen benchmarks therefore bind topology/cache/deterministic policy, separate cold-first-use from warmed repeated trials, and keep throughput/latency evidence separate from Mandarin quality.
- **2026-08-28 — Identity fidelity and motion fidelity become separate continuity evidence dimensions.** A recognizable subject with wrong/frozen/degenerate motion is not a successful motion-conditioned result, while strong motion cannot substitute for subject identity. Routes that claim both controls must persist and pass both dimensions independently before promotion.
- **2026-08-27 — Creative reference memory becomes canonical retrieval/preference memory, not template reuse or RL.** Successful and failed Hottop work may be retrieved for causal mechanism, native visual/dialogue/audio grammar, product-role logic, user feedback, promotion lessons, platform packaging and negative guardrails. Fresh current hotspot evidence remains authoritative; retrieval happens after current hotspot analysis and before ideation when useful. Past images/layouts/characters/scenes/punchlines are not default templates. Training work is deferred until a clean rights-safe labeled corpus and measured value justify it. This supersedes the weaker state where reusable creative lessons lived only in examples/chat/decision docs instead of the canonical charter.
- **2026-08-27 — Neural-TTS silence is judged on serialized PCM, not only model-returned float samples.** Non-zero sub-LSB floats can quantize to int16 digital silence. Qwen3-TTS/CosyVoice3 quantize first and reject all-zero PCM before WAV/temp-file creation; broad RMS/VAD remains separate.
- **2026-08-27 — Neural-TTS waveform integrity is non-empty + finite + serialized-PCM non-silent before serialization.** Model return is not production success; duration, intelligibility, delivery and final-media checks remain separate.
- **2026-08-26 — Production repeatability is quality-contract-first; byte equality is scoped evidence.** Reproducible visual/audio/media/integrity contracts plus bound source/provenance/runtime identity are authoritative; universal bitwise determinism is not required.
- **2026-08-26 — Guaranteed local speech fallback operationalizes role/delivery when safe controls exist.** Stable bounded pitch + cadence make preserved role/delivery metadata operational without claiming neural/natural identity.
- **2026-08-26 — Mobile subtitle readability includes line-break quality.** Safe-area containment alone is insufficient; avoid one-character orphan lines when readable single-line layout fits.
- **2026-08-26 — Qwen delivery control is checkpoint-capability gated.** Do not infer `instruct` support from API surface; current reviewed 0.6B and 1.7B capabilities remain distinct.
- **2026-08-26 — Mobile-first framing requires readable principal-subject scale and placement.** Thresholds are measured/style/backend specific.
- **2026-08-25 — Deterministic story routing is fail-closed.** Unsupported/missing stories never silently reuse another historical template.
- **2026-08-25 — CJK subtitle rendering is fail-closed.** CJK text requires a real local CJK-capable font.
- **2026-08-25 — Generator source provenance is part of continuity evidence.** Actual executed source, model/checkpoint when independently verifiable, evaluator revision and output bytes are separate dimensions.
- **2026-08-25 — Continuity evidence is subject-bound and complete within evaluated scope.** No cherry-picked shot subset can prove cross-shot identity.
- **2026-08-25 — Hotspot mechanism mapping is canonical; image-first is quality recovery, not a template.** Product changes the story outcome; slideshows do not count as successful video.
- **2026-08-25 — Fresh hotspot research is a mandatory generation gate.** Historical creative never silently becomes the new default.
- **2026-08-25 — GitHub is Chat generation source of truth; existing capability wins over duplicate installation.**
- **2026-08-25 — Autonomous operation + continuous ecosystem radar are canonical.**
- **2026-08-25 — Software 3D is the guaranteed zero-cost motion baseline, not the quality ceiling.**
- **2026-08-24 — Zero-cost hybrid video is the unattended default.**
- **2026-08-24 — Video roughness is style-routed and audio is first-class.**
- **2026-08-24 — Anti-Polish / Controlled Badness is first-class selectable strategy.**
- **2026-08-24 — Social creative is ad-light by default; motion-native ideas stay motion-native.**

## Reusable skills

- `skills/brand-metaphor-creative/SKILL.md` — intent, reframing, mechanism-first hotspot mapping, bridge search, format/medium routing, Controlled Badness, image-first recovery and creative review.
- `skills/creative-reference-research/SKILL.md` — provenance-first grammar-only visual-reference research.
- `skills/creative-reference-memory/SKILL.md` — prior success/failure retrieval, user-feedback/preference memory, negative guardrails and no-template/no-RL reuse rules.
- `skills/hottop-meme/SKILL.md` — hotspot acquisition/analysis, evidence-aware comparisons, medium routing and four-panel execution when selected.

Use existing suitable capabilities first; add external/operator skills/MCPs/plugins only after a concrete gap and admission review.

## Current milestone

**Production v0.2 — repeatable real video output**

Acceptance target: playable vertical shorts generated from checked-in render/config sources with coherent moving imagery, stable original subject identity, continuous geography/action, intelligible Mandarin dialogue, original BGM/SFX, natural transitions, product benefit emerging through story, quality/provenance gates and H.264/AAC-compatible final delivery.

Priority order:

1. produce/verify end-to-end config → moving shots → audio → MoviePy → FFmpeg → final MP4 evidence;
2. keep software3d guaranteed zero-cost while benchmarking stronger operator-owned/open reference-conditioned routes;
3. improve output-side identity/reference evidence and reject failures before composition;
4. improve Mandarin dialogue through reviewed local Qwen3-TTS/CosyVoice routes while preserving rights gates/eSpeak fallback;
5. archive render/config, generator/model/evaluator provenance, artifact hashes and final-media verification;
6. turn successful runs into reusable production baselines and creative-memory lessons instead of accumulating unproven provider abstraction.

## Session recovery

1. Read `PROJECT.md`.
2. Read `STATUS.md`.
3. Read relevant reusable skills, including `creative-reference-memory` when prior Hottop cases can help.
4. Read the newest relevant spec/plan or decision/research record.
5. Inspect current `main`, open PRs and exact-head CI/production-smoke.
6. Perform targeted ecosystem freshness checks for the current measured Production gap.
7. For new creative generation, perform fresh/supplied-hotspot mechanism analysis before any memory retrieval or generation.
8. Continue the highest-value safe action autonomously; do not stop for routine approval or a scheduled-run boundary.