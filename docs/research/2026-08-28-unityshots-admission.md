# UnityShots admission review

Date: 2026-08-28
Status: **research-only / not integration-ready**

## Why it matters to Hottop

UnityShots directly targets the highest-value remaining Production v0.2 gap: coherent multi-shot storytelling rather than isolated good-looking shots. Its published design turns an LTX-2.3 22B single-shot audio-video model into a 3–9 shot sequence with persistent identity/world state, synchronized audio and controllable cuts.

The architecture is especially relevant because it keeps **constant-size cross-shot memory** instead of growing an unbounded history:

- visual/audio long-term memory anchored to the opening shot;
- short-term memory from the immediately preceding tail;
- a boundary-aware gate at cuts;
- reference speaker conditioning carried across shots.

This is useful architecture evidence for Hottop's continuity work. It does **not** prove that UnityShots itself is admissible for production.

## Reviewed upstream

- Repository: `JIA-Lab-research/UnityShots`
- Exact source revision: `36fa057002cf4c5759333c11cab73c8cee4db1af`
- Repository default branch at review: `main`
- Repository last pushed at review: 2026-06-25
- Paper: `UnityShots: Memory-Driven Multi-Shot Audio-Video Generation with Boundary-Aware Gating`, arXiv:2606.21661
- Claimed base: LTX-2.3 22B

## Admission gates

### Source / model / data rights

The reviewed repository declares **CC BY-NC 4.0** and explicitly scopes release/demo use to academic, non-commercial research. GitHub's repository metadata exposes no separate SPDX license. This alone blocks commercial/default Hottop production integration.

The README also states that **model checkpoints, training code and the agent system are not released yet**. There is therefore no executable checkpoint revision to admit, hash, benchmark or bind to generated artifacts.

UnityShotsBench is a separate published benchmark with reference identity images and voice clips. Its dataset/media rights must be reviewed independently before any ingestion; this review does not admit or copy benchmark assets.

LTX-2.3 base-model code/weights/output terms remain a separate dependency gate. A UnityShots paper/demo claim cannot substitute for exact base-model and checkpoint provenance.

### Runtime / cost / hidden behavior

No released UnityShots inference stack exists at the reviewed revision, so Hottop cannot truthfully establish:

- exact package/runtime requirements;
- actual VRAM or multi-GPU requirements;
- network/download behavior;
- offline execution support;
- checkpoint size or storage burden;
- reproducible latency/throughput on operator hardware.

Do not infer readiness from paper demos or LTX-2.3 compatibility.

### Production evidence

The paper/repository claims cross-shot identity, world consistency, synchronized audio and controllable cuts. Hottop has not independently reproduced these claims on its rights-safe Odyssey sequence, so they remain upstream claims rather than Hottop evidence.

## Decision

**Do not integrate UnityShots code, model weights, benchmark media or a `video-run` route. Do not auto-download anything.**

Keep it as a research-only architecture candidate. The transferable idea is behavioral, not code reuse: a bounded long-term + short-term memory contract with explicit cut-boundary gating may be worth testing inside a future permissively licensed/operator-owned route.

This does not change the guaranteed software3d baseline or the tested LightX2V/Wan2.2 path.

## Re-admission criteria

Re-evaluate only if all of the following become true:

1. an exact source/checkpoint release exists with rights compatible with the intended Hottop use;
2. base-model, UnityShots checkpoint, benchmark/reference assets and output/publication rights are separately reviewable;
3. an operator has already provisioned the exact runtime/checkpoints without Hottop auto-installing or downloading multi-GB assets;
4. network/download behavior can be disabled or fail-closed for local execution;
5. the same rights-safe multi-shot benchmark is run against the existing LightX2V/Wan2.2 baseline;
6. Hottop persists output-side **identity fidelity, motion fidelity, world/geography consistency, audio continuity, cut quality, generator/model provenance and exact artifact bytes** separately.

A strong demo, popularity or paper score is not sufficient for admission.