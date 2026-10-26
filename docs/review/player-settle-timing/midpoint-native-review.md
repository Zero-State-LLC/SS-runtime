# Proposed midpoint native review

Latest owner feedback rejects 0.25 seconds as too abrupt; the earlier 0.5 seconds was too slow. The authored 0.375-second midpoint remains proposed.

Recording run: 1 test, eight Standard/Reduced Motion variants, zero failures, 32.735 seconds. Rational-timing cancellation regression: 13 triggers, zero failures. The prior full 20-test pass predates the timing representation change and is not claimed as a full rerun of this version.

Native Standard Motion clips are in outputs/SS-player-settle-timing, named native-midpoint-phase-05 and -13, each at normal and quarter speed. Review pages: midpoint-normal-speed.html and midpoint-quarter-speed.html. Phase 5 preserves 133 frames per speed; phase 13 preserves 139. Relative timestamps scale by four within one microsecond. First/last frames visually checked: backed player texture to neutral, without menu/setup fallback. The black simulator device cutout is capture UI, not game art.

No production default, asset-family admission, or device acceptance is implied. Next gate: normal-speed timing and separate quarter-speed contact review.

## Coverage limitation

Recording telemetry observes13/17 poses for release5 (missing zero-based5,6,10,13) and16/17 for release13 (missing8). Reduced Motion correctly bypasses settling. See midpoint-recorded-pose-coverage.json and its reproducible analyzer. Video frame preservation does not establish authored-pose coverage. These videos support timing review; complete contact inspection still needs native frame-step/all-pose evidence.

Follow-up verification: specs validator passes23 JSON artifacts/7 schemas/33 registered contracts/55 indexed files; specs diff whitespace check passes. Full core tests launched with `swift test --disable-sandbox` after nested SwiftPM sandbox initialization failed in the execution environment. Completed successfully: 779 tests in110 suites,372.949 seconds, exit0. Archived output: midpoint-core-tests.log. This verifies core behavior, not the new iOS native frame-step capture test.

Native pose diagnostic: testMidpointSettleNativePoseInspection selects every midpoint pose at its first eligible60Hz tick, verifies backed texture identity and root/size/anchor, and attaches17 SpriteKit offscreen renders per release phase. It is intentionally static, isolated evidence, not a real-time capture or shared-scene occlusion proof. Full DisplayedPlaybackTests run launched in Xcode at approximately16:18 local; source/asset hash inventory: native-pose-suite-inputs.json. Outcome pending.

First native-pose attempt failed before rendering: SpriteLibrary benchmark initializer requires delivered-path keys to equal provided texture keys; the new fixture incorrectly included15 intermediate settle textures as catalog delivery. Corrected setup supplies entry/idle only to the catalog; all17 textures remain in the settle sequence and preload/outline preparation. No assertions removed or weakened. Current full-suite result is the pre-correction compiled binary recorded in native-pose-suite-inputs.json; correction requires a separate focused run.

## Final native pose inspection — 2026-10-19

- Core:779 tests in110 suites passed (372.949s), archived in midpoint-core-tests.log.
- Full playback:21 tests,20 passed; new static diagnostic failed fixture setup before capture (361.964s). Existing20 playback tests passed against rational midpoint timing. Source inventory: native-pose-suite-inputs.json. Result: native-pose-full-suite-result.json. This is not reported as a clean full-suite run.
- Focused diagnostic fixes: catalog delivered-key mismatch corrected; Float storage representation asserted exactly; scene-root framing replaced by node-local crop; outline hidden using the same review-only treatment as SharedTraversalScene. No production behavior or cadence changed.
- Final focused test passed:1 test,0 failures,6.728s. Result native-pose-clean-result.json;34 images and two pose records in native-pose-clean-attachments. Earlier failed and poorly framed captures remain separate evidence, not the review deliverable.
- Final viewer: outputs/SS-player-settle-clean-pose-review/index.html. Both17-pose plates visually inspected: complete body visible, no crop clipping or white outline. These are static native captures of the two existing source-backed stops, not full-family acceptance, projected-world contact proof, or normal-speed delivery proof.
- Apple documents texture(from:crop:) rectangles in the rendered node's coordinates: https://developer.apple.com/documentation/spritekit/skview/texture%28from%3Acrop%3A%29 . Capturing renderer.root avoids the observed SKScene scaling in this diagnostic.

Next: review proposed0.375s cadence alongside these all-pose captures; resolve moving contact and remaining release/interruptions before four-facing production. Timing remains unapproved.
