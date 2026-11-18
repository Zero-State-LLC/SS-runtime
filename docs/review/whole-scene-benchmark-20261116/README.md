# Whole-scene benchmark: control and composition diagnostic

**Status: DIAGNOSTIC, NOT A CORRECTION, NOT VISUAL ACCEPTANCE.**

The owner clarified at 04:51:26 UTC on 2026-11-16 that the rejection applies to the whole scene, not only the Camera. This packet compares the existing midpoint control with a composition-only diagnostic. Both use the real GameScene and WorldRenderer, at the +45° ground rotation with 0.5 vertical scale retained.

## Coordinator decisions (04:56 UTC), recorded verbatim in scope

1. No registered replacement building was supplied. `building-constrained.png` is used only as a fallback, and the building remains **NOT SOLVED**. Replacing it requires a canvas, a coordinate convention, an authored root and footprint corners, and a full provenance hash.
2. No muted paving asset was supplied. Narrowing the plaza and adding asphalt is a composition-only diagnostic, and the **paving material mismatch remains open**.
3. Soft contact shadows are deliberately absent. No blurred or procedural shadow art was authored, and no shadow provenance was invented. **Missing soft contact shadows remain open.**
4. The authoritative Camera field geometry and the production HUD are kept as they are. Their prominence is an **open deficit**. The `.paired` field contrast and the zoom levels are diagnostics, not a waiver.

## Fixture

`AppTests/WholeSceneBenchmarkTests.swift` is a new test-only file. It adapts the quiet fixture from `ReferenceProjectionCaptureTests.swift:79-137` and the capture code from `:214-300`. The scene contains:

- the kiosk solid;
- the player at (+160, −50);
- one Camera at integrity 3, with field contrast `.paired`.

Arms:

- **control:** the exact BP001 quiet-street values.
- **diagnostic:** a test-only `BenchmarkReviewArt`. The asphalt patch starts at x = 800 instead of 900, so the dark roadway enters from the right of frame. The cross-street asphalt is extended to y = 600, which narrows the pavement. The curb and rails are shifted to match. The building, paving and prop textures are unchanged.

Views:

- **ORDINARY (primary):** the HUD and Camera field render as normal.
- **STAGED (secondary, clearly labelled):** the HUD nodes are hidden with `isHidden`, and the presentation snapshot sets `fieldVisible = false`. The simulation and authority are untouched; the digest is asserted unchanged for every capture.

Each arm is captured at zoom 1, 1.25 and 1.4, as native, half-size and grayscale PNGs. That gives 36 plates, plus a records JSON with input hashes, the upright actor roots and the open deficits.

No production, input, collision, asset or spec-pin change was made. There was no merge or admission. The approved concept `street-corner-approved-concept.png` (SHA `49aa3544…`) is read-only and is not overlaid on or blended into any plate.

## Run

```bash
xcodebuild -project SSRuntime.xcodeproj -scheme SSRuntime -sdk iphonesimulator -configuration Debug \
  -destination 'platform=iOS Simulator,id=CACB3927-A76E-43A5-9ACA-C389EB38C0C3' \
  CODE_SIGNING_ALLOWED=NO ENABLE_TESTABILITY=YES SS_RENDERER_TEST_CONDITIONS=SS_RENDERER_TEST_SUPPORT \
  -derivedDataPath /Users/appliedalchemylabs/.jcode/scratch/ss-releasevariation-native-derived-20261116 \
  -resultBundlePath /Users/appliedalchemylabs/.jcode/scratch/ss-wholescene-20261116-0458.xcresult \
  -only-testing:SSRuntimeTests/WholeSceneBenchmarkTests test
```

- **Timing:** 04:58:04 to 04:59:07 UTC, 63 s including the build.
- **Result:** `TEST SUCCEEDED`. 1 test passed with 0 failures in 14.9 s, on an iPhone 17 Pro simulator running iOS 26.5.
- **Retained in `capture/`:** 36 plates, `wholescene-records.json`, `summary.json`, `tests.json`, `attachment-manifest.json` and `xcode-test.log`.

## Results

