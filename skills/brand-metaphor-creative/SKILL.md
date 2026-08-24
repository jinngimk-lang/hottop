---
name: brand-metaphor-creative
description: Use when creating promotional creative that connects a brand, product, service, feature, campaign, keyword, or idea with a film, animation, cultural trend, meme, competitor, or category convention.
---

# Brand Metaphor Creative

## Overview

Create advertising people understand before they finish reading it. The promoted subject should become part of the cultural idea—an action, object, transformation, role, material, route, environment, or reveal—not a logo pasted onto a trend.

Core principle: **reframe before optimize**. Do not automatically make a better version of the category's current answer. First ask whether the category default itself should disappear.

## 1. Resolve the subject before the joke

Identify the promoted subject's category, job-to-be-done, pain point, differentiator, physical/sensory properties, usage ritual, emotional payoff, and recognizable alternatives. Research current facts when the subject or market is unfamiliar or time-sensitive.

A product does not have to be the hero character. It can be the decisive prop, material, gesture, route, transformation, environment, or final reveal.

## 2. Find the category default

Name the assumption competitors are mostly optimizing: the **category default**. Examples: more buttons, a better keyboard, a faster queue, more tools, more steps, more features, a familiar packaging convention, or a standard interaction ritual.

Then run **constraint deletion**:

- Why must this assumption exist?
- What if it disappears entirely?
- What user outcome remains after deleting it?
- What new competition axis becomes important instead?

Prefer `old premise → deleted constraint → new axis` when it creates a more truthful, surprising and ownable idea than ordinary feature comparison.

## 3. Bridge search

Find the strongest natural bridge between the subject and the hotspot. Search across:

- **shape/material** — length, stretch, texture, color, liquid, transparency, weight;
- **action/motion** — pull, shoot, wrap, snap, transform, connect, launch, escape;
- **role** — guide, key, shield, director, breaker, fuel, shortcut;
- **function** — coordinate, unlock, cool, protect, energize, simplify;
- **emotion/ritual** — relief, indulgence, speed, confidence, habit, celebration;
- **language/symbol** — a phrase, gesture, visual grammar, or culturally recognizable structure.

The bridge must make the product feel inevitable in the idea. If the link only works after a paragraph of explanation, reject it.

## 4. Explore beyond the first obvious idea

Before locking a concept, internally explore at least three distinct directions when the brief allows it:

1. **pain-point contrast** — old way or competitor friction vs. desired outcome;
2. **bridge-led metaphor** — product property/action naturally becomes part of the hotspot;
3. **constraint-deletion reframe** — challenge the premise the category is currently optimizing.

Do not force all three into the final answer. Use them to avoid settling for the first merely acceptable joke. Prefer the idea with the strongest natural linkage, product specificity and surprise.

## 5. Format selection

Do not force every concept into four panels. Choose the smallest format that makes the metaphor land:

- **single visual metaphor** — one instantly legible fusion;
- **swipe-reveal carousel** — tease the cultural cue, extend the transformation, then reveal the product/brand;
- **four-panel narrative** — setup → escalation → reversal → punchline;
- **faux film still/poster** — strong cinematic role or emotion;
- **split old-vs-new** — ideal for category reframing and constraint deletion;
- **product-as-prop/action** — the product itself performs the recognizable cultural action.

For swipe-reveal, each frame must add information. Do not show the full answer in frame one.

## 6. Competitor logic

Research direct competitors, incumbents, adjacent substitutes, legacy workflows, and manual workarounds. A **named competitor** is useful only when the contrast is accurate and supported, or unmistakably subjective satire. Never invent defects, benchmarks, outages, prices, safety failures, or customer sentiment.

Sometimes the strongest antagonist is not another brand but the old category assumption itself. Prefer that when it makes the idea cleaner, more surprising and less misleading.

## 7. Match the source medium

Film/live-action hotspots should feel like original live-action cinema; animation hotspots should use an original animation-native treatment; real people/social phenomena should feel documentary/social-native; food/consumer products can use polished commercial product photography; internet-native jokes should match their distribution grammar.

Match **medium and recognition cues**, not protected assets. Do not reproduce actor likenesses, exact frames, official posters, protected character designs, proprietary UI, logos, or distinctive trade dress unless the user supplied assets they are entitled to use.

## 8. Distribution-native restraint and motion

Treat the social asset as entertainment first and attribution second when the brief is hotspot participation, meme reach, or brand memory. Do not turn a good joke into a conversion poster by default.

