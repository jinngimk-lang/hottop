# Hottop Status

Last updated: 2026-08-27
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot, not a self-updating `main` pointer. Always recover `PROJECT.md` first and re-fetch GitHub before exact branch/head/CI claims.

## Current verified repository truth

Latest owner closure: PR #119 **Refresh Production v0.2 media evidence and radar** passed exact-head CI #1847 at `a9509b6ad0c8102b8778c5967969921a575b1f0c`, was squash-merged as `33753c39ecd6ebf9347ce58bcbeb552fbe6ec8d6`, and the resulting `main` push passed CI #1848 on Python 3.11/3.12. Re-fetch GitHub before treating that SHA as the live head.

PR #117 **Bound Qwen TTS generation by planned duration** was squash-merged to `main` as `a3b14c2191fc37447f27d77754ab650c9c0bbbf8` after exact head `1d038af7a12b43553678f8e9641483c0983631ef` passed CI #1843 on Python 3.11/3.12 with Ruff + full pytest. Post-merge `main@a3b14c21…` then passed CI #1844 on both Python versions.

The closure adds a Qwen-specific pre-generation resource guard without changing provider routing or the guaranteed eSpeak fallback:

- RED exact `8c012eec4328f2a11cb71fcdfef0332acc69e065`, CI #1840 — Ruff passed; Python 3.12 pytest finished **1 failed / 515 passed**. The sole failure proved that a bounded 2.0-second Qwen dialogue request still called `generate_custom_voice(...)` without `max_new_tokens`.
- GREEN implementation `1bd3187043739ec0b2fb467497312a86500ef601`, CI #1841 — Python 3.11 and 3.12 both passed Ruff + full pytest.
- For bounded dialogue, Qwen now receives `min(2048, ceil(max_duration_seconds × 12.5) + 1)` before inference. The upstream default ceiling is never increased, and unbounded requests preserve prior behavior.
- The existing output-side exact PCM duration gate remains independently mandatory. A token ceiling limits runaway compute; it is not proof that final speech fits the slot.

No model download, GPU provisioning, credential, network TTS, serving-stack or paid-path behavior was introduced. Detailed record: `docs/research/2026-08-27-neural-tts-duration-bound.md`.

## Fresh real-media inspection — production-smoke #191

The newest downloadable full software3d production artifact at recovery time was `production-smoke #191` on `main@98dfc943a2ada756fffdaa50e60172ebd944dd66`, artifact digest `sha256:87938d4ae4874932293f4d5592c00f580c35ca86803f7b5c4b796769430fe71e`.

Direct inspection of the actual cow and Odyssey final MP4s found no new deterministic defect that justifies tuning:

- both final assets are exactly 15.0 seconds, H.264 `360×640` / `yuv420p` with AAC stereo at 44.1 kHz;
- `ffmpeg silencedetect` at `-35 dB` with a 0.5-second minimum found no long silent region in either final mix;
- cow mean/max audio level measured about `-24.8 / -4.2 dB`; Odyssey about `-23.9 / -4.0 dB`;
- cow seam quality remains intra-shot p95 `1.223319`, max seam delta `4.431528`, seam/intra ratio `3.622543`;
- Odyssey remains intra-shot p95 `1.710326`, max seam delta `5.196111`, ratio `3.038082`;
- direct frame inspection at 1/3/5/7/9/11/13 seconds showed continuous readable story frames/subtitles and no new measured framing, lighting or transition regression.

This reinforces the existing owner rule: do not change framing, lighting, loudness or transitions from aesthetics alone when the real artifact continues to pass the accepted production contracts.

## Neural-TTS integrity closure

The local neural-TTS production boundary now has four distinct layers rather than treating successful model return as success:

1. model-returned samples must be non-empty and finite;
2. the exact int16 PCM destined for WAV must contain at least one non-zero sample;
3. for bounded Qwen dialogue, generation receives a duration-derived codec-token ceiling before inference to bound obviously inadmissible runaway work;
4. exact produced PCM duration must still fit the planned `AudioCue.duration_seconds` slot before any WAV is admitted.

### Serialized-PCM non-silence

- RED `78bc20073a6fa313c3ad0c72fd925f6992761d50`, CI #1828: Qwen3-TTS and CosyVoice3 accepted non-zero sub-LSB float waveforms that quantized entirely to digital int16 silence.
- GREEN `409d3e37ed4a03cd9b3769042eaf350315b9e43c`, CI #1830: both local neural-TTS writers validate the exact int16 PCM that would be serialized and reject all-zero output before WAV/temporary-file creation.
- The gate remains deliberately narrow: no broad RMS/VAD/loudness heuristic is introduced.

### Planned dialogue duration

