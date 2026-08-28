# Hottop Status

Last updated: 2026-08-28
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is a short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

PR #161 `Bind motion fidelity to requested plan actions` exact head `12421f4da397bf945c811fa5475f693c0870e156` passed **CI #1976**, **production-smoke #207** and **cinematic-delivery-smoke #74**, had no review threads and was mergeable. It was squash-merged as `81e5fdb0a8b87976d6c6e970263a38bfadb042d3`.

On that exact merge head, **CI #1977**, **production-smoke #208** and **cinematic-delivery-smoke #75** all passed. #75 completed the real 720p24 Odyssey delivery, captured runtime provenance, verified media/provenance and uploaded the evidence artifact.

The #208 downloadable production artifact was independently re-inspected in this owner cycle:

- cow final MP4: 15.0 s, H.264/yuv420p + AAC, SHA-256 `8c23e3ea76dad18d5d2092e52b944365f267df363a16e9624db08a5be0e339b5`, seam max delta `4.431528`, max seam/intra ratio `3.622543`;
- Odyssey final MP4: 15.0 s, H.264/yuv420p + AAC, SHA-256 `f30a15c8e146f07d2bae8416a7bae3ebe5a54cfb5cb65bac5fbb82f6ac39795c`, seam max delta `5.196111`, max seam/intra ratio `3.038082`.

Both final hashes match the previously verified deterministic smoke baseline; `-35 dB / 0.5 s` inspection found no long silence in either file. Direct 1/5/9/13 s frame inspection found no new measured framing/subtitle/lighting regression that justifies retuning the guaranteed path.

PR #162 `Research PersonaShot narrative-continuity dimensions` exact head `83a95edfad7a2331a5247f1239a6dc62731ded11` passed **CI #1979**, had no review threads and was mergeable. It was squash-merged as `0559d21d2338fe58cb47646d5a0aceffe7889f9c`; post-merge **CI #1980 passed**.

## Canonical guaranteed baseline

Unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

`ZERO_COST_MODE=true` remains canonical. The guaranteed route uses no GPU/model, credentials, paid fallback or implicit multi-GB download. Existing evidence covers meaningful motion, mobile framing/subtitle readability, dialogue/audio coverage, seam quality, shot-byte provenance, composition-time byte verification, runtime provenance and final-media verification.

Do not retune deterministic cow/Odyssey visuals or audio without a measured defect.

## Reference-conditioned continuity boundary

Input locks are constraints, not output proof. Generated continuity evidence must cover all subject-bearing plan shots and bind exact reference bytes, generated shot bytes, generator/model/source provenance when independently verifiable, and evaluator identity/revision.

**Identity fidelity and requested-action/motion fidelity are separate dimensions.** PR #161 closes a remaining provenance gap: when motion or anti-copy evidence is claimed, `hottop.reference-continuity-benchmark.v1` now requires `motion_spec_sha256`, derived from the exact ordered subject-bearing plan fields (`scene`, `intent`, `continuity_instruction`, `generation_prompt`, `negative_prompt`). A generic motion score can no longer be reused against different requested action semantics. Historical identity-only evidence remains backward-compatible.

Current primary operator route remains **LightX2V/Wan2.2**. Other continuity/motion candidates remain benchmark/research-only unless exact source/checkpoint rights, operator runtime and output evidence clear admission. Runtime success never substitutes for identity, motion, geography, provenance or final-media proof.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains an operator-owned benchmark candidate; CosyVoice3 remains correctness-gated.

Speech execution remains fail-closed across independent layers: semantic dialogue input validation, non-empty/finite/non-silent serialized PCM, Qwen duration-derived token ceiling, produced PCM slot-fit, and final media verification. Future Qwen3-TTS 1.7B Mandarin A/B must bind model/runtime/hardware provenance and separately inspect short-onset stability plus normal production-length intelligibility, speaker consistency, delivery and naturalness.

## Fresh ecosystem radar — 2026-08-28

- **LightX2V:** upstream `main` advanced to `5169278f6bfb343f339b59ce8ebdb261a57a27e2` with `fix h3 ref2v resize mode (#1451)`. The change adds MiniMax-H3 reference-image resize modes/configuration and does not provide Hottop-measured benefit for the currently tested Wan2.2 I2V subset. Keep the tested Hottop pin; no freshness-only repin.
- **Qwen3-TTS:** official `main` remains `022e286b98fbec7e1e916cb940cdf532cd9f488e`; no official change removes the operator-local 1.7B benchmark gate.
- **PersonaShot:** arXiv:2608.16717, published 2026-08-17, reports roughly 1,000 multi-shot segments and 16 metrics spanning physical continuity, affective dynamics and cinematic grammar. It shows that perceptual quality, identity and generic motion can still coexist with physical-state resets, abrupt affective shifts and broken shot relations. The paper states that benchmark/evaluators/code will be released, but targeted public searches in this run found no official/reviewable release or license surface. Hottop therefore records only a research-level evaluator-design signal; no code/data/evaluator dependency or PersonaShot-calibrated threshold is imported. See `docs/research/2026-08-28-personashot-narrative-continuity-admission.md`.

No reviewed candidate in this run clears admission strongly enough to replace the guaranteed software3d route or current tested operator route.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, generate at least two subject-bearing shots and require complete byte-bound identity + requested-action motion evidence before composition.
3. For real multi-shot narratives, do not collapse all continuity into one generic score. When story semantics require it, separately consider physical-state continuity, affective trajectory and cinematic relations in addition to identity/motion; do not claim PersonaShot-compatible evaluation until an admissible release or independently specified evaluator exists.
4. When operator-local Qwen3-TTS 1.7B is genuinely provisioned, run same-line Mandarin A/B against the guaranteed fallback with bound runtime/hardware provenance and repeated cold/warm trials.
5. Continue targeted ecosystem radar around measured gaps. Do not add freshness-only pins, large dependencies, hosted paid fallbacks or provider abstraction without measurable value and rollback.
6. For fresh creative generation, resolve current source-event + active derivative meme first, then use creative memory only as mechanism/grammar/guardrail support.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills, including creative-reference memory when prior cases can help.
4. newest relevant spec/plan/decision/research record.
5. live `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. continue the highest-value safe action autonomously.
