# Hottop

Hottop is an **evidence-aware hot-topic brand creative engine** for static and motion content.

It turns current cultural, tech, film, product, and internet signals into original brand-native creative concepts, then carries selected concepts into structured render and video-production plans. It is not limited to four-panel memes, AI products, InkClawAgent, or static images.

## What the pipeline does

The current foundation covers:

1. **Intent and promotion semantics** — resolve the user's real goal, audience, platform, product role, constraints, and desired ambition without forcing a long questionnaire.
2. **Trend and comparison research** — collect/enrich current signals, deduplicate/rank them, and keep factual competitor claims evidence-bound.
3. **Category reframing and bridge search** — identify category defaults, remove unnecessary constraints, and find a natural story/metaphor that connects the hotspot to the product.
4. **Creative generation and review** — support multiple expression forms and media, then apply hard creative/evidence/rights gates before ranking.
5. **Provider-neutral rendering** — emit `hottop.render.v2` instead of coupling creative semantics to one image/video provider.
6. **Config-driven motion production** — transform `hottop.render.v2` into `hottop.video-plan.v1`, generate/validate shots, produce dialogue/music/SFX, compose headlessly, and finalize delivery media.

## Creative doctrine

Hottop treats references as **grammar, not pixels**. Third-party material may teach pacing, archetypes, visual grammar, or meme structure, but generated outputs should not directly reproduce protected film frames, actor likenesses, official character designs, proprietary UI, copied ad layouts, distinctive trade dress, source footage, or copyrighted soundtrack.

Comparative factual claims require evidence. When evidence is absent, the creative should remain unmistakably satirical, subjective, fictional, or metaphorical.

For social/hotspot work, destination URLs, QR codes, and hard CTA copy are not placed inside the asset by default. The product should earn its place in the joke or story rather than turning the piece into a banner ad.

## Motion and video

The motion path is:

`hottop.render.v2 → hottop.video-plan.v1 → generation → audio → compositor → FFmpeg`

**MoviePy is the default unattended headless compositor.** FFmpeg performs compatibility finalization and final media verification. Motion Canvas remains an optional planning/interactive-preview path unless an operator supplies a real executor.

Generation is provider-neutral and fail-closed:

- `zero-cost-router` supports configured cost-zero candidates with bounded attempts, rights-safe reference I2V, generated-video quality gates, provenance manifests, and optional explicit deterministic reference-motion degradation.
- `external` currently supports an operator-managed WanGP adapter. Hottop never auto-installs WanGP or auto-downloads its models. Reference I2V uses an exported Settings placeholder contract and is preflighted before GPU execution.
- `wan22-*` remains an optional operator-controlled local Wan2.2 route.
- `comfy-api-v2` is an optional explicitly configured remote/self-hosted adapter; credentials remain environment-only and execution requires `--execute`.

Generated footage is not accepted just because a process exited successfully. Hottop checks fresh outputs, reference rights, backend provenance, exact shot bytes where applicable, motion/duplicate-frame quality, compositor inputs, and final delivery codecs/media integrity.

## Style routing

Surface polish is selectable rather than universal. `roughness_score` allows both presentable cinematic work and **Anti-Polish / Controlled Badness**: deliberately cheap-looking visuals, awkward motion, deadpan acting, crude Foley, and low-budget music can be creative choices, while character continuity, scene geography, cause/effect, subtitle correctness, dialogue intelligibility, comedy timing, product semantics, claim safety, and rights safety remain hard requirements.

Representative profiles include:

- `config/video/anti-polish-direct.yml`
- `config/video/cinematic-meme-direct.yml`
- `config/video/cinematic-zero-cost.yml`
- `config/video/wangp-operator.yml`

## Install

Python 3.11+ is required.

```bash
python -m pip install -e ".[dev]"
```

For local MoviePy video composition:

```bash
python -m pip install -e ".[dev,video]"
```

FFmpeg is expected on `PATH` for video finalization. Optional external generators, model files, GPUs, credentials, and cloud endpoints remain operator-controlled; Hottop does not silently provision them.

## Useful commands

Resolve a natural-language creative request:

```bash
hottop intent "为我的产品做一个结合当前热点的品牌梗"
```

Inspect a video profile without installing/downloading anything:

```bash
hottop video-doctor --config config/video/cinematic-zero-cost.yml
```

Build a production plan from `hottop.render.v2`:

```bash
hottop video-plan examples/video/inkclaw-cow-snake.render.json \
  --config config/video/anti-polish-direct.yml
```

Materialize a safe dry-run workspace and structured commands:

```bash
hottop video-run examples/video/inkclaw-cow-snake.render.json \
  --config config/video/anti-polish-direct.yml \
  --output-dir artifacts/video-run
```

Actually run trusted configured stages only after readiness passes:

```bash
hottop video-run examples/video/inkclaw-cow-snake.render.json \
  --config config/video/anti-polish-direct.yml \
  --output-dir artifacts/video-run \
  --execute
```

## Representative sources

- `examples/video/inkclaw-cow-snake.render.json` — original high-roughness Anti-Polish story source.
- `examples/video/inkclaw-odyssey-witch-pigs.render.json` — lower-roughness cinematic mythic meme source.
- `examples/video/hottop-zero-cost-reference-i2v.render.json` — rights-safe generated-original reference-I2V example.

## Project state

Foundation v0.1 is under active closure review on `feat/hottop-foundation`. The implementation is developed evidence-first with RED→GREEN tests, dry-run-first external execution, no hidden paid fallback, no secret persistence, and explicit rights/provenance checks at production boundaries.

See `PROJECT.md` for durable doctrine and architecture, `STATUS.md` for the current closure state, and `skills/brand-metaphor-creative/SKILL.md` for the reusable creative operating rules.
