# IPVG identity-continuity candidate review

Date: 2026-08-27
Milestone: Production v0.2
Decision: gated benchmark candidate; no normal Hottop installation, download or routing

## Why this candidate was reviewed

Hottop's highest-value generated-video gap remains real multi-shot subject continuity evidence. A useful candidate therefore needs to improve the identity mechanism itself, not merely add another generic video provider.

`rain152/IPVG` (IPVG-STD: Spatial-Temporal Decoupled Identity Preserving Video Generation) is directly relevant. Its public README describes a three-stage pipeline:

1. spatial/temporal prompt decomposition, using Qwen3-8B in the reference implementation;
2. identity-preserving first-frame generation through ComfyUI-HyperLoRA;
3. Wan2.2 TI2V-5B or I2V-A14B video generation.

The repository reports second place in the Identity-Preserving Video Generation Challenge and was accepted at ACM Multimedia 2025. That makes it a stronger mechanism-level benchmark candidate than another ordinary Wan2.2 wrapper.

## Exact source inspected

Repository: `rain152/IPVG`

Exact `main` revision inspected:

`cd70f169e9a86d47e7860392b8b80c8d59a6d75a`

The latest commit on that branch is dated 2025-09-19, so the project is not currently a high-frequency maintained upstream despite being newly surfaced in this radar pass.

## Admission review

### Code-license packaging

The README displays an MIT badge, links to `LICENSE`, and says the project is MIT-licensed. However, the exact root tree inspected at `cd70f169...` contains no `LICENSE` file.

That mismatch is enough to block code ingestion into Hottop. Hottop must not infer a usable exact-source license from a README badge alone.

### Model/runtime rights and downloads

The reference pipeline additionally requires:

- Wan2.2 model checkpoints;
- ComfyUI-HyperLoRA and its models;
- Qwen3-8B for prompt decomposition in the documented path.

Those are separate code/model/checkpoint/license/runtime dimensions. The README explicitly instructs operators to download those external models. Hottop must not perform those downloads automatically from normal `video-run` or CI.

### Hardware practicality

The inspected README does not provide a bounded Hottop-like hardware contract or a demonstrated dual-DGX-Spark execution profile. The underlying Wan2.2/HyperLoRA/Qwen stack is materially heavier than the guaranteed software3d baseline.

No operator runtime is therefore marked ready from this research alone.

### Measurable value

The mechanism is promising because it separates identity-preserving first-frame construction from temporal video generation and has external competition evidence. But Hottop does not yet have a same-story benchmark proving that it improves Odyssey identity continuity over the already-tested LightX2V/Wan2.2 reference-conditioned route under Hottop's output-side continuity evaluator.

Popularity, challenge placement and a paper claim are not substitutes for that local evidence.

## Decision

Track IPVG as a **gated continuity benchmark candidate**, not as an admitted backend.

Do not:

- vendor or copy the repository code while the exact-source license packaging is incomplete;
- install its ComfyUI custom node automatically;
- download Qwen3-8B, HyperLoRA or Wan2.2 checkpoints automatically;
- route normal unattended `video-run` through IPVG;
- claim identity improvement without Hottop continuity evidence.

If the exact-source license becomes unambiguous and an operator has already provisioned the required local models/runtime, the smallest useful experiment is architectural rather than wholesale integration: compare its accepted rights-safe first-frame/identity-conditioning result against Hottop's existing reference-conditioned Wan2.2 route for the same recurring Odyssey subject, while preserving Hottop's generator source/model/reference/shot-byte/evaluator provenance contract.

## Relationship to existing candidates

- **LightX2V/Wan2.2** remains Hottop's tested operator-owned local route; no freshness-only repin is justified.
- **Memento** remains a stronger explicit multi-shot memory mechanism candidate, but is gated by license packaging and very high published hardware guidance.
- **IPVG** adds a useful alternative mechanism: identity-preserving image construction before Wan2.2 temporal generation. It is worth benchmarking if its exact license/runtime gate clears, but it does not currently replace either route.

No heavy dependency, GPU provisioning, automatic model download, credential or paid path is admitted by this review.
