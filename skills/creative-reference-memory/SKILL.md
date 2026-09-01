---
name: creative-reference-memory
description: Use inside Hottop when prior successful/failed creative examples, user feedback, promotion lessons, platform performance, or generalized portable logic can improve a new concept without reusing an old template.
---

# Creative Reference Memory

## Purpose

Use Hottop's prior creative work as **mechanism/grammar/preference memory**, not as a template library.

Hottop now has two complementary memory layers:

1. **Concrete reference memory** — successful/failed cases, user feedback, visual/dialogue grammar and packaging evidence.
2. **Portable creative logic** — product-independent hook families, search keywords, hotspot domains and product-role mappings that survive a product swap.

Canonical sources:

- `integrations/creative-reference-library.yml`
- `docs/creative/creative-reference-memory.md`
- runtime: `hottop.creative_memory`
- CLI: `hottop-references search`
- `integrations/portable-creative-logic-library.yml`
- `skills/portable-creative-logic/SKILL.md`
- `docs/creative/portable-creative-logic-taxonomy.md`

## When to use

Use this after the current request has a resolved product and current hotspot context, especially when:

- a new hotspot resembles a past causal/relationship mechanism;
- the desired medium resembles a past successful native grammar;
- product insertion feels generic and past product-role examples could challenge it;
- a fresh hotspot contains a recognizable question/number/action/reversal and generalized hook logic could improve the bridge;
- the promoted product has changed and the old brand-specific wording must be remapped to a new product role;
- the request risks a known failure such as slideshow motion, weak product salience, over-polishing or internal production labels;
- a social-post request would benefit from remembered packaging patterns such as meme + product explainer + platform copy/hashtags.

Do not let retrieval replace fresh hotspot work. If the user supplied a hotspot, analyze that hotspot first. If none was supplied, perform current hotspot discovery first according to `PROJECT.md`.

## Retrieval workflow

1. Extract the current hotspot's exact repeated **question, phrase, number, action, object or reaction**, plus source-event facts and derivative-meme grammar.
2. Resolve the promoted subject's real job-to-be-done and candidate product roles.
3. Use `portable-creative-logic` to retrieve 3–7 generalized hook/bridge candidates by hotspot domain, signals, audience intent, product role, platform and risk.
4. Query the concrete reference library for the closest **mechanism**, **visual grammar**, **product role** and relevant negative guardrails.
5. Read why positive cases worked and what the user liked.
6. Read negative cases as hard warnings.
7. Generate fresh directions that preserve the current hotspot's own logic and current product truth.
8. Reject any direction that is merely a prior layout/character/scene/headline with names swapped.
9. Continue normal Hottop mechanism mapping, creative review and generation preflight.

Concrete-reference example:

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

Portable-logic lookup is conceptually keyed by IDs and keywords in `integrations/portable-creative-logic-library.yml`, for example:

- `open_question`
- `specific_number`
- `not_x_but_y`
- `constraint_deletion`
- `hotspot_question_product_work`
- `hotspot_action_product_action`
- `proof_demo`
- `one_sentence_compression`

## Product-swap rule

Never preserve a brand-specific line merely because the old campaign worked.

When the promoted product changes:

1. keep only the product-independent hotspot/hook mechanism that still makes sense;
2. re-resolve the new product's real capability;
3. assign a new product role;
4. rebuild the story consequence around that role;
5. re-rank platform format and copy.

Example generalized lesson:

`大家都想知道宇树值多少钱，问 InkClawAgent`

must **not** be stored as “Unitree + InkClaw.” Its reusable form is:

`active public question -> promoted product performs the real work required to investigate/answer/act`

Possible migrations:

- research product -> gather evidence / compare assumptions / produce research;
- sales-intelligence product -> find buyers, sellers and demand signals;
- knowledge product -> organize sources and decision context;
- automation product -> execute the workflow triggered by the question;
- creative product -> turn the question into a publishable asset;
- coding product -> implement/test the implied technical task.

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

Portable logic may teach:

- hook families and keyword banks;
- question/number/action/reversal detection;
- product-role migration;
- platform routing priors;
- domain-specific risk checks.

They may **not** silently become:

- the same four-panel template;
- the same actors/characters/mascot;
- the same composition;
- the same film frame/poster;
- the same punchline with nouns replaced;
- the same brand name with a new product swapped in;
- a substitute for current hotspot evidence.

`reuse_mode=guardrail_only` means the concrete reference entry is never a generation template.

## User feedback and platform performance are evidence

When the user gives concrete feedback, preserve the lesson when it is durable. Current examples include:

- film/movie hotspot creative must feel native to cinematic scene grammar;
- rough viral 3D should remain deliberately rough when roughness carries recognition;
- high-quality stills with pan/zoom are not cinematic video;
- do not print internal labels such as `热点梗图`, `今日热搜 TOP1`, or other research/workflow labels on audience-facing assets;
- keep the promoted product visually prominent enough that the promotional purpose is unmistakable;
- when useful, publish a hotspot meme together with a separate product explainer and platform-native title/body/#hashtags;
- hotspot exploration must go beyond the news event into the **active derivative meme**: what phrase, action, number, blame joke, callback, screenshot or remix people are actually repeating now;
- social titles should use **meme-native hook compression** rather than newsroom summaries. A strong pattern is `short utterance + concrete consequence`; reuse the pattern, not the people, exact event, brand, or layout;
- project-local 2026-09-01 platform screenshots suggest concrete conflict/outcome framing can outperform brand-name-first self-introduction for the shown account, and low image-depth supports putting the core promise/joke in the first image; classify this as `account_specific_observation`, not a universal platform law;
- the 2026-09-01 Unitree valuation creative established a portable `hotspot_question_product_work` mechanism: use the real public question as the hook and let the current product perform the truthful work needed behind that question;
- if a source story is marked fictional/satirical or a claim is unverified, keep that boundary explicit even when the derivative meme is real and widely circulating.

Do not invent user ratings or numeric quality scores. Store qualitative feedback unless an actual score exists.

## Learning classification

A new lesson belongs in **portable creative logic** only when it passes the product-swap test:

> If the promoted product changes, does the mechanism still make sense after reassigning the product role?

If yes, it can become a generalized hook/bridge rule.

If it depends on one mascot, exact visual, exact title, brand feature, source asset or campaign, keep it in concrete reference/campaign memory instead.

The current system is **retrieval + few-shot/preference memory + portable mechanism retrieval**, not reinforcement learning.

A later training path may use accumulated clean data for SFT, pairwise preferences/DPO, a reward model and eventually RL experiments. Do not introduce training infrastructure until dataset size, quality and measured value justify it.

## Asset policy

Normal Git stores the metadata, not large binary media by default.

- bind exact known reference bytes by SHA-256 where available;
- use approved Git LFS or object storage later for generated/original/user-authorized assets when an ingestion path exists;
- keep ordinary third-party copyrighted assets as metadata/source-analysis only;
- rights metadata never overrides copyright, likeness or trademark restrictions;
- prior Hottop images are normally retrieved for grammar/mechanism learning, not pixel copying.

## Persistent project protocol

On long/new/stale context, recover `PROJECT.md` then `STATUS.md`. After fresh/supplied-hotspot analysis, load `portable-creative-logic` when generalized mechanisms can help, then load concrete creative-reference memory when useful. Fresh hotspot evidence remains authoritative.

After durable new success/failure/performance learning:

- write campaign-specific evidence to concrete reference/campaign memory;
- promote only genuinely transferable logic into the portable library;
- record selected logic IDs so future platform performance can be attributed to a mechanism rather than a mascot or brand name.
