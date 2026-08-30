# DiffSynth-Studio MiniMax-H3 NF4 admission review — 2026-08-30

## Decision

**Research / operator benchmark signal only. Do not add a production adapter or model-hub runtime-ready entry.**

This route is materially relevant to Production v0.2 because DiffSynth-Studio now exposes MiniMax-H3 FL2VA/Ref2VA inference with NF4 quantized weights and aggressive CPU/disk offload. The published model card says the route can run with as little as 8 GB VRAM, so it may lower the hardware barrier for H3 audio/video and reference-conditioned experiments.

It does **not** clear Hottop's unattended admission gate. The example path performs explicit remote model resolution/download, the complete NF4 repository is tens of GB, CUDA remains required for the documented path, and the derivative/base-model rights surface is not clean enough to treat the quantized model-card label as the whole license story.

## Reviewed provenance

- Framework: `modelscope/DiffSynth-Studio@102fe9980b9375ecb6436d360297a00327472535` (v2.1.5 head reviewed 2026-08-30).
- Framework root license: Apache-2.0.
- Quantized model: `DiffSynth-Studio/MiniMax-H3-NF4`.
- Quantized model-card metadata currently says `apache-2.0` and describes the artifact as a quantized derivative of `MiniMax/MiniMax-H3`.
- Public model tree is roughly 72.5 GB and includes FL2VA/Ref2VA, pruned variants, text encoder, video VAE and audio VAE artifacts.
- Official base model: `MiniMaxAI/MiniMax-H3`; official LICENSE reviewed 2026-08-30 from `https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE`.
- Official MiniMax H3 license date: 2026-08-02.

## Rights boundary

The quantized repository's `apache-2.0` metadata is **not sufficient by itself** to erase obligations inherited from the MiniMax-H3 base model.

The official MiniMax H3 Community License reviewed on 2026-08-30 makes the boundary concrete:

- the default `Applicable Territory` is worldwide **excluding the European Union, the United Kingdom, the Republic of Korea and the United States of America**;
- use outside that territory is not authorized by the default agreement and MiniMax directs interested users in excluded territories to seek a separate license;
- commercial products/services generating more than **USD 20 million equivalent in yearly revenue** require separate prior written authorization from MiniMax;
- commercial products/services using MiniMax H3 must prominently display `MiniMax H3` in the user interface;
- distribution carries NOTICE/agreement obligations;
- the agreement prohibits using MiniMax H3 Works or their Outputs/results to improve another AI model other than MiniMax H3 or its Model Derivatives;
- Outputs are not themselves defined as Model Derivatives, and MiniMax states that it claims no rights over generated Outputs, while the user remains responsible for downstream use and compliance.

Hottop therefore treats these as separate layers:

1. DiffSynth-Studio framework code license;
2. DiffSynth quantized-weight repository metadata;
3. MiniMax-H3 base-model license and acceptable-use terms;
4. reference image/audio rights;
5. generated-output/publication rights.

Before any operator benchmark is promoted beyond research, bind the **official MiniMax-H3 license text/model revision actually used** and reconcile it with the derivative NF4 model card. A permissive derivative metadata field never overrides a more restrictive upstream/base-model grant. Geography and operator/commercial-use eligibility are hard admission gates, not documentation footnotes.

## Runtime / cost boundary

The reviewed example uses `ModelConfig(model_id=...)` / ModelScope resolution and therefore can fetch model artifacts. Normal Hottop `video-run` must not invoke this route, install DiffSynth-Studio, or download the NF4 repository automatically.

Allowed future experiment:

- operator manually provisions an exact DiffSynth checkout and exact model files;
- local preflight binds source revision, every required model artifact path/size/SHA-256 and runtime/hardware identity;
- execution is forced offline/fail-closed so missing artifacts cannot trigger a network fetch;
- no paid endpoint, credits or hidden hosted fallback;
- operator geography and intended commercial use are compatible with the exact MiniMax-H3 license or are separately authorized;
- output is evaluated through the existing identity, requested-action motion, geography, anti-copy, audio/dialogue and final-media gates.

## Why this matters

H3 NF4 is interesting specifically as a **hardware-accessibility benchmark**, not as evidence that H3 is already better than the tested LightX2V/Wan2.2 route. The 8 GB VRAM claim and quantization support are upstream runtime claims. Hottop still needs its own same-sequence output evidence before making continuity, motion, lip-sync, cinematic-quality or performance claims.

The existing MiniMax H3 Motion Lab recovery record remains orthogonal: it can only repair a measured post-generation bursty-motion-smear failure and cannot substitute for generator admission or requested-action semantics.

## Re-admission gate

Promote only if all of the following are true:

- exact official base-model/derivative rights are compatible with the intended use, operator geography and commercial context;
- any required separate MiniMax authorization is already in place before execution;
- operator-provisioned local artifacts pass byte/provenance preflight with no implicit downloads;
- runtime is practical on the actual hardware and measured rather than inferred from upstream marketing;
- the same rights-safe subject sequence is compared against the current primary route;
- identity fidelity and requested-action motion fidelity pass independently;
- audio/dialogue/lip-sync, geography, anti-copy and final-media checks pass when applicable;
- rollback remains simply disabling/removing the optional adapter/config without affecting software3d.
