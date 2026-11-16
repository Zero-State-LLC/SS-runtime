# Existing-art viewport/accessibility diagnostic, slice10

**Actual0653 simulator result imported and technically verified. Visual acceptance remains UNREVIEWED.**

## Actual0653 evidence

Open `capture-0653/index.html` for all ten original captures with native/half-size display. Retained `summary.json`, `tests.json`, raw export manifest/files, `records.json`, `verification.json` and `files-sha256.json` make the import independently reproducible. Actual result: exactly **1 passed / 0 failed / 0 skipped / 0 expected failures**, focused test duration **9.627963066 seconds**, on **iPhone SE (3rd generation), iOS26.5 Simulator**, not physical hardware. Result path: `/Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-viewports-20261116-0653.xcresult`.

All ten PNGs decode and byte-match their runtime JSON SHA256 values. The resource inventory contains **1,030 reachable bundled PNG records**, a superset, not proof of per-node consumption. Reader now recognizes xcresulttool's occurrence/UUID filename suffix while retaining strict test identity and exact plate census.

Observed hosted bounds: both SE captures have host and window `[0,0,667,375]`; both reference captures have host and window `[0,0,844,390]`. **No requested-versus-observed bounds mismatch occurred in0653.** This is an observation about this run, not a guarantee UIKit will preserve these requests elsewhere. All four records retain requested size, actual host/window bounds and observed safe insets.

Direct initial image inspection found nonblank scene and accessibility3 upgrade output. The accessibility3 screenshot shows only the top of the scrolling first upgrade card, not all choices or proof that the rest can be reached. Scene captures retain existing art/HUD, not benchmark fidelity. Coordinator visual/browser verification remains independent and pending.

Reproduce import to a NEW output path (refuses replacement):

```sh
python3 -B docs/review/existing-art-viewports-20261116/import_capture.py \
  /Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-viewports-20261116-0653.xcresult \
  /Users/appliedalchemylabs/.jcode/scratch/ss-existing-art-viewports-exports-20261116-0653 \
  "$NEW_OUTPUT"
```


Authority: accepted `intent/2026-11-16-benchmark-faithful-scene.md`, slice10, unchanged BP-001–BP-012 gates. Owns only `AppTests/ExistingArtViewportTests.swift` and this packet. No production, shared project, CI, art or collision edit. No commit.

## Avoided duplication

Existing `Tests/SurveillanceCoreTests/HUDMappingTests.swift` and `HUDPresentationTests.swift` already check mapped geometry, control targets, smallest supported safe canvas and labels. `AppTests/WeaponUpgradePresentationTests.swift:94–107` already checks upgrade column selection and accessibility hosting. `InterruptionTests.swift:85–106` owns system Reduce Motion preference behavior. This slice does not replace or weaken them.

The added test records actual produced GameScene control rectangles and rendered nodes plus production SwiftUI upgrade views. It adds retained, byte-hashed PNGs and built-resource inventory rather than another copy of the existing layout rules.

## Captured census: 10 PNGs, one JSON

- Six GameScene renders: safe canvases 667×375 and 844×390, plus synthetic 844×390 view with top/left/bottom/right insets `[0,47,8,47]`, yielding existing HUDMappingTests safe size 750×382. Each has standard HUD/normal motion and extra-large HUD/Reduced Motion.
- Four hosted production UpgradeSelectionView capture requests: 667×375 and 844×390 output canvases, each `.large` and `.accessibility3` Dynamic Type. These are requests, NOT assumed actual UIKit host sizes. Each record retains actual `hostViewBounds` and `windowBounds` separately from `requestedSize`, and marks `logicalSize` as `requested-output-canvas-not-host`. UIKit may normalize the window. The reader reports `requestedViewportObserved: false` if either actual bound differs, without relabelling a normalized run as the requested viewport. `drawHierarchy` draws at observed host bounds into the requested canvas with no resize, so larger hosts may be clipped and smaller hosts may leave unused canvas. Model is presented through its existing API, not an actual legal encounter progression. No choice is submitted.
- The six scene PNGs use `SKView.texture(from:crop:)` on the real GameScene and manually compose its aspect-fit viewport/letterbox at one output pixel per logical point. They are **offscreen static scene-node renders**, not hardware screen screenshots or post-action cadence evidence.
- Upgrade PNGs use real UIHostingController/window and `drawHierarchy(afterScreenUpdates:true)`. Observed host insets are retained, not assumed to match a device.
- Every PNG is attached as the exact Data whose SHA256 appears in JSON. A reachable accepted runtime-PNG superset is read through RuntimeAssetBundle and hashed in the same run. Workspace fallback is rejected. This inventory does **not** prove that every listed file was consumed by a drawn node. No test/configuration/executed-source attestation is claimed.

