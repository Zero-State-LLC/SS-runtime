# Player south ground contact, slice2

Status: actual core trace, source proposal and corrected static native comparison. The first native fixed-time control was invalid because it clamped instead of looping (runtime #238); it is preserved as rejected evidence. The fresh0428-looped xcresult independently reports1 passed,0 failed,0 skipped. This is not live displayed contact or cadence evidence. No visual acceptance, controller change, production asset, pin or merge.

## What changed

- `Tests/SurveillanceCoreTests/PlayerGroundContactTraceTests.swift` executes public `Simulation.step` twice for12 scenarios: diagonal quarter/half/full, cardinal quarter/half/full, collision stop, wall slide, reversal, dodge, no-step pause and stationary. Setup uses existing test-only placement/solid hooks. The Python analysis never reimplements movement, normalization or collision.
- `build_source.py` reruns the recovered editable paint/mesh assembly from `/Users/appliedalchemylabs/Documents/Codex/2026-10-13/can/outputs/SS-player-bounded-proportions/` in this packet. Original inputs remain read-only and1,012 hashes stay unchanged.
- Proposal: lower recovery pelvis rise by at most0.6 source units in keys06–08 and14–16, then solve knees with the existing fixed12.5/14.5 solver. All heel/toe/ankle targets, contacts, timing, costume layers, the0.5s cycle, existing0.375s settle and approved release5/13 are unchanged. It adds no bounce or cadence.

## First trace failures

Measured from actual Q8 core travel plus exported south toe landmarks. These are not native displayed-pixel results or thresholds.

| Input | Fixed-time support drift | Distance-phase support drift |
|---|---:|---:|
| Quarter diagonal | 8.750267 logical px | 3.500427 logical px |
| Half diagonal | 6.250534 logical px | 3.498825 logical px |
| Full diagonal | 2.748505 logical px | 2.498932 logical px |

The legal cardinal route meets real arena geometry after76–78 travel units. The held south source on cardinal, slide and reversal exposes a missing-facing problem, not a valid south contact. Isolated collision stop excludes zero-motion walk samples. Dodge rows are excluded so no walking contact is fabricated.

Proposed correction: the source change targets weight transfer only. Because feet are preserved, it cannot reduce modeled slip. The evidence favors comparing native distance-phase partial-input selection next. No policy is selected or adopted here.

## Review

Open `normal-speed.html` and the separate `quarter-speed.html`. Both draw the actual core trajectory with unchanged versus proposed painted source frames, plus a grayscale option.

## Validation

- `swift test --filter PlayerGroundContactTraceTests`: one XCTest passed in49.392s. Twelve scenarios reproduced exact rows and final digests. See `core-test.log`.
- `test_packet.py`: twelve independent tests passed. They check original hashes, exact unchanged keys, exactly six changed keys, limb lengths, foot targets, retained costume, manifest drift, real core coverage, projection inverse, nonwalking exclusion and all exported page rows. See `packet-tests.log`.
- Actual Brave checks (local file pages): both pages became ready. Each page passed120 scenario/phase/scrub checks plus Play/Pause/grayscale. Neither page reported a loader error or horizontal overflow. A screenshot confirmed painted source art. Browser timing is not cadence evidence.

## Native constrained comparison (static)

See `native-results.md` for the corrected run and `native-pairs.html` for38 paired retained captures. The actual Brave gallery passed228 pair/size/grayscale checks against the fresh captures at04:32UTC, with no loader failure or horizontal overflow. The Node regression harness also verifies all38 pairs plus missing/empty-image failure and stale-load isolation. These checks validate the review interface, not displayed playback.

## Open gates

The first static native run remains invalid history: `ClipTiming.frameIndex` clamped after the first cycle. The corrected run wraps by the authored30-tick cycle and independently checks all16 frames and repeat-cycle selection, while preserving pause holds. Runtime #238 remains open until the verified correction is published and its integration checked. Source landmarks transformed into native scene coordinates are not measured contact pixels. The existing `DisplayedPlaybackTests` capture and issue#237 remain unchanged. Normal/quarter owner review, cardinal/east/west facings, partial-input policy, live cadence, device and production admission all remain open.

## Independent corrected-native verification, November16 04:38UTC

Direct `xcresulttool` inspection of `ss-groundcontact-native-20261116-0428-looped.xcresult` reports exactly1 passed,0 failed,0 skipped. The live `verify_native.py` independently matches retained records and all76 captures against actual exports, validates24 runtime-recorded bundled-resource hashes, reconstructs all2,400 selected samples and116 planted segments, and confirms33 changed/5 unchanged image pairs. The resulting hash inventory is retained in `native/coordinator-verification.json`. Source/configuration hashes are post-run observations, not embedded binary-source attestation.

Fourteen portable mutation tests passed without calling xcrun. They reject the original freeze, shifted roots/contacts, changed segment spans/counts/sides, changed source/attachment bytes and false run summaries. The portable suite uses retained real artifacts to test the verifier, while only the separate live CLI proves equality with the local xcresult. The failed0425 run was independently inspected: its newly introduced frame-dominance heuristic incorrectly rejected a valid paused pose. The replacement asserts exact pause-hold behavior and preserves all16-frame coverage and loop checks. No existing production or playback assertion was weakened, and#237 is unchanged.

## Independent coordinator verification, November 16 04:10 UTC

The focused real-core test passed again (1 test, 0 failures, 14.973s), and its newly exported twelve traces byte-match `core-traces.json`. No unfiltered Swift run was attempted. All thirteen packet tests passed against the external originals, including all1,012 unchanged hashes and equality to the previously published inventory. Portable execution with an absent external source root passes twelve checks and explicitly skips only the full external-master audit; copied source, costume and baseline bytes are still checked against the archived inventory.

Actual Brave normal and separate quarter pages each passed120 scenario/policy/scrub selections and Play/Pause/grayscale controls with no loader error or horizontal overflow. The real xcresult summary reports1 passed test,0 failed,0 skipped. Native provenance hardening and publication are tracked separately. These technical checks do not select a partial-input policy or accept the proposed recovery motion.
