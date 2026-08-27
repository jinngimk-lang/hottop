# ReWorld admission review — 2026-08-28

## Why this candidate matters

Hottop Production v0.2 still has one high-value generated-video gap that the guaranteed software3d baseline cannot prove: **real reference-conditioned multi-shot identity / scene continuity**. ReWorld is relevant because it attacks long-horizon scene/viewpoint drift rather than merely adding another generic video provider.

Reviewed source:

- repository: `zhifeichen097/ReWorld`
- exact reviewed revision: `fce2895ad8cbaa1b0b9e688675f51d052373cb4b`
- backbone family: Wan2.2

The mechanism combines a bounded recent KV cache with a pose-indexed landmark bank. Recent state stays bounded; older viewpoint state can be recalled by camera pose when the generation revisits a prior view. That architecture is directly relevant to Hottop's need to preserve geography and recurring subject/viewpoint state across longer sequences.

## Admission decision

**Decision: research-only architecture candidate. Do not integrate code, weights, runtime or routing.**

ReWorld does not clear Hottop's production admission gate at the reviewed revision:

1. **Source license:** the reviewed repository is published under **CC BY-NC-SA 4.0**. That is non-commercial and share-alike, so Hottop must not copy or vendor the implementation into the project.
2. **Checkpoint availability:** upstream states that the ReWorld generator and 4-step DMD LoRA checkpoints are not yet released. There is therefore no reproducible operator benchmark path to admit today.
3. **Runtime footprint:** the documented path requires a CUDA/PyTorch environment, FlashAttention and separately provisioned Wan2.2 base assets. None of those are implied ready merely because the source repository exists.
4. **Model/base rights remain separate:** Wan2.2 source/base checkpoint rights, any future ReWorld checkpoint rights, reference-image rights and output/publication rights must each be reviewed independently.
5. **No unattended provisioning:** normal Hottop must not run upstream installers, auto-download model assets, provision GPU compute or consume paid services to make this candidate appear ready.

## What Hottop may reuse

Only the **architecture idea** may inform a future clean implementation after independent review:

- bounded recent temporal memory rather than unbounded cache growth;
- a persistent landmark/state bank indexed by viewpoint/pose;
- retrieval of older state only when the camera returns to a related view;
- explicit separation between recent-motion memory and durable scene/viewpoint memory.

Do **not** copy ReWorld code, configuration, training assets or checkpoint material into Hottop under the current reviewed licensing state.

## Re-admission gate

Re-evaluate only if all of the following become true:

1. a permissively licensed implementation and checkpoint path exists for the intended use;
2. exact source and checkpoint revisions can be pinned independently;
3. an operator has already provisioned the required local runtime/models without Hottop auto-downloading multi-GB assets;
4. a rights-safe reference pack exists;
5. the candidate can run against the same Odyssey subject sequence used by the current LightX2V/Wan2.2 continuity benchmark;
6. output passes Hottop's existing generated-video motion/decodability, byte/provenance and final-media gates;
7. continuity evidence covers **all** subject-bearing shots and binds exact reference bytes, exact generated shot bytes, generator source/model provenance and evaluator revision;
8. it produces a measurable continuity/scene-memory gain over the current tested route.

Until then, ReWorld is evidence for a possible future memory architecture, not a production backend.

## Relationship to current doctrine

This review reinforces existing Hottop rules rather than changing them:

- popularity or a strong demo is not admission evidence;
- code license and model/checkpoint rights are separate;
- runtime success is not generated-quality proof;
- operator-owned GPU/model execution is fail-closed and never auto-provisioned;
- generated identity continuity must be proven from real output, not inferred from input locks or architecture claims.
