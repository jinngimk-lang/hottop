# Stand-In Wan2.2 identity-continuity candidate review

Date: 2026-08-27
Milestone: Production v0.2
Decision: admit to the model registry as an unprobed operator-local benchmark candidate only; no normal execution routing

## Measured gap

Hottop's highest-value generated-video gap remains output-side subject continuity across multiple subject-bearing shots. Input `subject_id` / reference locks are already enforced, but they are constraints rather than proof that the generated pixels preserve identity.

`WeChatCV/Stand-In` is directly relevant because it adds a lightweight identity-control module to Wan-family video generation rather than introducing a generic provider abstraction.

## Exact source reviewed

Repository: `https://github.com/WeChatCV/Stand-In`

Exact source revision:

`e351224366be169076e94af1454115d91d458313`

The latest commit on that revision is dated 2026-08-10 and announces Stand-In-V2 as upcoming. V2 is not treated as an available or benchmarked route.

The exact root tree contains `LICENSE`; the file is Apache License 2.0.

The project README reports:

- CVPR 2026 acceptance;
- 153M-parameter identity control (about 1% additional parameters relative to the base model);
- released Wan2.2 support since 2025-12-22;
- human and non-human subject-preserving examples;
- an official Wan2.2 inference path using an identity/reference image.

## Weights and base-model rights

The public `BowenXue/Stand-In` Hugging Face model card declares Apache-2.0, and the repository contains Wan2.2 Stand-In checkpoint files. This is evidence for the Stand-In adapter-weights license metadata, not a blanket license for every dependency.

Base Wan2.2 code/checkpoint rights remain a separate provenance dimension. The official Wan2.2 I2V A14B model card is also currently marked Apache-2.0, but Hottop must still bind the exact operator-provisioned checkpoint/revision actually used rather than infer it from this review.

## Runtime and download boundary

The official Stand-In quickstart intentionally provides `download_models.py`, which downloads base Wan models, face-recognition assets and Stand-In weights. The Wan2.2 example also offers an automatic download path.

That behavior is **not admitted into normal Hottop execution**. Hottop's registry entry must say the opposite explicitly:

- no automatic download;
- no auto-install of Stand-In or its dependencies;
- no model provisioning in CI or normal `video-run`;
- operator-provided local source + local weights only;
- physical DGX/runtime readiness remains `unprobed` until local preflight.

The Wan2.2 A14B family is a heavyweight route. Public model artifacts are tens of gigabytes and ordinary BF16 guidance is high-memory. The declared dual-DGX-Spark pool may be a useful benchmark environment, but this research does not prove the actual driver/CUDA/PyTorch/model placement or feasible performance on those machines.

## Security / rights boundary

Identity-conditioning inputs can involve likeness/biometric semantics. For Hottop:

- only `generated-original` or `user-provided-rights-cleared` reference inputs are admissible;
- no face/identity asset may be fetched from third parties merely to exercise the model;
- reference bytes, subject identity, generator source/model/checkpoint and generated shot bytes remain separate provenance dimensions;
- output-side continuity evidence must cover all subject-bearing benchmark shots rather than cherry-picking one favorable result.

## Smallest useful integration

Stand-In clears the gate for a **registry-level benchmark admission**, not for runtime integration.

Add an `integrations/model-hub.yml` entry with:

- exact repository/source context documented here;
- Apache-2.0 code-license metadata;
- Stand-In adapter-weights Apache-2.0 metadata with base Wan2.2 rights explicitly separate;
- `status: benchmark_candidate`;
- `integration_ready: false`;
- `runtime_status: unprobed`;
- self-owned compute only;
- explicit prohibition on automatic download;
- identity/reference capabilities, but no claim that Hottop has already proved multi-shot preservation.

This lets the one-stop model hub remember a stronger continuity candidate without making it selectable by the existing integration-ready route.

## Benchmark required before promotion

If an operator later provisions the exact reviewed local runtime and rights-safe Odyssey references, compare Stand-In against the existing LightX2V/Wan2.2 route on the same recurring subject and shot prompts.

Promotion requires:

1. exact local Stand-In source revision;
2. exact Stand-In adapter checkpoint identity;
3. exact base Wan2.2 checkpoint identity;
4. exact reference bytes;
5. exact generated shot bytes;
6. meaningful-motion quality gates;
7. Hottop's complete subject-bearing continuity evaluator coverage;
8. final media/provenance gates after composition;
9. measured continuity/quality gain large enough to justify the extra runtime footprint.

## Comparison with other candidates

- **LightX2V/Wan2.2** remains the tested operator-owned base route and is not repinned for freshness alone.
- **Memento** directly adds multi-shot keyframe memory, but remains gated by incomplete exact-source license packaging and very high published inference hardware guidance.
- **IPVG** uses prompt decomposition + HyperLoRA identity-preserving first frames + Wan2.2 and has external challenge evidence, but its exact reviewed root tree lacks the README-linked LICENSE and the documented route adds Qwen3-8B/HyperLoRA/Wan2.2 provisioning.
- **Stand-In** is currently the cleanest newly surfaced registry-level candidate because its exact source has Apache-2.0 licensing, its public model card declares Apache-2.0, and a Wan2.2 path is already released. It is still not a production route until Hottop measures it on operator-owned hardware and rights-safe assets.

No heavy dependency, model download, GPU provisioning, credential, paid service or default-route change is admitted by this decision.
