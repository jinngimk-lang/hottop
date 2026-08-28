# Motion fidelity and anti-copy evidence for reference-conditioned video

Date: 2026-08-28
Status: accepted production-evidence contract; evaluator implementation remains external/operator-selected

## Measured gap

Hottop already had two useful but different evidence layers:

- `video_quality.py` verifies that generated media is valid and that sampled frames contain enough pixel change / are not mostly duplicates;
- `hottop.reference-continuity-benchmark.v1` binds reference adherence and cross-shot subject identity to exact reference bytes, exact generated-shot bytes, all subject-bearing planned shots, candidate/source provenance and evaluator revision.

Those layers were still insufficient for a combined **identity + motion** claim. A reference-conditioned route could preserve a recognizable subject while the requested action is wrong, frozen or degenerate. It could also keep a nearly rigid copy of the reference pose while camera motion produces enough frame-level pixel change to pass the generic motion gate.

Therefore generic pixel motion is necessary artifact evidence, but it is not requested-action fidelity and it is not anti-copy evidence.

## Fresh research signal: MuSS

Reviewed upstream:

- repository: `zhang-haojie/MuSS`
- exact reviewed source: `19f5808a776e9b12fcf5e5efa0cacc2f5e4886d8`
- paper: arXiv `2604.23789`

MuSS separates multi-shot subject evaluation into independent dimensions including subject consistency, `Act.Str` (action strength) and `ACP-Var` (Anti-Copy-Paste Variance). Its public README states that `ACP-Var` measures pose/structural diversity between the reference image and generated frames and explicitly penalizes rigid 2D reference copying.

This is a useful acceptance pattern because it reinforces Hottop's existing doctrine that identity fidelity and motion fidelity must be proved separately.

### Admission boundary

MuSS is **not** a Hottop dependency:

- the reviewed repository currently contains data-side code but intentionally omits the benchmark implementation;
- the repository reports no finalized code license metadata;
- its README says the code and dataset license are still being finalized;
- Hottop therefore does not vendor MuSS code/data, copy metric implementations, or claim MuSS-calibrated thresholds.

Only the independently useful behavior — separate requested-action evidence and anti-copy pose-diversity evidence — is expressed in Hottop's provider-neutral benchmark contract.

## Hottop contract

Production change merged through PR #157:

- RED exact head: `f5e92654f55e4f1ad4a8d16a68cf47c66c85fd2b`, CI #1963;
- GREEN exact head: `aff90211ff3de1027a248a4c7ac691c6921897eb`, CI #1964;
- exact-head production-smoke #202: success;
- exact-head 720p cinematic-delivery-smoke #69: success;
- squash merge: `451ab42817229a5d0dbde58e9daaeaaa8130b849`;
- post-merge CI #1965: success.

`ReferenceContinuityPolicy` now provides an explicit opt-in `require_motion_fidelity` mode. When a benchmark claims combined identity + motion success, every evaluated subject must carry evaluator-supplied normalized values for:

- `motion_fidelity` — whether the requested subject action/performance is actually present;
- `reference_pose_diversity` — whether generated subject states materially depart from simply reproducing the reference pose/structure.

The policy fails closed when either value is missing or below the configured policy threshold. Historical identity-only evidence remains backward compatible because motion evidence is opt-in rather than silently imposed on old archives.

The current default thresholds (`0.65` motion fidelity, `0.20` reference-pose diversity) are **Hottop policy defaults**, not MuSS-derived calibrated thresholds. Future real operator benchmarks may revise them only with representative rights-safe evidence and documented evaluator semantics.

## Evidence rules for future operator benchmarks

A route that claims reference-conditioned identity **and** motion quality must bind all of the following:

1. exact rights-safe reference bytes and their role/subject identity;
2. every subject-bearing generated shot byte required by the plan;
3. exact candidate/source/model provenance when independently verifiable;
4. evaluator identity and evaluator revision;
5. reference adherence and cross-shot identity;
6. requested-action / performance fidelity;
7. reference-pose diversity or equivalent anti-copy evidence;
8. generic media/motion quality, scene geography and final-media integrity through the existing gates.

No one dimension substitutes for another. High identity with wrong/frozen motion fails. Strong motion with subject drift fails. Camera motion around a rigid reference-like sticker does not establish subject-action fidelity.

## Rollback / compatibility

The new fields are optional and the combined-motion gate is opt-in. Removing this contract would weaken evidence claims but is mechanically reversible without changing generation providers or media production. No model download, evaluator dependency, GPU provisioning, credentials, paid service or provider rerouting was introduced.
