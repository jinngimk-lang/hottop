# Adaptive Creative Orchestrator Design

## Goal

Make Hottop feel like a creative director rather than a configuration tool: accept a natural-language request, infer what is already known, ask only high-impact questions that materially affect the result, then produce platform-native, project-appropriate, culturally relevant creative with strong humor or visual metaphor and a clear path to render.

## Product principle

The interaction should optimize for **minimum interruption, maximum creative specificity**.

The system must know when to ask, when to infer, and when to stop asking. A long static form is explicitly not the target.

## Interaction model

Hottop exposes two entry modes that share one backend contract:

1. **Direct mode** — the user gives one natural-language request. The system resolves as much intent as possible and proceeds immediately when confidence is sufficient.
2. **Guided mode** — the system offers compact choices only for unresolved, high-impact decisions.

The default behavior is adaptive rather than fixed. If the user already supplied platform, style, product and campaign goal in the initial request, Hottop must not ask for them again.

## Core intent contract

Introduce `CreativeIntent` as the canonical front-door contract.

Fields:

- `promotion_target`: brand/product/service/feature/campaign/person/idea/keyword/tool plus optional URL or source profile;
- `campaign_goal`: awareness, pain-point contrast, product launch, conversion, brand memory, hotspot participation, category reframe, or auto;
- `platform`: xiaohongshu, douyin, wechat, weibo, instagram, x, linkedin, paid-social, generic-social, or auto;
- `style`: funny-meme, minimal-premium, cinematic, animation-native, documentary-real, social-native, commercial-product, or auto;
- `creative_ambition`: safe, witty, breakout, category-breaking;
- `product_visibility`: metaphor-first, balanced, product-first;
- `audience`: optional free-text or inferred working assumption;
- `hotspot_preference`: optional film/animation/tech/internet/social/consumer/native-meme/current-best;
- `constraints`: user restrictions, mandatory copy, excluded topics, rights-cleared assets, etc.

Each field carries provenance: `explicit`, `inferred`, or `defaulted`, plus a confidence value when inferred.

## Question router

Introduce `QuestionRouter` operating on `CreativeIntent` + unresolved fields.

A question is asked only when all of these are true:

1. the field is unresolved or low-confidence;
2. changing that field could materially change the creative output;
3. the answer cannot be safely inferred from the request, product profile, platform context, or existing project data;
4. the remaining question budget has not been exhausted.

Default question budget: **0–3 questions**. Most requests should require 0–1.

Priority order:

1. promotion target ambiguity;
2. campaign goal when multiple radically different goals remain plausible;
3. platform when format/copy structure materially depends on it;
4. creative ambition when the request does not imply desired boldness;
5. product visibility when reveal timing changes the concept;
6. audience only when it materially changes tone, risk or channel grammar.

The router returns either:

- `ready_to_create = true`, or
- one compact question with 2–6 options plus optional free-text fallback.

It must never emit a generic questionnaire containing every field.

## Creative ambition

`creative_ambition` is not a cosmetic control; it changes search behavior.

- `safe`: recognizable, low-risk, clear benefit communication; favor familiar format and modest surprise.
- `witty`: increase punchline, contrast and meme potential while keeping the core category frame.
- `breakout`: raise bridge surprise, reveal mechanics and ownability; permit more non-obvious hotspot mappings.
- `category-breaking`: explicitly increase constraint-deletion weight; challenge category defaults and prefer a new competition axis when truthful.

## Platform profiles

Introduce `PlatformProfile` as a reusable policy object. Platform selection changes the concept before rendering, not merely the aspect ratio after generation.

### Xiaohongshu

Favor strong cover hook, visual polish, 3–5 frame reveal/carousel when useful, compact Chinese copy, save/share motivation and product texture.

### Douyin

Favor first-second hook, immediate motion/readability, 3–8 second beat structure, stronger escalation and fast reveal/punchline.

### WeChat / Moments

Favor one strong visual or short carousel, lower information density, concise shareable copy and brand clarity.

### Weibo / X

Favor single-image or short-thread meme grammar, fast topical recognition and one-line punchline.

### Instagram

Favor visually ownable single image, carousel or short reel structure with minimal copy and strong art direction.

### LinkedIn

Reduce pure meme dependence; increase category insight, reframe, professional tension and evidence-aware comparison.

### Paid social

Prioritize product comprehension, brand attribution and conversion clarity earlier in the sequence; do not hide the product too long.

## Style profiles

Style must change creative grammar, not only prompt adjectives.

- `funny-meme`: increase conflict, reversal, exaggeration and punchline weight.
- `minimal-premium`: reduce text, prefer one dominant object, negative space and a single visual metaphor.
- `cinematic`: increase world-building, action, camera language, lighting/material realism and dramatic reveal.
- `animation-native`: allow stylized motion, transformation, exaggeration and animation-specific timing.
- `documentary-real`: favor credible everyday behavior, observational framing and low-artifice staging.
- `social-native`: optimize for scroll-stop hook, creator/social rhythm, compact overlays and distribution grammar.
- `commercial-product`: favor material/texture, product photography, sensory cues and product-led metaphor.

## Product visibility

`product_visibility` controls when the product is revealed:

- `metaphor-first`: product may remain partially hidden until the visual association is established;
- `balanced`: product is recognizable by the midpoint;
- `product-first`: product/brand appears immediately and the cultural idea supports it rather than delaying attribution.

