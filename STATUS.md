# Hottop Status

Last updated: 2026-08-31
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot. Always re-fetch live GitHub state before exact branch/head/CI claims; recorded SHAs are historical evidence points, not a self-updating `main` pointer.

## Current verified repository truth

Latest merged production point is **`main@2e60742e47a9fcc85c35c948a881c8be85ba1bd1`** (`fix: bind LightX2V I2V reference provenance`), SHA-locked squash-merged from PR #354 after exact-head verification.

TDD/prod evidence for that merge:

- RED `8bc6b7f3e1054c3f348a964440574b0ed88cccc9`: CI #2533 failed exactly on the new I2V artifact-manifest contract because accepted LightX2V output did not yet persist the conditioning reference SHA-256, byte count and rights classification;
- final GREEN PR head `9d6581ddeedaf60f131b5aee93ebf5cfb4cab52c`: exact-head CI #2535 succeeded on Python 3.11/3.12, production-smoke #264 succeeded, and cinematic-delivery-smoke #131 succeeded;
- production-smoke #264 executed both checked-in anti-polish cow and cinematic Odyssey production paths and verified their final media/provenance chains;
- cinematic-delivery-smoke #131 executed the real 720p24 Odyssey delivery, captured media runtime provenance, verified delivery media/provenance and uploaded evidence;
- reviewed diff was additive only: 73 additions, 0 deletions across `video_artifacts.py`, `video_lightx2v.py` and the LightX2V tests;
- SHA-locked squash merge: `2e60742e47a9fcc85c35c948a881c8be85ba1bd1`.

The immediately preceding reference-stability merge remains useful historical evidence: PR #352 reached final head `2a27134cde4278af1e6632d67eaa6455e63be028`, where CI #2529, production-smoke #261 and cinematic-delivery-smoke #128 all succeeded before squash merge `bf1ca8ad21d894fe63c654e6d3285529ed889efa`. PR #353 then synchronized STATUS and merged as `0c962af8cf5df0f32a2c8626689126a1d74490c1` after CI #2531.

Previous retained production evidence remains valid: `main@bbe129b695eb253c505790a1cef886be51e4ae6b` passed post-merge CI #2513, production-smoke #255 and cinematic-delivery-smoke #122, including the real 720p24 Odyssey delivery, media runtime provenance capture, final media/provenance verification and evidence upload.

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

Primary operator route remains **LightX2V/Wan2.2**. Input locks are constraints, not output proof. Generated continuity evidence binds exact reference bytes, generated-shot bytes, plan semantics, generator/source/config provenance when independently verifiable, evaluator identity/revision and fail-closed thresholds.

**Benchmark scope is explicit.** Incidental or single-shot reference-bearing subjects do not automatically become continuity targets. For every subject that is explicitly evaluated, however, evidence must cover **all** byte-bound subject-bearing plan shots for that subject; partial/cherry-picked coverage fails closed.

Multi-subject integrity remains fail closed: unique evidence subject IDs, distinct reference bytes for distinct subjects, distinct generated artifact bytes across distinct subjects, subject-matched plan hashes, and matching candidate/source/generation-config provenance.

**Identity fidelity and requested-action/motion fidelity remain separate dimensions.** Motion/anti-copy evidence binds `motion_spec_sha256` from exact ordered subject-bearing plan semantics. Runtime success or generic motion never proves requested action or subject identity.

LightX2V I2V now closes both the local reference race and the durable evidence gap. For rights-safe I2V, Hottop captures the resolved reference image SHA-256 and byte size before spawning LightX2V, re-reads the same resolved file after generation returns, and deletes the generated output if the reference was replaced, deleted or otherwise changed. After quality acceptance, the shot artifact manifest also persists the exact `reference_sha256`, `reference_size_bytes` and `reference_rights` as one all-or-none provenance tuple. This makes the accepted artifact identify the exact reference bytes and rights classification that conditioned generation instead of leaving that fact only in process memory. T2V and older manifests remain compatible because these fields are optional when no reference input exists.

The new manifest binding does **not** prove output continuity, identity fidelity, requested-action motion or semantic correctness. Those remain independent generated-media gates. It adds no provisioning, model download, network route, paid dependency or provider surface and is fully regression-testable with a local fake operator checkout.