- RED `b3aef79e9739238c03291304d803de0e237dcf21`, CI #1834: Qwen3-TTS accepted a 1.25-second waveform for a 1.0-second dialogue slot, and normal `video-run` routing omitted `--max-duration-seconds` for a bounded Qwen dialogue cue.
- GREEN `3a2c8a6c41b8b541188751aad63ee3e86c84c35a`: Qwen request/CLI accepts optional positive `max_duration_seconds`; normal routing forwards bounded `AudioCue.duration_seconds`; actual PCM frames/sample-rate exceeding the planned slot fail closed before WAV creation.
- PR #117 adds the generation-side companion guard using upstream `max_new_tokens`; natural-language instructions remain style/prosody hints, not timing evidence.

## Guaranteed zero-cost production baseline

The unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

The baseline remains free of GPU/model requirements, paid fallback, credentials and implicit multi-GB downloads. Production evidence continues to enforce meaningful pixel motion, mobile framing/subtitle readability, dialogue/audio coverage, transition/seam quality, byte-bound shot provenance, composition-time byte verification, runtime provenance and final-media verification.

Anti-Polish may remain intentionally crude; lower-roughness cinematic profiles must remain presentable. Roughness never relaxes continuity, timing, Mandarin intelligibility, product semantics, rights/evidence safety or encoding integrity.

## Neural-TTS quality boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the admitted operator-owned delivery-controlled benchmark candidate; 0.6B must not silently discard `delivery`/`instruct` semantics. CosyVoice3 remains a correctness-gated operator benchmark candidate, not a default route.

Shared local neural-TTS integrity is fail-closed on **non-empty + finite + serialized-PCM non-silent** audio before WAV creation. Routed Qwen dialogue additionally treats a planned cue duration as both a pre-generation resource bound and a hard output artifact constraint. Intelligibility, delivery/naturalness, rights review and final-media coverage remain separate higher-level gates.

A real same-line Qwen3-TTS 1.7B Mandarin A/B still requires an already-provisioned local model/runtime plus publication-rights review. No automatic model download or GPU provisioning is allowed.

## Generated/reference-conditioned quality boundary

The highest-value generated-quality proof remains a rights-safe reference-conditioned multi-shot identity benchmark. Input identity/reference locks are constraints, not proof.

- LightX2V/Wan2.2 remains the tested operator-owned local base route; no freshness-only repin without measured Hottop value.
- Stand-In/Wan2.2 remains a benchmark candidate, not an automatically installed route.
- Memento/IPVG and later candidates remain gated by license/runtime/hardware/provenance evidence.
- Actual generator source revision, model/checkpoint identity when independently verifiable, exact reference bytes, generated shot bytes and evaluator revision remain separate provenance dimensions.

Do not fabricate DGX readiness. GPU/driver/CUDA/PyTorch/model/reference state must be probed on the actual operator machines before a generated-quality claim.

## Ecosystem radar snapshot

Targeted 2026-08-27 freshness checks still do not justify a provider switch or freshness-only repin:

- Qwen3-TTS public missing-EOS / long-generation reports continue to reinforce the already-merged duration-derived `max_new_tokens` resource guard. This is corroborating evidence for the existing boundary, not evidence that natural-language duration instructions or a token ceiling prove final timing; exact PCM duration remains authoritative.
- CosyVoice3 correctness reports remain material: an official-checkpoint TensorRT+FP16 report observed non-finite audio across all 64 tested generations, and a separate streaming path reported an STFT device mismatch. Keep CosyVoice3 correctness-gated rather than promoting it to the default route without a controlled Hottop benchmark.
- Current LightX2V/Wan2.2 public activity still does not provide a Hottop-measured improvement to the already-tested I2V subset, so no freshness-only repin is justified.

No upstream candidate in this scan passed the admission gate strongly enough to warrant a new dependency, adapter or model/runtime change.

## Immediate next actions

1. Continue inspecting fresh real cow/Odyssey MP4 evidence and change deterministic visuals/audio only for a **measured** defect; do not tune framing, lighting, transitions or loudness from aesthetics alone.
2. Once a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, run at least two subject-bearing Odyssey I2V shots and require meaningful motion plus complete subject-bound continuity evidence before composition.
3. When operator-local Qwen3-TTS 1.7B is genuinely provisioned, run same-line Mandarin A/B against the guaranteed fallback and promote it only on measured intelligibility/delivery/naturalness evidence plus publication-rights review.
4. Continue targeted ecosystem radar around the measured gap. Do not add freshness-only pins, large dependencies or provider abstraction without measurable value and rollback.
5. For fresh creative output, continue live hotspot research + mechanism mapping + generation preflight; historical cow/Odyssey cases remain fixtures, not defaults.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. current `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. fresh hotspot/mechanism analysis for new creative generation.
8. continue the highest-value safe action autonomously.
