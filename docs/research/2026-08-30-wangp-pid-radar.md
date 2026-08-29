# WanGP / Wan2GP PiD radar — 2026-08-30

## Why this check exists

Production v0.2's generated-video gap is still real reference-conditioned multi-shot continuity evidence, not lack of another provider abstraction. WanGP/Wan2GP is already a reviewed **operator-managed interoperability candidate** because it can orchestrate low-VRAM local video workflows, post-processing and auxiliary tooling without forcing Hottop to vendor the upstream application.

This refresh asks a narrow question: **does the latest upstream change materially improve Hottop's tested Wan2.2 reference-conditioned identity or requested-action motion route enough to justify a repin or new production dependency?**

## Exact upstream evidence

Reviewed upstream:

- repository: `deepbeepmeep/Wan2GP`
- branch: `main`
- exact head: `c3aa2915b039f898285d4a5de102d89eabf83237`
- commit time: 2026-08-29 17:11:26 UTC
- commit message: `deepy optimisations`
- parent: `260f87e4d7b5bb5b3ac4bea394e2431ea076683b`

The reviewed diff is small and confined to PiD post-processing / upsampling support:

- `postprocessing/pid/runtime.py`
  - renames/exposes the PiD spatial block-size helper;
  - keeps Flux2 at block size 16 and other PiD backbones at 8;
  - routes existing tiling calculations through the shared helper.
- `postprocessing/pid/wgp_bridge.py`
  - aligns incoming frame height/width to the selected PiD backbone's spatial block size before upsampling;
  - moves dtype/device conversion after that shape normalization;
  - feeds the active backbone into sample preparation.

The change therefore addresses **PiD post-processing input alignment / upsampler maintenance**. It does not add a new Wan2.2 identity-control mechanism, a new reference-conditioning contract, a new requested-action motion-control path, or Hottop-measured continuity evidence.

## Admission decision

**No freshness-only repin.**

Hottop keeps its existing tested LightX2V/Wan2.2 operator route and current WanGP interoperability boundary. This WanGP head is worth recording because it is fresh maintenance, but the inspected change does not clear Hottop's admission bar for changing a tested production pin or introducing new post-processing dependencies.

A repin or new PiD integration would require a measured Hottop gap and evidence that the candidate improves it, for example:

1. a rights-safe operator-generated sequence that currently fails a defined resolution/alignment or post-processing quality gate;
2. exact source/model/runtime provenance for the compared route;
3. before/after output artifacts with the same source plan and references;
4. measurable gain in final-media quality, identity continuity, requested-action motion, or reliability;
5. no regression in artifact byte/provenance binding, composition-time verification, final codec/media gates, zero-cost policy or rollback.

## License / runtime / cost boundary

The existing WanGP admission remains unchanged:

- interoperate with an **operator-provided** local installation rather than copying/bundling the upstream application;
- treat WanGP's own license separately from every third-party model/checkpoint it orchestrates;
- do not auto-install WanGP, custom nodes or auxiliary runtimes;
- do not auto-download models/checkpoints;
- do not infer model/output rights from the application license;
- do not expose a hidden paid fallback or consume credits;
- runtime readiness remains a real local preflight fact, never a registry assumption.

## Production consequence

This refresh produces **no production behavior change**. The guaranteed zero-cost baseline remains software3d → Mandarin audio/music/Foley → MoviePy → FFmpeg → verified MP4. The primary generated-video operator experiment remains LightX2V/Wan2.2 with rights-safe references and complete output-side **identity fidelity + requested-action motion fidelity** evidence.

The next useful WanGP event is a real operator-provisioned benchmark, not another speculative adapter or freshness-only pin change.