All insets are test fixtures, not physical-device measurements. No view is identified as an iPhone17Pro hardware run.

## Exact focused run, coordinator slot required

**Do not run until the coordinator assigns the simulator slot.** The local generated project must include the new file via the existing `AppTests` source directory rule. Only the coordinator may refresh it with the documented `xcodegen generate` if necessary. No shared project edit is part of this slice.

Based on `.github/workflows/ci.yml:129–134`, with the new focused selector:

```sh
xcodebuild -project SSRuntime.xcodeproj -scheme SSRuntime -sdk iphonesimulator \
  -destination "platform=iOS Simulator,id=$SIM_ID" -configuration Debug \
  CODE_SIGNING_ALLOWED=NO ENABLE_TESTABILITY=YES \
  SS_RENDERER_TEST_CONDITIONS=SS_RENDERER_TEST_SUPPORT \
  -only-testing:SSRuntimeTests/ExistingArtViewportTests/testExistingArtViewportEvidence \
  -resultBundlePath "$RESULT" test > "$LOG" 2>&1
```

Use new non-existing RESULT path and the coordinator's simulator ID. Retain all failed/zero-test results. Expected: exactly one passing focused test, ten PNG attachments and `existing-art-viewports-records` JSON. The worker is not authorized to operate the physical device independently. The accepted ten-slice intent permits a coordinator-managed physical diagnostic when prerequisites are satisfied, but this packet contains no such run.

## Fresh evidence import/report

```sh
xcrun xcresulttool get test-results summary --path "$RESULT" --format json > "$SUMMARY"
xcrun xcresulttool get test-results tests --path "$RESULT" --format json > "$TREE"
xcrun xcresulttool export attachments --path "$RESULT" --output-path "$EXPORTS"
python3 -B verify_export.py "$SUMMARY" "$TREE" "$EXPORTS"
```

Run the Python command from this packet, or supply its full path. Verifier rejects zero-test, wrong identity, failed/skipped/expected-failure runs, missing/duplicate plates, hash/dimension/settings changes, malformed resources and truncated PNGs. It decodes PNGs but applies **no numerical visual tolerance** or acceptance inference. Actual images must still be independently inspected for blank capture, clipping, legibility and resource fidelity. No report is pre-populated as a successful native result.

Portable verifier regressions plus retained actual0653 validation (Pillow required):

```sh
python3 -B -W error::ResourceWarning docs/review/existing-art-viewports-20261116/test_verify.py
```

## Explicit unsupported checks

Physical-device execution/performance, VoiceOver focus/speech, Switch Control interaction, upgrade scrolling/reachability, terminal/settings/title surfaces, OS text scaling of SpriteKit labels, live motion/cadence, orientation transitions, real device safe-area changes, grayscale comprehension, coherent-source benchmark acceptance and production admission. Reduced Motion and HUD scale are paired presentation settings here, not independently isolated motion experiments. The scene stays on existing production art/projection, not the unresolved coherent-source midpoint proposal.

## Handoff state

Coordinator executed0653. This worker performed read-only result extraction/import, not another native run. No physical-device operation occurred. Swift remains frozen at SHA256 `fa7ecfda2a466e486f74d6de987b36da0be357d38b7814085bf46ecb71b3e221`. Coordinator review and actual interactive accessibility acceptance remain pending. At06:55:57UTC, the command above passed **7 tests in0.624s**: six synthetic verifier cases and one retained actual-packet/gallery-integrity case. Diff whitespace checks passed. No new native execution or commit.
