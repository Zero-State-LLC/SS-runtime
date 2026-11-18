# Live world projection review, November17 2026

Status: **DEBUG TECHNICAL VALIDATION COMPLETE. BENCHMARK NOT MET. NOT ACCEPTED ART.** Owner approved the broader presentation-projection correction at03:40:46.895UTC. See `../../../intent/2026-11-17-live-world-projection.md` and `COORDINATOR-REVIEW.md`.

## Why this exists

The previous actual playable kiosk review put an already-projected kiosk source into the ordinary world while leaving its authoritative rectangular foundation unprojected. The earlier native geometry comparison was a controlled transformed still, not continuous playable projection. This packet addresses the coordinate-system mismatch without redesigning neighbors or changing gameplay authority.

## Boundaries and verification

The implementation is explicitly opt-in and Debug-only. Current/candidate kiosk sources and all previous evidence remain frozen. The new route must consistently transform ground and registered upright roots, preserve upright local shapes, retain visible foundation/fields, keep HUD in screen space, map manual input back to world direction, and restore authoring coordinates before frame processing. The world-space pilot must not be inverse-mapped twice.

`verify_scope.py` compares tracked Git bytes/modes against base2baaeb1. It protects all Sources, Tests, RuntimeAssets, existing AppTests and historical review packets, with only the new packet and live production board excluded. It allows new AppTests but rejects editing an existing test or adding authority/art files. It does not inspect or delete unrelated untracked work. Six isolated-Git guard tests pass, including staged changes concealed by restored worktree bytes, and the actual repository check protects11876tracked files. This is preservation evidence, not visual acceptance.

Apple's SKScene lifecycle documentation distinguishes `didEvaluateActions` (after actions but before physics/constraints) from `didFinishUpdate` (after frame processing, before rendering). Neither callback runs for a paused scene. Final projection therefore needs a deliberate render-stage lifecycle and explicit paused redraw/toggle handling, not an assumption that a post-action still proves live behavior. Sources: Apple Developer Documentation, SKScene `didEvaluateActions()` and `didFinishUpdate()`.

## Evidence index

- `scope-baseline.json`, `scope-tests.log`: initial preservation and guard tests.
- `TRAIL-CHECK.md`, `trail-scope-check.log`: retained scope-check conflict and reasoned disposition.
- `WORKER-VALIDATION.md`, `tests-0350-summary.json`, frozen executed source and raw result bundle: retained17/18failure, not a pass.
- `PROBE-DEFECT.md`, issue261 and `probe-only-correction-0407.diff`: authorized child-owned test instrumentation only, strict assertions unchanged.
- `tests-0407-summary.json`, raw result bundle/log and `source-build-hashes-0408.txt`:18/18native pass,0skips, independently matched8hashes. Focused host10tests pass separately.
- `COORDINATOR-REVIEW.md` and3raw current/candidate/default screenshots: real-app inspection with explicit remaining contact/scale/depth deficiencies.
- `release-coordinator-0411.json`: independently verified final Release exclusion across1032PNG files; additional new projection marker checks passed.

No production asset admission, merge, release, deployment, paid generation, physical-device performance or owner art acceptance is authorized by this engineering approval.
