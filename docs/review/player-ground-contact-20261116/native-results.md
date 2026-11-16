# Native constrained comparison (static renderer, not live display)

Active run: attempt 03, after the runtime#238 correction. Earlier attempts are kept in `attempts/`. Attempt 01 is invalid because its fixed-time selection froze. Attempt 02 failed on an arbitrary assertion I had added.

## Exact command (bounded, focused, fresh result path)

```bash
xcodebuild -project SSRuntime.xcodeproj -scheme SSRuntime -sdk iphonesimulator -configuration Debug \
  -destination 'platform=iOS Simulator,id=CACB3927-A76E-43A5-9ACA-C389EB38C0C3' \
  CODE_SIGNING_ALLOWED=NO ENABLE_TESTABILITY=YES SS_RENDERER_TEST_CONDITIONS=SS_RENDERER_TEST_SUPPORT \
  -derivedDataPath /Users/appliedalchemylabs/.jcode/scratch/ss-releasevariation-native-derived-20261116 \
  -resultBundlePath /Users/appliedalchemylabs/.jcode/scratch/ss-groundcontact-native-20261116-0428-looped.xcresult \
  -only-testing:SSRuntimeTests/PlayerGroundContactNativeTests test
```

- **Run:** 04:27:22 to 04:29:01 UTC, about 99 s including the build, under a 540 s tool cap.
- **Result:** `TEST SUCCEEDED`. 1 test passed with 0 failures in 56.432 s, on an iPhone 17 Pro simulator running iOS 26.5.
- **Files kept from the xcresult:** `native/summary.json`, `native/tests.json`, `native/native-records.json`, and 76 PNG captures. Exports are in `<scratch>/ss-groundcontact-native-20261116-0428-looped-exports`.

## Correction (runtime#238)

Fixed-time frame selection is now `frameIndex(atTickOffset: (tick - start) % durationTicks(at: 60))`. The cycle is 30 ticks, matching `ClipTiming`'s own duration rule. `frameIndex` clamps by design, as the Trail learning notes, so the wrap is required.

The XCTest now checks all 16 groups (trace × policy × family):
- all 16 frames are selected;
- the cycle wraps at least once;
- every fixed-time frame equals `(offset % 30) * 32 / 60`;
- each pause tick holds exactly one pose, over a hold of at least 15 rows.

A frozen control fails these checks. The test also records the SHA-256 of all 24 bundled resources as they were read at run time.

## Results: native-scene support span (logical px, no threshold)

| Input | Fixed-time (looped) | Distance-phase |
|---|---:|---:|
| Quarter | 9.128693 | 3.964478 |
| Half | 6.300262 | 3.813721 |
| Full | 3.106598 | 3.106598 |
| Pause (full + 15-tick hold) | 3.106598 | 3.106598 |

- Baseline and weight-transfer are identical in every cell, because the feet are preserved.
- Counts: 2,400 samples, 116 planted segments and 76 captures. Attempt 01 had only 54 segments because frozen frames merged its segments.
- With the fixed-time control now valid, distance-phase reduces modeled slip at quarter input (9.13 to 3.96) and at half input (6.30 to 3.81), and is equal at full input.
- The fixed-time maxima are close to attempt 01's. The freeze happened after support had already been sampled, so this agreement is coincidental. The attempt 01 values remain invalid.
- This is evidence for a comparison, not an adopted policy.

## Exclusions (no walking contact fabricated)

| Trace | Rows excluded |
|---|---:|
| cardinal-quarter | 316 |
| cardinal-half | 166 |
| cardinal-full | 91 |
| collision-stop | 91 |
| wall-slide | 91 |
| reversal | 91 |
| dodge | 91 |
| stationary | 91 |

These are excluded because the movement is not toward south, it is a dodge, or the Player is not moving.

## Independent numeric reconstruction

`verify_native.reconstruct` rebuilds every row from the snapshot whole-unit position and the bundled pose landmarks, without using the recorded root or contacts:

- **Root:** midpoint projection around (736, 654) to (352, 163).
- **Contact points:** root plus (toe.x, −0.5·toe.y).
- **Segments:** the planted-segment boundaries and each maximum pairwise span.

