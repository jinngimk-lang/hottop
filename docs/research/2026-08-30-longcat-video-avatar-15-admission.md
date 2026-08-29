# LongCat-Video-Avatar 1.5 admission — 2026-08-30

## Why this matters

Hottop's current generated-quality gap is not generic video generation. It is repeatable, rights-safe subject identity plus requested-action motion across multiple shots, with Mandarin dialogue/audio evidence and zero-paid operator-owned execution when possible.

LongCat-Video-Avatar 1.5 is relevant because it combines audio-driven character animation, image conditioning, long-video continuation, identity consistency, motion stability and multilingual audio conditioning in one open local stack. Upstream explicitly reports support for stylized domains including animals and animation, which makes it more relevant to Hottop than a human-only talking-head route.

## Exact reviewed upstream evidence

- Repository: `meituan-longcat/LongCat-Video`
- Reviewed source revision: `6b3f4b8582a8bc3f20f795735f5383716c4ba794`
- Repository source license: MIT.
- Official model: `meituan-longcat/LongCat-Video-Avatar-1.5`.
- Official model-card license: MIT.
- Upstream release date: 2026-05-21.
- Upstream claims/implements Audio-Text-to-Video, Audio-Image-to-Video and video continuation, single- and multi-audio modes, Whisper-Large-v3 audio conditioning, 8-step distillation, INT8 DiT loading, 480p/720p selection and long-video continuation.
- Upstream specifically notes animals, animation and complex scenes as supported domains.

## Runtime and download boundary

The public quick-start is not an unattended Hottop route:

- Python 3.10 environment;
- PyTorch 2.6 + CUDA 12.4;
- FlashAttention 2.7.4.post1 by default;
- ffmpeg/librosa plus project requirements;
- explicit `huggingface-cli download` for LongCat model assets;
- Avatar 1.5 examples use `torchrun --nproc_per_node=2` with context parallelism;
- v1.5 requires distilled inference and optionally supports INT8 loading.

Hottop must not auto-install this stack, invoke upstream model-download helpers, provision GPU resources or silently make it a fallback. Any future run must use operator-provisioned local source and model assets with exact byte/revision binding.

## Admission decision

**Admit as a gated research/benchmark candidate, not as a production backend.**

Reasons to keep it in the radar:

1. source and official weights have a clear permissive MIT license surface;
2. audio-image-to-video plus continuation directly matches Hottop's motion-native, dialogue-first video direction;
3. upstream explicitly targets temporal stability, identity consistency, stylized subjects and animals;
4. dual-audio/multi-character support is relevant to role-aware dialogue scenes;
5. long-video chunking/continuation is useful evidence for future multi-shot or continuous-scene production.

Reasons not to promote it yet:

1. Hottop has no operator-provisioned local runtime/model evidence for this stack;
2. no Hottop rights-safe same-sequence output has been evaluated;
3. upstream identity/stability claims are not a substitute for Hottop output-side continuity evidence;
4. audio-driven animation does not automatically prove the requested non-speech action is correct;
5. model/reference/audio/output publication rights still need to be bound per benchmark asset even though source/model licenses are permissive;
6. the default setup is materially heavier than the guaranteed software3d route and normal unattended execution must not trigger its downloads/install steps.

## Re-admission / benchmark gate

Only move beyond research/benchmark status after an operator locally provisions the exact source/runtime/model stack. Then use the same rights-safe subject-bearing sequence as the primary LightX2V/Wan2.2 route and persist independently:

1. exact source revision and model/checkpoint bytes;
2. runtime/hardware identity and execution settings;
3. exact rights-safe image/audio/reference bytes;
4. subject identity fidelity across all subject-bearing outputs;
5. requested-action/motion fidelity independently from identity;
6. lip-sync/dialogue timing when speech drives the scene;
7. long-video/continuation seam and geography stability when continuation is used;
8. anti-copy, artifact SHA-256/size provenance and final-media verification;
9. zero-paid/operator-owned cost posture.

If it cannot beat or fill a measured gap versus the existing LightX2V/Wan2.2 path, do not add an executable adapter merely because the upstream project is permissively licensed or popular.
