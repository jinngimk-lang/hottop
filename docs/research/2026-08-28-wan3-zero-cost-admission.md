# Wan3.0 zero-cost admission review

Date: 2026-08-28

## Why this was reviewed

Production v0.2 still has a measured generated-quality gap around reference-conditioned multi-shot identity + motion continuity. Wan3.0 is Alibaba Cloud's current flagship video family and advertises stronger reference-based generation, longer clips and native audio, so it is relevant enough to review immediately rather than treating Wan2.2 as the newest Wan option by default.

## Exact public source evidence

- Official GitHub repository: `AlibabaCloud-Official/Wan3.0`
- Reviewed source revision: `4ff8ec7c43049d975f724feab26bdcbafb16d888`
- The reviewed repository contains only `README.md` and an Apache-2.0 `LICENSE`; it does **not** expose local inference code or downloadable model/checkpoint assets at that revision.
- Official Alibaba Cloud Model Studio documents `wan3.0-video` as an all-in-one reference-based model supporting text-to-video, image-to-video, reference-to-video and editing, with up to 30-second output and native dialogue/BGM/SFX.
- Official API documentation requires an Alibaba Cloud Model Studio API key and region-matched endpoint/model configuration.
- Official Model Studio pricing is metered per generated second. The currently documented list prices are approximately USD $0.05/sec at 480P, $0.10/sec at 720P and $0.20/sec at 1080P for the standard model; promotional pricing can change and must never be treated as a zero-cost guarantee.

## License and rights interpretation

The Apache-2.0 file in the official GitHub repository licenses the repository work that is actually published there. It does **not** prove that Wan3.0 model weights/checkpoints are openly licensed or locally distributable, because no such weights/checkpoints are present in the reviewed repository.

Model/API terms, input-reference rights, voice/audio rights and generated-output rights remain separate gates. Hottop must not infer model-weight rights from the documentation repository license.

## ZERO_COST / runtime admission decision

**Decision: hosted paid candidate only; not admitted to unattended ZERO_COST or operator-local execution.**

Reasons:

1. the reviewed official public path requires an API key and metered billing;
2. no reviewed local inference implementation or downloadable first-party Wan3.0 weights/checkpoints are present in the official repository;
3. therefore Hottop cannot perform an operator-owned zero-paid local preflight against an auditable Wan3.0 runtime today;
4. adding the hosted API as a fallback would violate `ZERO_COST_MODE=true`, the no-paid-fallback invariant and the rule against consuming credits without explicit high-risk approval.

Hottop therefore must **not**:

- add Wan3.0 as an unattended `video-run` backend;
- create or request an API key;
- call Alibaba Cloud Model Studio automatically;
- consume promotional/free-trial credits and relabel that route as guaranteed zero-cost;
- infer local checkpoint rights from the Apache-2.0 documentation repository;
- claim Wan3.0 identity/motion quality from public demos without Hottop's own output-side benchmark evidence.

## Re-admission gate

Re-evaluate only if at least one of these materially changes:

1. Alibaba publishes a first-party local inference implementation plus auditable Wan3.0 weights/checkpoints with explicit rights compatible with the intended use; or
2. an operator explicitly provisions a separately reviewed local/runtime route whose code/model/output rights and zero-paid execution can be independently verified.

Any future benchmark must use Hottop's own rights-safe subject sequence and persist identity fidelity, motion fidelity, scene geography, audio, generator/model provenance, artifact bytes and final-media verification separately.

## Impact on current roadmap

Wan3.0 is important competitive/quality radar evidence, but it does not replace the current tested LightX2V/Wan2.2 operator route or the guaranteed software3d baseline. The immediate Production v0.2 execution target remains a real operator-provisioned, rights-safe local reference-conditioned benchmark rather than a paid hosted API integration.
