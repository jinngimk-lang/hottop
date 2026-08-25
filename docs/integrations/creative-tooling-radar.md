# Creative Tooling Integration Radar

This document records **current integration decisions**, not a shopping list. Hottop should adopt external tools only when they improve a measured part of the creative pipeline without weakening provenance, safety, portability or context efficiency.

Status meanings:

- **ADOPT** — useful now; keep behind a small adapter.
- **PILOT** — next bounded experiment once the prerequisite exists.
- **DEFER** — useful idea, but current corpus/workflow does not justify the dependency yet.
- **HOLD** — intentionally not integrating now because a smaller tool solves the current problem.

## Decision table

| Tool / project | Status | Hottop role | Why | Integration boundary / risk |
| --- | --- | --- | --- | --- |
| Microsoft `playwright-cli` | **ADOPT** | Public visual-reference inspection and screenshot capture | Token-efficient coding-agent browser interface; supports named sessions and screenshots | Use ephemeral in-memory sessions by default; public HTTP(S) only; no imported cookies/persistent profile by default; Apache-2.0 |
| Microsoft `playwright-mcp` | **DEFER** | Stateful exploratory visual/DOM research | Valuable when persistent browser state and iterative DOM reasoning outweigh context cost | Do not make it the default while CLI solves capture with lower schema/context overhead |
| Crawl4AI | **ADOPT** | Dynamic-page enrichment, Markdown extraction, screenshots, multi-page crawl | Already fits enrichment path | Optional isolated service; respect site boundaries; no credentials in repo |
| Agent-Reach | **ADOPT** | Multi-platform hotspot acquisition | Existing acquisition layer | Pin tested upstream; authenticated channels remain operator opt-in |
| Firecrawl | **ADOPT / FALLBACK** | Hosted enrichment fallback | Useful after self-hosted/browser path | API key optional; never a core requirement |
| plain HTTP | **ADOPT / FALLBACK** | Public static-page retrieval | Zero-extra-service fallback | No JavaScript; preserve provenance |
| DIYgod/RSSHub | **PILOT** | Expand source coverage through RSS routes | Hottop already understands RSS, so RSSHub can remain outside the codebase and feed configured endpoints | AGPL-3.0 upstream: do not vendor/copy implementation into Hottop; operator supplies endpoint; source routes still need quality/freshness metadata |
| OpenCLIP | **DEFER** | Multimodal image/text embeddings for visual-reference retrieval | Strong fit once the reference manifest corpus becomes large | Use inference only and pin a stable release; current `main` training stack is moving quickly; embedding does not erase source rights/provenance |
| Qdrant / `mcp-server-qdrant` | **DEFER** | Semantic memory for reference manifests/embeddings | Official MCP supports store/find and local path / read-only operation | Add only after a retrieval benchmark proves local manifests are insufficient; provenance/rights metadata must travel with vectors; Apache-2.0 |
| ComfyUI | **PILOT AFTER render.v2** | Optional local/offline image/video render backend | Modular workflows, API integration, reusable workflow JSON and broad image/edit/video support | GPL-3.0 upstream; isolate as external service/adapter; pin tested stable release/workflow; track model licenses separately; disable paid API nodes by default; GPU cannot become core requirement |
| Browser Use | **HOLD** | Fully agentic interactive web research | Powerful, but larger execution/provider surface than needed for current public-reference task | Revisit only for workflows Playwright CLI + Crawl4AI cannot solve; do not add autonomous login/stealth complexity by default |
| Canva / Figma connectors | **DEFER TO OUTPUT PHASE** | Editable social/carousel/template handoff | Useful after a creative has already passed the Hottop strategy/review gate | These are authoring/export destinations, not sources of creative truth; keep provider-neutral render contract first |

## Current adopted architecture

### Visual-reference acquisition

1. Start from a specific research question.
2. Fetch public source evidence.
3. Use `PlaywrightCliAdapter` when dynamic visual inspection or a screenshot is needed.
4. Abstract the result into a provenance-first `VisualReference` manifest.
5. Treat ordinary captures as `analysis-only` and avoid committing protected screenshots.
6. Feed composition/reveal/medium grammar into `brand-metaphor-creative`, not source pixels.

The browser is an observation tool, not a design copier.

### Semantic visual memory gate

Do **not** deploy OpenCLIP + Qdrant simply because the components exist. Promote them only after all of the following are true:

- a non-trivial rights-aware reference-manifest corpus exists;
- keyword/tag filtering is demonstrably insufficient;
- a fixed retrieval test set exists;
- embedding + vector retrieval improves top-k useful-reference recall/precision over the local baseline;
- latency/storage/maintenance cost is acceptable;
- every result can still surface source URL, observation date, rights mode and `what_not_to_copy`.

First pilot should be local and read-only where practical.

### Render-backend gate

`hottop.render.v2` is the stable boundary Hottop should improve before adding heavyweight render providers. A ComfyUI pilot becomes justified when:

- flexible concepts (single, carousel, split, faux still, product-as-prop) serialize cleanly through render v2;
- at least one deterministic provider-neutral fixture exists for each expression form;
- workflow/model provenance can be archived;
- paid API nodes are disabled by default;
- one local workflow can consume Hottop's prompt/frames/medium metadata without rewriting creative strategy inside ComfyUI.

Hottop owns the **creative decision**; the renderer owns execution.

## Integration principles

1. **Small adapter over vendoring.** Prefer commands/HTTP/MCP interfaces around upstream projects.
2. **No tool becomes doctrine.** `PROJECT.md` and reusable skills remain canonical; an integration cannot silently change the creative method.
3. **Provenance survives every layer.** Search, screenshot, embedding, vector retrieval and render artifacts must retain traceability.
4. **Rights metadata is not optional.** Embeddings and screenshots do not make protected material reusable.
5. **Offline/local is preferred where it materially reduces cost/risk**, but not if it creates large unmeasured operational burden.
6. **No paid fallback by surprise.** Hosted/render nodes that can incur cost must be explicit operator choices.
7. **Benchmark before promotion.** New infrastructure graduates from DEFER/PILOT only with a falsifiable test and measured gain.

## Next bounded pilots

1. Finish `VisualReference` manifest + local JSONL archive contract.
2. Add `hottop reference-plan <url>` to emit a safe public-reference acquisition plan before executing a browser.
3. Add RSSHub as an external source preset that consumes operator-provided base URL rather than vendoring upstream.
4. Build a small consumer-brand / swipe-reveal reference corpus and evaluate whether local manifest search is sufficient.
5. After render v2 is exercised by real concepts, prototype a ComfyUI adapter with one pinned offline workflow.
6. Revisit OpenCLIP + Qdrant only after the corpus/retrieval gate is reached.
