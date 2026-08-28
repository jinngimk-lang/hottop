---
name: creative-reference-memory
description: Use inside Hottop when prior successful/failed creative examples, user feedback, promotion lessons, or platform performance can improve a new image/video concept without reusing an old template.
---

# Creative Reference Memory

## Purpose

Use Hottop's prior creative work as **mechanism/grammar/preference memory**, not as a template library.

Canonical sources:

- `integrations/creative-reference-library.yml`
- `docs/creative/creative-reference-memory.md`
- runtime: `hottop.creative_memory`
- CLI: `hottop-references search`

## When to use

Use this after the current request has a resolved product and current hotspot context, especially when:

- a new hotspot resembles a past causal/relationship mechanism;
- the desired medium resembles a past successful native grammar;
- product insertion feels generic and past product-role examples could challenge it;
- the request risks a known failure such as slideshow motion, weak product salience, over-polishing or internal production labels;
- a social-post request would benefit from remembered packaging patterns such as meme + product explainer + platform copy/hashtags.

Do not let retrieval replace fresh hotspot work. If the user supplied a hotspot, analyze that hotspot first. If none was supplied, perform current hotspot discovery first according to `PROJECT.md`.

## Retrieval workflow

1. Extract current mechanism terms, native visual grammar, product-role candidates and likely failure patterns.
2. Query the library for the closest **mechanism**, **visual grammar**, **product role** and relevant negative guardrails.
3. Read why positive cases worked and what the user liked.
4. Read negative cases as hard warnings.
5. Generate fresh directions that preserve the current hotspot's own logic.
6. Reject any direction that is merely a prior layout/character/scene with names swapped.
7. Continue normal Hottop mechanism mapping, creative review and generation preflight.

Example:

```bash
hottop-references search \
  --mechanism obstruction,breakout \
  --visual cinematic,live_action \
  --product-role route,breakout
```

Guardrail lookup:

```bash
hottop-references search \
  --negative-pattern slideshow,pan_zoom,internal_label \
  --include-negative
```

## Reuse rules

Positive references may teach:

- causal structure;
- relationship structure;
- product role;
- timing/reversal logic;
- visual medium grammar;
- dialogue rhythm;
- audio/BGM/Foley grammar;
- platform packaging;
- promotion clarity lessons.

They may **not** silently become:

- the same four-panel template;
- the same actors/characters;
- the same composition;
- the same film frame/poster;
- the same punchline with nouns replaced;
- a substitute for current hotspot evidence.

`reuse_mode=guardrail_only` means the entry is never a generation template.

## User feedback is evidence

When the user gives concrete feedback, preserve the lesson in structured memory when it is durable. Current examples include:

- film/movie hotspot creative must feel native to cinematic scene grammar;
- rough viral 3D should remain deliberately rough when roughness carries recognition;
- high-quality stills with pan/zoom are not cinematic video;
- do not print internal labels such as `热点梗图`, `今日热搜 TOP1`, or other research/workflow labels on audience-facing assets;
- keep InkClawAgent/product visually prominent enough that the promotional purpose is unmistakable;
- when useful, publish a hotspot meme together with a separate product explainer and platform-native title/body/#hashtags;
- hotspot exploration must go beyond the news event into the **active derivative meme**: what phrase, action, number, blame joke, callback, screenshot or remix people are actually repeating now;
- social titles should use **meme-native hook compression** rather than newsroom summaries. A strong pattern is `short utterance + concrete consequence`, e.g. the user-approved `俩字，省了5000W` hook for the 2026-08-28 AI-decision meme. Reuse the pattern, not the people, exact event, or layout;
- if a source story is marked fictional/satirical or a claim is unverified, keep that boundary explicit even when the derivative meme is real and widely circulating.

Do not invent user ratings or numeric quality scores. Store qualitative feedback unless an actual score exists.

## Asset policy

Normal Git stores the metadata, not large binary media by default.

- bind exact known reference bytes by SHA-256 where available;
- use approved Git LFS or object storage later for generated/original/user-authorized assets when an ingestion path exists;
- keep ordinary third-party copyrighted assets as metadata/source-analysis only;
- rights metadata never overrides copyright, likeness or trademark restrictions;
- prior Hottop images are normally retrieved for grammar/mechanism learning, not pixel copying.

## Learning classification

The current system is **retrieval + few-shot/preference memory**, not reinforcement learning.

A later training path may use accumulated clean data for SFT, pairwise preferences/DPO, a reward model and eventually RL experiments. Do not introduce training infrastructure until dataset size, quality and measured value justify it.

## Persistent project protocol

On long/new/stale context, recover `PROJECT.md` then `STATUS.md`. When a fresh creative run can benefit from past cases, load this skill and the canonical creative-reference library before ideation, but still perform the request's fresh/supplied-hotspot analysis first.

After a durable new success/failure lesson, update the library and documentation so the next session does not depend on chat memory.
