---
name: hottop-meme
description: Turn fresh film, AI, technology, internet and culture trends into original four-panel product-comparison meme briefs.
---

# Hottop Meme

Use this skill when the user asks for current-event memes, film/TV-inspired marketing memes, "来几个梗", or a four-panel comparison that promotes InkClawAgent or another configured product.

## Recovery first

When working in the `hottop` repository, read `PROJECT.md` and `STATUS.md` first. If a milestone is active, continue its open PR/CI work before starting unrelated refactors.

## Core rule: semantics stay, characters change

Do **not** force a recurring mascot. The visual cast, genre, location and panel composition may change every run. Preserve this invariant instead:

1. current recognizable topic;
2. recognizable conflict or role relationship from that topic;
3. promoted product mapped to solver / breaker / winner;
4. optional comparison target mapped to obstacle / gatekeeper / cumbersome approach;
5. four panels: setup → escalation → reversal → punchline;
6. short product-centric final caption.

Example semantic pattern: a current mythic-seafaring film may suggest an original one-eyed cave guardian as the obstacle and an original tactician/seafarer as the solver. The roles can map to comparison target vs. promoted product without copying the movie's actor face, costume, frame or poster.

## Research workflow

1. Pull candidates from at least two independent source families when possible: hot-list aggregator, news/RSS, video/social/community, or direct publisher.
2. Prefer topics from the last 24–72 hours; allow older topics if discussion is spiking now.
3. Merge duplicates and record cross-source presence.
4. Rank for recency, recognizability, conflict clarity, visual potential, product fit and evidence quality.
5. For the selected topic, write a one-sentence "why people recognize this now" note with source URLs.

## Role-mapping workflow

Extract only the narrative logic needed for the joke:

- obstacle vs. solver;
- monster vs. clever hero;
- maze vs. guide;
- siege/gate vs. breaker;
- fragmented tools vs. orchestrator;
- slow manual process vs. automation.

Map the promoted product to the role that naturally demonstrates the configured strengths. Do not invent product capabilities merely to fit a joke.

## Four-panel writing

Each panel must do one job:

- **Panel 1 — setup:** immediately recognizable world/problem.
- **Panel 2 — escalation:** comparison target or legacy workflow becomes the friction/obstacle.
- **Panel 3 — reversal:** promoted product enters and changes the logic of the scene.
- **Panel 4 — punchline:** visual resolution + one short product line.

Panels may use different shot scales, locations or supporting characters. Continuity of the joke matters more than identical compositions.

## Copy rules

Default to Chinese when the active marketing conversation is Chinese. Keep captions short enough to read on a phone.

Good satirical endings include:

- `还得是 <Product> 强`
- `真破局，还得看 <Product>`
- `别跟困局耗，直接上 <Product>`

These are subjective/satirical. Claims like `快 10 倍`, `最便宜`, `准确率第一`, or `比 X 快` are objective comparison claims and require evidence. Without evidence, rewrite or mark `needs_evidence`.

## Visual safety / originality

Use a topic's narrative archetype and broad atmosphere, not protected production assets. Explicitly exclude:

- actor/celebrity likeness;
- exact movie frame or camera composition;
- official poster layout;
- copied costume/prop design;
- studio logo or official title treatment;
- a protected character design reproduced closely.

Create original faces, clothing, props, color/lighting decisions and compositions. A generic mythic cyclops, sea voyage, cave, labyrinth, siege or superhero-like archetype can be used as transformed narrative language; do not claim it is an official scene.

## Output contract

Prefer the repository `MemeBrief` schema. Every ready concept should include:

- topic and timestamp;
- source/evidence URLs;
- conflict summary;
- product role and optional comparison role;
- four scene descriptions + captions;
- 1–3 punchlines;
- master image prompt;
- negative prompt / exclusions;
- risk flags;
- claim status: `satire`, `supported`, or `needs_evidence`.

Archive strong concepts under `examples/runs/YYYY-MM-DD/` so future runs can reuse successful structures without repeating copyrighted visuals.
