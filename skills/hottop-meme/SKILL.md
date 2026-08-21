---
name: hottop-meme
description: Turn fresh film, AI, technology, internet and culture trends into original four-panel product-comparison meme briefs with medium-matched visual treatment.
---

# Hottop Meme

Use this skill when the user asks for current-event memes, film/TV-inspired marketing memes, "来几个梗", or a four-panel comparison that promotes InkClawAgent or another configured product.

## Recovery first

When working in the `hottop` repository, read `PROJECT.md` and `STATUS.md` first. If a milestone is active, continue its open PR/CI work before starting unrelated refactors.

## Core rule: semantics stay, characters and medium change

Do **not** force a recurring mascot or one universal art style. The visual cast, genre, location, panel composition **and rendering medium** may change every run. Preserve this invariant instead:

1. current recognizable topic;
2. recognizable conflict or role relationship from that topic;
3. promoted product mapped to solver / breaker / winner;
4. optional comparison target mapped to obstacle / gatekeeper / cumbersome approach;
5. four panels: setup → escalation → reversal → punchline;
6. short product-centric final caption.

Example semantic pattern: a current mythic-seafaring film may suggest an original one-eyed cave guardian as the obstacle and an original tactician/seafarer as the solver. The roles can map to comparison target vs. promoted product without copying the movie's actor face, costume, frame or poster.

## Visual medium router — default, no extra user round-trip

Before writing the image prompt, classify the hotspot and automatically choose the rendering language that best matches how people recognize that hotspot. Do not ask the user to restate this unless the requested style is genuinely ambiguous.

### Film / live-action entertainment

Default to **highly photorealistic cinematic live-action** treatment: believable practical locations, natural skin/material texture, film lighting, dramatic lenses, depth, atmospheric haze, physically plausible scale and theatrical color grading. It should feel like a premium original movie still from the same broad genre, while remaining a newly staged composition.

- Epic/myth → large practical sets, natural landscape, torch/sunlight, textured costumes and props, cinematic scale.
- Sci-fi → realistic production design, practical/CG-integrated lighting, believable screens/objects, no copied franchise hardware.
- Horror/thriller → grounded practical darkness, motivated lighting, realistic spaces, suspenseful framing.
- Comedy → live-action realism with expressive staging and timing rather than cartoon rendering.

Never recreate an identifiable official frame, actor likeness, exact costume, prop, set, poster or title treatment. The target is **genre-faithful realism, not frame replication**.

### Animation / animated-film hotspots

Match the **broad animation medium** that makes the trend legible:

- 3D animated trend → original stylized 3D characters, materials, lighting and squash-and-stretch appropriate to animated cinema.
- 2D/anime/cartoon trend → original 2D illustration/cel language, line work and motion exaggeration appropriate to that family of media.
- deliberately crude/low-budget animation trend → preserve the cultural contrast (roughness, handmade awkwardness, low-poly feel) without copying protected character silhouettes or exact models.

Do not force photorealism onto an animation-native joke unless contrast itself is the joke.

### Internet personalities / creators / real-world social phenomena

Default to **real-world documentary/social-video realism**: plausible people, street/home/office environments, phone-camera or editorial photography cues, natural wardrobe and contemporary objects. Use original anonymous people unless the user provides a usable image or the likeness is otherwise permitted. Do not fabricate a recognizable real person's face.

### AI / technology / software-product hotspots

Default to **realistic contemporary tech-world imagery with light cinematic polish**: offices, launch events, control rooms, labs, creator desks, project rooms and believable devices. Prefer metaphorical physical props (queues, relay races, control towers, tool belts, assembly lines) over copying proprietary UI. Product superiority should be communicated through the joke's workflow outcome, not fake benchmark dashboards.

### Memes / slang / native internet formats

Match the format's **distribution grammar** rather than one house style: screenshot-like composition, reaction-photo realism, deliberately rough collage, low-budget 3D, poster parody, chat-style framing, etc. Rebuild the structure with original assets instead of tracing the source meme pixel-for-pixel.

### Mixed or uncertain hotspots

Choose the medium associated with the most recognizable part of the joke. If a movie becomes a real-world cosplay trend, for example, a real-world phone-camera treatment may outperform a film-still treatment. Optimize for instant recognition and punchline delivery.

## Style fidelity hierarchy

When generating a visual prompt, preserve these layers in order:

1. **medium fidelity** — film should feel filmed; animation should feel animated; real-world trends should feel real;
2. **genre fidelity** — epic, horror, comedy, tech launch, street meme, etc.;
3. **semantic fidelity** — recognizable roles/conflict from the hotspot;
4. **product mapping** — product visibly becomes the solver/breaker/winner;
5. **originality distance** — faces, costumes, layouts, props and exact shots remain original.

Do not solve copyright risk by making every concept generic clip-art. Keep the medium and genre highly legible while changing protected expression.

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

Use a topic's narrative archetype, medium and broad atmosphere, not protected production assets. Explicitly exclude:

- actor/celebrity likeness;
- exact movie frame or camera composition;
- official poster layout;
- copied costume/prop design;
- studio logo or official title treatment;
- a protected character design reproduced closely;
- proprietary product UI copied as a comparison prop.

Create original faces, clothing, props, color/lighting decisions and compositions. A generic mythic cyclops, sea voyage, cave, labyrinth, siege or superhero-like archetype can be used as transformed narrative language; do not claim it is an official scene.

## Output contract

Prefer the repository `MemeBrief` schema. Every ready concept should include:

- topic and timestamp;
- source/evidence URLs;
- conflict summary;
- product role and optional comparison role;
- `visual_medium` and `genre_treatment`;
- four scene descriptions + captions;
- 1–3 punchlines;
- master image prompt;
- negative prompt / exclusions;
- risk flags;
- claim status: `satire`, `supported`, or `needs_evidence`.

Archive strong concepts under `examples/runs/YYYY-MM-DD/` or the current run archive convention so future runs can reuse successful structures without repeating copyrighted visuals.
