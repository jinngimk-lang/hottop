# Reference-continuity evaluator radar — 2026-08-25

## Measured gap

Production v0.2 already has rights-safe reference inputs, stable `subject_id` / identity-lock prompt semantics, generated-shot motion/media gates, and byte-bound artifact provenance. The remaining quality gap is different: **prove that generated output still depicts the intended subject and that the same subject remains recognizable across shots**.

Input-side locks are necessary but are not evidence of output-side visual continuity. Promotion of a reference-conditioned route therefore needs a provider-neutral result contract that can bind visual scores to the exact reference and exact generated shot bytes.

## Admission decision

This cycle admits the **benchmark contract**, not a new evaluator dependency. `hottop.reference-continuity-benchmark.v1` records exact candidate/revision, evaluator/revision, reference SHA-256, generated-shot SHA-256 values, reference-adherence score, cross-shot-identity score, and fail-closed thresholds. The artifact verifier recomputes the actual reference bytes, reuses `VideoArtifactManifest` byte verification for generated shots, and requires the real `hottop.video-plan.v1` so each subject's evidence is restricted to shot hashes from plan shots carrying that same `reference.subject_id`.

An evaluated subject must cover **all** byte-bound plan shots carrying that subject ID. A subset is not acceptable because it permits cherry-picking the best-looking shots while omitting identity-drift failures. This completeness rule is scoped to subjects explicitly included in the benchmark; it does not implicitly expand benchmark scope to single-shot/background subjects that are not being evaluated for cross-shot continuity.

The benchmark also binds candidate attribution to generated-artifact provenance when that provenance is available. LightX2V production artifacts are the first route required to carry this binding: the benchmark `candidate_id` / `candidate_revision` must match the exact candidate metadata on every evaluated LightX2V shot. `candidate_revision` means **actual local generator source revision**, not model-weights revision. A real git checkout records its actual HEAD; a packaged/non-git checkout falls back to a SHA-256 identity of the local `lightx2v/infer.py` entrypoint. This prevents a byte-valid run from being relabelled as another LightX2V source revision while avoiding the opposite error of pretending a reviewed registry commit is necessarily the code actually executed.

Model/weights provenance remains a separate admission dimension. Hottop must not infer a checkpoint revision from the framework source revision; a future real operator benchmark should bind independently verifiable local model metadata when the provisioned runtime exposes it.

A future evaluator adapter must write into this contract rather than becoming the contract itself.

## Targeted upstream review

### LightX2V

- Source: <https://github.com/ModelTC/LightX2V>
- Code license checked: Apache-2.0 at <https://github.com/ModelTC/LightX2V/blob/main/LICENSE>.
- Hottop status: already integrated only as an operator-owned local route with explicit checkout/model/config preflight, no auto-provisioning, shared quality gates and artifact provenance.
- Tested Hottop integration pin remains `926299962ed32a142411e45468a289623432b4e4`. A freshness check on 2026-08-25 observed upstream `main` at `5dc5d6372654406761474719647763ac7b4bd018` (`fix(swiftvr): convert BF16 images before NumPy export (#1429)`). That newer commit is not automatically promoted into Hottop: the current change is outside the tested Wan2.2 CLI contract, and popularity/freshness alone is not evidence that a re-pin improves the active production path.
- Decision: keep as the high-priority Wan2.2 inference candidate. Record the **actual local checkout revision** in every LightX2V artifact used for continuity evaluation. Do not infer model/weights permissions or revision from the framework's Apache-2.0 code license; exact checkpoint terms and provenance remain a separate gate.

### WanGP / Wan2GP

- Source: <https://github.com/deepbeepmeep/Wan2GP>
- Current project license checked: `WanGP Community License 2.0` at <https://github.com/deepbeepmeep/Wan2GP/blob/main/LICENSE.txt>.
- The license permits broad private/internal/company production use, including private headless/API use, but restricts monetized embedding, paid API/SaaS/hosted/white-label access without a separate commercial license. Third-party models/weights remain separately licensed.
- Freshness: upstream August 2026 releases continue to improve H3 sliding-window/reference continuity and LTX 2.5 visual quality. These are materially relevant for later operator benchmarks, but they do not change the community-license boundary and do not justify vendoring or automatic model/runtime provisioning.
- Decision: preserve Hottop's narrow operator-owned interoperability adapter. Do not vendor WanGP code into Hottop and do not make it an unattended/public paid backend. Its reference/continuation capabilities remain useful for operator benchmarks when the operator has a compliant local installation and separately reviewed model weights.

### DreamSim

- Source: <https://github.com/ssundaram21/dreamsim>
- Code license checked: MIT at <https://github.com/ssundaram21/dreamsim/blob/main/LICENSE>.
- Upstream usage documentation indicates pretrained model construction downloads weights on first use. The code license therefore does not by itself clear the downloaded model/backbone artifacts, and normal unattended Hottop execution must not introduce this hidden network/download step.
- Decision: do not add DreamSim as a default dependency in this cycle. It remains an evaluator candidate only after exact weights/backbone licenses, revisions, download behavior, hardware cost and benchmark value are reviewed. A future operator-owned adapter can emit the provider-neutral continuity contract if admitted.

