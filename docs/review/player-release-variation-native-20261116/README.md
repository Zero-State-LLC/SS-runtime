# Native baseline/variation comparison

Owner approved slice1 at **2026-11-16 03:10:28UTC**. This packet measures the actual renderer with both frozen source families. It is not a new source proposal, shipping selection, live-cadence result or art admission. Original5/13 are unchanged and excluded.

## Scope

- New `AppTests/ReleaseVariationSourceTests.swift`, adapted explicitly from `AllReleaseSourceTests:14-129`.
- New isolated `AppTests/ReleaseVariationAssets/`:210 exact variation intermediate PNGs and one435-entry resource-hash catalog. Baseline intermediates and shared endpoints reuse existing test resources read-only.
- New variation-specific preparation/import/verification/regression scripts. No existing source/native packet edits, App/Sources/production asset changes, specification pin, input or mapping changes.
- Existing test-only `COMPRESS_PNG_FILES: NO` and `STRIP_PNG_TEXT: NO` are unchanged. `project.yml` already includes `AppTests` recursively, so only the gitignored Xcode project is regenerated. No shared project or CI file was edited by this worker.

## Focused actual tests

`ReleaseVariationSourceTests` contains exactly three XCTest cases:

1. **Paired all-pose capture**:14phases ×17poses ×2families =476 actual SpriteKit crop attachments. Checks exact bundle PNG SHA against the catalog before constructing textures, selected texture object identity at every pose, root, registration size and anchor. Records family/phase/pose, texture resource name, actual bundle digest and tick offset. Both families use the real `WorldRenderer` and existing test-only injection, not a replacement renderer.
2. **ReducedMotion**: both families ×14phases ×entry bypass/active cancellation. Standard mode after cancellation does not resurrect the release.
3. **Interruption**: both families ×14phases. Repeated paused ticks preserve pose8. Movement cancels the release, a fresh stop restarts at entry, the final intermediate remains at offset22 and neutral is selected at offset23. Reset while idle does not resurrect a stale release.

The source neutral boundary is exactly48/128=0.375s. Static native sampling reaches it at the first eligible whole60Hz tick, offset23 (23/60s). This is not a claim that a live display callback delivered neutral at exactly0.375s or displayed every intermediate frame.

## Reproduction

From repository root, using the already available local Python with NumPy and Pillow:

```bash
PY=/Users/appliedalchemylabs/Developer/video-use/.venv/bin/python
P=docs/review/player-release-variation-native-20261116
SCRATCH=/Users/appliedalchemylabs/.jcode/scratch

# Resources are supplied as test-only source copies. Verify them without rewriting.
"$PY" -B scripts/prepare_release_variation_native.py --verify
# For the initial setup only, when ReleaseVariationAssets does not exist:
# "$PY" -B scripts/prepare_release_variation_native.py

xcodegen generate
xcodebuild -project SSRuntime.xcodeproj -scheme SSRuntime \
  -sdk iphonesimulator -configuration Debug \
  -destination 'platform=iOS Simulator,id=CACB3927-A76E-43A5-9ACA-C389EB38C0C3' \
  CODE_SIGNING_ALLOWED=NO ENABLE_TESTABILITY=YES \
  SS_RENDERER_TEST_CONDITIONS=SS_RENDERER_TEST_SUPPORT \
  -derivedDataPath "$SCRATCH/ss-releasevariation-native-derived-20261116" \
  -resultBundlePath "$SCRATCH/ss-releasevariation-native-20261116-0313.xcresult" \
  -only-testing:SSRuntimeTests/ReleaseVariationSourceTests test

# Use fresh result/export/output paths for a reproduction. Never overwrite evidence.
xcrun xcresulttool export attachments \
  --path "$SCRATCH/ss-releasevariation-native-20261116-0313.xcresult" \
  --output-path "$SCRATCH/ss-releasevariation-native-20261116-0313-exports"
"$PY" -B scripts/import_release_variation_native.py \
  --exports "$SCRATCH/ss-releasevariation-native-20261116-0313-exports" \
  --xcresult "$SCRATCH/ss-releasevariation-native-20261116-0313.xcresult" \
  --output "$P/capture"
"$PY" -B scripts/import_release_variation_native.py --verify "$P/capture"
"$PY" -B scripts/test_release_variation_native.py
```

