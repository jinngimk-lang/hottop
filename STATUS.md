# Hottop Status

Last updated: 2026-08-27
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot, not a self-updating `main` pointer. Always recover `PROJECT.md` first and re-fetch GitHub before exact branch/head/CI claims.

## Current verified repository truth

PR #115 **Fail closed on invalid or overlong neural TTS audio** was squash-merged to `main` as `98dfc943a2ada756fffdaa50e60172ebd944dd66` after exact head `1855cb530aaa7073cfb0e921e300cf7d02830eb8` passed all three merge gates:

- CI #1836 — Python 3.11/3.12 Ruff + full pytest passed;
- production-smoke #190 — complete cow + Odyssey software3d → Mandarin audio/music/Foley → MoviePy → FFmpeg → media/provenance chain passed;
- cinematic-delivery-smoke #57 — 720×1280/24fps Odyssey delivery and provenance verification passed;
- inline review threads were empty and the PR was mergeable.

Post-merge `main@98dfc943…` has passed CI #1837 and production-smoke #191. Cinematic-delivery-smoke #58 is still running at this snapshot and remains the final post-merge 720p regression check; do not infer its result before GitHub reports completion.

## Neural-TTS integrity closure

Two concrete production-integrity gaps are now closed without changing the guaranteed eSpeak fallback, adding a provider, downloading a model or enabling paid/GPU behavior.

### Serialized-PCM non-silence

- RED `78bc20073a6fa313c3ad0c72fd925f6992761d50`, CI #1828: Qwen3-TTS and CosyVoice3 accepted non-zero sub-LSB float waveforms that quantized entirely to digital int16 silence.
- GREEN `409d3e37ed4a03cd9b3769042eaf350315b9e43c`, CI #1830: both local neural-TTS writers now validate the exact int16 PCM that would be serialized and reject all-zero output before WAV/temporary-file creation.
- The gate remains deliberately narrow: no broad RMS/VAD/loudness heuristic is introduced.

### Planned dialogue duration

- RED `b3aef79e9739238c03291304d803de0e237dcf21`, CI #1834: Qwen3-TTS accepted a 1.25-second waveform for a 1.0-second dialogue slot, and normal `video-run` routing omitted the bounded cue duration.
- GREEN `3a2c8a6c41b8b541188751aad63ee3e86c84c35a`: Qwen request/CLI accepts optional positive `max_duration_seconds`; normal routing forwards bounded `AudioCue.duration_seconds`; actual PCM frames/sample-rate exceeding the planned slot fail closed before WAV creation.
- Natural-language instructions remain style/prosody hints, not timing evidence. Fresh upstream Qwen reports show second-level duration prompting is unreliable and missing-EOS/over-generation can occur.

Detailed records:

- `docs/research/2026-08-27-neural-tts-quantized-silence.md`;
- `docs/research/2026-08-27-neural-tts-duration-bound.md`.

## Guaranteed zero-cost production baseline

The unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

The baseline remains free of GPU/model requirements, paid fallback, credentials and implicit multi-GB downloads. Production evidence continues to enforce meaningful pixel motion, mobile framing/subtitle readability, dialogue/audio coverage, transition/seam quality, byte-bound shot provenance, composition-time byte verification, runtime provenance and final-media verification.

Fresh production-smoke #190 inspection found no new measured deterministic defect: cow max seam delta/ratio remained `4.431528 / 3.622543`, Odyssey `5.196111 / 3.038082`, both within the existing fail-closed gates. No framing, lighting, transition or loudness change is justified from aesthetics alone.

Anti-Polish may remain intentionally crude; lower-roughness cinematic profiles must remain presentable. Roughness never relaxes continuity, timing, Mandarin intelligibility, product semantics, rights/evidence safety or encoding integrity.

## Neural-TTS quality boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the admitted operator-owned delivery-controlled benchmark candidate; 0.6B must not silently discard `delivery`/`instruct` semantics. CosyVoice3 remains a correctness-gated operator benchmark candidate, not a default route.

Shared local neural-TTS integrity is now fail-closed on **non-empty + finite + serialized-PCM non-silent** audio before WAV creation. Routed Qwen dialogue additionally treats a planned cue duration as a hard artifact constraint. Intelligibility, delivery/naturalness, rights review and final-media coverage remain separate higher-level gates.

A real same-line Qwen3-TTS 1.7B Mandarin A/B still requires an already-provisioned local model/runtime plus publication-rights review. No automatic model download or GPU provisioning is allowed.

## Generated/reference-conditioned quality boundary

The highest-value generated-quality proof remains a rights-safe reference-conditioned multi-shot identity benchmark. Input identity/reference locks are constraints, not proof.

- LightX2V/Wan2.2 remains the tested operator-owned local base route; no freshness-only repin without measured Hottop value.
- Stand-In/Wan2.2 remains a benchmark candidate, not an automatically installed route.
- Memento/IPVG and later candidates remain gated by license/runtime/hardware/provenance evidence.
- Actual generator source revision, model/checkpoint identity when independently verifiable, exact reference bytes, generated shot bytes and evaluator revision remain separate provenance dimensions.

Do not fabricate DGX readiness. GPU/driver/CUDA/PyTorch/model/reference state must be probed on the actual operator machines before a generated-quality claim.

## Ecosystem radar snapshot

Targeted 2026-08-27 freshness checks did not justify a provider switch or freshness-only repin:

- Qwen3-TTS reports continue to show explicit duration-in-seconds instructions are not a reliable wall-clock contract and that missing-EOS/codec repetition can produce overlong output; this strengthens Hottop's output-side duration gate rather than justifying a hidden serving stack.
- LightX2V/Wan2.2 activity did not provide a Hottop-measured improvement to the already-tested I2V route, so the tested local subset remains pinned until a real operator benchmark shows value.

## Immediate next actions

1. Verify post-merge cinematic-delivery-smoke #58 on exact `main@98dfc943…`; if green, remove this pending note and retain the merge as fully post-merge verified.
2. Inspect fresh real cow/Odyssey MP4 evidence and change deterministic visuals/audio only for a **measured** defect; do not tune framing, lighting, transitions or loudness from aesthetics alone.
3. Once a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, run at least two subject-bearing Odyssey I2V shots and require meaningful motion plus complete subject-bound continuity evidence before composition.
4. When operator-local Qwen3-TTS 1.7B is genuinely provisioned, run same-line Mandarin A/B against the guaranteed fallback and promote it only on measured intelligibility/delivery/naturalness evidence plus publication-rights review.
5. Continue targeted ecosystem radar around the measured gap. Do not add freshness-only pins, large dependencies or provider abstraction without measurable value and rollback.
6. For fresh creative output, continue live hotspot research + mechanism mapping + generation preflight; historical cow/Odyssey cases remain fixtures, not defaults.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. current `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. fresh hotspot/mechanism analysis for new creative generation.
8. continue the highest-value safe action autonomously.
