# Hottop Status

Last updated: 2026-08-31
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest merged production point is **`main@3489a9321a0cdeb3708a652c88cb2d5e408fc000`** (`fix: fail closed on stale LightX2V preflight outputs`, PR #361), SHA-locked squash-merged from exact verified head `b393171deecdca600a6a21b867571da2e8802578`.

TDD/prod evidence for the fresh-target cleanup workstream:

- RED `ff80188c7cd70d12c7c459177325076148738c96`: CI #2554 failed the new regression contract proving the old implementation could leave a previous MP4/artifact manifest when a fresh LightX2V invocation failed local preflight;
- GREEN `b393171deecdca600a6a21b867571da2e8802578`: exact-head CI #2555 succeeded;
- the same GREEN head passed production-smoke #275, executing both checked-in anti-polish cow and cinematic Odyssey zero-cost production paths and final media/provenance verification;
- the same GREEN head passed cinematic-delivery-smoke #142, executing the 720p24 Odyssey delivery, runtime provenance capture, final-media/provenance verification and evidence upload;
- draft PR #360 preserved RED/GREEN history but could not be marked ready because the connected GitHub Ready mutation failed with a connector-side GraphQL schema error; GitHub REST correctly refused merging a draft, so the unchanged exact verified head was reopened as non-draft PR #361 and SHA-locked squash-merged as `3489a9321a0cdeb3708a652c88cb2d5e408fc000`.

A fresh `run_lightx2v_shot()` now invalidates the requested MP4 and optional artifact-manifest target **before** local LightX2V preflight. A failed fresh invocation therefore cannot leave stale prior-run media/provenance at the requested paths. Durable implementation/evidence record: `docs/research/2026-08-31-lightx2v-fresh-target-cleanup.md`.

The immediately preceding bounded-runtime work remains valid: PR #358 merged as `6d2c3cdc3f8e289b29b7bcb2a75a4552f37f2ecc` after exact-head CI #2550, production-smoke #273 and cinematic-delivery-smoke #140. LightX2V inference remains network-offline, no-auto-provisioning and bounded by positive `generation_timeout_seconds`, with timeout deleting partial expected output and becoming `LightX2VError`.

Exact request/reference provenance work also remains in force: accepted LightX2V artifacts bind `model_cls`, `task`, `seed`, `prompt`, `negative_prompt`, generation-config bytes, source revision and, for rights-safe I2V, exact reference SHA-256 + byte size + rights classification. Source/config/reference mutation fails closed.

`PROJECT.md` is intentionally unchanged for the fresh-target cleanup: stale-evidence invalidation is implementation closure under already-canonical fail-closed artifact-byte/provenance doctrine, not a new durable direction.

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

Primary operator route remains **LightX2V/Wan2.2**. Input locks are constraints, not output proof. Generated continuity evidence binds exact reference bytes, generated-shot bytes, plan semantics, exact generation-request identity, generator/source/config provenance when independently verifiable, evaluator identity/revision and fail-closed thresholds.

For every subject explicitly evaluated, evidence must cover all byte-bound subject-bearing plan shots; partial/cherry-picked coverage fails closed. Multi-subject integrity remains fail closed across subject IDs, distinct reference/generated bytes, plan hashes and candidate/source/config provenance.

**Identity fidelity and requested-action/motion fidelity remain separate dimensions.** Motion/anti-copy evidence binds exact ordered plan semantics. Runtime success, a request digest or generic motion never proves requested action, subject identity or semantic correctness.

For rights-safe I2V, Hottop captures reference SHA-256 + byte size before LightX2V, re-checks the same resolved file after generation, deletes output on mutation, and persists `reference_sha256`, `reference_size_bytes` and `reference_rights` after quality acceptance. Newly accepted artifacts also bind canonical request identity over model/task/seed/prompts. Source provenance continues to fail closed on dirty tracked code, untracked/ignored importable runtime code, escaping tracked symlinks, source-revision drift and generation-config byte drift.

LightX2V inference is time-bounded, network-offline, no-auto-provisioning, and now fresh-target fail-closed. These execution controls do not substitute for output-side identity, requested-motion, media-quality or provenance gates.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated.

Prepared local candidates remain qwentts.cpp, CrispASR, audio.cpp and Pure-C for 1.7B CustomVoice, plus the lower-hardware 0.6B ncnn benchmark candidate. All remain operator-provisioned and no-auto-download.

Comparable `inspect-tts-benchmark` evidence still requires exact text/language/supported speaker, canonical generation protocol, coherent hardware/execution shape, cold/warm independent trials, one runtime + one model revision per candidate, finite positive latency, distinct resolved WAV paths, PCM integrity and `listening_required=true`.

## Fresh ecosystem radar — 2026-08-31

- **LightX2V** public `main` remains `2ea24fe794f3bc488d9cd9473cc97d6094bbf00f`, committed 2026-08-31 11:57:20 UTC. The tip restores SeedVR distributed-op exports and reports SeedVR2 BF16/FP8 validation; it does not provide Hottop-measured Wan2.2 I2V identity, requested-motion, continuity or output-quality gain for the tested route. Continue **no freshness-only repin**.
- The existing path-specific LightX2V field report about meaningless I2V color blocks continues to support independent output quality gates; it is not treated as a project-wide defect claim.
- **5uck1ess/tts-bench** was reviewed as a benchmark-harness candidate. Its harness code is MIT, while its LICENSE explicitly separates each model's license from the bench-code license. Its repository/install surface is large and it has not yet demonstrated measurable superiority over Hottop's existing provenance/coherence benchmark contract, so it remains radar-only: no vendoring, auto-install or model download.
- **Qwen3-TTS official** remains a prepared operator-owned benchmark route rather than an unattended dependency. Existing same-line A/B, speaker/onset, bounded-generation and final PCM gates remain in force.
- No candidate in this cycle clears admission strongly enough to replace the guaranteed software3d route, tested LightX2V/Wan2.2 operator route or prepared local TTS candidates.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. The next true LightX2V quality milestone is **real generated media**, not more provider abstraction. When a reviewed local checkout, Wan2.2 model and suitable GPU are genuinely operator-provisioned, run fail-closed preflight and generate at least two subject-bearing rights-safe I2V shots under the bounded-runtime + fresh-target contract.
3. Require complete byte-bound **identity + requested-action motion + media quality + exact request/source/config/reference provenance** before composition.
4. A suitable NVIDIA GPU availability check remains a measured local-preflight hardening gap; implement it only with an explicit injectable/testable runtime contract that does not weaken real production fail-closed behavior or force GPU presence in ordinary unit tests.
5. When an operator provisions local Qwen3-TTS 1.7B runtime/model, run read-only preflight and same-line Mandarin generation under existing provenance/coherence gates.
6. Continue targeted ecosystem radar around measured gaps. Do not add freshness-only pins, large dependencies, hosted paid fallbacks or provider abstraction without measurable value and rollback.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. live `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. continue the highest-value safe action autonomously.
