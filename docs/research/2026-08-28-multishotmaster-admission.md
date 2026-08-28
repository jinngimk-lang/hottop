# MultiShotMaster admission review

Date: 2026-08-28
Status: gated research/benchmark candidate; not an executable Hottop backend

## Why this candidate matters

Hottop Production v0.2 now treats identity fidelity and motion fidelity as separate evidence dimensions, and its highest-value generated-quality gap is still a real multi-shot, reference-conditioned benchmark over rights-safe subject-bearing shots.

MultiShotMaster is directly relevant because it is designed for controllable multi-shot narrative generation rather than isolated clips. Its public README states support for:

- text-driven inter-shot consistency;
- variable shot counts and durations;
- customized subject with motion control;
- background-driven customized scene control.

That shape is materially closer to Hottop's current continuity problem than another single-shot I2V wrapper.

## Reviewed upstream

- repository: `KlingAIResearch/MultiShotMaster`
- exact reviewed source: `1df812dda262639e4a3ca6e4a1da9000b0a8e124`
- repository code license: Apache-2.0
- upstream base family: Wan2.1 T2V 1.3B / 14B
- public model repository: `KlingTeam/MultiShotMaster`

The GitHub repository reports Apache-2.0 and the reviewed source contains training/inference code. The public model repository is available, but the reviewed model-card surface does not provide sufficiently clear license metadata to let Hottop treat checkpoint rights as automatically equivalent to the repository code license.

**Code license and checkpoint rights therefore remain separate admission gates.**

## Runtime and provisioning boundary

The upstream README requires a separately prepared Python environment and explicitly instructs users to install dependencies including FlashAttention. Checkpoints are downloaded with `huggingface-cli` or Git LFS and then wired into local model-path configuration.

Published inference shapes include:

- 1.3B single-GPU inference at 480p;
- 14B single-GPU inference at 480p/720p;
- optional multi-GPU `torchrun` execution for the 14B path.

Those properties make operator-owned local benchmarking plausible, but they do **not** qualify the project for unattended Hottop execution. Normal `video-run` must never invoke its download/install paths, provision its environment or infer GPU readiness from repository metadata.

## Important capability limitation

The upstream open-source plan marks **multi-shot generation** as released while **multi-shot + multi-reference generation** remains unreleased. Therefore the current public release cannot be treated as a complete replacement for Hottop's rights-safe reference-conditioned LightX2V/Wan2.2 route.

It is best understood as a future benchmark candidate for multi-shot narrative coherence plus subject/motion control, with an unresolved gap around the released multi-reference path.

## Hottop admission decision

Do not add an executable adapter or integration-ready model-hub route now.

Admission state:

- `research/benchmark candidate`: yes;
- executable Hottop backend: no;
- unattended zero-cost route: no;
- automatic install/download: forbidden;
- operator-owned local benchmark: allowed only after exact local provisioning and rights review.

No source code, checkpoint or training data is copied into Hottop by this admission.

## Re-admission gate

Re-evaluate only when all of the following are true:

1. exact checkpoint/model rights are independently verified for the intended use;
2. an operator has already provisioned the exact source revision, dependencies, checkpoints and GPU runtime locally;
3. rights-safe Hottop subject/reference inputs are available;
4. the relevant public capability is actually released (including multi-reference behavior if that is the claimed advantage);
5. the benchmark uses the same Hottop subject-bearing sequence and output-side evaluator contract used for existing routes;
6. identity fidelity, requested-action/motion fidelity, reference-pose diversity/anti-copy evidence, scene geography, artifact provenance and final-media integrity are persisted separately.

A successful process exit, attractive upstream demo or Apache-2.0 source license alone cannot promote the route.

## Rollback

This record is documentation-only and mechanically reversible. It introduces no dependency, model download, provider rerouting, credentials, paid action, GPU provisioning or production-quality claim.
