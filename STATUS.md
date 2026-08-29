# Hottop Status

Last updated: 2026-08-30
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest verified production evidence point: **`main@370dd5162f5ef5cc05e9ee4c39e939580a029c5b`**. Post-merge CI **#2151** passed on Python 3.11/3.12. Live GitHub state must still be re-fetched on every recovery.

### audio.cpp Qwen3-TTS 1.7B operator route

The candidate remains `benchmark_candidate / integration_ready=false / runtime_status=unprobed / self_owned_compute`. No normal `video-run`, automatic runtime/model download, model conversion, dependency build, container pull, GPU provisioning, credentials or paid path is admitted.

Existing read-only command:

`hottop-models probe-audio-cpp --executable <audiocpp_cli> --model-dir <Qwen3-TTS-12Hz-1.7B-CustomVoice>`

It binds an already provisioned local executable plus `model.gguf` and `speech_tokenizer/model.gguf` using resolved-target binding, bounded-memory SHA-256, stable before/after filesystem snapshots, executable permission, GGUF v3 fixed-header checks, non-zero tensor counts and incompatible-role path/byte distinctness. `ready=true` is only benchmark-input readiness; it does not prove checkpoint identity, licensing, speaker capability, runtime success, Mandarin quality or publication rights.

This cycle added a reviewed **manual prebuilt-runtime option** without widening unattended behavior:

- source capability audit remains pinned separately at `0xShug0/audio.cpp@a76ec04f620da829e4a53032247369083ba1ad45`;
- official release `v0.7.0` maps to commit `d2ff37009c69d464bcab6aa4a44a13746e84a914`, Apache-2.0 source at that revision;
- reviewed Ubuntu CPU archive: `audio-v0.7.0-bin-ubuntu-x64-cpu.tar.gz`, SHA-256 `400774c3f92f3da4c5fedfa2e43d50482e951ec288eb39e66c10e63fb46de47d`, 39,878,502 bytes;
- reviewed Ubuntu Vulkan archive: `audio-v0.7.0-bin-ubuntu-x64-vulkan.tar.gz`, SHA-256 `e49676f1da28df0d2a6ca2073118964e91f3d14aa3c2ca3ad984e3d09b96932d`, 66,981,995 bytes;
- upstream release workflow enables the native model manager, so normal Hottop must **not** use it to fetch models. A release digest proves only runtime-archive identity; the extracted executable still goes through local preflight and real Qwen capability/audio quality remain separate execution gates.

TDD/merge evidence:

- RED `4fde05b086cd8a4d3330d38d3127f9dbad8669f3` → CI **#2147**: Ruff passed; pytest failed before reviewed-prebuilt provenance existed.
- GREEN/docs exact head `bb1e88fcb32531f82670fc3008a2a574e115a770` → CI **#2149**: Python 3.11/3.12 Ruff + full pytest passed.
- ready-for-review hit the known GitHub connector `fullDatabaseId` GraphQL compatibility failure; draft #225 was closed and non-draft #226 recreated on the **same verified exact head**, with no force/update-ref/history rewrite.
- PR #226 squash-merged as `370dd5162f5ef5cc05e9ee4c39e939580a029c5b`; post-merge CI **#2151** passed on Python 3.11/3.12.

## Canonical guaranteed baseline

Unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

`ZERO_COST_MODE=true` remains canonical. The guaranteed route uses no GPU/model, credentials, paid fallback or implicit multi-GB download. Existing evidence covers meaningful motion, mobile framing/subtitle readability, dialogue/audio coverage, seam quality, shot-byte provenance, composition-time byte verification, runtime provenance and final-media verification.

Latest retained deterministic smoke evidence:

- cow final MP4: 15.0 s H.264/yuv420p + AAC, SHA-256 `8c23e3ea76dad18d5d2092e52b944365f267df363a16e9624db08a5be0e339b5`, seam max delta `4.431528`, max seam/intra ratio `3.622543`;
- Odyssey final MP4: 15.0 s H.264/yuv420p + AAC, SHA-256 `f30a15c8e146f07d2bae8416a7bae3ebe5a54cfb5cb65bac5fbb82f6ac39795c`, seam max delta `5.196111`, max seam/intra ratio `3.038082`;
- 720×1280/24 fps Odyssey: final SHA-256 `c1353b556cb8675b94e58bb1d41624c69b4711ad1b83c690f1e81dd60b3f58df`, seam max delta `4.184792`, max seam/intra ratio `4.480971`, with bound CPU/NumPy/OpenBLAS/FFmpeg/FFprobe/eSpeak-NG/font provenance.

Do not retune deterministic cow/Odyssey visuals or audio without a measured artifact defect.

## Reference-conditioned continuity boundary