It then checks the recorded `projectedRoot`, the contacts, the segment order, side and sample counts, and every span. Roots and contacts must match within 0.002 px. This is the same Float32 bound the XCTest asserts, not an acceptance threshold. Spans must match within 0.004 px.

## Portable offline tests

`test_native_evidence.py` runs without xcrun, a simulator or the external scratch folder. It rebuilds the xcresult export layout in a temp folder from the retained `native/` files and `native/attachment-manifest.json`, which is a copy of the real export manifest. The summary and test tree come from the retained `native/summary.json` and `native/tests.json`. One test patches `subprocess` to fail if xcrun is ever called.

Result: 14 of 14 tests passed in 31.4 s, with `PATH=/usr/bin:/bin`.

The live CLI, `verify_native.py --exports --xcresult`, is separate. It still queries the real bundle and requires the retained JSON to equal it, and it passed against the 0428-looped result. The new mutation coverage includes:

- a shifted projected root and an inconsistent snapshot position;
- a moved contact point and a changed segment span;
- a changed segment sample count and swapped segment sides.

## Swift comment mismatch (no code change after passing run)

In `AppTests/PlayerGroundContactNativeTests.swift`, the comment "recover scene pixels via the actual tree" is inaccurate for contacts. The root is converted through the actual SpriteKit tree, but contacts are then computed arithmetically from that root and the pose landmarks. The verifier reconstruction above independently checks that arithmetic. I left the Swift unchanged so the source still matches the passing run.

## Guards

- Approved releases 5/13 (zero-based 4/12) are hash-checked and byte-identical in both families.
- The 6 candidate keys (06–08 and 14–16) are pinned by SHA and differ from baseline.
- Native image pairs: 33 changed, all on changed keys, and 5 identical, all on unchanged keys.

## Portable verification

Run `python -B verify_native.py --exports <scratch>/ss-groundcontact-native-20261116-0428-looped-exports --xcresult <scratch>/ss-groundcontact-native-20261116-0428-looped.xcresult`. The verifier adapts `scripts/import_release_variation_native.py`. It checks:

- The live xcresult summary and test tree show exactly 1 passing test with the expected identity. `native/summary.json` and `native/tests.json` must equal them.
- The attachment census is exactly 76 captures plus 1 record attachment, with no path escape or duplicates. Every retained file is byte-equal to its attachment.
- Approved 5/13, the candidate keys and the core-trace hashes match. All 24 run-time SHAs equal the current source files.
- The recorded capture count is 76 and the loop declaration is present.
- All 2,400 rows match core tick, Q8 position, texture identity, quantization and planted sides. Both policies' frames are recomputed independently.
- Every group selects all 16 frames and wraps at least once.
- 116 segments; the 8 exclusions with their row counts.
- Crops are 480×330 PNG and not flat; 33 pairs changed and 5 unchanged.

`test_native_evidence.py` runs 12 tests, all passing, in 25.6 s on real evidence. They cover the actual pass case and these rejections:
- attempt 01 rejected by its frame selection alone (counts padded so only selection can fail);
- a frozen fixed-time row, a missing loop declaration and a wrong capture count;
- zero, failed or skipped runs, and a wrong test identity;
- changed attachments or retained summary, a path escape, missing or duplicate captures;
- changed source hashes or run-time bundled bytes;
- wrong counts or exclusions, an invented threshold or status;
- wrong selection, texture, position, tick, contacts or quantization;
- a changed/unchanged pair mismatch, and blank or wrong-size crops.

## Limitations and gaps

- The renderer draws whole-unit snapshot positions, up to 0.996 units behind Q8 (truncation). The native span includes this.
- These are static explicit renders, not SKView callback cadence. They are not live-cadence, Reduced Motion or device evidence.
- Frame selection is the test-side override, not production clip playback.
- South facing only. Partial-input policy, owner visual review and admission remain open.
- Provenance gap: the xcresult does not embed the Swift test source or `project.yml`. The run-time SHAs bind the bundled resources. The test file and configuration are bound by current hashes and were unchanged after the passing run.
