# Existing-art traversal: slice8 diagnostic

**CAPTURED TECHNICAL DIAGNOSTIC, NOT VISUALLY ACCEPTED.** Corrected central0659 run passed exactly1 test in37.312s, with0 failures/0 skips and xcodebuild exit0. Worker independently verified the actual xcresult and imported52 scene screenshots,51 selected-texture PNGs and824 callback rows across2 arms. No repaired-scene, source fidelity or visual acceptance follows.

Authority: accepted runtime `intent/2026-11-16-benchmark-faithful-scene.md`, slice8, canonical SS-specs d1bfd1c and existing BP-008/BP-009/BP-012. [Visual acceptance contract](../visual-acceptance-20261116/CONTRACT.md). This is expressly an **existing shipping-art diagnostic**, not a coherent repaired whole scene. It does not expand rejected sources, states or clips, select a new production treatment, change the pin or weaken issue237's separate playback checks.

## Failed native attempt and corrected retry gate

The 0654 run failed: 1 failed, 0 passed, 0 skipped, with 1,408 assertions exclusively at the incorrect fractional-root comparisons. See [retained attempt02](attempts/02-q8-snapshot-mapping/README.md) for exact source, raw log, summary, tree and105 attachments. This is not admitted active evidence. Issue #239 remains open as a harness mapping defect, not an established production defect. Corrected Swift SHA256 is `f2c21f395c1cebfd7b7352acb26902ef99a7c40cb11ff1cca5daab1d89908a7a`. It records raw Q8 authority, integer snapshot roots and observed renderer roots separately and asserts both production mappings exactly. Negative fractional and one-unit mutation guards pass. Corrected native retry passed as documented below. Issue #239 remains open.

## Narrow implementation

New fixture: `AppTests/ExistingArtTraversalTests.swift`, focused XCTest `ExistingArtTraversalTests/testExistingArtLiveTraversalReversalCollisionPauseAndReducedMotion`.

It presents actual `GameScene` in a real `UIWindow`/`SKView`, drives existing stick touch methods, uses normal `GameSession.step` and retains observations through the existing `benchmarkPlaybackObserver` in `didEvaluateActions`. It does not derive selected texture identity from tick arithmetic or install a deterministic frame selector. The selected delivered source path is read through the existing SpriteLibrary observation of the actual sprite texture. Selected GPU texture PNG attachments and source byte hashes are retained separately.

Seed1 begins at the existing test-only position (736,654), adjacent to the real transit kiosk. This is **not a legal replay from the normal initial spawn**. No runtime input, collision solid or Camera is edited. Two arms use the same commands, one normal and one with the supported presentation Reduced Motion setting. Both must finish at tick380 with equal authority digests and separately replay the actual recorded commands through a second real GameSession initialized with the same test position. The replay equality is asserted and serialized. Python does not implement movement or a simulation.

| Planned route phase | Ending tick | Stick position fraction (not normalized command magnitude) |
|---|---:|---|
| quarter-west |20| -0.25,0 |
| half-west |40| -0.5,0 |
| approach-west |55| -1,0 |
| reverse-east |75| 1,0 |
| collision-west |105| -1,0 |
| slide-northwest |155| -1,1, using production radial clamp |
| rear-west |190| -1,0 |
| rear-south-collision |220| 0,-1 |
| return-east |265| 1,0 |
| front-south |325| 0,-1 |
| front-west |355| -1,0 |
| release |380| neutral |

Production TouchController dead-zone/remapping remains active. Actual commands are recorded, not inferred from those stick fractions. At tick55 production `setPaused(true)` holds eight actual callbacks. The harness asserts unchanged tick, position, digest and action-selected texture, resumes with fresh stick input, and freezes the scene at terminal callback to prevent teardown tick races. SwiftUI's pause overlay is not exercised.

## Images and scope

Each phase endpoint and one paused callback retained a shipping screenshot and a reversible selected-midpoint post-action still: **52 actual scene screenshots**. Additional actual selected texture attachments total51. The packet contains824 callback rows and1073 runtime-resource hash bindings. Exact one-test identity, result and attachment provenance passed before import. [Portable comparison gallery](index.html) offers13 keypoints x2 mappings x3 display modes with normal/Reduced Motion pairs, shipping primary. Browser interaction verification is pending coordinator review.

