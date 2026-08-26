# Dual DGX Spark Local Model Fabric

Date: 2026-08-26
Status: durable operator architecture for Production v0.2+

## Why this exists

Hottop is not a model-demo repository. Its purpose is to maximize promotional effectiveness by connecting a current hotspot to a product through a strong cultural mechanism, then delivering the idea in the hotspot-native image/video/audio language at a quality level that preserves the joke and the product truth.

The local model fabric exists **after** creative correctness. More models do not compensate for a weak script, generic hotspot reference, replaceable product role, broken character consistency or low-quality output.

## Durable production hierarchy

Every image/video campaign follows this order:

1. **Current truth** — recover `PROJECT.md`, `STATUS.md`, relevant skills, this operator spec and `integrations/model-hub.yml`.
2. **Hotspot evidence** — if the user supplied a hotspot, analyze and freshly verify it when needed; otherwise discover current hotspots before ideation.
3. **Promotion objective** — define the product truth, user pain/outcome and what the asset is supposed to maximize: recognition, relevance, memory, category reframe, launch, conversion or another explicit goal.
4. **Mechanism fit** — borrow the hotspot mechanism, not the skin. Extract recognition hook, causal/relationship structure, visual grammar, dialogue grammar and motion/audio grammar.
5. **Script / beat sheet** — product takes a functional role inside the mechanism and changes the story outcome. Reject concepts where another unrelated brand could be swapped in without changing the logic.
6. **World / character model** — define a reusable character bible, costume/prop rules, environment geography, scale relationships, subject IDs and identity locks before multi-shot generation.
7. **Keyframes / style frames** — lock the hotspot-native visual quality and character/world look. Film hotspots require original cinematic live-action quality; crude-3D memes may deliberately remain crude when that is the native grammar.
8. **Model routing** — only now select image, I2V/T2V/Animate/S2V, restoration, interpolation and TTS models from the model hub according to capability, measured quality, local hardware, license and cost.
9. **Real motion** — cinematic video requires generated physical action: body/head/eye movement, secondary cloth/hair motion, environment motion and action-continuous camera work. Static frames with pan/zoom are not cinematic video.
10. **Continuity review** — identity, costume, props, geography, action, lighting and cause/effect must remain coherent across all subject-bearing shots.
11. **Audio** — dialogue performance, BGM, Foley/SFX and silence/timing follow the hotspot-native audio grammar; music ducks under speech. Audio quality is not post-production decoration.
12. **Post / delivery** — restoration/interpolation only improve accepted generated footage; MoviePy/FFmpeg assemble and verify the final artifact. Post tools may never masquerade as motion generators.
13. **Campaign-effect review** — re-check instant hotspot recognition, product centrality, natural linkage, punchline strength, visual/audio fit and whether the final asset still serves the promotional objective.

## Operator-owned hardware baseline

The user has declared a local pool of **two NVIDIA DGX Spark systems**. This becomes Hottop's preferred heavy-compute execution pool before any paid SaaS.

Known platform capability recorded from NVIDIA product documentation:

- NVIDIA GB10 Grace Blackwell platform per node;
- 128 GB coherent unified system memory per node;
- 273 GB/s memory bandwidth per node;
- ConnectX-7 200 Gbps capable networking;
- two nodes therefore represent 256 GB aggregate physical unified memory capacity.

**Do not misrepresent aggregate memory as one automatically shared GPU address space.** Multi-node execution requires the chosen runtime/model to support the actual topology and communication mode.

The actual user-machine hostname, DGX OS, driver, CUDA, PyTorch, free disk, model paths and configured ConnectX/RDMA state are deliberately **unknown until probed**. Run `python scripts/probe_dgx_spark.py` independently on each node and archive the JSON outside Git if it contains local topology/path details that should remain private. Never infer current runtime versions from NVIDIA release notes.

## Cost boundary

Default production is local/self-owned compute or verified free capacity.

- no paid fallback;
- no credits/overage;
- no SaaS call merely because local setup is inconvenient;
- paid providers remain optional only after explicit per-run user approval;
- model hub discovery never installs packages, accepts licenses or downloads weights;
- multi-GB weights are operator-provisioned after source/license/storage review.

## One-stop model fabric

Canonical machine-readable registry: `integrations/model-hub.yml`.

Safe discovery command:

