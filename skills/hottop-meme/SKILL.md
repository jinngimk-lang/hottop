---
name: hottop-meme
description: Turn fresh cultural trends into original four-panel marketing memes for any user-supplied brand, product, service, feature, campaign, person, idea, keyword, or tool, with evidence-aware competitor discovery and medium-matched visual treatment.
---

# Hottop Meme

Use this skill when the user supplies a marketing term or subject and wants a current-event meme, film/TV-inspired marketing meme, “来几个梗”, or a four-panel comparison. **Do not assume the promoted subject is InkClawAgent, AI software, or even a technology product.** The subject can be any brand, product, service, feature, campaign, person, idea, keyword, or tool.

## Recovery first

When working in the `hottop` repository, read `PROJECT.md` and `STATUS.md` first. If a milestone is active, continue its open PR/CI work before starting unrelated refactors.

## Core rule: resolve the marketing semantics before choosing the joke

The input term is only a name. First infer or research what it means commercially. Build a compact promotion context:

1. **subject type** — brand / product / service / feature / campaign / person / idea / keyword / tool;
2. **category** — what buyers/users would compare it with;
3. **job to be done** — what the user is trying to accomplish;
4. **pain point** — what friction the subject plausibly removes;
5. **differentiator** — what is distinctive about this subject for that pain point;
6. **recognizable alternatives** — direct competitors, adjacent substitutes, incumbent defaults, legacy workflows, or manual workarounds.

If the subject is unfamiliar, ambiguous, current, or could have changed, research it before writing the meme. Never force AI-agent language onto a shoe, drink, car accessory, beauty product, restaurant, travel service, consumer app, creator brand, or other unrelated category.

## Comparison discovery — automatic when the user does not name a rival

When the user gives only a promoted term, automatically find comparison candidates. Do not ask them to supply a competitor unless research genuinely cannot resolve the category.

Search in this order:

1. **Direct competitor** — a recognizable brand/product serving the same category and job.
2. **Incumbent/default** — the thing people already use by habit.
3. **Adjacent substitute** — a different category that solves the same job imperfectly or differently.
4. **Legacy workflow** — an older multi-step way of doing the job.
5. **Manual workaround** — spreadsheets, queues, paper, phone calls, DIY steps, etc.

Useful research queries are generated from the resolved semantics, for example:

- `"<subject>" competitors`
- `"<subject>" alternatives`
- `best <category> for <job-to-be-done>`
- `<pain point> alternatives`
- `"<subject>" vs "<known alternative>"`

Prefer current direct brand/product pages plus independent reputable sources. Do not treat SEO listicles as proof of a competitor weakness.

### Comparison target selection

Pick the target that maximizes:

- recognizability;
- category/job overlap;
- clarity of the pain-point contrast;
- evidence quality;
- meme-role fit;
- low risk of misleading factual claims.

A famous competitor is not automatically the best target. Sometimes the clearest antagonist is the incumbent habit or manual workaround.

### Named competitors: compare the situation, not invented defects

The meme may name a real brand when useful, but the negative side of the joke must be one of:

- a **supported factual limitation** backed by evidence;
- a **category/design tradeoff** that is accurately described;
- a **specific pain point the competitor is not designed to solve**;
- a clearly subjective/satirical framing;
- a fictionalized category proxy when a named-brand attack would overstate the evidence.

Never invent outages, prices, benchmark results, quality defects, safety failures, customer sentiment, or “X cannot do Y” claims. If evidence is insufficient, keep the contrast metaphorical and set claim status to `satire` or `needs_evidence`.

## Topic mapping: semantics stay, characters and medium change

Do **not** force a recurring mascot or universal art style. Preserve this invariant:

1. current recognizable topic;
2. recognizable conflict or role relationship from that topic;
3. promoted subject mapped to solver / breaker / winner / desired outcome;
4. selected comparison target mapped to obstacle / gatekeeper / cumbersome or mismatched approach;
5. four panels: setup → escalation → reversal → punchline;
6. final line names the promoted subject or its key phrase.

The subject’s category determines what “winning” means. For software it may be finishing a workflow; for shoes it may be comfort or pace; for a drink it may be convenience/taste occasion; for a service it may be removing waiting; for a campaign it may be recall or participation. Do not invent capabilities merely to make the metaphor work.

## Visual medium router — default, no extra user round-trip

Before writing the image prompt, classify the hotspot and automatically choose the rendering language that best matches how people recognize it.