### DINOv3

- Source: <https://github.com/facebookresearch/dinov3>.
- Freshness check: upstream remains active in August 2026 and documents dense visual features suitable for similarity-style evaluation.
- License check: code **and** released model weights are governed by the custom DINOv3 License, not Apache/MIT. Access to pretrained weights also requires accepting upstream terms and obtaining weight URLs; normal hub helpers can download weights from those URLs.
- Decision: do not add DINOv3 to the guaranteed/default evaluator environment. It is technically attractive for dense reference/shot comparison, but license acceptance plus gated/hidden download behavior make it an operator-owned candidate only. Any future adapter must require an explicit local checkout + local weights path and record exact revision/weights provenance before it may emit Hottop continuity scores.

### SigLIP 2

- Reviewed official model cards declare Apache-2.0.
- `google/siglip2-so400m-*` remains a high-capacity option, but reviewed checkpoints are multi-GB and standard `from_pretrained(...)` usage downloads from Hugging Face when not already local.
- A materially lighter official candidate is `google/siglip2-base-patch16-256`: its repository is about **1.54 GB** and the main safetensors file is about **1.5 GB** (SHA-256 `6125cacc01fa93bdc98a0c5101cefcd69b2ed1f8ab4f38d86f4ad5984f5dc863` at the reviewed revision). This is substantially easier to admit for an operator-local benchmark than the SO400M route, while keeping the same Apache-2.0 model-card posture.
- Standard Transformers usage still performs implicit network download when the model is absent, so neither Base nor SO400M may enter unattended Hottop/CI through `from_pretrained(...)` model IDs.
- Decision: promote **SigLIP 2 Base 256** to the preferred evaluator experiment candidate ahead of SO400M for the first operator-local benchmark. Any adapter must accept an explicit local model path, pin exact revision/file hash, perform no download, and demonstrate useful separation between same-subject and identity-drift controls before becoming a preferred production evaluator.

### Smaller SigLIP control

- The official Apache-2.0 `google/siglip-base-patch16-256` (SigLIP v1) remains materially smaller than SigLIP 2 Base 256: the reviewed repository is roughly **816 MB**, with an approximately **813 MB** `model.safetensors` (SHA-256 `f0cee7c815135c44a515eff72ab3040499744920442bc25567cd04efc93f8f65`).
- This lower footprint is useful as a **benchmark control/fallback candidate**, not evidence that SigLIP v1 is a better continuity evaluator. Hottop should only prefer it if an operator-local same-subject vs identity-drift benchmark shows sufficient separation for the active acceptance thresholds.
- Like SigLIP 2, it must be supplied by explicit local path; no unattended model-ID download is admitted.

### DINO-family evaluators

Older DINO/DINOv2-style embeddings remain plausible building blocks for reference/identity similarity, but the project must not infer weights rights from repository code rights. Exact selected checkpoint/model licenses must be reviewed independently before any adapter is admitted. No DINO-family dependency is added in this cycle.

## Durable implications

- Structural `subject_id` / prompt identity locks are **input constraints**, not proof of generated visual identity.
- Visual-continuity evidence must bind to exact reference and shot bytes **and to the subject-bearing shots in the production plan**, not filenames, global manifest membership or manually copied hashes.
- Generated continuity evidence must also bind to the generator candidate/source revision when the production route can prove it; a byte-valid artifact cannot be relabelled as another generator revision.
- Generator source revision and model/weights revision are separate provenance dimensions. Never claim the latter from the former.
- For every subject that is actually evaluated, continuity evidence must cover the full set of that subject's plan shots; partial cherry-picked coverage fails closed.
- Benchmark scope remains explicit: completeness within an evaluated subject does not mean every incidental/single-shot plan subject must become a continuity target.
- Evaluator identity and revision are part of provenance; thresholds are explicit and fail closed.
- Hottop remains evaluator-neutral. No model evaluator may silently download weights, use paid APIs, or weaken the guaranteed software3d / zero-cost baseline.
- Code license, model/weights license, hidden network behavior, operator hardware burden and commercial restrictions remain separate admission gates.
- A permissive evaluator checkpoint can still be unsuitable for unattended Hottop if its normal loading path implicitly downloads multi-gigabyte weights. Prefer explicit local-path-only operator adapters before considering any model-based evaluator for default use.

## Next evidence step

When an operator-controlled LightX2V/Wan2.2 or compliant WanGP reference-conditioned run is available, generate at least two byte-bound shots for the same rights-safe evaluated subject, run an admitted/reviewed evaluator or documented operator review, serialize the continuity benchmark with exact generator source revision, exact reference/shot hashes and coverage of **all** evaluated subject plan shots, and require the configured thresholds before promoting that route as identity-preserving. Record model/weights revision independently when the operator can prove it locally; do not substitute the framework source revision for weights provenance. For the first model-based evaluator experiment, prefer the reviewed SigLIP 2 Base 256 local-path route over a larger SO400M checkpoint unless benchmark evidence shows the larger model is necessary; use SigLIP v1 Base 256 only as a lower-footprint control unless it proves sufficient separation.