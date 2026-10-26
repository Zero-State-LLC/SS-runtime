# Matched recorded / unrecorded midpoint runs — 2026-10-19

OBSERVED: same existing test and build, no runtime/fixture edits; all130 inventoried source/fixture files unchanged. Simulator UI Record Screen was used for the first run, stopped before the second. First native test passes8 variants in30.978s; second passes8 variants in31.612s. These are focused runs, not full-suite reruns. Device:iPhone17Pro simulator/iOS26.5. Prior core779-test result remains the applicable unchanged-runtime regression evidence.

| Standard midpoint | Recorded release5 | Unrecorded release5 | Recorded release13 | Unrecorded release13 |
|---|---:|---:|---:|---:|
| Observed settling poses | 15/17 | 17/17 | 17/17 | 17/17 |
| Callback median ms | 17.47 | 16.54 | 16.81 | 16.90 |
| Callback maximum ms | 26.62 | 23.95 | 46.12 | 22.32 |
| Update median ms | 7.98 | 7.35 | 7.57 | 7.32 |
| Update maximum ms | 14.06 | 11.22 | 22.73 | 11.69 |

The recorded midpoint5 misses indices3/6. Reduced Motion bypasses remain covered by both runs. Movie packet-PTS intervals within approximate telemetry-aligned midpoint windows reach101.667ms/73.333ms, with4 intervals above50ms in each. These movie windows use creation timestamp alignment and have not undergone exact visible endpoint validation; they are capture diagnostics, not finalized review exports. The raw movie remains outputs/SS-shared-distance-review/midpoint-recorder-comparison.mov.

INFERRED: capture/system load contributes to observed cadence loss. A single sequential pair does not isolate all host-load or warm-cache effects and does not prove causal performance improvement. Callback observations are not physical display proof. No production FPS, device floor, contact or animation-family gate closes from these results. Do not change the accepted0.375s timing to compensate for the recording.

Next: obtain a less intrusive visual capture of the same midpoint fixture, or profile the recorder/system interaction before repeating the same capture path. Preserve complete idle tail, geometry, authority and separate normal/quarter reviews. Do not generate interpolated frames to hide gaps. Remaining contact/weight transfer and release/facing coverage stay open.

Evidence: recapture-result.json, unrecorded-control-result.json, corresponding attachment directories, recapture-inputs.json, recording-control-comparison.json, recapture-callback-costs.json, recapture-packet-gaps.json. Native result bundles archived under work/midpoint-recapture.xcresult and work/midpoint-unrecorded-control.xcresult. Static support detail is explicitly offscreen SpriteKit render evidence, not physical-screen capture.

Independent capture attempt: QuickTime opened through native UI, but File → New Screen Recording was disabled. The macOS Screenshot shortcut produced no observed toolbar; app inventory showed no running Screenshot surface. No alternative capture was started. Cause is unverified (do not infer lock or privacy denial). Owner was asked to open the Screenshot toolbar manually so only the Simulator region can be selected. Existing gapped captures remain diagnostic, and timing/contact acceptance stays open. Host-isolation experiment was separately rejected and reverted to the prior tested source.
