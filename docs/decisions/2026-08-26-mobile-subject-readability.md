# Mobile Subject Readability Decision

Date: 2026-08-26
Milestone: Production v0.2

## Finding

Production-smoke #105 artifact inspection showed that **vertical placement and mobile readability are different quality dimensions**. The software3d cow flagship primary subject occupied roughly 21% of portrait frame height at midpoint, while key Odyssey characters were typically about 12–15% even after both stories passed the existing top/bottom placement contract.

The concrete RED contract required the primary Odyssey narrative character to occupy at least 14% of the 360×640 portrait canvas at shot midpoint. CI #1539 isolated the failure at shot 4: the hero measured `0.128614250658297` of frame height, with Ruff green and exactly one pytest failure.

A later direct artifact inspection found a third mobile-readability dimension: **subtitle block occupancy**. In the guaranteed software3d Odyssey MP4, long captions at about 3 s and 7 s occupied roughly 22.8% and 21.4% of frame height. They remained inside the bottom safe area, but rose far enough into the portrait canvas to compete with the principal subject. This proved that bottom-edge containment alone does not establish readable mobile subtitle layout.

Production-smoke #127 then exposed a fourth dimension: **line-break quality in short mixed-script captions**. The cow caption `用 InkClawAgent。` was technically inside the safe region and below the block-height limit, yet MoviePy wrapped it as a one-character first line (`用`) plus a second Latin-heavy line. The first implementation tried a natural-width single-line label before wrapping; CI passed, but direct inspection of production-smoke #130 proved the artifact still orphaned `用` because the default-size single line was only slightly wider than the 88% mobile text budget. That evidence showed that line-break quality must be checked in the real MP4 and cannot be inferred from safe-area or height gates alone.

## Correction

PR #53 changes only the Odyssey portrait camera focal multiplier from `0.98` to `1.10`; landscape remains `0.98`. It does not alter cow rendering, story geometry, provider routing, audio, provenance, or the lower subtitle-safe region.

PR #59 adds adaptive MoviePy caption fitting. Captions begin at the existing readable default size; only a rendered block exceeding 18% of portrait frame height is reduced, with a readable font-size floor. Text is never truncated, local CJK-font fail-closed behavior remains unchanged, and final placement still uses the rendered caption height plus the existing bottom safe margin.

PR #62 extends the same fitting policy for short mixed CJK/Latin captions. MoviePy first measures a natural-width single-line label. If it is slightly too wide, Hottop reduces the label font size within the existing readable floor and retries single-line layout before allowing wrapped-caption fallback. Long copy still uses the existing block-height-constrained wrapped path; CJK font fail-closed behavior, bottom safe area, copy semantics, and provider/audio/provenance boundaries remain unchanged.

Evidence:

- RED CI #1539: 1 failed / 458 passed, target subject-scale contract only.
- GREEN CI #1540: Python 3.11 and 3.12 passed.
- GREEN production-smoke #106: both checked-in cow and Odyssey config→moving shots→audio→MoviePy→FFmpeg→verified MP4 chains passed.
- Direct inspection of the #106 Odyssey MP4 confirmed visibly larger key characters without subtitle clipping or broken scene geography.
- Valid caption-layout RED CI #1560: Ruff passed and pytest failed because the adaptive caption fitter did not exist.
- GREEN CI #1561 and production-smoke #115 passed on PR #59 exact head; post-merge CI #1562 and production-smoke #116 passed again on `main`.
- Using the same bottom-half white-text pixel-band measurement before/after PR #59, the Odyssey ~3 s caption fell from about 22.8% to 10.2% of frame height and the ~7 s caption from about 21.4% to 15.8%. Full copy remained present.
- Direct production-smoke #127 inspection found the one-character `用` orphan in `用 InkClawAgent。`.
- PR #62 first RED CI #1578 isolated the missing natural-width single-line path at 1 failed / 470 passed. The first GREEN CI #1580 passed, but direct production-smoke #130 inspection still showed the orphan; that artifact invalidated the first implementation as sufficient evidence.
- The second RED CI #1581 isolated the missing "shrink single line before wrap" behavior at 1 failed / 471 passed.
- GREEN CI #1582 passed on Python 3.11 and 3.12, and production-smoke #132 passed the full cow + Odyssey production chain.
- Direct inspection of the #132 cow MP4 at the same ~5 s point confirmed `用 InkClawAgent。` remains on one line within the bottom safe area.

## Durable rule

For 9:16 production evidence, **mobile-first readability must inspect principal-subject placement, readable subject scale, subtitle-block occupancy, and line-break quality**. Safe-area placement alone is insufficient. Numeric thresholds remain style/backend/story specific and should be derived from real artifacts rather than promoted into universal constants.

Subtitle fitting should preserve semantic content first: adapt layout/size within a readable floor before considering copy truncation. A caption that is technically inside the frame but visually displaces the subject is still a production-quality failure. For short mixed CJK/Latin captions, prefer a natural-width single-line layout when it fits; if it is only slightly too wide, shrink within the readable floor before wrapping. Avoid one-character orphan lines created solely by the compositor's generic wrapping behavior.

This supersedes the weaker working assumptions that correcting empty upper-canvas placement by itself proves mobile framing quality, that bottom-safe-area containment by itself proves subtitle readability, or that a caption passing block-height limits necessarily has acceptable line breaks.
