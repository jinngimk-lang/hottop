# Config-Driven Video Production Design

## Goal

Make motion/video a first-class Hottop output that can be produced from repository configuration rather than reconstructed ad hoc in chat. The system must preserve Hottop's creative doctrine, especially continuous narrative motion, ad-light distribution, product benefits as consequences, and the new **Anti-Polish / Controlled Badness** strategy.

## Strategic differentiation: Controlled Badness

Most AI video systems compete on polish: more realistic lighting, smoother motion, cleaner CGI, more cinematic detail, and more expensive-looking output. Hottop must deliberately support the opposite competition axis when the idea benefits from it.

**Controlled Badness = low production feel + high comedy control.**

The output may intentionally use:

- visibly cheap / rough 3D or low-poly rendering;
- simple materials, imperfect lighting, slightly stiff motion and awkward timing;
- blunt Foley, cheap MIDI/xylophone/bass-pluck/folk-instrument cues;
- deadpan acting and absurd events treated seriously;
- simple story logic that is immediately legible;
- intentionally unsophisticated visual effects.

But the following are never allowed to become random or broken:

- character identity and scene continuity;
- shot geography and cause/effect;
- subtitle correctness and legibility;
- dialogue intelligibility;
- comedy timing;
- product semantics and claim safety;
- evidence / rights constraints;
- output encoding compatibility.

Internal principle: **Do not polish the badness away; make the badness precise.**

Anti-Polish is not a permanent global default. It is a selectable creative style / production profile used when a hotspot, film/animation grammar, meme, or campaign benefits from intentionally crude production.

## Video architecture

Hottop keeps `hottop.render.v2` as the provider-neutral creative handoff. Video production is a downstream adapter layer, not a parallel creative system.

Pipeline:

`CreativeRenderRequest → VideoProductionConfig → VideoProductionPlan → generation backend → compositor → encoder`

### 1. Generation backend

Primary open-source local backend candidate: **Wan2.2** (`Wan-Video/Wan2.2`, Apache-2.0).

Use it for shot-level source video generation or image-to-video generation. The adapter emits explicit commands / inputs but does not download models or require GPU in CI.

Supported planned modes:

- `wan22-ti2v-5b` — preferred general local path; text/image-to-video, 720P-capable;
- `wan22-i2v-a14b` — stronger image-to-video path where hardware allows;
- `external` — a provider-neutral placeholder for hosted/user-supplied generated clips.

Model download, paid APIs, and GPU execution remain operator-controlled.

### 2. Motion compositor

Primary compositor: **Motion Canvas** (`motion-canvas/motion-canvas`, MIT).

Use it for deterministic timing that generative video models are bad at preserving reliably:

- shot timing and continuity;
- captions / dialogue subtitles;
- labels and benefit beats;
- camera-like crop/pan/zoom over generated source clips when useful;
- cheap intentionally awkward motion graphics for Anti-Polish;
- sound-effect timing;
- background-music ducking and scene cues;
- title / end attribution.

Hottop should emit a Motion Canvas-ready timeline manifest rather than vendor the upstream repository.

### 3. Encoder

Use **FFmpeg** as final encoding / compatibility layer:

- MP4 H.264 + AAC + `yuv420p` + fast-start for social/chat compatibility;
- optional WebM;
- optional GIF for short loops;
- loudness / audio mix normalization when requested.

FFmpeg is an external executable. CI validates command construction only.

### 4. Remotion

Remotion remains an optional adapter candidate, not the default. Its current license allows free commercial use only for specified eligible entities and otherwise requires a company license. Hottop must not silently create a paid/commercial-license dependency. A future `remotion` backend must be explicit and operator-enabled after license review.

## Configuration contract

Add repository-owned video production profiles under `config/video/`.

A `VideoProductionConfig` contains:

- `schema_version`;
- `name`;
- `style_profile` (`anti-polish`, `cinematic`, `social-native`, etc.);
- `generation_backend`;
- `compositor_backend`;
- `encoder_backend`;
- `width`, `height`, `fps`, `duration_seconds`;
- `output_format`;
- `shot_policy`;
- `audio` settings;
- `text` settings;
- `anti_polish` settings when enabled;
- backend-specific configuration that contains paths/identifiers but never secrets.

