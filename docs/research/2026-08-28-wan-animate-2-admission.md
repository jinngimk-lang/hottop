# Wan-Animate-2 admission review — 2026-08-28

## Decision

Track Wan-Video/Wan-Animate-2 as an **operator-provisioned benchmark candidate** for the Production v0.2 identity + motion gap. Do not add it to unattended `video-run`, auto-install its runtime, or auto-download its checkpoints.

This route is unusually relevant because it directly consumes a rights-safe reference image plus a rights-safe driving video and claims both identity preservation and motion/performance transfer. That makes it a stronger same-sequence benchmark candidate than routes that control only still-image identity or only trajectories. It does **not** remove Hottop's requirement to measure identity fidelity and motion fidelity independently on generated output.

## Reviewed upstream

- Source: `Wan-Video/Wan-Animate-2`
- Reviewed source revision: `3ad2fef7d61d6200c9c653e0fe47be7616b323f3`
- Source license: Apache-2.0 (`LICENSE` exists at the reviewed revision).
- Upstream release notes say inference scripts plus Base and Distillation weights were released on 2026-08-07.
- Public inference accepts a reference image and driving/template video.
- Upstream documents 720p settings tuned for **8× A800 GPUs** and says 480p was tested on **2× A800 GPUs**.
- Runtime setup includes Python 3.11, PyTorch 2.7/CUDA 12.6, repository requirements, FlashAttention and an editable local install.
- Upstream download instructions use Hugging Face or ModelScope CLI. Normal Hottop execution must not invoke those download paths.

## Rights and provenance boundary

Apache-2.0 source licensing does not by itself prove publication rights for every checkpoint, reference image, driving video or generated output. Before an operator benchmark:

1. re-verify exact source and checkpoint/model-card licensing and revisions;
2. require local, already-provisioned checkpoint paths and bind their independently verifiable provenance;
3. require `generated-original` or `user-provided-rights-cleared` reference image **and** driving-video bytes;
4. never use actor/celebrity likenesses, copyrighted source performance footage or cloned identity without rights-cleared authority;
5. bind generated artifact bytes, actual generator source identity and evaluator revision exactly as required by Hottop's continuity contract.

## Zero-cost/runtime admission

The route is compatible with operator-owned compute in principle, but it is **not** a guaranteed zero-cost unattended backend. Its documented multi-A800 execution shape and large local model stack require explicit operator provisioning and preflight. Hottop must not:

- auto-install PyTorch/FlashAttention or upstream dependencies;
- auto-download Wan-Animate-2 weights;
- provision or rent GPUs;
- silently call a hosted demo/API;
- infer readiness from a configured path without probing the actual local runtime.

## Future benchmark protocol

If the operator already has a reviewed local stack, compare Wan-Animate-2 against the strongest admissible existing route using the same rights-safe subject/performance sequence. Persist at minimum:

- exact reference-image and driving-video bytes;
- source/checkpoint/runtime/hardware provenance;
- identity fidelity across every subject-bearing output;
- motion/performance fidelity independently from identity;
- viewpoint/camera adherence when requested;
- scene geography and temporal coherence;
- motion/duplicate and media integrity gates;
- final MP4 bytes and final-media verification.

A successful runtime invocation is not evidence of identity or motion quality. Promotion requires Hottop-owned output evidence and a rollback path.
