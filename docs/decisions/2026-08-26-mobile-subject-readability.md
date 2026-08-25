# Mobile Subject Readability Decision

Date: 2026-08-26
Milestone: Production v0.2

## Finding

Production-smoke #105 artifact inspection showed that **vertical placement and mobile readability are different quality dimensions**. The software3d cow flagship primary subject occupied roughly 21% of portrait frame height at midpoint, while key Odyssey characters were typically about 12–15% even after both stories passed the existing top/bottom placement contract.

The concrete RED contract required the primary Odyssey narrative character to occupy at least 14% of the 360×640 portrait canvas at shot midpoint. CI #1539 isolated the failure at shot 4: the hero measured `0.128614250658297` of frame height, with Ruff green and exactly one pytest failure.

A later direct artifact inspection found a third mobile-readability dimension: **subtitle block occupancy**. In the guaranteed software3d Odyssey MP4, long captions at about 3 s and 7 s occupied roughly 22.8% and 21.4% of frame height. They remained inside the bottom safe area, but rose far enough into the portrait canvas to compete with the principal subject. This proved that bottom-edge containment alone does not establish readable mobile subtitle layout.

## Correction

PR #53 changes only the Odyssey portrait camera focal multiplier from `0.98` to `1.10`; landscape remains `0.98`. It does not alter cow rendering, story geometry, provider routing, audio, provenance, or the lower subtitle-safe region.

PR #59 adds adaptive MoviePy caption fitting. Captions begin at the existing readable default size; only a rendered block exceeding 18% of portrait frame height is reduced, with a readable font-size floor. Text is never truncated, local CJK-font fail-closed behavior remains unchanged, and final placement still uses the rendered caption height plus the existing bottom safe margin.

Evidence:

- RED CI #1539: 1 failed / 458 passed, target subject-scale contract only.
- GREEN CI #1540: Python 3.11 and 3.12 passed.
- GREEN production-smoke #106: both checked-in cow and Odyssey config→moving shots→audio→MoviePy→FFmpeg→verified MP4 chains passed.
- Direct inspection of the #106 Odyssey MP4 confirmed visibly larger key characters without subtitle clipping or broken scene geography.
- Valid caption-layout RED CI #1560: Ruff passed and pytest failed because the adaptive caption fitter did not exist.
- GREEN CI #1561 and production-smoke #115 passed on PR #59 exact head; post-merge CI #1562 and production-smoke #116 passed again on `main`.
- Using the same bottom-half white-text pixel-band measurement before/after PR #59, the Odyssey ~3 s caption fell from about 22.8% to 10.2% of frame height and the ~7 s caption from about 21.4% to 15.8%. Full copy remained present.

## Durable rule

For 9:16 production evidence, **mobile-first readability must inspect principal-subject placement, readable subject scale, and subtitle-block occupancy**. Safe-area placement alone is insufficient. Numeric thresholds remain style/backend/story specific and should be derived from real artifacts rather than promoted into universal constants.

Subtitle fitting should preserve semantic content first: adapt layout/size within a readable floor before considering copy truncation. A caption that is technically inside the frame but visually displaces the subject is still a production-quality failure.

This supersedes the weaker working assumptions that correcting empty upper-canvas placement by itself proves mobile framing quality, or that bottom-safe-area containment by itself proves subtitle readability.