The live scene retains shipping presentation, ordinary production HUD and authoritative Camera fields. The extra midpoint capture uses the existing `ReferenceProjectionTrial.midpoint` and the reversible upright/ground-tree pattern in `ReferenceProjectionCaptureTests.capture` (226-273). It preserves the action-selected textures and restores every node before the next live update. It is **not live midpoint display evidence**, new source registration, a synthetic benchmark backdrop or a production mapping change. HUD remains excluded from that ground transform. No new shadow or overlay art is authored.

Independent importer checks reconstruct Q8 authority and deltas, exact truncation-toward-zero snapshot roots, exact snapshot-to-renderer roots, circle-vs-serialized-authoritative-solid separation, world front/rear relations, actual collision stop/reversal/wall-slide, command/tick boundaries, pause holds, actual projected node roots, selected texture/scene PNG attachment hashes and image dimensions. The 0.002 scene-root allowance is the existing Float-backed SpriteKit transform precision guard, not a visual slip tolerance. More than64 colors is an exact blank-image guard, not aesthetic acceptance.

World-side relations are **not visible-pixel occlusion segmentation**. Screenshots support later manual occlusion review but do not assert that front/rear/corner coverage is complete or readable. No fixed16-pose, four-facing family, dodge, dense encounter, complete occlusion ordering, source fidelity, SwiftUI settings controls, scanout cadence, physical-device or production acceptance follows.

## Resource provenance

The actual test-bundle resource inventory follows the existing `ExistingArtEncounterTests.resourceInventory` convention: reachable runtime asset catalog entries resolve through `RuntimeAssetBundle`; development `/Sources/` fallback is rejected. Every inventoried file is hashed from resolved runtime bytes. This is a reachable-resource **superset**, not per-pixel attribution. Observed Player paths are additionally hashed directly at observation. The packet and importer do **not** attest every executed Swift/build/configuration input. Source snapshots and exact command/result paths remain separate observations.

## Validation performed before native gate

- `xcrun swiftc -frontend -parse -DDEBUG AppTests/ExistingArtTraversalTests.swift`: exit0. This is **syntax only**, not iOS type checking or a native pass.
- `PYTHONDONTWRITEBYTECODE=1 /Users/appliedalchemylabs/Developer/video-use/.venv/bin/python -m unittest -v test_evidence_guards`: **10 synthetic guard regressions passed in0.103s**. They test identity/zero-test rejection, path/attachment mutations, hash/size mutations, independent root arithmetic, pause mutations, PNG dimensions/blankness and exact phase boundaries. They do not fabricate gameplay traces or replace native evidence.
- Before import, `verify_retained.py capture` deliberately rejected absent evidence. After actual import it passes offline with52 captures/824 rows/51 textures/1073 resource bindings.
- `/Users/appliedalchemylabs/Developer/video-use/.venv/bin/python -m unittest -v test_evidence_guards test_retained_evidence`: **19 tests passed in9.234s**, including9 actual retained-evidence mutation regressions. No xcrun or external export directory is used by these offline tests.
- `build_gallery.py`: built from all52 actual captured files. `python -m unittest -v test_gallery`:3 portable gallery tests passed in0.245s, checking all52 image hashes/dimensions, complete keypoint/mapping combinations, links and honest controls. These are not real-browser size measurements. Gallery browser validation remains independently coordinator-owned.

Observed per arm: normal412 rows/25 selected textures/380 commands, Reduced Motion412 rows/26 selected textures/380 commands. Both final and separate command-replay digests equal `8c1a3872ea4a135ea4be69b30188db3856e3514c99b876ed948a300cc5b3e895`. Different selected-texture counts are observed live scheduling, not evidence of different authority or complete pose coverage.

## Compiler attempt history and frozen source

