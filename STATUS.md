# Hottop Status

Last updated: 2026-08-27
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable evidence-backed image/video production**

> `PROJECT.md` is durable doctrine. This file is the short-lived execution snapshot, not a self-updating `main` pointer. Always recover `PROJECT.md` first and re-fetch GitHub before exact branch/head/CI claims.

## Current verified repository truth

Latest verified `main` at this update is `ca74c568fad9b05fbebfba538f91eb153d57f2be`. It contains the canonical creative-reference-memory doctrine plus the follow-up status sync; exact-head CI **#1877** passed on Python 3.11/3.12. No pull request was open at the start of this status-sync workstream.

The reusable creative-memory capability is canonical in `PROJECT.md`. Hottop explicitly treats it as **retrieval + few-shot/preference memory, not RL**:

- fresh supplied/live hotspot evidence stays authoritative;
- current recognition hook + causal/visual/dialogue/audio grammar is resolved before memory retrieval;
- memory retrieves mechanisms, native grammar, product roles, real user/promotion lessons and negative guardrails;
- historical layouts, characters, scenes, punchlines and visual templates are never implicit generation defaults;
- SFT/DPO/reward-model/RL remains deferred until a sufficiently large clean rights-safe labeled corpus and measured value exist.

Canonical memory artifacts include `integrations/creative-reference-library.yml`, `src/hottop/creative_memory.py`, `src/hottop/creative_memory_cli.py`, `skills/creative-reference-memory/SKILL.md`, `docs/creative/creative-reference-memory.md` and `docs/decisions/2026-08-27-creative-reference-memory.md`.

## Guaranteed zero-cost production baseline

The unattended guarantee remains:

`checked-in render/config → software3d moving shots → Mandarin eSpeak-family dialogue + original synthetic music + procedural Foley → MoviePy → FFmpeg → verified H.264/AAC/yuv420p MP4`

It remains free of GPU/model requirements, paid fallback, credentials and implicit multi-GB downloads. Production evidence enforces meaningful pixel motion, mobile framing/subtitle readability, dialogue/audio coverage, transition/seam quality, byte-bound shot provenance, composition-time byte verification, runtime provenance and final-media verification.

Latest directly inspected 720p Odyssey evidence remains cinematic-delivery-smoke **#64** at `main@d53a472ab5fea2a0c0dde8e302762486cb1e20d8`; subsequent work through `main@ca74c568…` changed creative-memory/docs only, so the media pipeline is unchanged. The downloaded final artifact measured:

- 15.000 s H.264/yuv420p video at 720×1280 / 24 fps;
- 15.000 s stereo AAC at 44.1 kHz;
- seam max delta **4.184792**, max seam/intra ratio **4.480971**;
- no `-35 dB / 0.5 s` long-silence detection;
- integrated loudness about **-20.0 LUFS**, true peak about **-3.9 dBFS**;
- 1/3/5/7/9/11/13 s visual inspection found no new measurable framing, subtitle, transition or lighting regression.

Therefore no deterministic production tuning is justified from this run.

## Neural-TTS quality boundary

The eSpeak family remains the guaranteed local fallback. Qwen3-TTS 1.7B CustomVoice remains the admitted operator-owned delivery-controlled benchmark candidate; current reviewed 0.6B does not preserve role-aware `instruct` semantics. CosyVoice3 remains correctness-gated rather than a default route.

Shared local neural-TTS integrity remains fail-closed on **non-empty + finite + serialized-PCM non-silent** output before WAV creation. Routed Qwen dialogue also uses a planned-duration generation token ceiling as resource protection and an exact produced-PCM duration gate as the authoritative slot-fit contract.

A real same-line Qwen3-TTS 1.7B Mandarin A/B still requires an already-provisioned local model/runtime plus publication-rights review. No automatic model download or GPU provisioning is allowed.

## Generated/reference-conditioned quality boundary

The highest-value generated-quality proof remains a rights-safe reference-conditioned multi-shot identity benchmark. Input identity/reference locks are constraints, not proof.

- LightX2V/Wan2.2 remains the tested operator-owned local base route; no freshness-only repin without measured Hottop value.
- Stand-In/Wan2.2 and Memento-style continuity routes remain benchmark candidates, not automatically installed defaults.
- actual generator source revision, model/checkpoint identity when independently verifiable, exact reference bytes, generated shot bytes and evaluator revision remain separate provenance dimensions;
- complete subject-bearing shot coverage is required for any cross-shot identity claim.

Do not fabricate DGX readiness. GPU/driver/CUDA/PyTorch/model/reference state must be probed on actual operator machines before a generated-quality claim.

## Fresh ecosystem radar — 2026-08-27

Targeted checks against the two measured operator-quality gaps did not justify a provider switch or freshness-only repin.

### Qwen3-TTS

Official `QwenLM/Qwen3-TTS` `main` remains at `022e286b98fbec7e1e916cb940cdf532cd9f488e`. No new official source change alters Hottop's reviewed 1.7B operator-local gate.

Recent H100/H200 Qwen3-TTS benchmark evidence continues to support benchmark-first admission: an optional Talker `torch.compile` path failed to show reproducible end-to-end improvement under the fixed protocol and was removed. Community wrappers that auto-download models on first use remain inadmissible for normal unattended Hottop execution.

### Wan2.2 / LightX2V

`ModelTC/LightX2V` `main` advanced again on 2026-08-27 to `680d9be199a69ebe4a02f86bdd653f23298ac02d` with `cleanup: remove retired model remnants (#1449)`, immediately after the earlier path-normalization cleanup. This confirms active maintenance, but the delta is repository cleanup rather than a Hottop-measured quality/runtime improvement for the tested Wan2.2 I2V subset, so there is still **no freshness-only repin**.

Wan2.2 ecosystem reports continue to expose correctness-sensitive details such as HIGH/LOW A14B LoRA expert routing. The tested Hottop subset does not rely on those community LoRA pairs; this remains a provenance/quality caution rather than a reason to add a dependency.

## Immediate next actions

1. Continue inspecting fresh real cow/Odyssey production evidence and modify deterministic visuals/audio only for a **measured** defect; do not tune framing, lighting, transitions or loudness from aesthetics alone.
2. Once a reviewed local LightX2V/Wan2.2 runtime plus rights-safe references is genuinely provisioned, run at least two subject-bearing Odyssey I2V shots and require meaningful motion plus complete subject-bound continuity evidence before composition.
3. When operator-local Qwen3-TTS 1.7B is genuinely provisioned, run same-line Mandarin A/B against the guaranteed fallback and promote it only on measured intelligibility/delivery/naturalness evidence plus publication-rights review.
4. Continue targeted ecosystem radar around the measured gap. Do not add freshness-only pins, large dependencies or provider abstraction without measurable value and rollback.
5. For fresh creative output, perform live/supplied hotspot mechanism analysis first; consult creative memory only after current context is resolved, and archive real feedback/performance lessons when evidence exists.

## Recovery order

1. `PROJECT.md`.
2. this `STATUS.md`.
3. relevant reusable skills, including `creative-reference-memory` when prior Hottop cases can help.
4. newest relevant spec/plan/decision/research record.
5. current `main`, open PRs and exact-head CI/production evidence.
6. targeted ecosystem scan for the measured gap.
7. fresh hotspot/mechanism analysis for new creative generation.
8. creative-memory retrieval when useful, after current context is resolved.
9. continue the highest-value safe action autonomously.
