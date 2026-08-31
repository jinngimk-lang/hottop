# Hottop Status

Last updated: 2026-08-31
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest merged production point is **`main@2eaa6f47a529e803999c798aae8c426a90c4c759`** (`fix: fail closed when LightX2V has no NVIDIA GPU`, PR #363), SHA-locked squash-merged from exact verified head `14905514fcf76fe64ba62fb2cccdd5184fc9f19a`.

TDD/production evidence for the NVIDIA local-preflight workstream:

- RED `e5ccb02f892c29641172a93935b9f2adb55a2859`: CI #2560 failed the new regression contract before an explicit NVIDIA availability check existed;
- GREEN `14905514fcf76fe64ba62fb2cccdd5184fc9f19a`: exact-head CI #2567 succeeded;
- the same GREEN head passed production-smoke #284 and cinematic-delivery-smoke #151;
- production-smoke #284 executed both checked-in anti-polish cow and cinematic Odyssey software3d paths through final media/provenance verification and uploaded artifact `hottop-software3d-production-smoke` (687,896 bytes, archive digest `sha256:181fa429933044c73d2cfe3f97374279c9d2f1ec76b925fb5f88b57237420f87`).

`run_lightx2v_shot()` now requires a bounded local `nvidia-smi` probe before generation. Missing `nvidia-smi`, timeout, non-zero probe status, OS execution failure or no visible GPU fails closed before the LightX2V inference runner starts. Production keeps the real probe by default; ordinary unit tests inject the probe explicitly only when testing independent generation behavior. No hardware provisioning, driver install, model download, hosted endpoint or paid fallback was added.

Durable evidence record: `docs/research/2026-08-31-lightx2v-nvidia-preflight.md`.

The earlier LightX2V protections remain in force: fresh requested targets are invalidated before preflight; generation runtime is positively bounded and network-offline; accepted artifacts bind exact request/source/config provenance; rights-safe I2V binds exact reference SHA-256 + bytes + rights classification and rejects reference mutation; source provenance rejects dirty/ambiguous runtime code and escaping tracked symlinks.

`PROJECT.md` is intentionally unchanged for this workstream because explicit local accelerator availability is direct implementation closure under existing operator-owned/fail-closed/no-auto-provisioning doctrine.

## Canonical guaranteed baseline

Unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

`ZERO_COST_MODE=true` remains canonical. The guaranteed route uses no GPU/model, credentials, paid fallback or implicit multi-GB download. Existing production-smoke evidence covers meaningful motion, mobile framing/subtitle readability, dialogue/audio coverage, seam quality, shot-byte provenance, composition-time byte verification, runtime provenance and final-media verification.

Retained deterministic smoke evidence:

- cow: 15.0 s H.264/yuv420p + AAC, SHA-256 `8c23e3ea76dad18d5d2092e52b944365f267df363a16e9624db08a5be0e339b5`;
- Odyssey: 15.0 s H.264/yuv420p + AAC, SHA-256 `f30a15c8e146f07d2bae8416a7bae3ebe5a54cfb5cb65bac5fbb82f6ac39795c`;
- 720×1280/24 fps Odyssey: SHA-256 `c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df`, with bound CPU/NumPy/OpenBLAS/FFmpeg/FFprobe/eSpeak-NG/font provenance.

Do not retune deterministic cow/Odyssey visuals or audio without a measured artifact defect.

## LightX2V / reference-conditioned continuity boundary

Primary operator route remains **LightX2V/Wan2.2**. Input locks are constraints, not output proof. Generated continuity evidence must bind exact reference bytes, generated-shot bytes, byte-bound plan semantics, generation request identity, actual source/config provenance when independently verifiable, evaluator identity/revision and fail-closed thresholds.

For every evaluated subject, evidence must cover all subject-bearing plan shots; cherry-picked coverage fails closed. **Identity fidelity and requested-action/motion fidelity are separate dimensions.** Runtime success, request digests or generic motion never prove requested action, subject identity or semantic correctness.

The next real quality gate is generated media, not another provider abstraction.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated.

Prepared local candidates remain operator-provisioned/no-auto-download. Comparable `inspect-tts-benchmark` evidence still requires exact text/language/supported speaker, canonical generation protocol, coherent hardware/execution shape, cold/warm independent trials, exact runtime/model revisions, finite positive latency, distinct WAV paths, PCM integrity and `listening_required=true`.

## Fresh ecosystem radar — 2026-08-31

- **LightX2V** remains evidence-pinned rather than freshness-pinned. Reviewed public tip work is centered on SeedVR/distributed-runtime changes and does not provide Hottop-measured Wan2.2 I2V identity/requested-motion benefit for the tested route; continue **no freshness-only repin**.
- A small Apache-2.0 **Wan2.2-Fast** code repository surfaced with a CUDA/ZeroGPU 4-step I2V path, but its effective runtime composes external Wan2.2 Diffusers weights, third-party dual-transformer weights, Lightning LoRAs and compiled CUDA artifacts. The combined code/weights/artifact licensing and exact provenance have not been admitted as one Hottop-compatible zero-cost bundle, and no Hottop benchmark shows a quality win. Radar-only; no vendoring, auto-install or model download.
- **Qwen3-TTS** community ports continue to show lower-hardware possibilities, including Rust/ONNX/llama.cpp CPU/Vulkan/CUDA routes, but published performance is not Hottop same-line Mandarin evidence. Existing prepared operator-owned benchmark candidates remain unchanged.
- No candidate in this cycle clears admission strongly enough to replace the guaranteed software3d route, tested LightX2V/Wan2.2 operator route or prepared local TTS candidates.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V checkout, Wan2.2 model and suitable operator NVIDIA GPU are genuinely provisioned, run fail-closed preflight and generate at least two subject-bearing rights-safe I2V shots.
3. Require complete byte-bound **identity + requested-action motion + media quality + exact request/source/config/reference provenance** before composition.
4. When an operator provisions local Qwen3-TTS 1.7B runtime/model, run read-only preflight and same-line Mandarin generation under existing provenance/coherence gates.
5. Continue targeted ecosystem radar around measured gaps; do not add freshness-only pins, large dependencies, hosted paid fallbacks or provider abstraction without measurable value and rollback.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. live `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. continue the highest-value safe action autonomously.