The actual build/test command is capped at540s, below the600s tool limit. It uses a direct focused `test` action, not the historical zero-selected-test `test-without-building` path. The importer queries the actual xcresult summary **and test identity tree**: exactly three named passing cases, no failures, skips or expected failures. Exit0 or a green unrelated suite is insufficient. The twice-capped unfiltered local core suite is not retried.

## Evidence verifier

The importer rejects missing, duplicate, reordered or wrong-family captures/records, path traversal, wrong source names or3/128 tick offsets. Every actual bundle hash must match the corresponding verified frozen source/test resource. It verifies both full frozen source packets before importing; baseline data is not relabeled as new variation.

Published verification rechecks476 capture hashes, record/test-tree hashes, all source/configuration hashes, strict status/timing, PNG dimensions and17 distinct decoded captures for every family/phase. It requires28 pixel-exact baseline/variation native endpoint pairs. Intermediate native pixel differences are measured, not assigned an invented acceptance threshold. The copied native test resources do not enter the production target.

Parser fixtures in importer unit tests are synthetic schemas only. Actual-capture regressions require the real completed packet and never skip or fabricate replacement native captures. All malformed copies are temporary; originals remain unchanged.

## Limits

Isolated192×144-point crops from a704×326-point test scene are not full shared-scene midpoint traversal, continuous moving-world support, live cadence, four-facing/family completion, physical-device evidence or visual acceptance. This slice adds movement interruption/restart/ReducedMotion evidence for these exact source candidates, not every reaction/direction interruption combination. Existing baseline captures remain historical evidence of that baseline. Historical runtime#237 and its16-pose assertion are untouched. Coordinator owns visual review, shared CI integration, source admission and commit. No commit is made by this worker.

## Actual completion results

Source: `capture/verification.json` (status `STATIC_NATIVE_VARIATION_COMPARISON_NOT_ADMISSION`), with `xcode-test.log` and `import.log`.

- Result bundle: `/Users/appliedalchemylabs/.jcode/scratch/ss-releasevariation-native-20261116-0313.xcresult`, iPhone 17 Pro simulator `CACB3927-A76E-43A5-9ACA-C389EB38C0C3`, iOS 26.5 (23F77).
- xcresult summary: `Passed`, totalTestCount 3, passed 3, failed 0, skipped 0, expected failures 0.
  1. `testPairedAllPosesUseExactSourceTexturesAndTiming` passed (120.233s)
  2. `testBothFamiliesBypassAndCancelReducedMotion` passed (42.906s)
  3. `testBothFamiliesInterruptAndRestartWithoutStalePose` passed (29.911s)
- Importer: 476 verified captures (14 phases × 17 poses × 2 families), 442 verified source files, 576×432 PNGs, 17 distinct decoded poses per family/phase.
- Endpoints: 28 pixel-exact baseline/variation RGBA pairs.
- Measured intermediate differences: 182 changed native poses (13 per phase across 14 phases: poses 2-7 and 9-15 differ; poses 0, 1, 8 and 16 match). This is a measurement, not an acceptance threshold.
- Timing: authored neutral boundary 0.375s, first eligible 60 Hz neutral tick offset 23.
- `liveCadenceVerified: false`. Not art admission. Limits from verification.json: isolated static WorldRenderer capture, not live callback timing. No shared-scene, four-facing, physical-device or family acceptance. Original5/13 unchanged and excluded. No shipping selection or mapping, input or production art changes.
- Python regressions: 29 parser and real-native tests passed, exit 0 (`importer-tests.log`).