Paid/conversion campaigns should bias toward `product-first` unless the user explicitly asks for a reveal.

## Project-shape adaptation

Hottop must fit different project categories rather than applying one meme template everywhere.

Examples:

- food/consumer goods → physical/sensory bridge, commercial-product or social-native medium, reveal and product texture;
- software/AI/B2B → workflow pain, category-default deletion, professional or tech-real medium, evidence-aware comparisons;
- entertainment/culture → cinematic/animation/native-meme grammar depending on the source medium;
- retail/fashion/beauty → form/material/style bridge, visual ownership and platform-native carousel/reel patterns;
- services/local businesses → ritual/outcome/emotion bridge, recognizable real-world scenario and social proof only when evidenced;
- campaigns/ideas/keywords → semantic and symbol bridges, more abstract visual metaphors, clear audience decoding.

The project category is a routing signal, not a permanent template.

## Creative orchestration

Once intent is ready, the orchestrator internally explores multiple directions before showing a result.

Minimum internal search set when feasible:

1. pain-point/old-way contrast;
2. natural bridge-led metaphor;
3. constraint-deletion/category reframe.

Additional candidates may be generated when the hotspot or product supports strong role, sensory, language or reveal mechanics.

Candidate generation must preserve platform/style/ambition/product-visibility constraints.

## Creative evaluation

Extend the existing seven-part Creative Review with contextual dimensions rather than replacing it.

Existing hard gate remains:

- instant comprehension;
- natural linkage;
- product centrality;
- surprise;
- ownability;
- evidence safety;
- original execution.

Add contextual scoring inputs:

- `platform_fit`;
- `style_fit`;
- `campaign_goal_fit`;
- `ambition_fit`;
- `project_shape_fit`;
- `hotspot_native_fit`;
- `humor_or_delight` when the selected style/goal expects humor.

Contextual scores help rank passing concepts; they do not allow a concept that fails the existing hard creative gate to pass.

## Humor quality

“H有梗” must not be reduced to adding a joke sentence. Humor/delight can come from:

- recognition + reversal;
- visual substitution;
- delayed reveal;
- category assumption being exposed as absurd;
- role inversion;
- product-specific physical behavior;
- concise language collision or double meaning;
- escalation that resolves into a product truth.

Reject generic punchlines that could be attached to any product unchanged.

## Creative package integration

The orchestrator produces a `CreativePackage` containing:

- resolved `CreativeIntent`;
- intent provenance/confidence;
- questions asked and answers, if any;
- promotion context and evidence;
- hotspot/comparison/reference inputs;
- 2–4 internal candidate concepts when available;
- review results;
- selected concept and selection rationale;
- `hottop.render.v2` handoff;
- optional alternate candidate summaries for “换方向 / 更大胆 / 更有梗 / 产品更明显”.

This package becomes the stable bridge between conversational front ends, future Studio UI, CLI and render adapters.

## Interaction output

The front end should not dump the full internal package by default. User-facing output is compact:

1. optional high-value question;
2. short “我准备这样做” preview only when useful;
3. final creative/result;
4. lightweight revision controls such as `换方向`, `更有梗`, `更大胆`, `产品更明显`, `更高级`, `换平台`.

These revision actions mutate `CreativeIntent` or candidate selection and rerun only the necessary stages instead of starting from scratch.

## CLI / API direction

Foundation implementation should remain CLI-first and provider-neutral.

Planned contracts:

- `hottop intent <request>` → structured intent + unresolved high-impact fields;
- `hottop next-question <intent.json>` → next question or ready state;
- `hottop orchestrate <package-input.json>` → candidate package + selected concept + render-v2;
- `hottop package-concepts <package.json>` remains the lower-level explicit candidate selection path.

A future Studio UI should consume the same contracts rather than introduce separate business logic.

## Error and fallback behavior

- If product/category facts are insufficient for a factual comparison, downgrade to satire/metaphor/generic proxy.
- If no strong hotspot bridge is found, fall back to category reframe or product-led metaphor rather than forcing a trend.
- If all candidates fail the creative hard gate, do not output a weak winner; regenerate with a different bridge/format strategy.
- If platform is unknown, use `generic-social` and preserve a platform switch without rebuilding product semantics.
- If the user supplies a rights-cleared asset, preserve that provenance through references/render handoff.

## Persistence and learning

This interaction/orchestration doctrine is durable project direction and must be reflected in `PROJECT.md`, relevant skills and loop prompts.

When repeated production reveals a better question, stronger platform grammar, better ambition mapping or recurring successful creative pattern, audit it. If durable, update the charter/skill/spec instead of leaving it in chat history.

## Non-goals for Foundation v0.1

- no heavy web dashboard before CLI contracts are stable;
- no mandatory LLM provider inside the core package;
- no vector database requirement;
- no attempt to replace creative judgment with deterministic scoring;
- no requirement to ask every intake question;
- no fixed number of visible concepts for every request.

## Success criteria

A request such as “给这个咖啡新品做一个小红书能出圈的电影热点广告，高级一点，产品别一上来全露” should resolve most fields without redundant questions, infer Xiaohongshu + premium/cinematic + breakout + metaphor-first, ask at most one material question if the promoted SKU is ambiguous, explore multiple internal directions, select a passing concept with strong platform/project fit, and emit a flexible render-v2 package suitable for direct image generation.
