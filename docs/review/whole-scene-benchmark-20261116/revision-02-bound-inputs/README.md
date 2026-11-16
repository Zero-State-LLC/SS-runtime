# Slice1 baseline: fresh revision02 bound-input capture

**Technical evidence only. Visual NOT ACCEPTED. No production admission, source replacement or gameplay change.** Authority: SS-specs d1bfd1c, accepted `intent/2026-11-16-benchmark-faithful-ten-slices.md`, slice1. See [visual acceptance contract](../../visual-acceptance-20261116/CONTRACT.md).

[Portable gallery](index.html). ORDINARY is primary with production HUD and authoritative Camera field. STAGED is secondary art-only with both suppressed, not a gameplay field-off event. This remains a quiet static SpriteKit fixture, not live cadence, physical-device or encounter coverage. [Existing coverage matrix](../coverage.md) is not expanded by this capture.

## Fresh evidence, not retroactive attestation

Revision01 benchmark (36 plates) and paving (18 plates), including their executed Swift fixtures, remain unchanged. Their five-PNG sidecar did **not** bind runtime plaza/asphalt or the complete Camera candidate frame family. Revision02 does not repair that historical gap by assertion. It executes a new dedicated `AppTests/WholeSceneBoundInputsTests.swift` fixture and loads/hashes actual bundled source bytes at runtime: two runtime ground assets, all sixteen Camera candidate frames and six upright inputs including the muted paving trial. Runtime-loaded source asset bytes, actual roots, records and attachments are retained and checked. The native test asserts that the simulation digest remains unchanged, but does not serialize that digest in the record. The retained xcresult summary/tree identify the focused test and configuration. The importer does **not** cryptographically bind all executed Swift/build inputs or the full configuration: its two Swift hash guards protect the original revision01 fixtures against current-file changes, not an embedded build-source attestation. Hashes establish bounded asset provenance, not complete build provenance, quality or acceptance.

The fresh 54 plates comprise whole-scene control and diagnostic, ordinary and staged, plus ordinary paving plaza and muted arms, each at zoom 1/1.25/1.4 and native/half/grayscale. There are 18 capture records and 55 attachments including records. All 54 RGBA images match their corresponding revision01 plate exactly. This is an independently checked output comparison, not a claim that the earlier run bound these inputs.

## Exact execution and provenance

Passed focused XCTest: `WholeSceneBoundInputsTests/testBoundInputsRevision02`, **1 passed, 0 failed, 0 skipped**, 22.582 seconds, approximately 56 seconds command wall time. No new simulator execution is needed for offline verification.

Actual result: `/Users/appliedalchemylabs/.jcode/scratch/ss-wholescene-r02-20261116-0601.xcresult`

Actual exported attachments: `/Users/appliedalchemylabs/.jcode/scratch/ss-wholescene-r02-20261116-0601-exports`

```sh
xcodebuild -project SSRuntime.xcodeproj -scheme SSRuntime -sdk iphonesimulator -configuration Debug -destination 'platform=iOS Simulator,id=CACB3927-A76E-43A5-9ACA-C389EB38C0C3' CODE_SIGNING_ALLOWED=NO ENABLE_TESTABILITY=YES SS_RENDERER_TEST_CONDITIONS=SS_RENDERER_TEST_SUPPORT -derivedDataPath /Users/appliedalchemylabs/.jcode/scratch/ss-releasevariation-native-derived-20261116 -resultBundlePath /Users/appliedalchemylabs/.jcode/scratch/ss-wholescene-r02-20261116-0601.xcresult -only-testing:SSRuntimeTests/WholeSceneBoundInputsTests/testBoundInputsRevision02 test
```

`capture/summary.json`, `tests.json`, `attachment-manifest.json`, `r02-records.json`, all PNGs and `xcode-test.log` retain the result identity and provenance. `verify_capture.py --exports <actual exports> --xcresult <actual result>` queries the live xcresult and rejects zero tests, wrong identity, changed bound asset hashes, changed labels/census/roles/dimensions, altered attachments and changed original fixtures. Test/configuration identity comes from the retained and live xcresult fields, not a complete source/configuration hash attestation. `test_capture_evidence.py` reconstructs temporary exports from retained attachments and uses retained summary/tree, requiring no xcrun, simulator or external scratch evidence on Linux. Negative mutations are mandatory, not visual thresholds.

## Failed attempt retained

`attempts/01-loader-scale-mismatch/xcode-test.log` preserves the initial failed run. `UIImage(data:)` ignored the Camera filename's @4x scale, yielding a 256x384 texture rather than the existing helper's 64x96 logical size. The dedicated harness was corrected to `UIImage(contentsOfFile:)` while hashing those exact source file bytes. The original fixtures and source pixels were not changed. The successful run uses a fresh xcresult path. This is a loader-equivalence assertion correction, not weakened coverage.

## Final portable and live validation

2026-11-16 06:17 UTC: `/Users/appliedalchemylabs/Developer/video-use/.venv/bin/python -m unittest -v test_capture_evidence test_color_threshold` passed **10 tests in 15.591 seconds**. This includes seven evidence mutation/identity tests plus the coordinator's exact 64/65/final-pixel color-threshold regressions. The CLI against the actual 0601 xcresult/exports returned `VERIFIED_BOUND_INPUTS_REVISION02_NOT_ACCEPTANCE`, 54 plates, 18 captures, 2 runtime assets, 16 Camera frames, 6 upright inputs and 54 revision01 pixel-equal images with zero mismatches. Combined command finished in 24.4 seconds. No simulator rerun.

06:18 UTC: `python -m unittest -v test_gallery` passed **3 tests**. Actual Brave browser measurements separately loaded all **54 selections**, found zero errors, measured native/grayscale 704x326 and half 352x163, preserved benchmark aspect and checked grayscale and document overflow at viewport width1200. `browser-validation.json` is a retained observation, not a substitute for rerunning a browser. Both old Swift SHA guards passed. A checksum check from `docs/review/` confirmed **64 original capture/evidence files unchanged**, including all54 original plates.

Coordinator independently corroborated the original benchmark suite as **14 tests (8 evidence + 6 gallery)**, original paving as **7 tests**, and this revision02 as **13 tests (10 evidence/color + 3 gallery)**. These are separate suite totals, not additional native captures.

## Remaining deficits and limits

- Building **NOT SOLVED**: constrained fallback remains. No registered stone replacement integrated.
- Muted paving is a trial only, no source repair. Opposite-edge RGB mean absolute difference is about 13 to 14/255, not mathematically seamless. Seam/repetition and material coherence remain open.
- Soft contact shadows absent: none supplied, none authored. No procedural shadow substitute.
- Production HUD and authoritative Camera cone prominence retained and open. No hidden gameplay legibility claim from staged plates.
- Player/Camera/building source coherence is not accepted. Static quiet plates do not establish movement, enemies, damage, UI-state, accessibility, live cadence or physical-device quality.

Native plates are 2112x978 pixels, half plates 1056x489. Gallery display is 704x326 native/grayscale and 352x163 half within locally scrollable panels. Benchmark original 1672x941 preserves aspect and is width-normalized, with different framing explicitly labelled. Grayscale reference is a CSS filter, not a source edit.