- **Retained control:** `wholescene-control-ordinary-z125-native.png` is 2112×978 with 0 differing pixels against `bp001-reference-trial-20261116/plates/BP001-trial-quiet-street-midpoint-z125-native.png`. Both RGBA SHAs are `863206ea…`. This shows the fixture reproduces the previous control. It is provenance, not visual acceptance. A mismatch would fail verification and report its sizes, pixel count and both SHAs.
- **Diagnostic versus control:** all 6 view and zoom combinations differ. The dark roadway now fills the right of frame and the beige plaza area is smaller.
- **Visual observation, not acceptance:** the saturated two-storey building, the beige repeating plaza texture, weak ground contact with no soft shadows, and the dominant cone and HUD all remain. This diagnostic addresses only roadway placement and pavement width.

## Verification

- `python -B verify_capture.py --exports <scratch>/ss-wholescene-20261116-0458-exports --xcresult <scratch>/ss-wholescene-20261116-0458.xcresult` → `VERIFIED_PROVENANCE_DIAGNOSTIC_NOT_ACCEPTANCE`. It checks:
  - exactly 1 passing test with the expected identity, rejecting zero, failed or skipped runs;
  - the retained summary and test tree equal the live xcresult;
  - the concept hash;
  - 36 plates plus 1 record attachment, with no path escape or duplicates, each byte-equal to its retained copy;
  - the record PNG hashes, input SHAs, the 12-capture census and ordinary/staged labelling;
  - the HUD is present, and all 5 upright roles exist;
  - the status and all 4 open deficits are present and not weakened;
  - plates are non-blank;
  - the control matches the retained plate exactly;
  - the diagnostic differs from the control in all 6 views, and staged differs from ordinary.
- `test_capture_evidence.py` → 8 of 8 tests passed offline with `PATH=/usr/bin:/bin`. It rebuilds the exports from `capture/` and fails if xcrun is called. Its mutation coverage includes a retained-control mismatch that must report `differingPixels`.

## Gallery and coverage matrix

- `index.html` is a portable comparison gallery. It shows three columns: the read-only fixed benchmark, the control and the diagnostic. ORDINARY is selected by default and is the primary view. STAGED is labelled secondary and carries a warning not to judge legibility from it. Controls cover zoom 100/125/140 and the native, 50% and grayscale sheets. The unsolved building, paving, shadows, HUD and field items are listed at the top. `build_gallery.py` builds the gallery and the matrix read-only from `capture/`.
- `coverage.md` is the game-wide coverage matrix, with 17 rows. Each row records whether it is captured or NOT CAPTURED, how it was technically verified, visual status (NOT ACCEPTED for every row) and an evidence path that must exist. Only the quiet and field-off rows cite this packet, and field-off is labelled a staged presentation flag. Dense legal play, occlusion, facings, enemies, effects, UI states, screen sizes, accessibility, live cadence and device are either cited from their own earlier evidence or marked NOT CAPTURED.
- `test_gallery.py`: 5 of 5 tests passed offline. They check all 36 record hashes, ordinary as primary and staged as secondary, the unsolved status and absence of any "solved" claim, the benchmark hash, honest coverage rows with existing paths, NOT CAPTURED rows that cite no evidence, and that a missing evidence path is rejected.
- Actual Brave check: all 18 view/zoom/sheet selections loaded both captures. Measured displayed size is exactly 704×326 for native and grayscale and 352×163 for half. The benchmark is normalized to 704 or 352 px wide with its 1672×941 aspect preserved, and CSS grayscale is applied to it in grayscale mode without changing its bytes. No errors and no page overflow; each panel scrolls locally. The gallery links to `../visual-acceptance-20261116/CONTRACT.md`.
- **Verifier scope (honest):** the records sidecar hashes only the 5 upright test PNGs (player, camera, building-constrained, newsbox, tree). It does NOT hash `env_ground_plaza`, `env_ground_asphalt` or the full Camera candidate frame family. Those are reported as `unboundInputs`, and this packet makes no full runtime-input attestation. The verifier checks exactly the 4 open-deficit strings, the 5 role names, the 3 sheet suffixes, the native size of 2112×978 (704×326 points at 3×), half at 1056×489, true grayscale plates, matching names and labels, and that staged differs from ordinary in both arms.
- All 36 plate bytes were unchanged after the gallery build (sha256 list compared before and after).
- The new stone facade from the coordinator is NOT integrated. Its 1254² canvas and visible slopes differ from the requested footprint, and registration is pending.

## Limits and gaps

- These are static captures. They are not live cadence, dense play or device evidence.
- The xcresult does not embed the Swift test source or `project.yml`. Their current hashes are reported, and they were unchanged after the passing run.
- Owner visual review is still required. Byte identity is provenance only.
