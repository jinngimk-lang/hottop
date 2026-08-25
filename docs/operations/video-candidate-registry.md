# Reviewed Video Candidate Registry

`integrations/video-candidates.yml` is the machine-readable companion to the autonomous ecosystem radar. It records only upstreams that have been reviewed far enough to affect Hottop decisions.

The registry is not an installer and is not permission to execute a model. A candidate entry separates repository/code licensing from model/checkpoint licensing, records the current integration status, and states the runtime boundary that must remain operator-controlled.

Statuses are intentionally conservative:

- `high_priority_benchmark` — source and license information are sufficiently clear to justify a controlled benchmark when an operator-owned runtime is available.
- `operator_backend` — Hottop may interoperate with an already installed operator-managed runtime but should not vendor or automatically provision it.
- `blocked_by_weights_license_review` — repository code may be open, but model/output terms prevent default execution until the exact current weights license clears the project gate.

The autonomous loop should refresh exact commits and license notes when a material upstream change lands. A candidate may be promoted into a production adapter only after a measurable benchmark against the current Hottop baseline and the normal zero-cost/security/rights gates.