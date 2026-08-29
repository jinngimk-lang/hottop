# Echo-Memory admission review — 2026-08-30

## Why this candidate matters

Hottop's Production v0.2 generated-video work already separates **identity fidelity**, **requested-action motion fidelity**, **scene geography**, provenance and final-media integrity. A recurring failure mode in longer/multi-shot generation is different: the camera leaves a location/object and later returns, but the world has drifted into a plausible yet different state.

`Echo-Team-Joy-Future-Academy-JD/Echo-Memory` is directly relevant to that **revisit / scene-memory** problem. Its core study compares raw context, compressed history, explicit spatial memory and state-space memory on an action-conditioned Wan video backbone.

This review asks whether it should become a Hottop production backend, benchmark candidate or architecture-only signal.

## Exact reviewed source

- repository: `Echo-Team-Joy-Future-Academy-JD/Echo-Memory`
- exact GitHub head: `194be716aedaa84d9bd377740d6e6d9c32a309cb`
- latest reviewed commit time: 2026-08-16 01:49:34 UTC
- repository license metadata / README badge: **CC BY 4.0**
- current public backbone: **Wan2.1 T2V 1.3B**
- upstream roadmap still lists Wan2.2 and multi-scale 5B/14B backbones as future work, not current released capability.

The repository exposes unified inference, training recipes, memory implementations, public evaluation assets, ComfyUI nodes and an interactive ZeroGPU demo.

## Public checkpoint / base-model rights

Public Echo-Memory checkpoints are hosted under `Echo-Team/Echo-Memory` and declare **CC BY 4.0**. The reviewed checkpoint set contains released rows such as raw-context and state-space/spatial-memory variants built on Wan2.1 1.3B.

The underlying `Wan-AI/Wan2.1-T2V-1.3B` model card/license surface declares **Apache-2.0** for the base model. These are separate provenance dimensions: Echo-Memory source, Echo-Memory checkpoint, Wan2.1 base-model bytes, reference inputs and generated outputs must remain independently bound.

No Hottop claim should infer commercial/output rights for arbitrary reference media merely from these software/model licenses.

## Runtime and zero-cost practicality

Echo-Memory is materially lighter than many 14B continuity candidates because the current released backbone is Wan2.1 1.3B. Official Wan2.1 documentation reports about **8.19 GB VRAM** for the 1.3B T2V model under its reference setup, while real speed varies substantially by GPU/offload/runtime.

The project also exposes a public Hugging Face **ZeroGPU** demo. This makes it relevant to Hottop's zero-paid-cost radar, but it is not a guaranteed service and does not automatically become an unattended production route. Space availability, exact runtime revision, base/checkpoint bytes, queue behavior and rights remain separate evidence dimensions.

Hottop must not auto-download the Wan base, Echo-Memory checkpoints, ComfyUI stack or training assets. Local execution remains operator-provisioned.

## Mechanism assessment

Echo-Memory studies a useful dimension that is not identical to Hottop's current primary gap:

- **Context memory** asks whether retaining recent raw frames is enough.
- **Compression memory** asks whether compact temporal history can prevent drift.
- **Spatial memory** asks whether retained spatial state improves layout/viewpoint recall.
- **State-space memory** asks whether recurrent state stabilizes longer revisit trajectories.

This is valuable for **scene geography / revisit consistency** and for evaluating long-horizon memory architecture.

It is **not** current evidence that a route preserves the exact recurring subject identity across multiple Hottop story shots, nor that it follows a specific requested character action. Runtime success or a successful revisit demo therefore cannot substitute for Hottop's separate identity and requested-action motion gates.

## Admission decision

**Research / benchmark candidate only. No production route.**

Reasons:

1. source/checkpoint licensing is relatively clear and the 1.3B backbone lowers the hardware barrier;
2. the mechanism directly addresses scene-memory/revisit drift;
3. however, the released system is currently Wan2.1-1.3B rather than Hottop's tested Wan2.2 operator route;
4. Wan2.2/5B/14B support remains roadmap work;
5. Hottop has no current measured production artifact showing that scene-revisit memory is the highest-priority failing gate versus identity + requested-action motion;
6. no Hottop same-sequence benchmark has shown measurable gain over the existing LightX2V/Wan2.2 route.

Therefore this review does **not** add an executable adapter, model-hub runtime-ready route, automatic downloader, ComfyUI dependency or production pin.

## Re-admission / benchmark gate

Revisit Echo-Memory only when a measured Hottop sequence requires scene-return memory, or when a compatible Wan2.2 release becomes available.

A meaningful benchmark must bind:

1. exact Echo-Memory source revision;
2. exact Echo-Memory checkpoint SHA-256/size;
3. exact Wan base-model revision/bytes;
4. exact rights-safe first-frame/reference and action/camera sequence bytes;
5. exact prompt/plan semantics;
6. generated output bytes and runtime identity;
7. scene-layout / viewpoint-return evidence;
8. identity fidelity and requested-action motion evidence separately when a recurring subject is present;
9. final-media/provenance gates identical to other Hottop routes.

Promotion requires measurable value over the existing tested route under the same Hottop sequence. A public ZeroGPU demo, benchmark paper score or successful local launch is not enough by itself.

## Production consequence

No current production behavior changes. The guaranteed software3d zero-cost baseline remains canonical. LightX2V/Wan2.2 remains the primary operator generated-video route when local runtime/models/references are genuinely provisioned.

Echo-Memory is retained as a permissively licensed **scene-memory/revisit benchmark signal**, not as evidence that Hottop's identity + motion quality boundary has been solved.