The syntax parser did not establish iOS type correctness. Coordinator's first native build found the CGPoint/CGRect overload ambiguity at `player.convert(.zero, to: scene)`. Coordinator corrected it to explicit `CGPoint.zero`, with no assertion or behavior change. The exact rejected source is retained in `attempts/01-compile-point-overload/ExistingArtTraversalTests.executed.swift`, SHA `6c6206b5892f1c0f1f4a805307c3a7fc3e56e93a26e7521c42dc20c7ad339356`. It was reconstructed from the corrected file by reversing only that spelling and verified against the previously recorded original hash. Raw compiler output and zero-test summary are retained separately in `attempts/01-compile/`; no native pass is claimed for that build. Worker preserved the frozen source and changed only the test harness after coordinator released it for the #239 correction. Frozen source for the failed0654 run SHA: `66a9d5feeca9c19d3ed900292ee1125816b29d410c71b819f0a6867d433c451b`.

`--coordinated-three` is a separate importer mode for the exact authorized traversal, encounter and viewport test identities, all required passed with no failed/skipped/expected-failure cases. The default remains exactly this single traversal test. Traversal attachment provenance is bound to its manifest testIdentifier in either mode; other cases cannot supply its attachments. Retained `run-scope.json` selects one of those two fixed whitelists for offline checking, never arbitrary test counts. Synthetic tests reject a wrong third identity and cross-test or failure-associated attachments. Actual capture verification/mutation tests in `test_retained_evidence.py` passed after real import and fail rather than skip if evidence is absent.

## Exact passing command, executed centrally, NOT BY WORKER

The actual command below is retained in `capture/native.log`. Coordinator serialized execution. Result is `capture/summary.json`, exact test tree is `capture/tests.json`, original export provenance is `capture/attachment-manifest.json`. Source SHA at correction is f2c21f395c1cebfd7b7352acb26902ef99a7c40cb11ff1cca5daab1d89908a7a. These source/command observations are not a complete executed build-input attestation.

```sh
/Applications/Xcode.app/Contents/Developer/usr/bin/xcodebuild -project SSRuntime.xcodeproj -scheme SSRuntime -sdk iphonesimulator -destination 'platform=iOS Simulator,id=84297C74-033E-408F-9622-D36BFF32F74E' -configuration Debug CODE_SIGNING_ALLOWED=NO ENABLE_TESTABILITY=YES SS_RENDERER_TEST_CONDITIONS=SS_RENDERER_TEST_SUPPORT -derivedDataPath /Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-native-derived-20261116 -resultBundlePath /Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-traversal-20261116-0659.xcresult -parallel-testing-enabled NO -only-testing:SSRuntimeTests/ExistingArtTraversalTests/testExistingArtLiveTraversalReversalCollisionPauseAndReducedMotion test
```

Actual exports: `/Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-traversal-exports-20261116-0659`. Live `verify_capture.py --exports <that path> --xcresult <0659 result> --import-to capture` independently passed in2.3s, exact single-case mode. Retained evidence is not overwritten on import. No worker simulator execution or commits.

## Earlier proposed command, NOT EXECUTED BY WORKER

Native execution is serialized by coordinator permission. Generate the ignored Xcode project with the existing `xcodegen generate` command to discover the new test file; do not edit project.yml. Run the following with a hard **480-second execution limit**, retaining raw output and a fresh result path. Never run the unfiltered suite.

```sh
xcodebuild -project SSRuntime.xcodeproj -scheme SSRuntime -sdk iphonesimulator -configuration Debug -destination 'platform=iOS Simulator,id=CACB3927-A76E-43A5-9ACA-C389EB38C0C3' CODE_SIGNING_ALLOWED=NO ENABLE_TESTABILITY=YES SS_RENDERER_TEST_CONDITIONS=SS_RENDERER_TEST_SUPPORT -derivedDataPath /Users/appliedalchemylabs/.jcode/scratch/ss-releasevariation-native-derived-20261116 -resultBundlePath /Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-traversal-20261116-first.xcresult -only-testing:SSRuntimeTests/ExistingArtTraversalTests/testExistingArtLiveTraversalReversalCollisionPauseAndReducedMotion test
```

After execution, export attachments using existing `xcresulttool export attachments` workflow. `verify_capture.py --exports <fresh exports> --xcresult <fresh result> --import-to capture` must pass exact one-test identity and verify every native attachment before importing. It refuses to overwrite existing evidence. Retained summary/tree/attachment manifest then support `verify_retained.py capture` with no xcrun, simulator or external export path. Add actual-evidence mutation regressions after that import. Preserve failed attempts and their executed source snapshot if a harness correction is needed. Worker commits are not authorized; coordinator-owned review-branch publication is separate.
