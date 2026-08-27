# MV-S2V admission review — 2026-08-27

## Why this candidate was checked

Production v0.2's highest-value generated-video gap is **real multi-shot subject continuity evidence** under rights-safe reference conditioning. Hottop already has input-side identity/reference locks, output byte/provenance binding and a continuity-evidence contract; the missing proof is a generator that materially improves recurring-subject consistency on real generated shots.

`Szy-Young/MV-S2V` is mechanism-relevant because it conditions generation on multiple views of the same subject rather than a single reference image, explicitly targeting 3D-level subject consistency.

## Exact upstream evidence

- GitHub repository: `Szy-Young/MV-S2V`
- reviewed source revision: `ccbc80944b36600b1dd39cb6bf671c285b9a1ebc`
- revision date: 2026-06-13
- paper: *MV-S2V: Multi-View Subject-Consistent Video Generation*, SIGGRAPH 2026 / arXiv:2601.17756
- public code includes `generate.py`, `generate_batch.py`, `infer.sh`, `requirements.txt` and a vendored `wan/` tree.
- the reviewed GitHub root does **not** contain a `LICENSE` file.
- Hugging Face model: `youngsong305/MV-S2V`; the model card currently exposes no license metadata and Hugging Face reports missing/empty YAML metadata.

The base `Wan-AI/Wan2.1-T2V-14B` model is separately published under Apache-2.0. That does **not** resolve the MV-S2V source/checkpoint license.

## Runtime and provisioning boundary

The public quickstart describes a 14B BF16 Subject-to-Video DiT at 480p and requires separate local checkpoints:

1. Wan2.1-T2V-14B base assets for VAE/T5;
2. MV-S2V DiT weights;
3. PyTorch >= 2.4;
4. `xfuser>=0.4.1` for multi-GPU inference.

The documented sample runs with:

```text
torchrun --nproc_per_node=2 ... --dit_fsdp --t5_fsdp --ulysses_size 2
```

and accepts comma-separated `--ref_image` inputs, including up to four object views plus one optional human view. This is operator-owned multi-GPU/model provisioning, not an unattended zero-cost route. Hottop must not invoke the upstream download instructions or install the runtime automatically.

## Relevance to Hottop

Potential value is high **if** the licensing and runtime gates clear:

- directly targets the current recurring-subject continuity gap;
- multi-view conditioning could reduce unseen-view hallucination versus single-reference I2V;
- can be evaluated with Hottop's existing exact-reference-byte, generated-shot-byte, generator-source and continuity-evaluator provenance contracts;
- supports a narrow same-subject benchmark without changing Hottop's provider-neutral render/plan/composition contracts.

The project is built on Wan2.1 rather than Hottop's currently tested LightX2V/Wan2.2 route, so it must prove measurable continuity gain before it can justify an additional heavyweight runtime.

## Admission decision

**Decision: gated research/continuity benchmark candidate only. Do not integrate code, weights or routing yet.**

Blocking gates:

1. exact GitHub source license is unresolved at the reviewed revision;
2. MV-S2V checkpoint/model-card license metadata is unresolved;
3. multi-GPU 14B runtime is heavyweight and has not been probed on an actual operator machine;
4. no Hottop benchmark yet proves it beats the already-admitted LightX2V/Wan2.2/Stand-In candidates;
5. reference-image rights and output publication rights remain separate per-run gates.

No automatic clone/install/download, no model-hub `integration_ready=true`, no `video-run` route and no quality claim are justified from public demos alone.

## Re-evaluation trigger

Re-open admission only when both of these become true:

- exact source/checkpoint licensing becomes explicit and compatible with intended use; and
- an operator provides an already-provisioned runtime/checkpoints plus a rights-safe multi-view reference pack.

Then run the same Odyssey subject-bearing sequence against the current LightX2V/Wan2.2 route and require complete subject-shot coverage, meaningful motion, byte/provenance binding and a measurable continuity improvement before promotion.
