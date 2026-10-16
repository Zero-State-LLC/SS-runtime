# Step 2 — real-renderer animation validation

2026-10-15 · **FAILED / shared-scene gate remains open**

The approved knee-pad-detail source is now installed in the test-only candidate bundle. All 16 PNGs are byte-identical to `SS-player-kneepad-detail/frames`; stance, arm swing, source poses, canvas, anchor, draw size and authored half-second timing are preserved. Production art and gameplay remain unchanged.

## What ran

WorldRenderer + SpriteLibrary + GameSession in a presented SpriteKit scene on iPhone 17 Pro simulator, iOS 26.5. Viewport 704×326; source 384×416; draw 64×69⅓; anchor (0.5, 1−336/416); ground Y projection 0.5 with upright-art compensation. Seed 1; test initial position (224,704); south input for 120 fixed ticks, then idle through tick 150. Quarter/half/full input and full-input Reduced Motion were captured independently. The simulation preflight verifies movement on every tick through the existing arena, without changing solids or speed.

The measured interval no longer extracts screenshots. Each record comes from `didEvaluateActions`, identifies the actual selected texture, and includes simulation tick, authoritative/projected position, camera position, view scale, dimensions and anchor. The final run includes the game’s post-action outline synchronization. This is renderer telemetry, **not continuous video or a device-performance measurement**.

## Final results

| Run | Displayed distinct frames | Observed frame-index wraps | Largest display interval |
|---|---:|---:|---:|
| Full input | 6 / 16 | 3 | 320 ms |
| Half input | 7 / 16 | 3 | 300 ms |
| Quarter input | 8 / 16 | 4 | 941 ms |
| Full input, Reduced Motion | 6 / 16 | 3 | 300 ms |

All four candidate tests fail the unchanged requirement to actually display all 16 frames. Travel, geometry, south-facing selection, repeated frame-index wraps and final idle assertions pass. No recorded moving tick lost the candidate. Wraps do not establish smooth seams or complete cycles: omitted intermediate frames remain a failure.

- Core: `swift test --disable-sandbox`, exit 0; **773 tests / 109 suites passed**, 589.811 seconds.
- Simulator final result: **106 passed executions, 4 failed executions** (104 passed named tests, 4 failed named tests; one test has three parameter cases).
- `git diff --check`: passed. All 16 test candidate PNGs match the reviewed source byte-for-byte.
- Result bundle: `Test-SSRuntime-2026.10.15_13-36-19--0700.xcresult`; writable retained copy in `work/player-step2-final.xcresult`.

The first attempt had a missing `dodgePressed: false` test-constructor argument, corrected before execution. The first executed run is retained in `first-run/`: 9–11 frames observed. Its Reduced Motion expectation incorrectly demanded one static frame. D-069 permits self-referencing locomotion clips, so the final test requires all 16 frames and repeated playback for this mode too. No gameplay behavior was changed to satisfy the test.

## Contact / seam evidence

`analysis.json` combines source toe annotations with observed texture identities and actual projected positions. Most support groups contain only one observation; their displacement is **null**, not zero. The few multi-sample groups do not establish complete planted phases. Foot slip and the 16→1 seam are therefore **not validated**. Displacements are reported in projected scene units, ground-equivalent units (inverse 0.5 Y projection, fixed contact height assumed) and equivalent output pixels. This is annotation-based analysis, not pixel tracking. No acceptance tolerance is invented.

## Findings and next work under runtime #132

1. **Instrument cold and warm renderer paths separately.** `OutlineTextures.outline` calls `texture.cgImage()` on a cache miss; `WorldRenderer.renderActors` synchronizes outlines, and the game also synchronizes after SpriteKit actions. Removing screenshot readback did not remove this renderer readback. It is a concrete candidate cause, not yet a measured attribution. Measure simulation, render, outline miss/hit and post-action cost before choosing a fix. Include fixture registration/size changes in that investigation.
2. **Eliminate the measured stall source while preserving actual frame coverage.** Do not slow the clip, skip outlines, relax the assertion or alter controller speed to manufacture a pass. Any preload/caching solution must retain contrast correctness and bounded memory. Recheck cold startup as well as warmed playback.
3. **Repeat these captures, then obtain separate uninterrupted normal-speed video and slow review.** Require all 16 observed frames and supported repeated contact phases before accepting seam/contact quality.
4. **Finish the remaining interaction matrix:** start/stop, collision stop, wall slide, reverse, dodge, pause/resume. Other cardinal/diagonal visual acceptance requires the corresponding authored sources; the south candidate cannot certify them.
5. Only then proceed to the shared player/camera/building/props scene. No device testing, production admission, new cadence policy, hidden-surface approval or benchmark closure is implied.

## Files

- `axis-*.json`: final post-action records.
- `test-summary.json`: authoritative final Xcode result summary.
- `analysis.json`, `analyze.py`, `poses.json`: reproducible contact analysis.
- `first-run/`: preserved initial execution results.
