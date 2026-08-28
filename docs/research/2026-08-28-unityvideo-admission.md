# UnityVideo admission — motion-control benchmark candidate

Date: 2026-08-28

## Why this candidate matters

Production v0.2 now treats **identity fidelity** and **motion fidelity** as separate output-side evidence dimensions. UnityVideo is relevant to the second dimension because it extends a Wan2.2-TI2V-5B base with an explicit auxiliary-modality stream and supports depth, DensePose, optical flow (RAFT), segmentation and skeleton conditions. It can therefore test whether a planned motion/pose/geometry signal improves subject-bearing shot motion without pretending that motion control alone proves identity continuity.

This is a **benchmark candidate**, not a production backend.

## Reviewed provenance

- Source repository: `https://github.com/JIA-Lab-research/UnityVideo`
- Source revision reviewed: `e79e9b6bd1c498dd919dceb4cdea47e20417bf70`
- Source code license: MIT (`LICENSE` exists in the reviewed tree).
- Published checkpoint repository: `KlingTeam/UnityVideo`
- Published model-card license metadata: Apache-2.0.
- Base model: `Wan-AI/Wan2.2-TI2V-5B`; base-model/checkpoint rights remain a separate execution-time provenance gate.
- Inference checkpoint: `checkpoints/unityvideo_wan22_ti2v_5b_step15000_ema.safetensors`
- Published size: `10,020,954,352` bytes.
- Published SHA-256: `0df3909e312526c46f68097958afa055868f73354fe4276d693f7ebc398e6a39`.

Source license, UnityVideo checkpoint metadata, Wan2.2 base-model rights, condition/reference input rights and generated-output publication rights must remain separate records. A permissive source license does not collapse those boundaries.

## Runtime and unattended-policy review

The public Python CLI uses PyTorch/CUDA and **auto-downloads** the UnityVideo checkpoint plus the Wan2.2 base model on first use. That behavior is incompatible with Hottop's normal unattended policy. Hottop must not call that first-use download path, install the project automatically, provision GPU resources, or infer runtime readiness from a registry entry.

The released checkpoint was evaluated at **256 x 256** with **33 frames**. Higher resolution, longer clips and unseen modality encodings explicitly require independent validation upstream. Hottop's vertical/720p production contract therefore cannot inherit quality or runtime claims from the public release.

Training guidance is substantially heavier than the minimal inference claim (the repository documents distributed, high-memory training). Hottop does not need or admit automatic training for this candidate.

## Admission decision

Admit UnityVideo only as:

- `status=benchmark_candidate`
- `integration_ready=false`
- `runtime_status=unprobed`
- `cost_class=self_owned_compute`

There is **no executable adapter** and no default route.

## Future re-admission / benchmark gate

Only re-evaluate for an executable operator route after all of the following are true:

1. the exact source, UnityVideo checkpoint and Wan2.2 base assets are locally provisioned and byte/provenance bound without invoking auto-download behavior;
2. the operator GPU/runtime is actually probed and the tested resolution/duration is recorded;
3. all condition/reference inputs are generated-original or otherwise rights-cleared;
4. a same-sequence benchmark compares the existing tested Wan2.2/LightX2V route against UnityVideo motion conditioning on at least two subject-bearing shots;
5. **motion fidelity** is measured independently (planned action/pose/trajectory adherence plus Hottop perceptible-motion gates), while identity fidelity, scene geography and artifact provenance remain separate hard evidence dimensions;
6. the candidate shows a measurable improvement without weakening final-media, continuity, rights, provenance or zero-paid-compute boundaries.

A visually impressive upstream demo or a successful process exit is not sufficient evidence.
