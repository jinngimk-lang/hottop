# Mobile Subject Readability Decision

Date: 2026-08-26
Milestone: Production v0.2

## Finding

Production-smoke #105 artifact inspection showed that **vertical placement and mobile readability are different quality dimensions**. The software3d cow flagship primary subject occupied roughly 21% of portrait frame height at midpoint, while key Odyssey characters were typically about 12–15% even after both stories passed the existing top/bottom placement contract.

The concrete RED contract required the primary Odyssey narrative character to occupy at least 14% of the 360×640 portrait canvas at shot midpoint. CI #1539 isolated the failure at shot 4: the hero measured `0.128614250658297` of frame height, with Ruff green and exactly one pytest failure.

## Correction

PR #53 changes only the Odyssey portrait camera focal multiplier from `0.98` to `1.10`; landscape remains `0.98`. It does not alter cow rendering, story geometry, provider routing, audio, provenance, or the lower subtitle-safe region.

Evidence:

- RED CI #1539: 1 failed / 458 passed, target contract only.
- GREEN CI #1540: Python 3.11 and 3.12 passed.
- GREEN production-smoke #106: both checked-in cow and Odyssey config→moving shots→audio→MoviePy→FFmpeg→verified MP4 chains passed.
- Direct inspection of the #106 Odyssey MP4 confirmed visibly larger key characters without subtitle clipping or broken scene geography.

## Durable rule

For 9:16 production evidence, **mobile-first framing must inspect both principal-subject placement and readable subject scale**. Safe-area placement alone is insufficient. Numeric scale thresholds remain style/backend/story specific and should be derived from real artifacts rather than promoted into a universal constant.

This supersedes the weaker working assumption that correcting empty upper-canvas placement by itself proves mobile framing quality.
