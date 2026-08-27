# Creative Reference Memory

Date: 2026-08-27
Status: durable Production v0.2 creative-memory contract

## Purpose

Hottop should get better from prior work without turning prior work into a template factory.

The canonical machine-readable library is `integrations/creative-reference-library.yml`. It stores reusable **mechanisms, native visual/dialogue/audio grammar, product-role logic, user feedback, promotion lessons and negative patterns** from successful and failed Hottop work.

Current implementation is **not reinforcement learning**. It is retrieval + few-shot/preference memory:

1. store structured examples and failures;
2. retrieve similar mechanisms/grammars before ideation when useful;
3. use positive cases as reasoning exemplars, not pixel/layout templates;
4. use negative cases as fail-closed guardrails;
5. continue fresh hotspot research for every new request;
6. collect platform performance signals when available;
7. only consider SFT/DPO/reward-model/RL work after enough clean labeled data exists to justify training.

## Retrieval order inside a creative run

Freshness remains authoritative. Creative memory never replaces current-hotspot research.

For a new generation:

1. recover `PROJECT.md`, `STATUS.md` and active creative skills;
2. analyze the user-supplied hotspot, or discover current hotspots if none was supplied;
3. extract the current hotspot's recognition hook, causal/relationship mechanism, native visual/dialogue/audio grammar and promotional objective;
4. query `hottop-references search` for similar **mechanisms**, **native grammar**, **product roles** and relevant negative patterns;
5. use retrieved positives to expand/check creative directions, not to reuse the old composition;
6. apply retrieved negatives as guardrails;
7. build a fresh product↔hotspot bridge and run normal generation preflight;
8. after user feedback or publication results, append/update memory with evidence rather than relying on chat recollection.

## What an entry should preserve

A useful case records:

- hotspot/category and recognition hook;
- causal or relationship mechanism;
- product bridge and product's functional role;
- story outcome before/after the product acts;
- native visual grammar;
- dialogue/language rhythm;
- audio/BGM/Foley grammar for motion;
- format/distribution grammar;
- why the concept worked or failed;
- direct user feedback;
- promotion lessons such as product salience or clarity;
- `what_not_to_copy` rights/originality boundaries;
- negative patterns worth blocking later;
- optional rights/provenance asset metadata;
- later platform performance metrics when actually available.

Do not invent numeric quality/performance scores. Add numbers only when they come from a real evaluator, user rating or platform analytics source.

## Positive and negative memory are equally important

Failures are first-class data. Current seeded guardrails include:

- still-image pan/zoom or Ken Burns motion cannot satisfy cinematic-video delivery;
- internal workflow labels such as `热点梗图` do not belong on audience-facing assets;
- a good joke can still fail promotion if InkClawAgent is visually buried;
- over-polishing a deliberately rough native meme can destroy recognition and humor;
- a meme-only post can attract attention yet leave the audience unclear about the product.

## Publishing-package memory

When the user is preparing content for social platforms, Hottop may choose a paired package when it increases clarity:

1. **hotspot-native meme/creative asset** — earns attention and carries the story/joke;
2. **product explainer asset** — clearly states what InkClawAgent/product does without overloading the meme;
3. recommended asset order;
4. platform-specific title/hook;
5. body copy;
6. hashtag set;
7. optional video caption/cover-line variants.

This is a packaging pattern, not a mandatory two-image template. If one asset communicates both joke and product clearly, do not add a second asset merely to satisfy a rule.

## Asset storage and rights

The library can describe an image without committing that binary to normal Git.

Default rules:

- generated/original or user-authorized assets may be ingested later through an approved Git LFS or object-store workflow;
- ordinary third-party film frames, meme screenshots, copyrighted posters and other non-cleared media remain metadata/source-analysis only;
- current conversation examples are bound by SHA-256 metadata so the exact files can be recognized later, but their PNG bytes are not added to ordinary Git in this change;
- `rights_mode` controls allowed reference use; metadata authorization never overrides copyright/likeness/trademark rules;
- even owner-authorized prior Hottop imagery should normally be reused for mechanism/grammar learning rather than copied as a new visual template.

## Current seeded lessons

### Odyssey transformation/rescue

Strong because the product participates in the source causal chain: hostile transformation/workflow complexity changes the crew's state, the rescuer/InkClawAgent reverses the blocked state, and the journey continues. Film/live-action grammar therefore stays cinematic and original.

### Niulai rough-3D family dialogue

Strong because the meme's low-budget 3D surface, family relationship, blunt Q&A and modern technical vocabulary collide naturally. The roughness is intentional native grammar, not a license for random quality failure.

### Product salience

Hotspot immersion and brand clarity are both hard requirements. The decisive InkClawAgent intervention/reveal must be legible at mobile scale and contrast clearly enough that viewers understand which product changed the outcome.

### Meme + product explainer

Use a second product card when the meme earns attention but cannot explain the product without damaging the joke. Package both with platform-native copy and hashtags when the user is preparing to publish.

## Future learning path

If the library grows into a large, clean dataset, Hottop may later derive:

- supervised fine-tuning examples;
- pairwise preference data;
- DPO/preference optimization datasets;
- a creative-quality/promotion reward model;
- eventually reinforcement-learning experiments if there is enough validated reward signal.

Do not call the current retrieval library RL, and do not start model training merely because examples exist. The immediate value is better retrieval, stronger critique and durable project memory at near-zero infrastructure cost.
