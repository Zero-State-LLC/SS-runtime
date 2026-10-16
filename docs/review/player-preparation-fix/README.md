# Player preparation repair — BP-007 / BP-008

2026-10-15. Candidate-only registration and preparation are implemented. Production artwork, controller speed, source poses, frame count and half-second cycle remain unchanged. Shared-scene and device acceptance are not claimed.

## Measured comparison

The same unobstructed south route, source textures and timing were run twice through each incremental stage in a presented SpriteKit scene. Measurements are simulator observations, not device performance. Controls report failed coverage explicitly; the four final-mode regression tests still require 16/16 frames and repeated wraps.

| Stage | Observed unique frames, runs 1 / 2 | Gameplay texture readbacks, runs 1 / 2 | Outline miss/build time during playback |
|---|---|---|---|
| Original registration, no preload | 7 / 8 | 14 / 15 | 1,336 / 1,543 ms |
| Correct registration only | 10 / 9 | 10 / 9 | 930 / 923 ms |
| Correct registration + preload artwork | 10 / 8 | 10 / 8 | 953 / 886 ms |
| Correct registration + prepare outlines + preload both | **16 / 16** | **0 / 0** | **0 / 0 ms** |

Prepared-path preparation took 354–362 ms in the comparison repeats (359–364 ms across the independent final-mode runs). This work is explicitly measured before presenting the scene; it is not described as free. Preparation timing covers mask preparation and preload, not all file loading or scene setup.

The controlled results support the combined preparation repair. They do not establish how much of the old cost was texture conversion versus the mask algorithm: those are measured together in outline miss/build time. Two repetitions are evidence, not a statistical performance guarantee. Source/preload caches may remain warm across sequential cases; these are fresh scene/cache instances, not process-cold launches.

## Implementation

- WorldRenderer accepts a DEBUG candidate registration before its contrast work. The fixture's 64×69⅓ canvas, anchor and upright scale are therefore consistent when the outline cache is accessed. Shipping defaults remain unchanged.
- OutlineTextures accepts a retained source CGImage on preparation calls, preserving its existing mask algorithm, padding, faction colors, bounded cache and fallback. The metrics count hits, misses, texture readback calls and construction time.
- The candidate fixture prepares masks for all 16 source images, then awaits SKTexture.preload for artwork and masks before presentation. Post-action outline synchronization remains active and uses cached entries.
- The bounded cache retains 299,904 bytes of prepared masks for the 16-player-frame family. This is generated mask payload, not total app/GPU memory. The existing 128-entry / 4 MiB mask bounds remain.
- A new regression proves source-prepared and fallback masks are pixel-identical and that subsequent playback lookup reuses the same texture without readback.

## Validation

- Final Xcode simulator suite: **112 executions / 110 named tests passed, zero failures, zero skips**. Includes existing animation, camera, outline, presentation and gameplay-facing app checks; four strict prepared player modes; repeated staged controls; and source-mask parity/cache reuse.
- Full/half/quarter input and Reduced Motion each observed **all 16 textures, three index wraps**, correct registration/travel, and zero playback outline misses/readbacks. No recorded moving tick lost the candidate sprite.
- Core suite: **773 tests / 109 suites passed**, exit 0, 558.322 seconds (`swift test --disable-sandbox`).
- `git diff --check`: passed.
- An additional terminal Release build attempt could not resolve the local package because sandbox permissions blocked SwiftPM diagnostic output in the user Library cache. No Release build success is claimed; the successful app suite is the Xcode simulator test configuration.
- One initial compilation attempt exposed a misplaced instrumentation variable in the test helper; it was corrected before the successful run.

Result bundle: Test-SSRuntime-2026.10.15_14-04-19--0700.xcresult, retained as work/player-preparation.xcresult. Core tests were started only after simulator timing captures completed. The source knee-detail frames remain byte-identical to the reviewed candidate.

## Remaining gates

**Startup:** all prepared runs still show their largest callback gap between tick 0 and tick 13/14, approximately 225–246 ms. Median callback spacing is approximately 16.67 ms in the four final modes; p95 ranges 26–38 ms. This is not a 60-fps performance acceptance. Scene/ground/fallback setup and scheduling require separate attribution. The prepared masks remove the demonstrated outline work but do not prove every other stall is fixed.

**Contact/cadence:** contact/analysis.json now has repeated multi-sample support observations. Maximum annotated ground-equivalent support displacement is 5 units at full input, 12.5 at half, 16.5 at quarter and 4.5 with full-input Reduced Motion. These are observed intervals, not pixel tracking or approved slip tolerances. The existing fixed-duration cycle runs at all input magnitudes; partial-input phase policy remains a specification/design decision. Do not alter limb geometry or gameplay speed to make these values disappear.

**Visual evidence:** post-action identities describe selected SpriteKit textures before scanout. They are not uninterrupted video. Normal/quarter-speed real-renderer visual review, complete seam/contact acceptance, stop/start and interaction matrix, other authored facings, shared-scene acceptance and physical device testing remain open. Passing the current suite does not close those gates.

## Evidence files

- comparison.json — twelve measured runs, including callback distributions and separate preparation/render/simulation/outline timings.
- BP008-stage-*-metrics.json and *-post-action-records.json — original exported measurement attachments.
- test-summary.json — authoritative Xcode summary.
- contact/ — exact final-mode records, source poses and reproducible annotation analysis.
- core-tests.log and release-build.log — command evidence.
