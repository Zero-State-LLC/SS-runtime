# Defect-first record: live callback test probe ownership

Recorded by coordinator 2026-11-17 03:59 UTC, before authorizing a retry.

## Frozen failure

`tests-0350-summary.json` records 18 tests, 17 passed, 1 failed, zero skipped. `testActualSKViewCallbacksRestoreBeforeActionsAndProjectAfterward` failed `XCTAssertGreaterThan(0, 10)` for its action probe. Preserve `tests-0350.xcresult`, raw log and `LiveWorldProjectionTests.executed-0350.swift` unchanged. This run is not a passing live-action-restoration result.

## Diagnosis and independent review

The frozen test attaches `projection-action-probe` to the Player sprite root before initiating movement. Existing `WorldRenderer.playClip` (`App/WorldRenderer.swift:317-378`) calls `sprite.removeAllActions()` on clip-token transition, intentionally replacing root playback. Coordinator inspected both the test and this implementation. The probe shares an action owner with playback and is therefore invalid instrumentation across that transition. No runtime animation defect is established by this failed probe.

## Authorized bounded correction

Rhino may create a child SKNode of the same Player and attach the exact probe action to that child. Keep its assertions on Player's restored parent and unprojected ground, the strict >10 action count, >30 ticks, >1 delivered texture, 60 actual callbacks, and all analytic projected Player/camera checks unchanged. Add an assertion of the probe's retained Player parent if useful. Do not alter runtime clip/action policy, bypass callbacks, weaken thresholds, skip the test or change authoritative behavior. Rebuild and rerun all 18 native tests in the reserved serialized simulator slot. Preserve new logs and source/build identities separately. A second failure requires diagnosis and reporting before further retries.

Status: correction authorized, retry result pending. Art acceptance, publication verification, merge/release and physical-device gates remain unchanged.
