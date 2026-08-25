# Hottop Status

Last updated: 2026-08-25
Active workstream: **Production v0.2 — operator-owned generative benchmark + cinematic quality proof**
Completed milestone: **Foundation v0.1**
Current milestone: **Production v0.2 — repeatable real video output**

> This file is the short-lived execution snapshot. `PROJECT.md` is durable doctrine. Re-fetch GitHub state before exact CI/head claims.

## Current production state

Hottop now has two distinct production layers:

1. a guaranteed **zero-cost deterministic software3d → audio → MoviePy → FFmpeg → verified MP4** baseline; and
2. isolated operator-owned/open generation routes that can be benchmarked without changing the creative/runtime contract.

Closed production evidence:

- PR #12 established the reproducible software3d config-to-MP4 loop with byte-bound provenance manifests and final media verification.
- PR #15 generalized software3d story routing beyond the cow/snake flagship and added the Odyssey witch/pigs cinematic profile. Exact-head CI run 1320 and production-smoke run 11 passed; the PR was squash-merged as `01e54432978f9694ea79a645e8b53308c474f3d5`.
- The production smoke now executes both checked-in stories end to end and verifies H.264/yuv420p + AAC output plus five per-shot provenance manifests for each case.
- PR #13 added the benchmark-ready offline local Qwen3-TTS 0.6B CustomVoice adapter and was merged as `b9743763316f240d5c095c84bc5f2f071ee32716`. It remains optional until a real operator-owned benchmark proves materially better Mandarin dialogue quality.
- PR #14 added a first-class `lightx2v-operator` generation backend for Wan2.2 T2V/I2V. The backend fails closed until an operator-provisioned LightX2V checkout, local model directory and config JSON exist; it resolves rights-safe I2V references, emits structured runtime commands, forces offline execution in the adapter, and never installs packages or downloads models. Exact-head CI run 1324 and production-smoke run 14 passed; the PR was squash-merged as `e32a0632d1245752baa0b60cd464a18af110a8df`.
- PR #16 was closed as fully superseded by #15; its only unique file was already present on `main` after #15.

## Durable governance state

`PROJECT.md` is canonical and now explicitly requires:

- repository-backed context recovery whenever a session is new, long or stale;
- Hottop-related image/video generation in Chat to re-read the current GitHub doctrine/status/relevant skills/examples/configs/constraints before generation;
- **existing-skill first** capability routing: reuse an available suitable skill/MCP/plugin instead of reinstalling or introducing a duplicate; add a new capability only for a concrete uncovered gap after permission/license/security/cost/reversibility review;
- targeted ecosystem freshness checks against measured project gaps, followed by real integration when a candidate clears the admission gate.

The governance update passed CI run 1327 and was merged to `main` as `737a53e9ee1439e3849112058006819577006536`.

## LightX2V / Wan2.2 operator route

Fresh upstream review on 2026-08-25 confirmed the current LightX2V route remains aligned with Hottop's adapter:

- reviewed upstream: `ModelTC/LightX2V@926299962ed32a142411e45468a289623432b4e4`;
- repository license: Apache-2.0;
- upstream `python -m lightx2v.infer` still exposes `wan2.2_moe`, `t2v` / `i2v`, local `--model_path`, `--config_json`, `--prompt`, `--negative_prompt`, `--image_path` and `--save_result_path` arguments matching the Hottop adapter boundary;
- official `Wan-AI/Wan2.2-I2V-A14B` weights are Apache-2.0;
- upstream continues to evolve rapidly, so Hottop pins the reviewed revision in the candidate registry and must re-review the CLI/config contract before adopting a materially newer revision.

The current follow-up workstream adds a checked-in operator profile `config/video/cinematic-lightx2v-wan22-i2v.yml`, a reviewed candidate-registry entry, and a contract test locking `cost_per_unit=0`, `operator_managed=true`, `auto_install=false`, and `auto_download_models=false`.

No actual Wan2.2 model is downloaded or executed by CI. A real cinematic benchmark remains gated on operator-provisioned local compute/model assets.

## Current ecosystem priorities

1. **Cinematic generated-video proof:** benchmark the merged LightX2V/Wan2.2 operator route when local assets exist, comparing motion quality, identity continuity, reference adherence, artifact rejection and runtime cost against the deterministic baseline.
2. **Cross-shot identity / continuation:** prioritize candidates with measurable reference/continuation capability rather than generic single-shot quality. LongCat-Video-Avatar 1.5 and SCAIL-2 remain high-priority reviewed candidates; WanGP remains an interop route rather than vendored code.
3. **Mandarin dialogue quality:** benchmark Qwen3 CustomVoice and CosyVoice3 only when operator-provisioned local models are available. eSpeak remains the guaranteed fallback; voice cloning remains rights-gated.
4. **Production evidence over abstraction:** every promoted route should end in a reproducible render/config → moving shots → audio → composite → verified MP4 case with hashes/provenance, not merely another provider interface.
5. **License separation:** new code repositories and model/weights licenses remain separate gates. New support in an Apache-licensed runtime does not clear a model whose weights use different terms.

## Immediate next actions

1. Merge the LightX2V operator profile + registry + contract-test sync after exact-head CI passes.
2. If no operator-owned GPU/model runtime is provisioned, do not auto-download anything; continue the next unblocked Production v0.2 task instead.
3. Build the next benchmark contract around **reference-conditioned identity continuity and multi-shot continuation**, so future model candidates are judged by Hottop's real creative requirement rather than demo aesthetics alone.
4. When a local LightX2V/Wan2.2 runtime becomes available, run a real Odyssey/reference-conditioned benchmark through the normal quality/provenance/composition gates and archive measured evidence.
5. Continue targeted upstream scans; integrate only changes that materially improve the measured gap and clear source/license/cost/hardware/security/rollback gates.

## Durable motion contract

`hottop.render.v2 → hottop.video-plan.v1 → generation → audio → MoviePy → FFmpeg → final media verification`

Default unattended target is zero-cost. Free GPU exhaustion may wait, bounded-retry, fail, or use an explicitly deterministic path; it must never become paid credits or a hidden paid provider. `video-run` is dry-run by default; only explicit `--execute` may spawn trusted stages after readiness passes.

Surface roughness is style-routed. Anti-Polish may deliberately look cheap; continuity, geography, subtitles, dialogue intelligibility, comedy timing, product semantics, evidence/claim safety, rights safety and final-media integrity remain hard gates.
