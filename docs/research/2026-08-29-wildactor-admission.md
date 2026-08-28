# WildActor admission — 2026-08-29

## Decision

**Status: research-only / gated benchmark candidate. Do not integrate executable code or assets into normal `video-run`.**

WildActor is materially relevant to Hottop's current reference-conditioned identity gap because its public release targets unconstrained identity-preserving human video generation and includes a Wan2.2-5B-compatible multi-reference inference path. The mechanism is worth retaining for future same-sequence identity + requested-action motion benchmarking, but the reviewed release does not clear Hottop's source/weights/data rights gate.

## Reviewed provenance

- Repository: `WildActor/WildActor`
- Exact reviewed source revision: `c858c2100ed14b32c36883e0570948f4c09e0d28`
- Revision date/message: 2026-06-29, `Release Actor-18M pipeline and Wan2.2 inference`
- Repository license metadata at review: **none**
- Root tree at the reviewed revision contains no `LICENSE` file.

The absence of an explicit source license means Hottop must not copy or vendor WildActor implementation code. Public availability is not permission to reuse code commercially.

## Capability fit

The upstream release describes:

- identity-preserving human video generation under unconstrained viewpoints, composition and motion;
- face/body/canonical multi-view identity references;
- a Wan2.2-5B / DiffSynth-compatible inference path;
- an Actor-18M construction pipeline and schema.

This makes WildActor a useful architecture/benchmark signal for Hottop's existing rule that identity fidelity and requested-action motion fidelity are independent output evidence dimensions. It does **not** prove that Hottop can reproduce upstream quality or that the route is production-ready.

## Rights, cost and provisioning boundary

The reviewed Actor-18M release says the full dataset is still under filtering/safety review and releases the construction pipeline/schema first. Its construction workflow expects licensed input data and may rely on separately supplied assets. The repository also exposes optional model-download helpers and an optional Gemini image API stage.

Therefore Hottop must keep these boundaries separate:

1. **Source code:** no explicit license observed at the exact reviewed revision; no copying/vendor integration.
2. **Model/checkpoint weights:** independently verify exact model/checkpoint license and bytes before any benchmark.
3. **Dataset/reference media:** only Hottop-generated-original or user-provided-rights-cleared reference bytes are admissible for Hottop benchmarks; Actor-18M data is not implicitly admitted.
4. **Hosted APIs:** Gemini or any other paid/keyed augmentation path is outside unattended `ZERO_COST_MODE=true`.
5. **Downloads/runtime:** normal `video-run` and CI must not invoke upstream model download helpers, install its environment, or provision GPU/model assets.

## Re-admission gate

Revisit only when all of the following are true:

- an explicit compatible source license is published for the exact implementation to be used, or Hottop independently reimplements only the architecture/behavior without copying restricted code;
- exact Wan2.2/base and WildActor checkpoint provenance + licenses are independently verified;
- an operator has already provisioned the runtime and model assets locally without Hottop auto-downloading them;
- rights-safe multi-reference subject bytes exist locally;
- the candidate can be run offline/fail-closed through a narrow adapter;
- generated artifacts bind actual generator source/model provenance and exact output bytes;
- the same subject-bearing sequence is evaluated against the current LightX2V/Wan2.2 route for identity fidelity **and** requested-action motion fidelity, plus scene geography, anti-copy, final-media and provenance gates.

Until then WildActor remains research-only. Upstream demos, architecture claims, repository popularity, or successful dependency installation are not production-quality evidence.