The first committed profile is `config/video/anti-polish-short.yml` for 9:16 meme shorts.

## Video production plan

Add `hottop.video-plan.v1` as a deterministic serialized contract derived from `CreativeRenderRequest` + `VideoProductionConfig`.

The plan contains:

- original `render_request` identity and product/topic metadata;
- resolved output dimensions / fps / duration;
- production style and backend routing;
- ordered shots with start/end/duration;
- continuity instructions;
- shot-level generation prompt and negative prompt;
- dialogue lines;
- subtitles;
- Foley / SFX cues;
- BGM cues / ducking instructions;
- product-benefit beats;
- final attribution policy;
- generation commands for the selected local backend where deterministic;
- compositor manifest;
- FFmpeg finalization command template;
- license / hardware / execution notes.

## Shot construction rules

When `distribution_mode=motion` or `motion_continuity_required=true`:

1. Treat render frames as narrative beats, not independent posters.
2. Preserve character identity, location, lighting and object state across adjacent shots unless the story explicitly changes them.
3. Prefer action-continuity transitions: follow, pan, eyeline, match-action, foreground occlusion, whip-pan, object crossing frame.
4. Never auto-insert an unrelated still-image slideshow transition.
5. Product benefits appear after or during the visible consequence of the product action.
6. In meme / hotspot / brand-memory work, no URL/QR/hard CTA unless the render request explicitly allows it.

## Anti-Polish production rules

For `style_profile=anti-polish`:

- generate prompts should request intentionally cheap / rough 3D, simple geometry/materials and slightly awkward animation;
- prohibit glossy commercial AI aesthetics, blue-purple hologram defaults, luxury product lighting, polished mascot teams, feature-card UI and high-end sci-fi interfaces unless demanded by the concept;
- allow 12–24 fps aesthetic cadence while final container may still encode at a compatible frame rate;
- Foley should be blunt and funny rather than cinematic-heavy;
- BGM should use simple, cheap-sounding instrumentation and leave room for dialogue;
- deadpan dialogue beats should be protected with short pauses;
- product UI should remain visually native to the crude world rather than becoming a glossy ad insert.

## Sound contract

Video plans explicitly model audio instead of treating it as an afterthought.

Each cue has:

- `kind`: `dialogue | foley | sfx | bgm`;
- `start_seconds`;
- optional `duration_seconds`;
- `text` for dialogue or semantic description for SFX/BGM;
- `character` for dialogue;
- `duck_bgm_db` when speech needs space.

The plan may reference user-supplied/right-cleared audio files by path. It must not automatically fetch copyrighted soundtrack/music from films or social platforms.

## Rights / evidence

- Film/animation references teach role, visual grammar, pacing and comic structure; source footage and protected production assets are not default generation inputs.
- Do not clone a protected character design at pixel-level or copy exact film frames.
- A broad low-budget 3D grammar, archetypal animal role, deadpan family dynamic or rough animation language can be recreated with original staging and assets.
- Named competitor negatives still require evidence or unmistakable satire/metaphor.

## CLI

Add:

`hottop video-plan <render-v2.json> --config config/video/anti-polish-short.yml [--output plan.json]`

This command validates the render request and video config and emits `hottop.video-plan.v1` without executing GPU/video tools.

A later execution command may consume the plan, but Foundation CI must stay independent of Node, GPU models and FFmpeg binaries.

## Upstream integration policy

Pin upstream repositories/commits in `integrations/versions.yml`:

- Wan2.2 — external local generation backend, Apache-2.0;
- Motion Canvas — external compositor/runtime, MIT;
- FFmpeg — external encoder;
- Remotion — optional/licensed adapter candidate only, with explicit license note.

Do not vendor large upstream repositories.

## Success criteria

- Anti-Polish doctrine is durable in `PROJECT.md` and reusable creative skill.
- A repository YAML profile can deterministically produce a validated video production plan from `hottop.render.v2`.
- The plan explicitly includes shots, continuity, dialogue/SFX/BGM, generation routing, compositor routing and encoding settings.
- Existing static and render-v2 paths remain backward compatible.
- CI remains green with no GPU/Node/FFmpeg requirement.