### Film / live-action entertainment

Default to **highly photorealistic cinematic live-action** treatment: believable practical locations, natural skin/material texture, film lighting, dramatic lenses, depth, atmospheric haze, physically plausible scale and theatrical color grading. It should feel like a premium original movie still from the same broad genre, while remaining a newly staged composition.

- Epic/myth → practical sets, natural landscape, torch/sunlight, textured costumes and props, cinematic scale.
- Sci-fi → realistic production design and believable devices, no copied franchise hardware.
- Horror/thriller → grounded darkness, motivated lighting and suspenseful framing.
- Comedy → live-action realism with expressive staging and timing.

Never recreate an identifiable official frame, actor likeness, exact costume, prop, set, poster or title treatment. The target is **genre-faithful realism, not frame replication**.

### Animation / animated-film hotspots

Match the broad animation medium that makes the trend legible: original stylized 3D for 3D animation; original 2D/cel language for 2D/anime/cartoon; deliberately rough/low-poly grammar for a crude-animation meme. Do not copy protected character silhouettes or exact models.

### Internet personalities / creators / real-world social phenomena

Default to **real-world documentary/social-video realism**: plausible anonymous people, streets, homes, offices, phone-camera/editorial cues and contemporary wardrobe. Do not fabricate a recognizable real person’s face.

### Technology / software-product hotspots

Use **realistic contemporary tech-world imagery with light cinematic polish**: offices, launch events, control rooms, labs, creator desks and project rooms. Prefer metaphorical physical props over copying proprietary UI.

### Memes / slang / native internet formats

Match the format’s distribution grammar: reaction-photo realism, rough collage, low-budget 3D, poster parody, chat-style framing, etc. Rebuild the structure with original assets instead of tracing the source meme pixel-for-pixel.

### Mixed hotspots

Choose the medium associated with the most recognizable part of the joke. Optimize for instant recognition and punchline delivery.

## Role-mapping workflow

Extract only the narrative logic needed for the joke, such as:

- obstacle vs. solver;
- monster vs. clever hero;
- maze vs. guide;
- siege/gate vs. breaker;
- two rivals fighting while the customer waits;
- flashy demo vs. useful work;
- expensive/slow ritual vs. simpler route;
- fragmented steps vs. one coherent experience;
- queue/waiting vs. instant access;
- bulky/heavy vs. light/portable;
- generic/default choice vs. purpose-built choice.

Map the promoted subject to the role that naturally demonstrates its real differentiator for the selected pain point.

## Four-panel writing

Each panel must do one job:

- **Panel 1 — setup:** recognizable hotspot world + real user pain point.
- **Panel 2 — escalation:** comparison target, incumbent, or old workaround embodies the friction.
- **Panel 3 — reversal:** promoted subject enters and solves that specific pain point through its real differentiator.
- **Panel 4 — punchline:** visual resolution + one short promoted-subject line.

Panels may use different shot scales, locations or supporting characters. Continuity of the joke matters more than identical composition.

## Copy rules

Default to Chinese when the active marketing conversation is Chinese. Keep captions short enough for phone viewing. Product-neutral endings include:

- `还得是 <Subject>`
- `这题，<Subject> 会解`
- `别跟痛点耗，直接上 <Subject>`
- `<Old way> 还在卡，<Subject> 已经过去了`

Statements such as `快 10 倍`, `最便宜`, `销量第一`, `续航更长`, `比 X 更安全`, or `X 做不到` are objective comparative claims and require evidence.

## Visual safety / originality

Use a topic’s narrative archetype, medium and broad atmosphere, not protected production assets. Exclude actor/celebrity likeness, exact movie frames, official posters, copied costume/prop designs, protected character replicas, competitor logos when unnecessary, proprietary UI, and distinctive packaging/trade dress copied as a visual attack prop.

## Output contract

Prefer repository schemas. Every ready concept should include:

- promoted subject profile: type, category, job, pain point, differentiator;
- topic and timestamp;
- source/evidence URLs;
- discovered comparison candidates and why one was selected;
- conflict summary;
- subject role and comparison role;
- `visual_medium` and `genre_treatment`;
- four scene descriptions + captions;
- 1–3 punchlines;
- master image prompt;
- negative prompt / exclusions;
- risk flags;
- claim status: `satire`, `supported`, or `needs_evidence`.

Archive strong concepts so future runs can reuse semantic structures without repeating copyrighted visuals.