```bash
hottop-models list --operator-profile dgx-spark-dual
hottop-models list --capability image_to_video --operator-profile dgx-spark-dual
hottop-models list --capability cinematic_real_motion --operator-profile dgx-spark-dual
```

This command only filters registry metadata. It does not execute or download anything.

### Current high-priority local stack

- **LightX2V + Wan2.2 I2V A14B** — primary existing reference-conditioned cinematic I2V route.
- **LightX2V Wan2.2 NVFP4 sparse Blackwell path** — DGX Spark high-priority benchmark candidate; upstream speed claims are not Hottop proof.
- **Wan2.2 TI2V 5B** — lower-footprint T2V/I2V benchmark candidate for 720p real motion.
- **Wan2.2 Animate 14B** — character animation/replacement candidate for strong character-motion tasks; identity must still be output-evaluated.
- **Wan2.2 S2V 14B** — speech-driven motion candidate after local benchmark.
- **Qwen-Image 2.x** — high-priority image/keyframe/editing candidate for film-style frames and text-heavy imagery.
- **Qwen3-TTS 1.7B CustomVoice** — local instruct-capable role/delivery Mandarin candidate behind existing rights gate.
- **Real-ESRGAN** — restoration/super-resolution only.
- **RIFE** — frame interpolation only.
- **ComfyUI** — GPL-separated interoperability/orchestration, never vendored into Hottop.

### Candidate / blocked lines

- FramePack: code is permissive but underlying checkpoint/weights terms remain separate; benchmark only after exact weights review.
- LTX-Video 0.9.5: isolated older-checkpoint benchmark only with exact checkpoint/license pin.
- LTX-2.x: license-blocked for default commercial routing until current community-license commercial terms are cleared for the operator entity.
- MiniMax H3, LongCat, SCAIL, WanGP and other existing radar candidates remain governed by their existing license/hardware/benchmark gates.
- Paid video SaaS is explicitly represented only so the default selector can prove it excludes that class.

## Integration meaning

"Collect models/projects into Hottop" does **not** mean copying third-party source trees or weights into this repository.

A candidate is integrated when Hottop has the smallest safe set needed for one-stop operation:

1. source/revision and license metadata;
2. capability + hardware/cost status in the model hub;
3. operator-local config/profile;
4. isolated adapter or existing interop route when execution is admitted;
5. preflight/readiness check;
6. benchmark fixture/evidence;
7. rollback path and no hidden download/paid behavior.

This preserves updateability and license separation while still giving Hottop one control plane.

## Cinematic fail-closed rule

For film/live-action tasks, an output may be called cinematic video only when the selected route produces meaningful subject/environment motion and passes continuity/media gates. If no admitted local/free real-motion generator is ready, **fail closed**. A still sequence, Ken Burns effect, camera push/pull over generated images or interpolation of static frames is not a substitute.

Software3d remains a valid deterministic motion baseline for styles where its visual grammar is appropriate. It is not a fallback that may silently satisfy a cinematic-realism request.

## First dual-DGX production proof

The next operator proof should use the existing Odyssey/Cyclops deployment-island concept because it has a known story but previously exposed the slideshow-vs-video failure clearly.

Required proof:

1. run the read-only probe on both DGX Spark nodes;
2. provision/pin one reviewed Wan2.2/LightX2V route without auto-download behavior inside Hottop;
3. create rights-safe cinematic keyframes + character/world bible;
4. generate at least two real subject-bearing I2V shots with visible human/giant/environment action;
5. bind generator source + checkpoint provenance + shot hashes;
6. run continuity and motion gates;
7. add Mandarin role-aware dialogue, original cinematic BGM and synced Foley;
8. compose/finalize H.264/AAC vertical MP4;
9. visually inspect real frames and reject slideshow-like or identity-drifting output;
10. only after that promote the route as a dual-DGX production baseline.

## Recovery rule

On a new/long/stale chat or owner loop, do not rediscover this architecture from memory. Read, in order:

1. `PROJECT.md`;
2. `STATUS.md`;
3. this file;
4. `config/operator/dgx-spark-dual.yml`;
5. `integrations/model-hub.yml`;
6. relevant creative/video skills and current benchmark evidence.

If later evidence finds a better product shape or model fabric, update the durable doctrine rather than preserving this design out of inertia.
