# Player startup and renderer review — 2026-10-15

## Result
Candidate renderer preparation now builds initial scene nodes, prepares outlines and preloads textures before timed playback. Two initial display callbacks keep simulation at tick zero before its clock starts. This fixes the reproduced startup catch-up in the benchmark fixture; it is not yet a shipping startup integration or device-performance certification.

Final Xcode run: 110 named tests / 112 executions passed, zero failures. All strict full-, half-, quarter-input and Reduced Motion captures observed all 16 frames. Outline readbacks during playback: zero. Five ClipTimingTests also passed. The unchanged core suite previously passed 773 tests across 109 suites; that full suite was not rerun this turn.

## Measurements
Stage 3 controls had first callback gaps of 271.62 and 293.47 ms. Prepared stage 4 had first live gaps of 16.67–22.42 ms across six captures. Preparation took 622–728 ms, including scene construction of 215–277 ms; initial display readiness additionally took 36–50 ms. Preparation remains visible startup cost rather than disappearing work. Later callback maxima remained 43–61 ms, so smooth 60 fps is not established.

Prior unrecorded run passed coverage but had a 1.44-second initial gap; this prompted the final readiness change. The recorded run had a Reduced Motion coverage failure (14/16); subsequent unrecorded runs passed. This evidence is retained; recording overhead has not been isolated as the sole cause.

## Separate visual reviews
- normal-speed.html: actual simulator/SpriteKit recording, normal speed.
- quarter-speed.html: same recorded frames at quarter speed, no interpolation.
- Both offer detail crop and full viewport. Review foot contact, knee-pad orientation, heel/tongue ownership, calf and boot detail, coat overlap, arm motion, and the repeated 16→1 transitions inside the clip. The movie's outer loop boundary is not a gait seam.

The footage predates the final readiness adjustment but uses the same animation assets, registration, outline and movement. The latest startup result is supported by test telemetry, not a new recording. Only the south-facing candidate walk is represented; candidate idle art is absent and the isolated player disappears at the end. Current outline remains for comparison. This is not the shared benchmark scene.

## Scope and next gate
Changes remain local. Runtime production assets are not admitted. Keep narrower stance, arm swing and restored knee-pad detail. Await normal-speed and separate quarter-speed contact/seam review before shared-scene work. Hidden surfaces, dimensions and amplitudes remain proposed. Physical-device testing and broader directional/idle coverage remain open.

## Evidence
- ready-test-summary.json: final Xcode summary.
- ready-evidence/comparison.json: final measured comparison and per-frame costs.
- visible-test-summary.json and visible-evidence/: recorded-run results, including failure.
- final-test-summary.json and final-evidence/: preceding unrecorded result with startup outlier.
- timing-tests.log: five timing tests.
- visible-renderer.mov: continuous original recording; review MP4s are timestamp-preserving crops/extracts.
