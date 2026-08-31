# Hottop Status

Last updated: 2026-08-31
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest verified code evidence point: **`main@29afecc37ed8fc414ff9a0e06f4e02e6ca677e5c`**. Post-merge CI #2467 is green. This merge closes the linked-Git-worktree revision gap in the LightX2V source-provenance boundary. The same head's 720p cinematic-delivery-smoke #92 was still executing when this snapshot was written, so this file does not infer that gate from ordinary CI.

The linked-worktree feature was exact-head verified before merge at `2bf92a433732d2420cb0157a6e7c7f68ebe63865`: CI #2465, production-smoke #223 and cinematic-delivery-smoke #90 succeeded. Its predecessor stable-source closure at `4ba114005f78e2a9396ead2787f527551859145a` passed CI #2460, production-smoke #220 and cinematic-delivery-smoke #87.

## Canonical guaranteed baseline

Unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

`ZERO_COST_MODE=true` remains canonical. The guaranteed route uses no GPU/model, credentials, paid fallback or implicit multi-GB download. Existing evidence covers meaningful motion, mobile framing/subtitle readability, dialogue/audio coverage, seam quality, shot-byte provenance, composition-time byte verification, runtime provenance and final-media verification.

Retained deterministic smoke evidence:

- cow: 15.0 s H.264/yuv420p + AAC, SHA-256 `8c23e3ea76dad18d5d2092e52b944365f267df363a16e9624db08a5be0e339b5`, seam max delta `4.431528`, max seam/intra ratio `3.622543`;
- Odyssey: 15.0 s H.264/yuv420p + AAC, SHA-256 `f30a15c8e146f07d2bae8416a7bae3ebe5a54cfb5cb65bac5fbb82f6ac39795c`, seam max delta `5.196111`, max seam/intra ratio `3.038082`;
- 720×1280/24 fps Odyssey: SHA-256 `c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df`, seam max delta `4.184792`, max seam/intra ratio `4.480971`, with bound CPU/NumPy/OpenBLAS/FFmpeg/FFprobe/eSpeak-NG/font provenance.

Do not retune deterministic cow/Odyssey visuals or audio without a measured artifact defect.

## LightX2V / reference-conditioned continuity boundary

Primary operator route remains **LightX2V/Wan2.2**. Input locks are constraints, not output proof. Generated continuity evidence must cover all subject-bearing shots and bind exact reference bytes, generated shot bytes, generator/model/source provenance when independently verifiable, evaluator identity/revision and fail-closed thresholds.

**Identity fidelity and requested-action/motion fidelity remain separate dimensions.** Motion/anti-copy evidence binds `motion_spec_sha256` from exact ordered subject-bearing plan semantics. Runtime success or generic motion never proves requested action or subject identity.

LightX2V source provenance is fail-closed across the generation window:

- inherited `PYTHONPATH` is isolated to the operator checkout root;
- tracked uncommitted changes are rejected;
- untracked **and Git-ignored** importable/runtime-code files (`.py`, `.pyc`, `.pyd`, `.so`, `.pth`) are rejected while unrelated local data may remain;
- Git source identity is resolved with `git -C <root> rev-parse --verify HEAD`, covering linked-worktree/common-dir and packed-ref layouts;
- a real Git checkout whose commit cannot be provenance-verified fails closed instead of degrading to an entrypoint-only hash;
- the exact local source revision is captured before spawn and re-verified after generation, before quality/provenance acceptance;
- if post-generation source verification fails, the produced video is deleted and no manifest is accepted.

This is an implementation of the existing actual-generator-source doctrine, not proof against a hostile actor that mutates source and restores the exact clean tree between boundary checks. Durable rationale: `docs/research/2026-08-31-lightx2v-source-provenance.md`.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated.

Prepared local candidates remain:

- `qwen3-tts-qwentts-cpp-1b7` — hardened read-only GGUF artifact preflight;
- `qwen3-tts-crispasr-1b7` — read-only GGUF artifact preflight;
- `qwen3-tts-audio-cpp-1b7` — read-only CustomVoice model-directory preflight;
- `qwen3-tts-pure-c-1b7` — read-only raw-safetensors model-tree preflight, registry-discoverable but `integration_ready=false` and `runtime_status=unprobed`;
- `qwen3-tts-ncnn-0b6` — lower-hardware CPU/Vulkan benchmark candidate only.

Comparable `inspect-tts-benchmark` latency/RTF evidence continues to require exact text/language/supported speaker, canonical generation protocol, recognized hardware backend with coherent CPU/device count, recognized `cli`/`server` execution shape, server worker/thread topology when applicable, cold/warm independent trials, one runtime revision + one model revision per candidate, finite positive latency, distinct resolved WAV trial paths, WAV/PCM integrity and `listening_required=true`. Hardware/execution profiles remain declared measurement provenance rather than proof of actual runtime utilization.

Durable method: `docs/research/2026-08-30-tts-bench-method-admission.md` plus the 2026-08-31 CPU/accelerator provenance records.

## Fresh ecosystem radar — 2026-08-31

- **LightX2V** public `main` advanced to `e7262940e8fcd63a91659ef1e9a2c2bb611480f2` on 2026-08-31. The tip fixes Hunyuan SR transformer weight loading and removes a stale run-step path; its parent `f85a5c6f5d97a2a031a9f11b8e7f521bde5fb691` fixes MiniMax-H3 tensor-parallel sharding. Neither provides Hottop-measured continuity, quality or runtime gain for the tested Wan2.2 I2V subset; keep the tested pin and do not freshness-only repin.
- **Qwen3-TTS official** remains operator-gated for 1.7B quality evidence; no fresh signal in this cycle removes the need for exact local runtime/model plus same-line Mandarin A/B.
- No candidate in this cycle clears admission strongly enough to replace the guaranteed software3d route, the tested LightX2V/Wan2.2 operator route or the prepared local 1.7B TTS candidates.

## Immediate next actions

1. Close the remaining post-merge cinematic-delivery-smoke #92 evidence for `main@29afecc3…`; repair any real media/provenance regression before opening unrelated work.
2. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
3. When a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, generate at least two subject-bearing shots and require complete byte-bound **identity + requested-action motion** evidence before composition.
4. When an operator provisions qwentts.cpp, CrispASR, audio.cpp or Pure-C plus exact Qwen3-TTS 1.7B CustomVoice assets, run the corresponding read-only artifact preflight first; then perform same-line Mandarin generation under the existing generation/hardware/execution-shape coherence gates.
5. Continue targeted ecosystem radar around measured gaps. Do not add freshness-only pins, large dependencies, hosted paid fallbacks or provider abstraction without measurable value and rollback.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. live `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. continue the highest-value safe action autonomously.
