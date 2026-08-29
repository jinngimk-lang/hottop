# MiniMax H3 Motion Lab radar — 2026-08-30

## Why this matters

Production v0.2 still lacks operator-generated reference-conditioned output proving both identity fidelity and requested-action motion fidelity. Fast/bursty motion is a particularly relevant failure mode because a route can preserve a recognizable subject while smearing or losing the requested choreography.

## Reviewed candidate

Repository: `matlowai/ComfyUI-MAINodes`

Reviewed source revision: `f4868b4a08e8a504ce86db54a17961d399ffa2bc` (`v1.1.3`, 2026-08-29).

Source license: **GPL-3.0-or-later** in the reviewed root `LICENSE`.

Relevant upstream behavior:

- Motion Lab is a MiniMax-H3/ComfyUI post-generation pipeline aimed at bursty-motion smearing;
- its core approach detects high-motion regions from the clip latent, retimes/holds those regions, performs partial-denoise video-to-video regeneration, then recovers the original frame rate;
- upstream explicitly positions this as inference-time repair: no additional model and no training for the core Motion Lab path;
- the current recommended graph also carries audio initialization so dialogue timing can survive the retiming/regeneration path;
- upstream reports a low-VRAM route that can run a long de-rope pass on a 16 GB GPU / 32 GB system-memory machine, but these are upstream measurements, not Hottop evidence;
- several newer repair/chaining/audio-prefix/drift-control components are explicitly alpha and must not be conflated with the stable Motion Lab core.

## Admission decision

**Research/benchmark signal only. Do not vendor or copy GPL code into Hottop.**

The candidate is useful because it suggests a measurable recovery experiment for a specific failure mode: a rights-safe Hottop-generated H3 clip that already fails requested-action motion because of fast-motion smearing. If such an operator-owned H3 runtime is later provisioned, compare the exact same baseline clip against the repaired clip and bind both byte sets.

No Hottop production adapter, dependency, ComfyUI node copy, automatic installation, model download or GPU provisioning is admitted from this review.

## Future benchmark gate

Revisit only when an operator has already provisioned a reviewed MiniMax-H3/ComfyUI stack and rights-safe input/output assets. A useful Hottop A/B must:

1. bind exact baseline and repaired clip bytes plus exact MAINodes source revision/config;
2. keep requested-action semantics fixed and preserve the existing `motion_spec_sha256` binding;
3. measure requested-action/motion fidelity before and after repair rather than accepting visual smoothness alone;
4. independently re-check subject identity, scene geography, anti-copy, dialogue/lip-sync when relevant, and final-media integrity because V2V repair can improve motion while damaging another dimension;
5. record runtime/hardware and latency/VRAM separately from quality;
6. treat GPL code as an external operator-managed runtime boundary unless a future legal/architecture review justifies another arrangement.

## Durable conclusion

Motion repair is a **post-generation recovery experiment**, not evidence that a generator is identity- or motion-correct by default. A repaired clip may only graduate when output-side evidence shows the requested action improved without regressing identity, geography, audio timing, provenance or final encoding. This fits existing Hottop doctrine, so no `PROJECT.md` change is required.