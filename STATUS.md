# Hottop Status

Last updated: 2026-08-30
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest verified pre-workstream evidence point: **`main@fd4afd7792ee609125ed27858459f5896225e071` / CI #2320** on Python 3.11/3.12. The current TTS execution-mode contract has exact-head GREEN through `1ba281e0b9d3f282346f9c8427c5f740abb59d39` / CI #2323; live `main` must still be re-fetched after merge before any post-merge claim.

## TTS benchmark coherence contract

`hottop-models inspect-tts-benchmark --spec <benchmark.json>` now treats latency/RTF as comparable evidence only when the following are bound:

1. exact text, language and checkpoint-supported preset speaker;
2. one concrete generation protocol for the benchmark, canonical SHA-256, integer seed, positive `max_new_tokens` ceiling and at least one explicit sampling control;
3. one concrete hardware profile for the benchmark, canonical SHA-256 and nonblank backend/device identity;
4. **backend/device coherence**: `cpu` requires a CPU identity; accelerator backends (`cuda`, `rocm`, `hip`, `vulkan`, `metal`, `mps`, `xpu`) require a GPU or generic accelerator identity;
5. **one recognized execution profile for the benchmark**, canonical SHA-256, `mode` restricted to `cli` or `server`, positive concurrency and positive batch size; `server` mode additionally requires a connection strategy;
6. at least one cold and one warm trial per candidate, with additional independent warm repeats allowed;
7. one exact runtime revision per candidate;
8. one exact model/checkpoint revision per candidate;
9. finite positive latency plus distinct resolved WAV artifact paths, byte identity and WAV/PCM integrity;
10. `listening_required=true`, keeping naturalness, speaker consistency and onset stability independent from speed/stream integrity.

The generation, hardware and execution profiles are **declared measurement provenance, not proof that the runtime internally obeyed the declaration**. Operator execution records and actual CLI/config provenance remain separately required. Candidates intentionally measured on incompatible hardware or execution shapes belong in separate evidence sets rather than one latency/RTF ranking. A future execution shape beyond `cli` or `server` requires an explicit evidence-contract extension before its timings can be called comparable.

### Latest TDD evidence

- hardware/backend mismatch RED `19b72add6a1bd166de088a3ab52a31520caab25c`, **CI #2304**: Ruff passed; pytest produced exactly **2 failed / 580 passed**;
- hardware/backend coherence GREEN `a9917c5a527da0e9ac217710936ab84f4c140256`, **CI #2305**: Python 3.11/3.12 Ruff + full pytest passed;
- execution-profile RED `26248bd4bdd22189c7e029d919a2992050ab5a48`, **CI #2306**: Ruff passed; pytest produced exactly **4 failed / 582 passed**;
- first execution-profile implementation `692853cd973521dab8924710ee0c89e22c26e84f`, **CI #2307**: new contracts passed; only legacy ready-fixtures lacking the newly mandatory profile failed, so fixtures were migrated rather than weakening the gate;
- prior execution-shape branch head `94159e33eb6d1839fcfde4c9dde43bdc166c8feb`, **CI #2316**: Python 3.11/3.12 Ruff + full pytest passed;
- prior execution-shape merge `903b9b406d73bf5b91de8fd472224e90900667bf`, post-merge **CI #2318**: both Python versions passed;
- unknown-mode RED `9c461ba07b2993993083b22ca33a965457f6f384`, **CI #2321**: Ruff passed and pytest failed on the new contract, proving an invented nonblank mode could become ready;
- unknown-mode GREEN `45f25e47329e17dab997ac46318980edfab3797e`, **CI #2322**: Python 3.11/3.12 Ruff + full pytest passed;
- durable-record head `1ba281e0b9d3f282346f9c8427c5f740abb59d39`, **CI #2323**: Python 3.11/3.12 Ruff + full pytest passed.

Durable rationale: `docs/research/2026-08-30-tts-execution-shape-evidence.md`.

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

Input locks are constraints, not output proof. Generated continuity evidence must cover **all subject-bearing shots** and bind exact reference bytes, generated shot bytes, generator/model/source provenance when independently verifiable, evaluator identity/revision and fail-closed thresholds.

**Identity fidelity and requested-action/motion fidelity are separate dimensions.** Motion/anti-copy evidence binds `motion_spec_sha256` from exact ordered subject-bearing plan semantics. Generic motion cannot prove a different requested action.

Primary operator route remains **LightX2V/Wan2.2**. Reviewed alternatives remain benchmark/research-only unless exact rights, local runtime and same-sequence output evidence clear admission. Runtime success never substitutes for identity, motion, geography, provenance or final-media proof.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated.

Prepared local benchmark candidates remain:

- `qwen3-tts-qwentts-cpp-1b7` — hardened read-only GGUF artifact preflight;
- `qwen3-tts-crispasr-1b7` — read-only GGUF artifact preflight;
- `qwen3-tts-audio-cpp-1b7` — read-only CustomVoice model-directory preflight;
- `qwen3-tts-ncnn-0b6` — lower-hardware 0.6B CPU/Vulkan benchmark candidate only.

Future 1.7B cross-runtime A/B must use the **same Mandarin line**, same checkpoint-supported preset speaker, semantically comparable generation controls, comparable hardware and comparable recognized execution shape, while preserving runtime/model/config provenance, cold/warm timing, distinct WAV instances, repeated speaker consistency, short-onset stability, intelligibility/naturalness and publication-rights posture. Unsupported conditioning fails closed; reference-audio cloning remains separately rights-gated.

## Fresh ecosystem radar — 2026-08-30

- LightX2V public `main` remains **`7b8a96cc0a3a561824a5e6a8807ba7fae0984ea6`**. The reviewed recent changes are Wan-Animate-2 example-path maintenance plus H3-specific Ref2V/XPU work; none provides Hottop-measured continuity/quality/runtime gain for the tested Wan2.2 I2V subset. Keep the tested pin; no freshness-only repin.
- Qwen3-TTS official `main` remains **`022e286b98fbec7e1e916cb940cdf532cd9f488e`**. No official change in this cycle removes the operator-local 1.7B benchmark gate.
- qwentts.cpp reviewed `master` remains **`a8a7716b530e49fed537c57711247c12fbbb903c`**. Its existing evidence that server connection/OpenMP-team and batch/concurrency shape can change performance continues to justify execution-shape binding; no new revision changes the current admission.
- No new candidate in this cycle clears admission strongly enough to replace the guaranteed software3d route, tested LightX2V/Wan2.2 operator route or prepared local 1.7B TTS candidates.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, generate at least two subject-bearing shots and require complete byte-bound **identity + requested-action motion** evidence before composition.
3. When an operator provisions qwentts.cpp, CrispASR or audio.cpp plus exact Qwen3-TTS 1.7B CustomVoice assets, run the corresponding read-only artifact preflight first; then perform same-line local WAV generation and inspect it with the generation + hardware + recognized execution-shape coherence contracts above. Retain the actual invocation/config separately because declared profiles are not execution proof.
4. Continue targeted ecosystem radar around measured gaps. Do not add freshness-only pins, large dependencies, hosted paid fallbacks or provider abstraction without measurable value and rollback.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. live `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. continue the highest-value safe action autonomously.
