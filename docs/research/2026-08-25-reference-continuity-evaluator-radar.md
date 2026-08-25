# Reference-continuity evaluator radar — 2026-08-25

## Measured gap

Production v0.2 already has rights-safe reference inputs, stable `subject_id` / identity-lock prompt semantics, generated-shot motion/media gates, and byte-bound artifact provenance. The remaining quality gap is different: **prove that generated output still depicts the intended subject and that the same subject remains recognizable across shots**.

Input-side locks are necessary but are not evidence of output-side visual continuity. Promotion of a reference-conditioned route therefore needs a provider-neutral result contract that can bind visual scores to the exact reference and exact generated shot bytes.

## Admission decision

This cycle admits the **benchmark contract**, not a new evaluator dependency. `hottop.reference-continuity-benchmark.v1` records exact candidate/revision, evaluator/revision, reference SHA-256, generated-shot SHA-256 values, reference-adherence score, cross-shot-identity score, and fail-closed thresholds. The artifact verifier additionally recomputes the actual reference bytes and reuses `VideoArtifactManifest` byte verification for generated shots before scores can be trusted.

A future evaluator adapter must write into this contract rather than becoming the contract itself.

## Targeted upstream review

### LightX2V

- Source: <https://github.com/ModelTC/LightX2V>
- Code license checked: Apache-2.0 at <https://github.com/ModelTC/LightX2V/blob/main/LICENSE>.
- Hottop status: already integrated only as an operator-owned local route with explicit checkout/model/config preflight, no auto-provisioning, shared quality gates and artifact provenance.
- Decision: keep as the high-priority Wan2.2 inference candidate. Do not infer model/weights permissions from the framework's Apache-2.0 code license; exact checkpoint terms remain a separate gate.

### WanGP / Wan2GP

- Source: <https://github.com/deepbeepmeep/Wan2GP>
- Current project license checked: `WanGP Community License 2.0` at <https://github.com/deepbeepmeep/Wan2GP/blob/main/LICENSE.txt>.
- The license permits broad private/internal/company production use, including private headless/API use, but restricts monetized embedding, paid API/SaaS/hosted/white-label access without a separate commercial license. Third-party models/weights remain separately licensed.
- Decision: preserve Hottop's narrow operator-owned interoperability adapter. Do not vendor WanGP code into Hottop and do not make it an unattended/public paid backend. Its reference/continuation capabilities remain useful for operator benchmarks when the operator has a compliant local installation and separately reviewed model weights.

### DreamSim

- Source: <https://github.com/ssundaram21/dreamsim>
- Code license checked: MIT at <https://github.com/ssundaram21/dreamsim/blob/main/LICENSE>.
- Upstream usage documentation indicates pretrained model construction downloads weights on first use. The code license therefore does not by itself clear the downloaded model/backbone artifacts, and normal unattended Hottop execution must not introduce this hidden network/download step.
- Decision: do not add DreamSim as a default dependency in this cycle. It remains an evaluator candidate only after exact weights/backbone licenses, revisions, download behavior, hardware cost and benchmark value are reviewed. A future operator-owned adapter can emit the provider-neutral continuity contract if admitted.

### DINO-family embedding evaluators

DINO/DINOv2-style embeddings remain plausible building blocks for reference/identity similarity, but the project must not infer weights rights from repository code rights. Exact selected checkpoint/model licenses must be reviewed independently before any adapter is admitted. No DINO dependency is added in this cycle.

## Durable implications

- Structural `subject_id` / prompt identity locks are **input constraints**, not proof of generated visual identity.
- Visual-continuity evidence must bind to exact reference and shot bytes, not filenames or manually copied hashes.
- Evaluator identity and revision are part of provenance; thresholds are explicit and fail closed.
- Hottop remains evaluator-neutral. No model evaluator may silently download weights, use paid APIs, or weaken the guaranteed software3d / zero-cost baseline.
- Code license, model/weights license, hidden network behavior, operator hardware burden and commercial restrictions remain separate admission gates.

## Next evidence step

When an operator-controlled LightX2V/Wan2.2 or WanGP reference-conditioned run is available, generate at least two byte-bound shots for the same rights-safe subject, run an admitted/reviewed evaluator or documented operator review, serialize the continuity benchmark with exact revisions and hashes, and require the configured thresholds before promoting that route as identity-preserving.
