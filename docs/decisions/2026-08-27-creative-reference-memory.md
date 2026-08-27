# Decision: Hottop creative memory is retrieval/preference memory, not template reuse or RL

Date: 2026-08-27
Status: durable

## Decision

Hottop will preserve successful and failed creative work as a structured reference library and retrieve it when useful for future image/video ideation.

The system stores mechanism, native visual/dialogue/audio grammar, product-role logic, user feedback, promotion lessons, failure patterns and later platform-performance signals. It does **not** treat past images as default templates, and it does **not** replace mandatory fresh/supplied-hotspot analysis.

Current learning classification is **retrieval + few-shot/preference memory**, not reinforcement learning. Training work (SFT/DPO/reward model/RL) is deferred until enough clean, rights-safe, labeled data and measurable value exist.

## Canonical artifacts

- `integrations/creative-reference-library.yml`
- `src/hottop/creative_memory.py`
- `src/hottop/creative_memory_cli.py`
- `skills/creative-reference-memory/SKILL.md`
- `docs/creative/creative-reference-memory.md`

## Seeded durable lessons

- Odyssey-style positive: reuse causal transformation/rescue grammar and cinematic medium; product changes the story outcome.
- Niulai-style positive: preserve native low-budget 3D + family/deadpan dialogue when that roughness is the joke.
- Negative: pan/zoom over stills is not cinematic video.
- Negative: internal labels such as `热点梗图` must not appear in audience-facing assets.
- Promotion guardrail: InkClawAgent/product must remain visually legible and clearly responsible for the outcome.
- Distribution pattern: when useful, deliver one hotspot-native meme plus one product explainer, recommended order, platform title/body copy and hashtag set.

## Asset policy

Current conversation images are bound in the library by SHA-256 metadata. Their binary PNG bytes are not committed to ordinary Git. Future approved ingestion may use Git LFS or object storage for generated/original/user-authorized assets. Third-party copyrighted references remain metadata/analysis only by default.

## Recovery rule

For creative work where historical Hottop examples may help, recover `PROJECT.md` and `STATUS.md`, analyze/discover the current hotspot, then consult `skills/creative-reference-memory/SKILL.md` and `integrations/creative-reference-library.yml` before ideation. Current hotspot evidence remains authoritative.
