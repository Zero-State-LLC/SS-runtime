# Awareness-hint snapshot optimization

GameSession now passes WorldState directly to AwarenessHintProjector instead of constructing the full PresentationSnapshot every tick. The read-only overload uses the same PresentationCamera.follow, Q8 truncation, alive/unaware filter and inclusive viewport containment. Both APIs share the unchanged once-per-run/300-tick lifecycle. Visibility work is lazy once the hint has latched.

The new parity vectors cover 567 visibility combinations (camera positions/headings, inclusive/outside edges, fractional coordinates and enemy condition), plus lifecycle expiry, rewind and reset. Existing awareness and readability tests also pass: 26 AwarenessTests + 21 ReadabilityFinishTests, both commands exit 0 using `swift test --disable-sandbox --filter …`. App suite: 117 named tests / 119 executions passed, zero failures. The opt-in timing test preserves every tick's state digest and events plus command logs.

Same-scenario Debug simulator measurement, 240 steps across both control/measured orders: the historical `awarenessSnapshotAndHint` stage label is retained for comparison, but now measures the direct query. Median fell from 1.235 to 0.00596 ms and from 1.2095 to 0.00501 ms (about 99.5%). These stage measurements include diagnostic overhead and do not establish end-to-end frame rate, GPU cost or physical-device performance.

No simulation rules, animation duration, route length, coverage gate or production art admission changed. The earlier recorded distance-phase miss remains open. The next measured candidate is the full snapshot still constructed in FeelPassPresenter.observe; it needs its own semantic parity and measurement before adoption. Then repeat recording-load coverage and the required Release/device profiling.
