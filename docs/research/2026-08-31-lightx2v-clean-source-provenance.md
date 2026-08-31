# LightX2V clean-source provenance closure — 2026-08-31

## Measured gap

Hottop already required generated artifacts to bind the actual generator candidate/source revision. The LightX2V adapter recorded Git HEAD for a local Git checkout, but a checkout with staged or unstaged tracked modifications could still execute modified source while the artifact manifest claimed only the clean HEAD commit.

That is a false provenance identity: runtime success and a Git SHA are not enough when the worktree bytes differ from that commit.

## TDD evidence

- RED exact head `c7b0fbf3d3dfa8a4476097419df60bdba346b1c6`, CI #2441: Ruff passed; pytest failed only the new dirty-checkout contract (`1 failed / 606 passed`) because generation still started from a tracked-dirty checkout.
- First GREEN implementation exact head `0251c751a8a735c7b222b31a5b2a04945161d6b8` correctly rejected dirty source, but full-suite CI #2442 exposed an old provenance fixture that only fabricated `.git/HEAD` instead of creating a real repository. The production gate was not weakened.
- Corrected exact head `b6c919dbfbfa0698abe98e0e65fac6c17e8d45d8` upgraded that fixture to a real committed clean Git checkout. CI #2443 passed on Python 3.11/3.12; production-smoke #210 and 720p cinematic-delivery-smoke #77 also passed.
- Squash merge: `e4f7486d8f5006302d955879d0b5ba42a6f73832`; post-merge CI #2445 passed.

## Production contract

For a real LightX2V Git checkout, preflight now runs a local structured Git status check before generation:

`git -C <root> status --porcelain --untracked-files=no`

- any staged or unstaged **tracked** change fails closed before GPU/model work;
- a clean Git checkout continues to record actual Git HEAD as generator source revision;
- a non-Git unpacked/operator source tree keeps the existing `source-sha256:<infer.py digest>` fallback;
- untracked files are intentionally ignored by this specific source-mismatch gate because operator checkouts may contain caches/output files that do not alter tracked generator source;
- if a path presents itself as a Git checkout but Git cannot verify its status, preflight fails closed instead of claiming trustworthy source provenance.

This gate does **not** prove model/checkpoint identity, weights rights, runtime correctness, identity fidelity, requested-action motion fidelity or final-media quality. Those remain independent evidence dimensions.

## Security / cost boundary

The closure adds no network access, model download, dependency installation, GPU provisioning, credentials or paid fallback. LightX2V execution remains operator-owned and network-offline under the existing config/runtime gates.

## Freshness check

Reviewed LightX2V public `main` remains `7b8a96cc0a3a561824a5e6a8807ba7fae0984ea6` (`Update scripts (#1452)`, 2026-08-28). The change is script/example maintenance and supplies no Hottop-measured continuity, quality or runtime gain for the tested Wan2.2 I2V subset. Keep the tested pin; do not freshness-only repin.

Public Wan2.2 I2V reports also continue to show that a route can execute successfully while producing unusable output. This reinforces Hottop's existing output-side quality/provenance gates; it does not justify a route change by itself.

## Doctrine relationship

No new `PROJECT.md` doctrine is required. This work concretely enforces the existing durable rule recorded on 2026-08-25: generator source provenance must describe the **actual executed source**, and reviewed registry pins must never substitute for runtime truth.