- **No in-asset destination by default** — omit URLs, QR codes, app-store badges and commands such as `立即体验` unless the user explicitly requests conversion creative or the channel genuinely requires the destination inside the asset. Brand/product attribution and a short payoff are usually enough.
- **Motion when timing carries the joke** — if recognition depends on character action, transformation, dialogue, sound, reaction timing, physical escalation, or a film/animation-native cue, prefer a short video, GIF, or animated sequence over flattening the idea into a static poster.
- **Continuous motion, not slideshow cosplay** — a narrative video should preserve scene geography, character continuity and action continuity with follow/pan/reaction/match-action/foreground-occlusion transitions where useful. Do not assemble unrelated stills with hard cuts and call it cinematic motion.
- **Benefits appear as consequences** — product advantages should emerge from what happens in the scene (the task starts, the obstruction disappears, the ritual shortens) before they appear as labels. Avoid feature-list end cards unless a conversion brief explicitly asks for one.
- **Keep the payoff light** — the final attribution should be compact enough that the audience still experiences the piece as a meme/scene rather than an advertisement.

This rule supersedes the older habit of automatically adding a URL CTA or forcing a dynamic hotspot into a static poster merely because the poster is easier to render.

## 9. Anti-Polish / Controlled Badness for motion

Use **Anti-Polish / Controlled Badness** when the creative advantage comes from looking deliberately cheap, strange, awkward or homemade while the comedy itself remains tightly directed. The stable formula is **low production feel + high comedy control**.

Deliberately permit rough/low-poly 3D, simple materials, imperfect lighting, slightly stiff movement, blunt Foley, cheap-sounding instrumentation, deadpan acting, abrupt physical comedy and absurd events treated seriously. These are aesthetic choices, not permission for random failure.

Never sacrifice **character continuity**, scene geography, cause/effect, **subtitle correctness**, dialogue intelligibility, **comedy timing**, product semantics, claim safety or rights safety. The story and joke must be more controlled precisely because the surface looks uncontrolled.

Keep the promoted product native to the intentionally crude world. Do not suddenly insert glossy blue-purple AI holograms, polished mascot teams, luxury product lighting, feature-card UI or a premium sci-fi end card unless the concept explicitly calls for them. Product benefits should be dramatized as dialogue, action and consequences inside the joke.

For config-driven video production inside Hottop, preserve the provider-neutral `hottop.render.v2` creative handoff and route downstream through `hottop.video-plan.v1`. **Wan2.2** is the primary optional open-source local shot-generation candidate. **MoviePy** is the default deterministic **headless** compositor for unattended config-driven execution: assemble generated shots, dialogue captions and original synthetic rough-comedy audio without requiring a browser or editor UI. **FFmpeg** is the final compatibility encoder. **Motion Canvas** remains available as an optional advanced vector-motion, interactive-preview and special-effects layer rather than a requirement for the automatic headless path. Model downloads, GPU execution and external binaries remain operator-controlled. Remotion may be evaluated only as an optional adapter after its current license is reviewed for the operator's entity.

`hottop video-run` must remain dry-run by default. Only explicit `--execute` may spawn trusted local stages, after fail-closed readiness checks, with structured argument arrays, `shell=False`, fixed stage order and explicit working directories. It must never silently install packages, download models, provision GPU resources, enable paid services or fetch copyrighted source footage.

Treat the editable `hottop.render.v2` plus the selected repository video profile as canonical source. `hottop.video-plan.v1` is a deterministic derived execution artifact and should be regenerated rather than maintained as a second manually edited source of truth.

Broad low-budget 3D grammar, archetypal animal roles, deadpan family dynamics and crude animation language may be re-created with original staging. Do not use exact film frames, soundtrack, source footage, protected character designs or pixel-level copies as generation targets.

## 10. Adaptive interaction routing

Treat intake as a creative-director conversation, not a static questionnaire. Resolve what the user already said, attach provenance/confidence to inferred values, and **ask only high-impact questions** that materially change the creative output. The default interaction budget is 0–3 questions; stop asking once the remaining uncertainty no longer justifies interruption.

The stable interaction dimensions are:

- **campaign goal** — awareness, pain-point contrast, launch, conversion, brand memory, hotspot participation or category reframe;
- **platform** — a creative input that changes structure, hook, pacing and copy grammar, not just export dimensions;
- **style** — changes the creative grammar itself, such as reversal/punchline, premium negative space, cinematic world-building, animation-native transformation or documentary realism;
- **creative ambition** — `safe`, `witty`, `breakout`, `category-breaking`; higher ambition increases surprise and category-reframing pressure without weakening evidence or originality rules;
- **product visibility** — `metaphor-first`, `balanced`, `product-first`, controlling when the product becomes explicit and how strong attribution should be;
- **audience** — optional by default; ask only when it materially changes tone, decoding, risk or channel conventions.

