# DomainShuttle admission review — 2026-08-28

## Decision

Admit **HKUST-C4G/DomainShuttle** as a **registry-only benchmark candidate** for subject-driven video consistency. Do not add a normal `video-run` route, auto-download path, or runtime-readiness claim.

This candidate is relevant because it directly targets open-domain subject fidelity/editability on a Wan2.2-A14B backbone. It is not production-ready for Hottop because its published path is extremely heavy, unprobed on operator hardware, and its public weight-license metadata is internally inconsistent even though the observed labels are both permissive.

## Exact reviewed provenance

- Source repository: `HKUST-C4G/DomainShuttle`
- Source revision reviewed: `ba7a7a3b275dcdb9896ca43ede3587b6c1dc6060`
- Source root license: `Apache-2.0`
- Weight repository: `CNcreator0331/DomainShuttle_weight`
- Weight revision reviewed: `418962e4db32ecce6c1542d536c0ab7326417938`
- Hugging Face weight metadata license: `MIT`
- DomainShuttle GitHub README statement for the models: `Apache-2.0`
- Base model: `Wan-AI/Wan2.2-T2V-A14B`, public Hugging Face metadata reviewed as `Apache-2.0`

The **MIT vs Apache-2.0 weight license metadata mismatch** must be preserved rather than silently normalized. Both observed labels are permissive, but Hottop does not infer which metadata source is legally authoritative. Re-check exact upstream terms before any operator benchmark or redistribution.

## Runtime / cost boundary

The public DomainShuttle weight tree is roughly **70 GB**. The public Wan2.2-T2V-A14B base tree is roughly **126 GB**. Normal Hottop therefore treats the combined stack as operator-provisioned only.

The reviewed quick-start path:

- installs PyTorch/CUDA dependencies plus `xfuser`, `yunchang` and `flash-attn`;
- instructs the operator to download both DomainShuttle and Wan2.2 model assets explicitly;
- defaults `NPROC_PER_NODE=8` in `run_wan22_domainshuttle.sh`;
- launches `torchrun` for a 14B 480p/720p inference path;
- identifies the inference implementation as unofficial while official code is under institutional review.

Those facts make automatic installation/download inappropriate for `ZERO_COST_MODE=true` unattended operation. **No auto-download**, no automatic dependency installation, no GPU provisioning and no paid fallback are admitted.

## Hottop admission state

- status: **benchmark candidate**
- integration-ready: **false**
- runtime status: **unprobed**
- cost class: self-owned/operator compute only
- route priority: below the already tested LightX2V/Wan2.2 operator path until same-subject evidence proves otherwise

A future benchmark may proceed only when an operator supplies an already-provisioned local checkout, exact local model/checkpoint identities, suitable multi-GPU runtime and rights-safe subject references. The benchmark must use Hottop's existing output-side continuity evaluator and byte/provenance gates over at least two subject-bearing shots. Runtime success alone is not identity proof.

## Why no executable adapter now

DomainShuttle fills the same measured gap as Stand-In/MV-S2V/Memento—subject consistency—but no local Hottop runtime is provisioned and no same-subject output evidence exists. Adding another executable adapter before that evidence would increase abstraction rather than Production v0.2 video quality.

The useful integration at this point is therefore the machine-readable registry entry plus this exact provenance/admission record. Promotion to an executable route requires measured value against the current tested LightX2V/Wan2.2 baseline and a clean exact license/runtime re-review.
