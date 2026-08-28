# TFM motion-fidelity admission — 2026-08-28

## Decision

`pzrain/TFM` is admitted as a **research-only / operator benchmark candidate for temporal-motion fidelity**, not as an executable Hottop backend.

It does **not** replace the guaranteed software3d baseline, LightX2V/Wan2.2 operator route, or the provider-neutral continuity benchmark. It does not prove subject identity continuity. Its value is narrower: testing whether a temporally-aware flow-matching objective can improve coherent, non-degenerate requested motion without adding inference-time machinery.

## Reviewed upstream

- repository: `pzrain/TFM`
- exact reviewed source: `ab791c05748019d90742e7fcebf599daacdbd824`
- paper: *Temporal-aware Flow Matching for Video Generation with Temporally Coherent Motion* (ICML 2026)
- repository code license: Apache-2.0
- base model used by upstream inference: Wan2.1-T2V-14B
- released adaptation: fine-tuned LoRA distributed through Google Drive
- upstream training data: ShareGPT4Video, approximately 40K video-text pairs

The code license is not treated as a blanket authorization for the LoRA, Wan2.1 base weights, training data, benchmark media, or generated outputs. Those remain separate rights/provenance gates.

## Why it is relevant

Hottop now treats **identity fidelity** and **motion fidelity** as independent evidence dimensions. TFM targets the latter directly. Its core idea adds explicit inter-frame constraints to the flow-matching training objective so motion dynamics are learned with temporal dependence rather than treating video merely as independent image-like frames.

This makes it potentially useful for a future same-sequence benchmark when an admitted route passes identity but exhibits frozen, incoherent, implausible, or weak requested motion.

It is **not** an identity/reference solution by itself. TFM's released inference path is text-to-video on Wan2.1-T2V-14B plus its LoRA; it should never be promoted as proof of subject consistency merely because motion looks better.

## Runtime / provisioning facts

Upstream documents:

- Python 3.10 environment;
- separately provisioned Wan2.1-T2V-14B base weights;
- separately provisioned `tfm-lora.safetensors`;
- inference on a single A100 40GB GPU;
- training on 4×A100 80GB for roughly one week;
- a DiffSynth-Studio-derived codebase.

These are operator-owned resources. Normal Hottop execution must not clone/install this stack, fetch the Google Drive LoRA, download Wan weights, provision CUDA/GPU, or train the method automatically.

## License / provenance gate

The reviewed repository itself reports Apache-2.0. The public README points to the LoRA through Google Drive but does not provide an independently reviewed LoRA-specific license declaration in the repository surface inspected for this admission.

Therefore:

- source code license: reviewed and permissive;
- LoRA rights: **unresolved for Hottop production admission**;
- Wan2.1 base rights: must be reviewed independently at the exact checkpoint revision used;
- ShareGPT4Video/data rights: relevant to retraining claims, not inherited from source code;
- generated-output/publication rights: remain an operator/project-level gate.

No TFM file is vendored into Hottop.

## Re-admission / benchmark gate

TFM may move beyond research-only status only when all of the following are true:

1. exact local source, base-model and LoRA revisions are independently identifiable;
2. LoRA/base/checkpoint licenses are compatible with the intended use;
3. the operator has already provisioned the required runtime/GPU/assets locally;
4. no unattended model download, package bootstrap, hosted API or paid fallback is required;
5. a rights-safe Hottop benchmark sequence is used;
6. motion evidence measures requested-action/performance fidelity and temporal coherence separately from generic pixel motion;
7. identity/reference fidelity, if claimed by a composed route, is measured independently and may not be inferred from TFM motion quality;
8. artifact bytes, generator/runtime provenance and final-media gates remain bound exactly as for other Production v0.2 evidence.

If those gates are satisfied, the first useful experiment is an operator-local A/B against the current tested route on the same prompts/sequence, measuring requested-action fidelity, temporal coherence, reference-pose diversity/anti-copy where relevant, identity continuity where the composed route claims it, and final-media integrity.

## Current action

Do not add a `video-run` adapter or model-hub executable route. Keep TFM in the research radar until the LoRA/checkpoint rights and operator runtime are actually provisioned and a measured Hottop motion-fidelity gap justifies the benchmark.
