# Hottop Status

Last updated: 2026-08-27
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot, not a self-updating `main` pointer. Always recover `PROJECT.md` first and re-fetch GitHub before exact branch/head/CI claims.

## Current verified repository truth

Live recovery on 2026-08-27 found `main@d53a472ab5fea2a0c0dde8e302762486cb1e20d8` with no open PRs before this status/charter sync branch was created.

That `main` commit, **feat: add reusable creative reference memory**, passed:

- CI **#1870** on Python 3.11/3.12;
- cinematic-delivery-smoke **#64** for the checked-in 720p Odyssey production route.

The merged creative-memory capability adds structured positive/negative case retrieval, user-feedback/promotion lessons, a search CLI and durable guardrails. Fresh hotspot/mechanism analysis remains authoritative; historical examples are retrieved for causal mechanism/native grammar/product-role/negative guardrails, never as visual templates and never as a substitute for current research.

This workstream also corrects a charter drift: `PROJECT.md` now explicitly classifies the system as **retrieval + few-shot/preference memory, not RL**, adds `skills/creative-reference-memory/SKILL.md` to canonical recovery, inserts memory retrieval after current hotspot analysis and before ideation, and records the durable no-template rule in the decision log.

## Guaranteed zero-cost production baseline

The unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

The baseline remains free of GPU/model requirements, paid fallback, credentials and implicit multi-GB downloads. Production evidence continues to enforce meaningful pixel motion, mobile framing/subtitle readability, dialogue/audio coverage, transition/seam quality, byte-bound shot provenance, composition-time byte verification, runtime provenance and final-media verification.

Anti-Polish may remain intentionally crude; lower-roughness cinematic profiles must remain presentable. Roughness never relaxes continuity, timing, Mandarin intelligibility, product semantics, rights/evidence safety or encoding integrity.

## Creative-memory boundary

Canonical artifacts:

- `integrations/creative-reference-library.yml`;
- `src/hottop/creative_memory.py`;
- `src/hottop/creative_memory_cli.py`;
- `skills/creative-reference-memory/SKILL.md`;
- `docs/creative/creative-reference-memory.md`;
- `docs/decisions/2026-08-27-creative-reference-memory.md`.

Operational rule:

1. resolve product/current hotspot first;
2. extract current recognition hook + causal/visual/dialogue/audio grammar;
3. retrieve similar mechanisms/native grammar/product roles and negative guardrails when useful;
4. use positives as reasoning exemplars, negatives as guardrails;
5. reject any direction that is merely a prior layout/character/scene/punchline with names swapped;
6. run normal creative review + generation preflight;
7. add durable user feedback/performance evidence back to memory only when real evidence exists.

Current creative memory is not RL. SFT/DPO/reward-model/RL work remains deferred until enough clean, rights-safe, labeled data and measured value exist.

## Neural-TTS quality boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the admitted operator-owned delivery-controlled benchmark candidate; current reviewed 0.6B does not preserve role-aware `instruct` semantics and must not silently discard delivery control. CosyVoice3 remains correctness-gated, not a default route.

Shared local neural-TTS integrity remains fail-closed on **non-empty + finite + serialized-PCM non-silent** output before WAV creation. Routed Qwen dialogue additionally uses a planned-duration generation token ceiling as resource protection and an exact produced-PCM duration gate as the authoritative slot-fit contract.

A real same-line Qwen3-TTS 1.7B Mandarin A/B still requires an already-provisioned local model/runtime plus publication-rights review. No automatic model download or GPU provisioning is allowed.

## Generated/reference-conditioned quality boundary

The highest-value generated-quality proof remains a rights-safe reference-conditioned multi-shot identity benchmark. Input identity/reference locks are constraints, not proof.

- LightX2V/Wan2.2 remains the tested operator-owned local base route; no freshness-only repin without measured Hottop value.
- Stand-In/Wan2.2 and Memento-style continuity routes remain benchmark candidates, not automatically installed defaults.
- Actual generator source revision, model/checkpoint identity when independently verifiable, exact reference bytes, generated shot bytes and evaluator revision remain separate provenance dimensions.
- Complete subject-bearing shot coverage is required for any cross-shot identity claim.

Do not fabricate DGX readiness. GPU/driver/CUDA/PyTorch/model/reference state must be probed on the actual operator machines before a generated-quality claim.

## Fresh ecosystem radar — 2026-08-27

Targeted scan against the current two measured gaps did not justify a provider switch or freshness-only repin.

### Qwen3-TTS

Official `QwenLM/Qwen3-TTS` `main` remained at `022e286b98fbec7e1e916cb940cdf532cd9f488e` in this run (upstream commit dated 2026-03-17), so there is no new official source change that alters Hottop's reviewed 1.7B operator-local gate.

SGLang-Omni's Aug. 23 Qwen3-TTS benchmark work reports that Talker `torch.compile` produced no reproducible end-to-end gain under the fixed protocol and was removed; CUDA Graph remained enabled. This reinforces Hottop's existing rule that acceleration/admission requires measured end-to-end evidence, not an optimization toggle or popularity claim.

Community self-hosted Qwen wrappers continue to exist, but at least some auto-download models on first use; that behavior is incompatible with normal unattended Hottop execution and is not admitted into `video-run`.

### Wan2.2 / LightX2V

`ModelTC/LightX2V` `main` advanced to `79842681ae93ff2bff3b72e7fa7316b381050a09` on 2026-08-27 with `config: normalize paths and clean up fields (#1448)`. This is active maintenance but supplies no Hottop-measured quality/runtime improvement to the tested Wan2.2 I2V subset, so it does **not** justify a freshness-only repin.

Recent Wan2.2 ecosystem work also continues to expose correctness-sensitive runtime details such as HIGH/LOW A14B LoRA expert routing. Hottop's currently tested route does not rely on those community LoRA pairs, so this is a cautionary quality/provenance signal, not evidence for a new dependency.

No scanned candidate supplied a measured Hottop improvement strong enough to justify a new runtime, large dependency or model download in this run.

## Immediate next actions

1. Finish this `PROJECT.md` + `STATUS.md` canonical-memory sync through exact-head CI/PR review and merge if green.
2. Continue inspecting fresh real cow/Odyssey production evidence and modify deterministic visuals/audio only for a **measured** defect; do not tune framing, lighting, transitions or loudness from aesthetics alone.
3. Once a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, run at least two subject-bearing Odyssey I2V shots and require meaningful motion plus complete subject-bound continuity evidence before composition.
4. When operator-local Qwen3-TTS 1.7B is genuinely provisioned, run same-line Mandarin A/B against the guaranteed fallback and promote it only on measured intelligibility/delivery/naturalness evidence plus publication-rights review.
5. Continue targeted ecosystem radar around the measured gap. Do not add freshness-only pins, large dependencies or provider abstraction without measurable value and rollback.
6. For fresh creative output, continue live hotspot/mechanism analysis first; consult creative memory only after current context is resolved.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills, including `creative-reference-memory` when prior cases can help.
4. newest relevant spec/plan/decision/research record.
5. current `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. fresh hotspot/mechanism analysis for new creative generation.
8. creative-memory retrieval when useful, after current context is resolved.
9. continue the highest-value safe action autonomously.
