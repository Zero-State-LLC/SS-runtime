# Native quiet-scene continuation, preparation only

## Issue247 revision3

Capture1020 passed its old checks but exposed omitted environment-upright projection.
It is retained unchanged, not accepted scene evidence. The exact old harness, importer,
tests, assembly, prepared inputs and all1020 capture files are copied in
`attempt-1020-before-upright-census/`; `attempt-1020-sha256.txt` inventories those bytes.
Current fixture is `source-scene-continuation-003-upright-census`, preparation schema
`source-scene-native-003`, records schema `source-scene-records-003`. `native.py prepare`
now writes **native-inputs-v3/**. Original **native-inputs/** is immutable historical input.
The current importer refuses old1020 records. Its archived importer retains the old
`validate_records` entry point; the historical regression exercises it on real1020 bytes.
See `UPRIGHT-CENSUS.md` for the exact existing-contract adaptation and validation.

Authorized extension at 09:47 UTC: new `AppTests/SourceSceneContinuationTests.swift`
plus this packet. **No native run or build has been performed by this worker.**
Coordinator owns simulator `CACB3927-A76E-43A5-9ACA-C389EB38C0C3` and the shared
`ss-releasevariation-native-derived-20261116` directory. Do not run concurrently.

## Explicit review-only compile gate

The entire XCTest class is guarded by `#if DEBUG && SS_SOURCE_SCENE_REVIEW`.
Ordinary Debug/Release CI cannot discover either checkout-dependent review test.
Only the focused commands below opt in, passing both conditions through the existing
`SS_RENDERER_TEST_CONDITIONS` setting. No project.yml or CI defaults are changed.
If the selected scene-capture test lacks prepared sources, it still fails immediately.
There is no skip or fallback. Portable Python guards remain runnable without native inputs.

## Source-independent authoritative placement probe

The coordinator-owned1014 export now records actual seed1 Camera id3 at[496,672],
visible with integrity3, and kiosk bounds[512,640]..[640,768]. Byte-identical placement
and export-manifest copies are bound in `assembly.json`; see `BINDING.md` for hashes.
This is placement evidence only, not scene capture. Arena socket definitions alone
were not used. The earlier cancelled `_dyld_start` probe is not a simulation failure.

The new `testReadAuthoritativeScenePlacement` constructs `GameSession(seed: 1)` using
the same initializer as the scene fixture, reads its snapshot without stepping, and
records all exact Camera IDs/roots/field origins (raw Q8 and world units), range,
heading, angle, integrity, visibility and clip state. It also records every solid's
ID/index/bounds/center/half-size, player root, arena bounds, tick and unchanged digest.
No source files, scene injection, screenshots or native preparation are needed.
The attachment `source-scene-authoritative-placement` is placement evidence only,
with `placementVersion=source-scene-seed1-placement-001`, fixtureVersion, actual loaded
Bundle executable SHA/path and source-read hash. It does not claim a rendered scene.

Coordinator can run this **first**, alone, without `native.py prepare`:

```sh
set -e
xcodegen generate
xcodebuild -project SSRuntime.xcodeproj -scheme SSRuntime -sdk iphonesimulator -configuration Debug -destination 'platform=iOS Simulator,id=CACB3927-A76E-43A5-9ACA-C389EB38C0C3' CODE_SIGNING_ALLOWED=NO ENABLE_TESTABILITY=YES SS_RENDERER_TEST_CONDITIONS='SS_RENDERER_TEST_SUPPORT SS_SOURCE_SCENE_REVIEW' -derivedDataPath /Users/appliedalchemylabs/.jcode/scratch/ss-releasevariation-native-derived-20261116 -resultBundlePath /Users/appliedalchemylabs/.jcode/scratch/ss-source-scene-placement-20261116-1007.xcresult -only-testing:SSRuntimeTests/SourceSceneContinuationTests/testReadAuthoritativeScenePlacement test
xcrun xcresulttool get test-results summary --path /Users/appliedalchemylabs/.jcode/scratch/ss-source-scene-placement-20261116-1007.xcresult
xcrun xcresulttool get test-results tests --path /Users/appliedalchemylabs/.jcode/scratch/ss-source-scene-placement-20261116-1007.xcresult
xcrun xcresulttool export attachments --path /Users/appliedalchemylabs/.jcode/scratch/ss-source-scene-placement-20261116-1007.xcresult --output-path /Users/appliedalchemylabs/.jcode/scratch/ss-source-scene-placement-20261116-1007-exports
```

Confirm exactly one passed placement test with zero failures/skips before using the
attachment. Read its exact Camera roots, do not choose guessed768,512 or496,672 socket
coordinates. Select an actual visible intact Camera and bind its unchanged world root
into the source registration. The scene-capture importer intentionally rejects this
placement-only result because its test identity/capture census are different.
These commands are provided, not executed by this worker. No placement result exists yet.

## Actual integration

The test uses `GameScene.renderBenchmark(snapshot:art:center:)`, not an SVG surrogate.
It adapts `WholeSceneBoundInputsTests.swift:19-44,64-78,185-241` with two ordinary arms:
original static controls and recommended candidate art. Original control PNG files,
prior review packets and production source remain untouched. It does **not** call
`installBenchmarkCameraFrames` or repeat one texture into 16 claimed clip frames.
There is one static south-neutral Player and one static intact neutral Camera per arm.

- Production HUD and control layout remain active, never hidden for an art-only plate.
- All seed-1 authoritative solids remain in the presentation snapshot. The Camera's
  position, field origin, heading, range, angle and visible intact state are retained.
  **Camera registration must name an actual visible intact seed-1 Camera root**.
  No field or collision is moved/resized to fit the art. The rendered field path is
  checked against `CameraFieldGeometry` using those same authoritative solids.
- Only the quiet presentation snapshot removes transient enemies/projectiles/etc.
  Simulation digest is checked before/after. This is not encounter or live-input proof.
- Candidate stone uses the existing building placement injection. The finite paving
  corner is one 576-square ground patch, not repeated across the arena. Existing plaza
  remains outside that bounded patch. No new production geometry is authored.
- The existing static injection hardcodes actor sizes/anchors. The test applies the
  explicit recommended source size/root to the resulting Player/Camera sprite nodes,
  refreshes review outlines, and records their actual roots/sizes/anchors. It never
  derives collision or fields from those nodes. Player and Camera roots must be in crop.
- Midpoint projection and native/half/grayscale extraction adapt the existing focused
  test. HUD remains outside the projected world chain. Retained zooms are exactly
  **1, 1.25 and 1.4** for each ordinary arm: **six records, eighteen image attachments**
  and one JSON record attachment. Every actor records world and actual projected root,
  source draw size and anchor. No staging, animation family or device claim.

The exact compiled fixture version is `source-scene-continuation-003-upright-census`.
The preparation manifest and importer require that identical value, rejecting older
single-zoom and pre-census fixtures. Native schema is `source-scene-native-003`.

## Fail-closed preparation

```sh
python3 -B docs/review/scene-source-assembly-20261116/native.py prepare
```

At10:19 UTC, strict preparation succeeded after all final source/recommendation and
placement-provenance dependencies were tracked. `native-inputs/` contains the four
exact checked PNGs and preparation JSON, not rendered scene evidence. Camera is the
final padded master, Player is canonical-identity-02 south-neutral, and stone is the
final normalized preview-alpha composite. Exact hashes and roots are in `assembly.json`.
No old rejected art enters the scene. `preparation-final-1019.json` retains the receipt.
Preparation reuses the strict assembly verifier before writing anything. It hashes
the current Swift source and assembly,
then copies exactly four checked PNGs and writes `native-inputs.json`.

The native test fails, not skips, if preparation is absent, pending, stale, a source
hash differs, source/evidence dependencies drift, or registration does not match.
It also rejects a changed harness source hash and invalid Camera placement. The
native inputs are simulator-host filesystem inputs resolved from the compiled
`#filePath`, not newly bundled production assets. Run from the same checkout used
to build. This is deliberately not a physical-device delivery mechanism.

No code in `native.py` launches tests. Its import action queries an actual xcresult
and exports attachments from that same result itself, rather than trusting unrelated
export directories. It requires exactly one passing test with the exact identifier,
zero failures/skips/expected failures, six ordinary records at the exact three zooms,
eighteen images, identical field authority, actual world/projected registration, original
control/runtime hashes and prepared source hashes. It writes only to a fresh capture directory.

### Binary provenance is not a source-read hash

The running test reads `Bundle(for: Self.self).executableURL`, records that actual loaded
`.xctest` executable's path and SHA256 under `loadedTestExecutable`, and separately
records `harnessSourceReadSHA256` from the current Swift file. The prepared expected
source hash is named `harnessSourceSHA256`, not an executable hash. Import requires
`--test-executable` naming the newly built test product and rejects a loaded-binary
hash mismatch even when the source-read hash is current. Installed and build-product
paths are retained separately because they normally differ. This catches stale installed
bundles without conflating source bytes and executable bytes. It does not prove source
compilation reproducibility. The coordinator must use the fresh build/test command,
retain its build log and original xcresult, and not substitute an older expected binary.

## Exact coordinator command, NOT executed here

After inputs are supplied and preparation passes, regenerate the project so the new
AppTests source is included by the existing `project.yml` directory source rule:

```sh
set -e
xcodegen generate
python3 -B docs/review/scene-source-assembly-20261116/native.py prepare
xcodebuild -project SSRuntime.xcodeproj -scheme SSRuntime -sdk iphonesimulator -configuration Debug -destination 'platform=iOS Simulator,id=CACB3927-A76E-43A5-9ACA-C389EB38C0C3' CODE_SIGNING_ALLOWED=NO ENABLE_TESTABILITY=YES SS_RENDERER_TEST_CONDITIONS='SS_RENDERER_TEST_SUPPORT SS_SOURCE_SCENE_REVIEW' -derivedDataPath /Users/appliedalchemylabs/.jcode/scratch/ss-releasevariation-native-derived-20261116 -resultBundlePath /Users/appliedalchemylabs/.jcode/scratch/ss-source-scene-continuation-20261116-1026.xcresult -only-testing:SSRuntimeTests/SourceSceneContinuationTests/testQuietSouthNeutralOrdinaryScene test
python3 -B docs/review/scene-source-assembly-20261116/native.py import --xcresult /Users/appliedalchemylabs/.jcode/scratch/ss-source-scene-continuation-20261116-1026.xcresult --output docs/review/scene-source-assembly-20261116/native-capture-1026 --test-executable /Users/appliedalchemylabs/.jcode/scratch/ss-releasevariation-native-derived-20261116/Build/Products/Debug-iphonesimulator/SSRuntime.app/PlugIns/SSRuntimeTests.xctest/SSRuntimeTests
```

Use fresh result/capture paths for retries and preserve failures. If a prior
`native-inputs/` exists, retain it under a distinct evidence directory before preparing
again. Do not run the native test while sources are pending just to produce an expected
failure. No native result or completed scene is claimed by this document.

## Historical non-native validation

```sh
python3 -B -W error::ResourceWarning docs/review/scene-source-assembly-20261116/test_native.py
xcrun swiftc -frontend -parse -D DEBUG -D SS_SOURCE_SCENE_REVIEW AppTests/SourceSceneContinuationTests.swift
```

At 09:53 UTC, **13 portable native guards passed** in 1.167 seconds. They use labeled
synthetic records/images only, never native evidence. Syntax-only Swift parsing also
passed, including the active Debug body. **Full iOS typecheck/build and actual native
execution remain unverified**, reserved for coordinator's slot. The harness is ready
for that compilation, not falsely certified compiled. `native-preparation-tests.log`
retains the initial focused run. No production, project configuration, shared handoff,
CI, commits or pushes were changed.

Final combined portable run at 09:54 UTC: **38 tests passed in 3.402 seconds**,
followed by successful `-D DEBUG` syntax parsing. Retained in
`tests-native-continuation.log`. Actual native import remains unexercised because
there is deliberately no xcresult yet.

## Three-zoom/executable follow-up validation, 10:03 UTC

`tests-three-zooms-final.log` retains **48 passing portable tests in 5.020 seconds**
(25 assembly plus 23 native/provenance guards) and successful active Debug syntax
parsing. New regressions reject missing/duplicate/wrong zooms, staged records,
missing/extra images, wrong projected roots, inconsistent paired roots, old fixture
versions, absent/invalid loaded executable metadata, and stale binary hashes even
when the source-read hash is current. Positive records/binaries are labeled synthetic
fixtures, not native evidence. `blockers-v2.json` retains the current real source gate.
No simulator, xcodebuild, full iOS typecheck or native importer execution occurred.

## Review opt-in/placement-probe validation, 10:07 UTC

`tests-review-optin-placement.log` retains **51 passing portable tests in 5.224 seconds**
and syntax-only parsing in both ordinary Debug and explicitly opted-in Debug modes.
The three new guards check the entire class's compile gate, absence of source
preparation/stepping/rendering dependencies in the placement probe, and both exact
focused commands opting in and selecting only one method. These checks do not claim
that the placement probe executed. Native runs and full iOS typechecking remain
coordinator-owned, and no actual selected Camera root is asserted yet.