Question priority is promotion target → campaign goal → platform → style → creative ambition → product visibility. Explicit user choices override inference. If the question budget is exhausted, proceed with conservative defaults instead of blocking production.

Route treatment by **project shape**, not one universal meme template:

- food/consumer → physical/sensory bridge, product texture and polished commercial/social-native treatment;
- software/AI/B2B → workflow pain, evidence-aware comparison and category-default deletion;
- entertainment/culture → source-medium cinematic, animation or native-meme grammar;
- fashion/beauty/retail → form/material/style bridge and visual ownership;
- services/local → ritual/outcome/emotion bridge and credible real-world scenarios;
- campaigns/ideas/keywords → semantic/symbol bridge and fast decoding.

The seven-part Creative Review remains the hard gate. Platform/style/goal/ambition/project-shape/hotspot-native fit may rank concepts that already pass; they must never rescue a weak, generic or unsafe concept. Revision controls such as `换方向`, `更有梗`, `更大胆`, `产品更明显`, `更高级` or `换平台` should mutate the smallest relevant intent dimension and reuse stable product understanding where possible.

## Creative review gate

Before approving a concept, score it on:

1. **Instant comprehension** — understandable in 1–3 seconds.
2. **Natural linkage** — hotspot and product connect through a real bridge, not a pasted reference.
3. **Product centrality** — removing the product breaks the idea.
4. **Surprise** — contains a non-obvious jump or category reframe.
5. **Ownability** — feels specific to this subject, not reusable for any brand.
6. **Evidence safety** — factual comparisons are supported; otherwise satire/metaphor.
7. **Original execution** — recognizable cultural grammar without copying protected production assets.

Reject concepts that are merely `hot character + logo`, feature lists wearing costumes, references needing a paragraph of explanation, or jokes that could advertise any competitor unchanged.

## Persistent project protocol

When this work becomes a new multi-session project, do not rely on conversation memory alone. Create a **living project charter** in the repository before substantial implementation or repeated production. For Hottop this is `PROJECT.md`; use `STATUS.md` for current execution state.

### Bootstrap a new project

The charter should capture durable direction rather than a transcript:

- mission, audience, success criteria and non-goals;
- canonical creative/product doctrine;
- architecture and major integrations;
- operating constraints and evidence/safety rules;
- stable workflow and output contracts;
- reusable skills and **recovery order**;
- major decisions plus a compact **decision log** when rationale matters.

Keep temporary CI IDs, hourly research and short-lived tasks in status/archives so the charter stays readable.

### Context recovery

When there is **context pressure**—a long conversation, new session, agent handoff, uncertainty about prior choices, or return after time away—reread repository truth before continuing. Recovery order:

1. project charter (`PROJECT.md` or equivalent);
2. current status (`STATUS.md`);
3. active skill(s);
4. newest relevant spec/plan/decision record;
5. live PR/CI/evidence state.

Do not ask the user to repeat stable direction that the repository already records.

### Evolve the project deliberately

If a durable new direction appears—a new creative structure, better medium rule, category-reframing principle, integration strategy, safety boundary, recurring instruction, or repeatedly successful pattern—review it against the existing doctrine before adopting it.

If it survives review, **update the charter** and the relevant skill/spec in the same workstream. Record what changed, what old assumption it supersedes, and why in the decision log when the rationale would otherwise be lost. Then update status so the next recovery sees the new direction immediately.

Do not silently stack contradictory rules. Keep one canonical current interpretation. After meaningful changes, reread the charter for contradictions, stale assumptions, duplication, missing recovery steps and examples that have become too narrow.

The target is not merely persistence. Each recovery should make the project **more precise, more stable and more creatively capable** because durable learning has been distilled into the repository.

## Output contract

Return or archive: promotion context; interaction intent/provenance; category default; deleted constraint; new competition axis; hotspot; bridge type + bridge sentence; comparison target + evidence mode; selected format; platform/style/project-shape treatment; distribution treatment; reveal/narrative beats; visual medium; copy/punchline; image/video prompt; dialogue/SFX/BGM cues when motion is selected; exclusions; risk flags; claim status; provider-neutral `hottop.render.v2`; and `hottop.video-plan.v1` when a config-driven motion plan is requested.

When working inside `hottop`, read `PROJECT.md` and `STATUS.md` first. Use `hottop-meme` for hotspot acquisition, evidence handling, and four-panel-specific execution when that format is selected.
