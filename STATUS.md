# Hottop Status

Last updated: 2026-08-27
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot, not a self-updating `main` pointer. Always recover `PROJECT.md` first and re-fetch GitHub before exact branch/head/CI claims.

## Current workstream

PR #115 **Fail closed on invalid or overlong neural TTS audio** is the only active workstream at this snapshot.

Quantized-silence closure:

- isolated RED `78bc20073a6fa313c3ad0c72fd925f6992761d50`, CI #1828: Ruff passed; Python 3.11 full pytest failed exactly twice because Qwen3-TTS and CosyVoice3 accepted sub-LSB non-zero waveforms that quantized to all-zero int16 PCM;
- GREEN `409d3e37ed4a03cd9b3769042eaf350315b9e43c`, CI #1830: Python 3.11/3.12 passed Ruff + full pytest;
- both local neural-TTS writers now reject digital silence on the **actual int16 PCM representation** before WAV/temporary-file creation; broad RMS/VAD/loudness heuristics remain intentionally out of scope.

Planned-dialogue duration closure:

- RED `b3aef79e9739238c03291304d803de0e237dcf21`, CI #1834: Ruff passed; full pytest exposed exactly two missing contracts — Qwen3-TTS accepted a 1.25-second waveform for a 1.0-second planned slot, and normal Qwen `video-run` routing omitted the cue duration;
- GREEN production implementation `3a2c8a6c41b8b541188751aad63ee3e86c84c35a`: Qwen request/CLI accepts positive optional `max_duration_seconds`, produced PCM exceeding the planned slot fails before WAV creation, and normal routing forwards bounded `AudioCue.duration_seconds` as `--max-duration-seconds`;
- exact-head CI #1835 passed on Python 3.11/3.12; production-smoke #189 passed the complete guaranteed cow + Odyssey software3d/audio/MoviePy/FFmpeg/media/provenance chain;
- cinematic-delivery-smoke #56 is the remaining 720p regression gate for this exact production-code head at snapshot time.

Detailed records:

- `docs/research/2026-08-27-neural-tts-quantized-silence.md`;
- `docs/research/2026-08-27-neural-tts-duration-bound.md`.

## Guaranteed zero-cost production baseline

The unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

The baseline remains free of GPU/model requirements, paid fallback, credentials and implicit multi-GB downloads. Production evidence continues to enforce meaningful pixel motion, mobile framing/subtitle readability, dialogue/audio coverage, transition/seam quality, byte-bound shot provenance, composition-time byte verification, runtime provenance and final-media verification.

Anti-Polish may remain intentionally crude; lower-roughness cinematic profiles must remain presentable. Roughness never relaxes continuity, timing, Mandarin intelligibility, product semantics, rights/evidence safety or encoding integrity.

## Neural-TTS quality boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the admitted operator-owned delivery-controlled benchmark candidate; 0.6B must not silently discard `delivery`/`instruct` semantics. CosyVoice3 remains a correctness-gated operator benchmark candidate, not a default route.

Shared local neural-TTS waveform integrity is fail-closed before serialization: returned audio must be non-empty and finite, and the exact PCM representation destined for WAV must contain at least one non-zero sample.

For the routed Qwen Production path, a bounded dialogue cue also carries a hard planned-slot constraint. Exact wall-clock duration is verified from produced PCM rather than assumed from natural-language instruction. Fresh upstream evidence (`QwenLM/Qwen3-TTS#23`) reports explicit “finish within N seconds” instructions do not reliably control duration, and discussion #211 documents over-generation/missing-EOS behavior; these support output-side validation rather than a provider switch or hidden serving stack.

A real same-line Qwen3-TTS 1.7B Mandarin A/B still requires an already-provisioned local model/runtime plus publication-rights review. No automatic model download or GPU provisioning is allowed.

## Generated/reference-conditioned quality boundary

The highest-value generated-quality proof remains a rights-safe reference-conditioned multi-shot identity benchmark. Input identity/reference locks are constraints, not proof.

- LightX2V/Wan2.2 remains the tested operator-owned local base route; no freshness-only repin without measured Hottop value.
- Stand-In/Wan2.2 remains a benchmark candidate, not an automatically installed route.
- Memento/IPVG and later candidates remain gated by license/runtime/hardware/provenance evidence.
- Actual generator source revision, model/checkpoint identity when independently verifiable, exact reference bytes, generated shot bytes and evaluator revision remain separate provenance dimensions.

Do not fabricate DGX readiness. GPU/driver/CUDA/PyTorch/model/reference state must be probed on the actual operator machines before a generated-quality claim.

## Ecosystem radar snapshot

Targeted 2026-08-27 review around the current TTS gap found no evidence to replace Hottop's reviewed operator-local route:

- official Qwen3-TTS `generate_custom_voice(...)` exposes speaker/language/optional instruction text and generic generation kwargs but no documented exact wall-clock duration guarantee;
- Qwen issue #23 reports explicit duration-in-seconds prompts were ineffective across the 1.7B model families;
- Qwen discussion #211 reports over-generation / missing-EOS / long-running inference cases, with `max_new_tokens` useful only as a mitigation rather than exact duration control;
- these findings strengthen artifact-level duration validation and bounded production admission; they do not justify auto-installing another serving stack, switching provider, or downloading new weights.

## Immediate next actions

1. Finish PR #115 only after its exact production-code head passes the 720p cinematic gate, then publish the prepared duration research/status update and require final exact-head CI before merge.
2. After merge, verify post-merge `main` CI/production evidence and remove PR #115 from the active snapshot.
3. Inspect fresh real cow/Odyssey MP4 evidence and change deterministic visuals/audio only for a **measured** defect; do not tune framing, lighting, transitions or loudness from aesthetics alone.
4. Once a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, run at least two subject-bearing Odyssey I2V shots and require meaningful motion plus complete subject-bound continuity evidence before composition.
5. When operator-local Qwen3-TTS 1.7B is genuinely provisioned, run same-line Mandarin A/B against the guaranteed fallback and promote it only on measured intelligibility/delivery/naturalness evidence plus publication-rights review.
6. Continue targeted ecosystem radar around the measured gap. Do not add freshness-only pins, large dependencies or provider abstraction without measurable value and rollback.
7. For fresh creative output, continue live hotspot research + mechanism mapping + generation preflight; historical cow/Odyssey cases remain fixtures, not defaults.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. current `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. fresh hotspot/mechanism analysis for new creative generation.
8. continue the highest-value safe action autonomously.
