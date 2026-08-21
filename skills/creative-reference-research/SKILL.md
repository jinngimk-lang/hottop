---
name: creative-reference-research
description: Use when Hottop needs public visual references to learn composition grammar, reveal pacing, product-photography structure, social distribution patterns, or source-medium cues without copying protected execution.
---

# Creative Reference Research

## Purpose

Research **visual reference** material to learn why an advertising or cultural image works, then convert that observation into reusable creative grammar. This skill is an analysis layer for `brand-metaphor-creative`; it is not a tracing, recreation, or style-copying workflow.

The rule is: **learn the grammar, do not copy the execution**.

## 1. Start with a research question

Before opening pages or collecting screenshots, state the specific uncertainty being studied. Examples:

- How does a strong swipe-reveal delay the brand reveal without confusing the viewer?
- What composition grammar makes a single-object food metaphor legible in one second?
- How do live-action movie-adjacent posts create cinematic scale without reproducing a film frame?
- How much copy can a mobile social image carry before the visual metaphor stops landing?

Do not collect references merely because they look good. Every reference should answer a concrete creative question.

## 2. Acquisition order

Prefer public, reproducible sources and the smallest tool that answers the question.

1. Public HTTP(S) pages and already-available source images.
2. **Playwright CLI** for dynamic pages, visual inspection and screenshot capture in coding-agent workflows.
3. Playwright MCP only when persistent browser state, iterative DOM reasoning or long-running exploratory navigation materially improves the research.
4. Crawl4AI when structured page extraction or multi-page enrichment matters more than interactive visual inspection.
5. Firecrawl/plain HTTP as existing enrichment fallbacks.

For Playwright, use an ephemeral in-memory session by default. Do not enable persistent browser profiles, import cookies, log into accounts or cross access boundaries merely to gather references. Authenticated/private material requires an explicit authorized operator flow.

## 3. Provenance before interpretation

Every retained observation needs **provenance**. Record the source URL, source/title, observed time, source type, and what was actually visible. Distinguish direct observation from inference.

A screenshot is evidence of what was visible at capture time; it is not permission to reproduce the design. Treat ordinary third-party screenshots as **analysis-only** unless the material is public-domain or rights-cleared.

Do not commit protected source screenshots to the repository by default. Prefer a derived reference manifest and temporary artifact hashes/paths. If an image must be retained for a legitimate rights-cleared workflow, record the rights mode explicitly.

## 4. Abstract the reference

Convert each useful example into design language that can transfer to an original execution. Capture only what is needed, such as:

- **composition grammar** — dominant object, negative space, focal hierarchy, framing, symmetry/asymmetry;
- shot/camera grammar — macro product crop, close-up, wide cinematic scale, POV, split comparison;
- reveal pattern — tease → extension → reveal, before/after, misdirection, escalating crop, delayed logo;
- motion/sequence grammar — pull, unwrap, launch, transform, connect, interrupt, escape;
- text grammar — approximate density, hierarchy, position and timing of copy;
- medium grammar — live-action realism, animation-native staging, documentary/social realism, commercial product photography;
- bridge logic — shape/material, action/motion, role, function, emotion/ritual, language/symbol;
- why it works — one short causal explanation;
- **what not to copy** — distinctive character design, actor face, exact layout, logo lockup, proprietary UI, packaging trade dress, exact costume/prop/set, unique color/graphic system or source pixels.

When possible, compare multiple references that demonstrate the same principle. A transferable pattern supported by several examples is safer and more useful than treating one source as an exact target.

## 5. Reference manifest

A durable **reference manifest** should contain, when relevant:

- `source_url`
- `source_title`
- `source_type`
- `observed_at`
- `visual_medium`
- `expression_form`
- `bridge_type`
- `composition_grammar`
- `reveal_pattern`
- `text_grammar`
- `why_effective`
- `what_not_to_copy`
- `rights_mode`: `analysis-only`, `public-domain`, `rights-cleared`, or `unknown`
- `artifact_hash` or temporary artifact locator when a capture was used
- a short `provenance_note`

The manifest is the reusable asset. The protected screenshot usually is not.

## 6. Hand off to creative generation

Return a concise research handoff to `brand-metaphor-creative` containing:

1. the creative question;
2. the reusable composition/reveal/medium grammar discovered;
3. the strongest applicable bridge patterns;
4. constraints and `what_not_to_copy`;
5. provenance links;
6. one sentence explaining how the grammar can become an original idea for the promoted subject.

The next creative stage must still run category-default analysis, constraint deletion and bridge search. A reference never replaces original ideation.

## 7. Do not copy

**Do not copy** or closely reconstruct an actor likeness, exact film frame, protected character design, official poster, distinctive costume/prop/set, proprietary UI, logo system, packaging trade dress, exact advertisement layout, or another creator's finished composition.

Do not use a third-party reference as a pixel-level target. Match broad communication mechanics such as scale, reveal pacing, negative-space use or shot class, then create original subjects, staging, geometry, copy, camera placement and visual details.

## 8. Visual-memory roadmap

Start simple. Keep reference manifests in repository JSON/YAML/JSONL or another transparent local store while the corpus is small.

Only add semantic visual-memory infrastructure when the corpus and retrieval problem justify it:

- **OpenCLIP** can provide image/text embeddings for similarity and concept retrieval;
- **Qdrant / Qdrant MCP** can provide a searchable semantic-memory layer over derived manifests and embeddings.

If adopted, pin tested versions, preserve source/rights metadata beside embeddings, support local/read-only operation where practical, and evaluate retrieval quality before making the infrastructure a core dependency. Do not add a vector database merely because one is available.

## 9. Review gate

Reference research is ready only if:

- it answers a specific creative question;
- every retained observation has provenance;
- the output is an abstraction, not a reproduction recipe;
- analysis-only assets are marked as such;
- `what_not_to_copy` is explicit for distinctive source material;
- the result improves the originality or clarity of the final concept;
- the research can be discarded without losing the source-of-truth project doctrine.

When working inside Hottop, read `PROJECT.md` and `STATUS.md` first. Use this skill before `brand-metaphor-creative` when visual-reference research is needed, then hand off the abstract grammar rather than source pixels.