LightX2V source provenance continues to fail closed across all reviewed execution surfaces: inherited `PYTHONPATH` is isolated to the operator checkout root; dirty tracked code and untracked/ignored importable runtime code are rejected; tracked symlinks resolving outside the checkout are rejected before generation because their target bytes are not bound by Git HEAD; exact local source revision is captured before spawn and re-verified after generation; generation config bytes are captured/re-verified; a post-generation provenance failure deletes output instead of accepting a manifest. Internal tracked symlinks resolving inside the checkout remain admissible. Durable rationale: `docs/research/2026-08-31-lightx2v-source-provenance.md`.

The current pre/post byte checks are a fail-closed stability contract for normal operator execution, not a claim of protection against a hostile concurrent process that mutates an input and restores the exact original bytes before the post-check. Stronger immutable-snapshot/process-isolation work should only be admitted when a concrete runtime threat or measured benefit justifies its operational cost.

Continuity benchmark rationale: `docs/research/2026-08-25-reference-continuity-evaluator-radar.md`.

## Dialogue / neural-TTS boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the higher-quality operator-owned benchmark target; CosyVoice3 remains correctness-gated.

Prepared local candidates remain qwentts.cpp, CrispASR, audio.cpp and Pure-C for 1.7B CustomVoice, plus the lower-hardware 0.6B ncnn benchmark candidate. All remain operator-provisioned and no-auto-download.

Comparable `inspect-tts-benchmark` latency/RTF evidence requires exact text/language/supported speaker, canonical generation protocol, recognized hardware backend with coherent CPU/device count, recognized `cli`/`server` execution shape, server worker/thread topology when applicable, cold/warm independent trials, one runtime revision + one model revision per candidate, finite positive latency, distinct resolved WAV trial paths, WAV/PCM integrity and `listening_required=true`. Hardware/execution profiles remain declared measurement provenance rather than proof of actual runtime utilization.

Durable method: `docs/research/2026-08-30-tts-bench-method-admission.md` plus the 2026-08-31 CPU/accelerator provenance records.

## Fresh ecosystem radar — 2026-08-31

- **LightX2V** public `main` advanced to `6f3c491bbf73ddf113f3da95da7e96f5a0649dd0` (2026-08-31 10:57 UTC). The tip optimizes Ulysses FP8 pre-quant row tiling/communication; the immediately preceding `d6cf4f13d152e636ae6daac604d46531077e8670` refactors ERNIE Image runner aliases. Neither change supplies Hottop-measured Wan2.2 I2V identity, requested-motion, continuity or output-quality gain for the tested operator route. Keep the tested pin and continue **no freshness-only repin**.
- A June 19, 2026 LightX2V issue reports one official Wan2.2-TI2V-5B I2V path producing meaningless color blocks for that reporter. Treat this as a path-specific field report, not a project-wide defect claim; it reinforces Hottop's rule that runtime success is insufficient and generated video must pass independent motion/semantic/media quality gates.
- **Qwen3-TTS official** remains `022e286b98fbec7e1e916cb940cdf532cd9f488e`. A fresh MLX-Audio report isolates progressive long-text pace acceleration to the Base ICL/reference-cloning path while CustomVoice preset speech stayed stable in that report. Treat it as runtime/path-specific evidence, not a defect claim against Hottop's CustomVoice route; the existing same-line A/B, speaker/onset, bounded-generation and final PCM gates remain appropriate.
- No candidate in this cycle clears admission strongly enough to replace the guaranteed software3d route, tested LightX2V/Wan2.2 operator route or prepared local 1.7B TTS candidates.

## Immediate next actions

1. Keep the guaranteed software3d path unchanged unless fresh MP4 evidence shows a measured defect.
2. Continue LightX2V/reference-continuity work only around concrete, reproducible execution/provenance/output gaps; the next true quality milestone is generated media, not more provider abstraction.
3. When a reviewed local LightX2V/Wan2.2 checkout, model and suitable GPU are genuinely provisioned, run the fail-closed local preflight, generate at least two subject-bearing I2V shots from rights-safe references, and require complete byte-bound **identity + requested-action motion + media quality** evidence before composition.
4. When an operator provisions a local Qwen3-TTS 1.7B runtime/model, run the read-only artifact preflight first, then same-line Mandarin generation under existing generation/hardware/execution-shape coherence gates.
5. Continue targeted ecosystem radar around measured gaps. Do not add freshness-only pins, large dependencies, hosted paid fallbacks or provider abstraction without measurable value and rollback.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills.
4. newest relevant spec/plan/decision/research record.
5. live `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. continue the highest-value safe action autonomously.
