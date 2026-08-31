# Hottop Status

Last updated: 2026-08-31
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest verified evidence point: **`main@8a8b63cf52d1b4d81b430db8caa5cb1e8b5eda94` / CI #2438** on Python 3.11/3.12. This merge closes the accelerator-device-count false-ready gap for TTS latency/RTF evidence. Every later recovery must still re-fetch live `main`, open PRs and exact-head CI.

## Canonical guaranteed baseline

Unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

`ZERO_COST_MODE=true` remains canonical. The guaranteed route uses no GPU/model, credentials, paid fallback or implicit multi-GB download. Existing evidence covers meaningful motion, mobile framing/subtitle readability, dialogue/audio coverage, seam quality, shot-byte provenance, composition-time byte verification, runtime provenance and final-media verification.

Retained deterministic smoke evidence:

- cow: 15.0 s H.264/yuv420p + AAC, SHA-256 `8c23e3ea76dad18d5d2092e52b944365f267df363a16e9624db08a5be0e339b5`, seam max delta `4.431528`, max seam/intra ratio `3.622543`;
- Odyssey: 15.0 s H.264/yuv420p + AAC, SHA-256 `f30a15c8e146f07d2bae8416a7bae3ebe5a54cfb5cb65bac5fbb82f6ac39795c`, seam max delta `5.196111`, max seam/intra ratio `3.038082`;
- 720×1280/24 fps Odyssey: SHA-256 `c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df`, seam max delta `4.184792`, max seam/intra ratio `4.480971`, with bound CPU/NumPy/OpenBLAS/FFmpeg/FFprobe/eSpeak-NG/font provenance.

Do not retune deterministic cow/Odyssey visuals or audio without a measured artifact defect.

## Reference-conditioned continuity boundary

Input locks are constraints, not output proof. Generated continuity evidence must cover all subject-bearing shots and bind exact reference bytes, generated shot bytes, generator/model/source provenance when independently verifiable, evaluator identity/revision and fail-closed thresholds.

**Identity fidelity and requested-action/motion fidelity are separate dimensions.** Motion/anti-copy evidence binds `motion_spec_sha256` from exact ordered subject-bearing plan semantics. Generic motion cannot prove a different requested action.

Primary operator route remains **LightX2V/Wan2.2**. Reviewed alternatives remain benchmark/research-only unless exact rights, local runtime and same-sequence output evidence clear admission. Runtime success never substitutes for identity, motion, geography, provenance or final-media proof.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated.

Prepared local benchmark candidates:

- `qwen3-tts-qwentts-cpp-1b7` — hardened read-only GGUF artifact preflight;
- `qwen3-tts-crispasr-1b7` — read-only GGUF artifact preflight;
- `qwen3-tts-audio-cpp-1b7` — read-only CustomVoice model-directory preflight;
- `qwen3-tts-pure-c-1b7` — read-only raw-safetensors model-tree preflight, registry-discoverable but `integration_ready=false` and `runtime_status=unprobed`;
- `qwen3-tts-ncnn-0b6` — lower-hardware 0.6B CPU/Vulkan benchmark candidate only.

`hottop-models inspect-tts-benchmark --spec <benchmark.json>` treats latency/RTF as comparable evidence only when it binds:

1. exact text, language and checkpoint-supported preset speaker;
2. one concrete generation protocol with canonical SHA-256, integer seed, positive `max_new_tokens` and explicit sampling control;
3. one concrete hardware profile with canonical SHA-256, one recognized backend class (`cpu`, `cuda`, `rocm`, `hip`, `vulkan`, `metal`, `mps`, `xpu`) and coherent device identity;
4. **for CPU backends, a nonblank CPU identity plus positive integer `logical_cpu_count`;**
5. **for accelerator backends, a nonblank GPU/generic-accelerator identity plus positive integer provider-neutral `device_count`;**
6. one recognized execution profile (`cli` or `server`) with positive concurrency and batch size;
7. for `server`, nonblank connection strategy plus positive `worker_count` and `threads_per_worker`;
8. cold/warm coverage, with additional independent warm repeats retained for warmed variance and repeated speaker-consistency evidence;
9. one exact runtime revision and one exact model/checkpoint revision per candidate;
10. finite positive latency plus distinct resolved WAV artifact paths, byte identity and WAV/PCM integrity;
11. `listening_required=true`, keeping naturalness, speaker consistency, onset stability and intelligibility independent from speed/stream integrity.

The accelerator-count closure was TDD-verified. RED head `77882ba1cc9100649728a8fbedc2cf19df86bfa2` passed Ruff and failed pytest in CI #2430 because `cuda + H200` without any device count could still become benchmark-ready. Minimal GREEN requires positive integer `device_count` for accelerator backends. Full-suite validation exposed one old fixture using unvalidated `gpu_count`; it was migrated to provider-neutral `device_count` rather than weakening the gate. GREEN head `6a835fa64af6ccc3eedcd3d9bbe29b45d2fa43df` passed CI #2434; docs-synced head `fad19c6f327d1a001db57170314b3fdfb28da9b1` passed CI #2436; squash merge `8a8b63cf52d1b4d81b430db8caa5cb1e8b5eda94` passed post-merge CI #2438.

Hardware profiles remain **declared measurement provenance**, not proof that a runtime actually used the declared CPU/GPU/backend/count or honored topology/affinity. Actual invocation/config/telemetry remains separate evidence. New backend classes or parallelism semantics must enter through explicit evidence-contract updates rather than arbitrary JSON labels.

Durable rationale: `docs/research/2026-08-30-tts-bench-method-admission.md`, `docs/research/2026-08-31-tts-cpu-count-provenance.md`, and `docs/research/2026-08-31-tts-accelerator-count-provenance.md`.

## Fresh ecosystem radar — 2026-08-31

- **LightX2V** public `main` remains `7b8a96cc0a3a561824a5e6a8807ba7fae0984ea6` (`Update scripts (#1452)`, 2026-08-28). No Hottop-measured continuity/quality/runtime gain exists for the tested Wan2.2 I2V subset; keep the tested pin and do not freshness-only repin.
- **Qwen3-TTS official** public `main` remains `022e286b98fbec7e1e916cb940cdf532cd9f488e`. No fresh official change removes the operator-local 1.7B model/runtime gate.
- Public Qwen3-TTS serving benchmarks continue to report concrete hardware scale and concurrency. Hottop uses this only as methodology context; public performance numbers are not imported as Hottop benchmark evidence.
- No candidate in this cycle clears admission strongly enough to replace the guaranteed software3d route, tested LightX2V/Wan2.2 operator route or prepared local 1.7B TTS candidates.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, generate at least two subject-bearing shots and require complete byte-bound **identity + requested-action motion** evidence before composition.
3. When an operator provisions qwentts.cpp, CrispASR, audio.cpp or Pure-C plus exact Qwen3-TTS 1.7B CustomVoice assets, run the corresponding read-only artifact preflight first; then perform same-line Mandarin generation and inspect it with the generation + hardware + execution-shape coherence gates above. Preserve actual invocation/config separately from declared benchmark profiles.
4. Continue targeted ecosystem radar around measured gaps. Do not add freshness-only pins, large dependencies, hosted paid fallbacks or provider abstraction without measurable value and rollback.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. live `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. continue the highest-value safe action autonomously.
