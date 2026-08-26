# Reviewed Video Candidate Registry

`integrations/video-candidates.yml` remains the historical machine-readable companion to the autonomous **video** ecosystem radar. It records upstreams that were reviewed far enough to affect Hottop video decisions.

For new one-stop routing across **image + video + character animation + restoration/interpolation + audio**, the canonical control plane is now `integrations/model-hub.yml`, with the dual-DGX operator architecture documented in `docs/operations/dgx-spark-local-model-fabric.md`.

The registries are not installers and are not permission to execute a model. Candidate entries separate repository/code licensing from model/checkpoint licensing, record integration status, and keep runtime boundaries operator-controlled.

Legacy video statuses remain intentionally conservative:

- `high_priority_benchmark` — source and license information are sufficiently clear to justify a controlled benchmark when an operator-owned runtime is available.
- `operator_backend` — Hottop may interoperate with an already installed operator-managed runtime but should not vendor or automatically provision it.
- `blocked_by_weights_license_review` — repository code may be open, but model/output terms prevent default execution until the exact current weights license clears the project gate.

The autonomous loop should refresh exact commits and license notes when a material upstream change lands. A candidate may be promoted into a production adapter only after a measurable benchmark against the current Hottop baseline and the normal zero-cost/security/rights gates. New capability families should normally enter the unified model hub rather than spawning another isolated registry.
