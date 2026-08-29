# Stand-In V2 radar — 2026-08-30

## Why this matters

Hottop's current measured generated-video gap remains reference-conditioned subject identity plus requested-action motion across multiple subject-bearing shots. Stand-In is already a reviewed identity-control candidate, and its upstream now advertises a forthcoming V2, so this is a targeted freshness check rather than a new provider admission.

## Exact reviewed upstream evidence

- Repository: `WeChatCV/Stand-In`
- Reviewed `main`: `e351224366be169076e94af1454115d91d458313`
- Commit date: 2026-08-10
- Commit message: `Add news about Stand-In-V2 release`
- Exact diff: one README news line, `Stand-In-V2 is coming soon!`
- Repository source license: Apache-2.0.
- The same README says a Wan2.2-compatible Stand-In version is already available and describes Stand-In as lightweight identity control that can combine with pose/control tasks.

## Admission decision

**No production or benchmark-route promotion yet.** The reviewed V2 evidence is an announcement only. It does not provide a V2 source revision, checkpoint revision, independent weight/license surface, hardware/runtime contract, or Hottop output evidence. A README announcement cannot substitute for those artifacts.

Do not:

- freshness-only repin Hottop to the announcement commit;
- download V2 or other Stand-In weights automatically;
- add a V2 executable adapter before exact source/checkpoint/runtime evidence exists;
- treat identity-control claims as requested-action motion proof;
- treat upstream demos as Hottop continuity evidence.

## Re-admission trigger

Re-open this candidate when Stand-In V2 publishes reviewable source and/or checkpoints. At that point independently verify:

1. exact source revision and code license;
2. exact checkpoint/model revision and weight license/terms separately from source code;
3. Wan2.2/base-model compatibility and runtime/hardware requirements;
4. hidden download/network/install behavior and operator-owned zero-paid viability;
5. rights-safe reference inputs and rollback path;
6. same-sequence Hottop evidence covering **identity fidelity** and **requested-action motion fidelity** independently, plus geography, anti-copy, artifact provenance and final-media gates.

Until then the tested LightX2V/Wan2.2 operator route and guaranteed software3d baseline remain unchanged.
