# Implementation validation chronology

## First build

`build-debug-0347.log`: compilation failed on ambiguous `.zero` overload in the new test's `SKNode.convert` call. Explicit `CGPoint.zero` corrected the compile-only defect. No runtime or test assertion change. `build-debug-0349.log` then reports TEST BUILD SUCCEEDED.

## First native execution, 03:50UTC

`tests-0350.xcresult`, raw log and exported actual summary are preserved. Exact18tests executed:17passed,1failed,0skipped. Prior8kiosk tests all pass unchanged. All analytic geometry, inverse-input, controller/dodge, world-command parity, legal pilot, restoration/new-node and paused/restart tests passed.

Only `testActualSKViewCallbacksRestoreBeforeActionsAndProjectAfterward` fails: action-probe count0did not exceed10. Its60actual displayed callbacks, >30ticks, >1delivered texture and all post-action projected Player/camera assertions passed. Diagnosis: the test attaches its probe action to Player's sprite root before the idle-to-move transition. Existing `WorldRenderer.playClip` clears all root actions when its clip token changes, intentionally replacing playback, so the unrelated probe is removed before it can execute. Coordinator notified and asked to record a defect before revising probe placement. Proposed child-node probe retains the same strict count and coordinate assertions and survives the existing root playback replacement. No threshold weakening or runtime animation-policy change is proposed.

## Host and Release

`swift-focused-0350.log`:10tests in3suites passed, exit0, using isolated scratch path. No shared main build tree touched.

`build-release-0350.log`: BUILD SUCCEEDED, exit0. `release-symbols-0351.log` and `release-strings-0351.log` contain no `LiveWorldProjection`, `SSKioskProjection`, `live-midpoint`, `KioskPlayableReview` or `SSKioskReview` markers. Executable SHA256 `963736d968a4a63f145cf76e2ec91b8a47ece70e40628c5c5ba51b9f12f72746`.

No passing live-action restoration claim at this first checkpoint. All failures remain retained. No source-art changes, gameplay change, acceptance, merge, release or physical-device qualification.

## Authorized child-probe retry, 04:07UTC

Coordinator independently inspected the defect and authorized only child-owned probe placement in `PROBE-DEFECT.md`. The exact bounded diff is retained as `probe-only-correction-0407.diff`: attach a child SKNode to the same Player, run the same probe action on that child, and additionally assert the child retains its Player parent. All existing strict assertions, thresholds, callback requirements and analytic geometry checks remain unchanged. No runtime animation or other runtime code changed during this retry.

`build-debug-0407.log` reports TEST BUILD SUCCEEDED. `tests-0407.xcresult`, raw log and exported `tests-0407-summary.json` report **18 total, 18 passed, 0 failed, 0 skipped**, exit0. This includes all10new projection tests and all8byte-unchanged kiosk tests. The actual live SKView test passed60display callbacks, >10action-time restoration probes, >30simulation ticks, >1delivered texture and all projected Player/camera assertions. Host `swift-focused-0407.log` also passed10tests in3suites, exit0.

Source and native product SHA256s are in `source-build-hashes-0408.txt`. Key identities:

- LiveWorldProjection.swift: `74e551043e73206160e791f1e2410d45105ee53a353216587c56679feaadac75`
- LiveWorldProjectionTests.swift: `479733e804b4d4d4a1ec98f893e3d754e86d89355ae012082d224fafb953724c`
- Debug implementation dylib: `a9e8d87abf61f63750d2a63e8d045f983af45e97267eaf29990cd07981fdd347`
- Native test bundle: `6f1c95f5e6aa9ca63feba21b04b83063493cfceb76bebda72393368555f5d037`
- Prior kiosk test source remains: `fc2f903d2f8c9cadbff3cdd425a607b50e77b2b86d5a9225acf67b29ae01efa6`

Final-source Release rebuild `build-release-0355.log` succeeded. Its executable SHA256 is `2297733e9e6dcb23b2c792095d0ebb0a21f444df15a6a8852e348db7a554f69a`. Fresh `release-symbols-0407.log`/`release-strings-0407.log` confirm all five forbidden projection/review marker patterns listed above remain absent.

Simulator slot returned to coordinator at04:08UTC. No worker commit. Coordinator owns independent review, actual current/candidate app captures, documentation/board/PR handling and publication. Geometry/lifecycle success is not art acceptance, full gameplay qualification or physical-device certification. All0350failure artifacts remain unchanged.