Input locks are constraints, not output proof. Generated continuity evidence must cover all subject-bearing plan shots and bind exact reference bytes, generated shot bytes, generator/model/source provenance when independently verifiable, and evaluator identity/revision.

**Identity fidelity and requested-action/motion fidelity are separate dimensions.** Motion/anti-copy evidence binds `motion_spec_sha256` derived from exact ordered subject-bearing plan semantics; generic motion cannot prove a different requested action.

Primary operator route remains **LightX2V/Wan2.2**. Stand-In, Aura, Wan-Animate-2, UnityVideo, DomainShuttle, MV-S2V, SMRABooth, ID-V2V, WildActor and other reviewed candidates remain benchmark/research-only unless exact source/checkpoint rights, operator runtime and output evidence clear admission. Runtime success never substitutes for identity, requested motion, geography, provenance or final-media proof.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated.

Current local benchmark candidates include:

- `qwen3-tts-qwentts-cpp-1b7` — read-only GGUF artifact preflight available;
- `qwen3-tts-crispasr-1b7` — read-only GGUF artifact preflight available;
- `qwen3-tts-audio-cpp-1b7` — read-only CustomVoice model-directory preflight available plus reviewed v0.7.0 manual runtime-archive provenance; **no production runtime adapter admitted**;
- `qwen3-tts-ncnn-0b6` — lower-hardware 0.6B CPU/Vulkan benchmark candidate only.

Future 1.7B cross-runtime A/B must bind exact source/build/backend or reviewed prebuilt digest, checkpoint capability mode, model/tokenizer/GGUF bytes, the **same Mandarin line**, the same checkpoint-supported preset speaker, seed/sampling/generation ceiling, cold/warm trial identity, every WAV's SHA-256/size/duration/PCM integrity, latency/RTF, repeated speaker consistency, short-onset stability, intelligibility/naturalness and publication-rights posture.

Unsupported speaker/voice/instruction/reference conditioning must fail closed before execution. Reference-audio cloning remains separately rights-gated.

## Fresh ecosystem radar — 2026-08-30

- **LightX2V/Wan2.2:** upstream `main` remains `7b8a96cc0a3a561824a5e6a8807ba7fae0984ea6`. Latest reviewed changes remain example-path cleanup plus H3/XPU-specific work and do not provide Hottop-measured continuity/quality/runtime improvement for the tested Wan2.2 I2V route. Keep the tested pin; no freshness-only repin.
- **Qwen3-TTS:** reviewed official `main` remains `022e286b98fbec7e1e916cb940cdf532cd9f488e`; no reviewed official change justifies altering the 1.7B operator-local benchmark gate.
- **audio.cpp:** upstream `main` has advanced to `e73c980fe259aa2b3931c8b6ea53517e769877ec`, including release/documentation/runtime maintenance after v0.7.0. Hottop keeps the separate source capability audit at `a76ec04f...` because no measured contract requires a freshness-only repin. The v0.7.0 official Ubuntu CPU/Vulkan archives are now exact-digest-reviewed manual operator options only.
- **qwentts.cpp/CrispASR:** existing admissions remain unchanged. Auto-download/build paths stay forbidden in unattended Hottop execution.

No reviewed candidate in this cycle clears admission strongly enough to replace the guaranteed software3d route or current tested LightX2V/Wan2.2 operator route.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. When a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, generate at least two subject-bearing shots and require complete byte-bound **identity + requested-action motion** evidence before composition.
3. If an operator provisions qwentts.cpp or CrispASR plus exact 1.7B CustomVoice GGUF assets locally, run the existing read-only preflight first; only after it passes may a separate explicit same-line Mandarin A/B execute.
4. For audio.cpp, an operator may manually provision the reviewed v0.7.0 Ubuntu CPU/Vulkan archive and verify its exact digest, or provide another independently reviewed build. Then run `probe-audio-cpp` against the extracted executable and independently reviewed local Qwen3-TTS 1.7B CustomVoice assets. Hottop itself must not fetch the runtime archive or invoke the bundled model manager.
5. In every 1.7B cross-runtime A/B, use the same line, supported preset speaker and bounded generation settings, and preserve repeated speaker/onset/intelligibility/naturalness/RTF/PCM/provenance as separate evidence dimensions.
6. Continue targeted ecosystem radar around measured gaps. Do not add freshness-only pins, large dependencies, hosted paid fallbacks or provider abstraction without measurable value and rollback.
7. For fresh creative generation, resolve current source-event + active derivative meme first, then use creative memory only as mechanism/grammar/guardrail support.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills, including creative-reference memory when prior cases can help.
4. newest relevant spec/plan/decision/research record.
5. live `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. continue the highest-value safe action autonomously.
