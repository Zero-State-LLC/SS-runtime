# Native constrained comparison (static renderer, not live display)

Focused test: `AppTests/PlayerGroundContactNativeTests.swift`, the only test selected (`-only-testing`). xcresult: `/Users/appliedalchemylabs/.jcode/scratch/ss-groundcontact-native-20261116-0348.xcresult`. Result: 1 test passed, 0 failures, 54.425 s. Simulator: iPhone 17 Pro, iOS 26.5. Log: `native-xcode-test.log`.

## What the test does

For each case it replays the actual core commands through `GameSession.step`. It asserts that every tick, every Q8 position and the final digest match `core-traces.json`. It then calls the real `WorldRenderer.render`, inside the midpoint ground tree (rotate +45 degrees, then y-scale 0.5). The art stays upright at the projected root. The test checks that the clip token is `player_move|s`. It then applies the candidate frame through the same explicit texture override the vetted distance-phase harness uses. The test asserts identity for:

- the texture
- the 64×69.333 size
- the root anchor
- the projected root

Contact points come from the bundled `player-source-s-poses.json`, with SHA `376fa7ad...` verified.

Coverage:

- 4 valid traces: quarter, half, full and pause.
- 2 selection policies: fixed-time and distance-phase.
- 2 source families: baseline, and the weight-transfer candidate (6 changed keys).
- 2,400 sample records, 54 planted segments and 76 crop PNGs, all in `native/`.

Excluded, with no walk contact fabricated:

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

## Measured native-scene support span (logical px, no threshold)

**Correction (verifier, 04:09 UTC):** the native fixed-time column is INVALID. The test selected fixed-time frames through `ClipTiming.frameIndex`, which clamps at the last frame and does not loop. After 30 ticks every fixed-time row froze on frame 15. That affects 900 of the 1,200 fixed-time rows. The fixed-time spans in the earlier slice2 report (9.128662 / 6.300262 / 3.106598) therefore measure a mostly frozen pose and must not be used. The source-model fixed-time numbers in `first-findings.md` loop correctly and are unaffected. A corrected native fixed-time run needs a new simulator run and coordinator agreement.

| Input | Distance-phase (valid) | Fixed-time (native) |
|---|---:|---|
| Quarter | 3.964478 | invalid, frozen |
| Half | 3.813721 | invalid, frozen |
| Full | 3.106598 | invalid, frozen |
| Pause (full + 15-tick hold) | 3.106598 | invalid, frozen |

The baseline and the candidate are identical in every distance-phase cell, as designed, because the feet are preserved. Because the native fixed-time data is invalid, these results alone do not establish that distance-phase is better than fixed-time natively. Only the source-model comparison supports that.

## Portable verification

Run `python -B verify_native.py --exports <scratch>/ss-groundcontact-native-20261116-0348-exports --xcresult <scratch>/ss-groundcontact-native-20261116-0348.xcresult`. The verifier adapts `scripts/import_release_variation_native.py`. It checks:

- The xcresult summary and test tree show exactly 1 passing test with the expected identity. Zero, failed, skipped and expected-failure runs are rejected.
- The attachment census is exactly 76 captures plus 1 record attachment, with no path escape and no duplicates.
- Retained `native/` files are byte-equal to the xcresult attachments.
- Approved keys 5/13, the bundled candidate keys and the bundled core traces match their source hashes.
- Every one of the 2,400 rows matches the core tick, Q8 position and texture identity. The quantization is recomputed. Planted sides match the pose landmarks.
- Distance-phase frames are recomputed independently. The fixed-time frozen-row defect census is pinned at 900.
- 54 segments, and the 8 excluded scenarios with their row counts.
- Crops are 480×330 PNG and not flat. Exactly 33 pairs changed and 5 unchanged, consistent with the changed-key set.

`test_native_evidence.py` runs 9 tests, all passing, on real evidence. They cover the actual pass case and deliberate mutations of the result, attachments, census, path escape, source hashes, counts, selection, identity, quantization, contacts and pairs.

Gaps:

- The verifier checks the current bytes of the native test, configuration and resource files. The xcresult does not embed the source-file bytes, so binding them to the executed build depends on the files being unchanged since 03:48 UTC. There were no edits after the passing run.
- `project.yml` is hashed but is shared.

## Guards

- Approved releases 5/13 (zero-based 4/12) are hash-checked and byte-identical in both families.
- The 6 candidate PNGs (06–08 and 14–16, zero-based 5–7 and 13–15) are SHA-pinned and differ from baseline.
- Pixel check of the native crops: 33 baseline/candidate pairs differ, all on changed keys. 5 pairs are identical, all on unchanged keys. No mismatch.

## Observed limitations

- The renderer consumes whole-unit `PresentationSnapshot` positions. The Q8 value minus the snapshot value reached 0.996 units, which shows truncation, not rounding. My first assumption of 0.5 or less failed and was corrected to a "less than 1" bound. The native span includes this quantization. That explains the difference from the source-model numbers (8.75 / 6.25 / 2.75).
- Static explicit renders with no SKView callback cadence. This is not displayed-playback, live-cadence, Reduced Motion or device evidence.
- Frame selection is the test-side candidate override, not the production clip action.
- Only south. Other facings, partial-input policy, owner visual review and admission all remain open.
