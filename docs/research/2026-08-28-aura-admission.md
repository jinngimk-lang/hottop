# Aura admission review

Date: 2026-08-28
Status: **research / operator benchmark candidate only**

## Why it matters

Aura directly targets Hottop's remaining reference-conditioned quality gap for **multiple bound subjects and scenes**. It uses structured director-level prompts plus person/object/scene reference images, a Qwen2.5-VL semantic-grounding encoder and separate high/low-noise 14B experts on a Wan2.2 T2V-A14B backbone.

This is materially closer to Hottop's existing `subject_id` / reference-lock semantics than a generic I2V wrapper because textual subject tags are explicitly grounded to heterogeneous visual references.

## Exact reviewed source / weights

- Source repository: `Camellia997/Aura`
- Exact source revision: `0fd72c355069cbe0ea53569ad1b6a84f72749266`
- Source license: Apache-2.0 (root `LICENSE` present)
- Public Aura weights repository: `Camellia997/Aura`
- Observed Hugging Face revision: `32f139552c8b60c546f9491b4b4c3d39d2181b7d`
- Observed published weight volume: approximately 77.2 GB
- Weight model-card license metadata: **missing/empty at review**
- Base lineage: Wan2.2 T2V-A14B + Wan VAE/UMT5-XXL, plus Qwen2.5-VL-3B-Instruct for meta-query grounding

Apache-2.0 source code does not establish rights for the Aura expert weights, Wan base assets, Qwen VLM assets, bundled validation references or generated-output publication. Those are separate gates.

## Runtime / provisioning boundary

The published inference package targets CUDA 12.4 / PyTorch 2.5 and builds FlashAttention. It supports:

- single-GPU inference with CPU offload;
- multi-GPU Ulysses/FSDP (documented 8-way path, with divisors of 40 attention heads also allowed);
- multi-node validation sharding.

Upstream ships setup/download scripts that create a conda environment and can fetch Wan, Qwen and Aura weights from Hugging Face, including optional token/mirror/accelerated transfer behavior. Normal Hottop must **not** invoke these installers/downloaders or silently access HF/network credentials.

A real Hottop benchmark therefore requires an operator to provision the reviewed source, exact local Aura/Wan/Qwen assets and compatible CUDA/PyTorch/FlashAttention runtime before Hottop probes it.

## Production evidence boundary

Aura upstream claims stronger identity and scene-context preservation for people/objects/scenes. Hottop has not independently reproduced those claims on rights-safe Odyssey assets. Upstream demo/reference material is analysis evidence only and is not admitted as generation input.

If later benchmarked, Aura must pass Hottop's existing output-side gates rather than receiving special treatment:

- exact rights-safe reference bytes and stable subject bindings;
- identity fidelity for every subject-bearing shot;
- motion fidelity/non-degeneracy separately from identity;
- scene/world/geography consistency where claimed;
- generated-video motion/duplicate/decodability gates;
- actual generator source + model/checkpoint provenance;
- exact artifact SHA-256/size and composition-time re-verification;
- final H.264/AAC/yuv420p media verification.

## Decision

Do **not** add an executable Aura route yet.

Aura is a stronger operator-benchmark candidate than a paper-only system because inference code and weights exist, but it still fails Hottop's production admission gate because:

1. Aura expert weight license metadata is unresolved;
2. the runtime and ~77 GB Aura weights plus separately provisioned Wan/Qwen assets are heavy and unprobed on operator hardware;
3. upstream setup/download helpers violate unattended Hottop's no-auto-install/no-large-download policy;
4. Hottop has no real rights-safe output benchmark proving identity + motion + scene consistency.

Classification: `research / operator benchmark candidate`, `integration_ready=false`, `runtime_status=unprobed`, `cost_mode=self_owned_compute`.

## Re-admission criteria

Re-evaluate for registry/executable admission only when:

1. the Aura expert checkpoint license is explicit and compatible with intended use;
2. Wan/Qwen/base/checkpoint/output rights are independently reviewed;
3. an operator has already provisioned exact local source/checkpoint/runtime assets without Hottop downloading them;
4. local preflight can prove CUDA/PyTorch/FlashAttention/model paths and disable hidden network behavior;
5. the same rights-safe multi-subject Odyssey-derived sequence is benchmarked against LightX2V/Wan2.2;
6. Aura demonstrates measured output-side value under the shared Hottop identity, motion, geography, provenance and media gates.

Popularity or upstream qualitative comparisons alone do not justify a route change.