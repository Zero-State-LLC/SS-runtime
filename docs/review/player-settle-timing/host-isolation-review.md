# Host-rendering isolation comparison — 2026-10-19

OBSERVED: the app shell retains GameplaySurface beneath TitleView. Apple documents SKView.isPaused as stopping its scene actions/physics: https://developer.apple.com/documentation/spritekit/skview/ispaused . Simulator recording already uses H.264 (verified by ffprobe); changing to the H.264 command shown in Apple's Simulator guide is not an evidenced codec improvement. ScreenCaptureKit exposes queue/interval controls, but those are a separate capture implementation, not configurable Simulator controls or a guaranteed cure: https://developer.apple.com/videos/play/wwdc2022/10155/ .

Implemented an opt-in pauseHostRendering comparison in the existing native traversal helper. Default=false leaves existing test controls unchanged. The comparison discovers pre-existing host SKViews before creating its own fixture window, saves their pause values, pauses them, and restores each value in defer. The tested fixture still uses its real renderer, same source, registration, exact0.375s timing, commands, warmup, Reduced Motion behavior, independent replay and existing assertions.

Native correctness result: one focused test passes four variants (phases5/13 × Standard/Reduced),16.859s. Each of four restoration attachments reports exactly one host view, originally unpaused, restored unpaused. This confirms actual host discovery/restoration, not a no-op comparison. No production renderer, gameplay or source-art change.

The core regression was running concurrently, so this run is not performance evidence. The core run is now terminal, so subsequent capture comparisons can proceed without that competing load. Core regression completed:779 tests in110 suites passed in455.035s, exit0; log: host-isolation-core-tests.log. Next run the same comparison with capture after host load settles, validate packet PTS/visible endpoints/callback poses, and separately verify the unchanged default control. Do not adopt the test option or claim cadence/contact acceptance from this correctness pass.

Evidence: host-isolation-result.json and host-isolation-attachments/. Archived native bundle: work/host-isolation-correctness.xcresult. Full native suite has not been rerun after this test-helper change.

Reproducible callback summaries: summarize_midpoint_capture.py requires exactly four midpoint variants, checks monotonic timestamps and records attachment hashes. host-isolation-callback-summary.json describes the concurrent-load correctness run only; it must not be used as a clean performance baseline.

## Recorded comparison and disposition

Recorded focused run passed4 variants in18.624s. Background pause/restoration again succeeded. Standard release5 observed15/17 poses, callback max41.47ms, update max38.16ms; release13 observed16/17, callback max31.41ms, update max24.80ms. Approximate telemetry-aligned movie windows still contain100.00/101.667ms packet gaps. This does not demonstrate capture improvement. Results and traces: host-isolation-recorded-result.json, host-isolation-recorded-attachments/, host-isolation-recorded-summary.json and host-isolation-recorded-comparison.json. Movie retained at outputs/SS-shared-distance-review/midpoint-host-isolated.mov.

Rejected as a capture fix. Removed the opt-in helper parameter, pause block and dedicated test. Verified resulting DisplayedPlaybackTests.swift SHA256 exactly matches recapture-inputs.json, restoring the prior tested source. Production code and source artwork never changed. Historical implementation/correctness records above describe the experiment, not current behavior. No repeated core run required solely for exact restoration to the already verified source. The remaining recording issue requires a different capture path, not another retry of this option.
