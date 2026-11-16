# Remaining south Player releases: static native evidence

Status: **verified static source delivery, not art or family admission**. Captured November 16, 2026 after the owner's midpoint selection. This packet covers the 14 new south release candidates only. Original releases 5/13 remain unchanged.

## Review

Open `index.html` for all 238 actual SpriteKit pose captures. Separate source-only normal and quarter-speed reviews are in `../player-all-release-source-20261116/artifacts/normal-speed.html` and `quarter-speed.html`. Those source movies are not recordings of this native run.

The native images are 576×432 pixels from 192×144-point crops in an isolated 704×326-point test scene. The gallery enlarges the logical crop for inspection. It does not show a full shared-scene midpoint traversal or establish the BP-012 native/50%/grayscale family bar.

## Observed checks

- Actual `AllReleaseSourceTests` run: **2 tests passed, 0 failed, 0 skipped**, 70.519 seconds of test execution. Static pose capture took 52.009 seconds and Reduced Motion checks took 18.510 seconds. Simulator: iPhone 17 Pro, iOS 26.5, arm64.
- Every new phase has 17 actual selected source textures, checked by object identity with unchanged root, size and anchor. All 238 captures have matching phase/pose/source/tick records.
- Authored holds remain 3/128 second. Neutral starts at 48/128 = 0.375 second, sampled on the first eligible whole simulation tick, offset 23. This is static selection evidence, not a claim that a display callback showed every pose in real time.
- Reduced Motion bypasses entry and cancels an active release for all 14 phases. Returning to Standard does not resurrect the cancelled release.
- Captured bundle-file SHA-256 values match all 225 distinct repository texture resources used by this run. `verification.json` additionally locks the native test and `project.yml`, 227 source/configuration hashes total, plus 238 image hashes and the record attachment hash.
- Independent image decoding found all 238 images at 576×432 pixels and 17 distinct decoded images per phase. Phase 7's midpoint crop was inspected visually for complete character framing. This is not owner visual acceptance.
- The 210 new intermediate resources are test-only copies of the corresponding verified source frames. Entry and neutral reuse existing resources. No production asset, renderer implementation, projection/input mapping or specification pin changed.

## Execution corrections, not hidden success

The first focused run at `ss-allrelease-native-20261116-0207.xcresult` passed both native tests, but the importer rejected its bundle hashes. The build log demonstrated `copypng -compress -strip-PNG-text` rewriting PNG bytes. That capture was not admitted into this packet. The strict equality guard was retained.

`COMPRESS_PNG_FILES: NO` and `STRIP_PNG_TEXT: NO` now apply only to `SSRuntimeTests`. Production target settings are untouched. These are the documented Xcode controls for copied PNG recompression and text metadata stripping (Apple's Build Settings Reference). An importer regression asserts that both controls remain scoped to the test target.

A subsequent `test-without-building` invocation at `...-0211.xcresult` selected zero tests despite an exit-zero status. It is not counted as successful validation. Compiled test symbols were present. The previously successful direct `test` action was used instead, producing the complete two-test `...-0213.xcresult` result recorded here. The discovery discrepancy was not attributed to a proven root cause.

## Reproduction

From repository root, after source artifacts and test resources have been verified:

```sh
xcodegen generate
xcodebuild -project SSRuntime.xcodeproj -scheme SSRuntime \
  -sdk iphonesimulator -configuration Debug \
  -destination 'platform=iOS Simulator,id=<available-simulator-id>' \
  CODE_SIGNING_ALLOWED=NO ENABLE_TESTABILITY=YES \
  SS_RENDERER_TEST_CONDITIONS=SS_RENDERER_TEST_SUPPORT \
  -derivedDataPath <isolated-derived-data> \
  -resultBundlePath <fresh-result.xcresult> \
  -only-testing:SSRuntimeTests/AllReleaseSourceTests test
xcrun xcresulttool export attachments --path <fresh-result.xcresult> \
  --output-path <fresh-export-directory>
python3 -B scripts/import_allrelease_native.py \
  --exports <fresh-export-directory> --xcresult <fresh-result.xcresult> \
  --output <fresh-review-directory>
python3 -B scripts/import_allrelease_native.py \
  --verify docs/review/player-all-release-native-20261116
python3 -B scripts/test_allrelease_native.py
```

The importer requires exactly two passing tests and rejects failed, skipped or zero-test runs, missing/duplicate poses, wrong source identity or tick offsets, and bundle/source byte drift. The portable verifier rechecks the published census and every recorded hash. Eleven regression tests cover these guards and test-only build settings.

## Gates retained

New release artwork/contact quality still requires visual review. Moving world-space support, continuous swept clearance, full-sole stability, live cadence, restart/reversal coverage for every new candidate, four facings, complete-family admission, shared-scene review and physical-device acceptance remain open. This packet does not close historical runtime #237 or weaken its 16-pose assertion. The twice-capped unfiltered local core path was not retried. No merge or receipt adoption is authorized.
