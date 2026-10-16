# BP-003 event-facing native capture

OBSERVED: testCaptureReactionTurningReadability captures 22 actual WorldRenderer frames: ticks 100–110, normal and Reduced Motion, 704×326 points / 2112×978 pixels. ReactionClipTracker receives a west-facing hurt at tick 100. Live presentation turns north at 101, travels 4 units/tick, and the reaction expires at 109. The source is the existing bundled v1 art, not the proposed benchmark character. No new art was admitted.

The normal sequence changes at the authored 3-tick boundaries. Reduced Motion retains the final hurt pose. Both return to the live north-facing move clip at expiry. Existing texture-identity tests independently verify the frame selection. The capture test also asserts occurrence facing and expiry.

VISUAL REVIEW: native crops show a pronounced silhouette change across the three hurt frames and an unclear west-facing read. The return to north-facing movement changes the silhouette again. The current source cannot establish acceptable directional continuity for benchmark art. This is a visual judgment from the exported frames, not a failed timing assertion. Keep the native readability gate open; do not activate v2 solely on passing timing tests.

Next source-art evidence must include coherent hurt poses and their transition to the approved hooded character's movement facings, preserving equipment, anatomy and anchor. Review normal timing and quarter speed in the shared renderer scene. This follows BP-002/BP-003 and the existing event-facing policy; it adds no mechanic or animation cadence.

Limits: synthetic presentation positions; no authoritative combat, collision, ground-travel or full benchmark scene validation. SKView paused: reactions are tick-sampled but fallback movement is a still, not complete SKAction playback evidence. Background belongs to the existing renderer and the synthetic path begins near its origin; it is not a proposed environment layout. Native-pixel crops are fixed 200×250 cuts, unscaled, from the full captures. Browser playback is a review aid, not frame-pacing measurement.

Validation: iPhone 17 Pro simulator / iOS 26.5, 92 test executions succeeded with no failure summaries (86 Swift Testing tests plus 4 XCTest methods, including parameterized executions). Focused core run: 15 tests, 2 suites, 1.089 seconds. No physical device used. Raw result and attachments were read through xcresulttool legacy object export; the newer attachment exporter required an unavailable cache write, so it was not used.

Active v1 metadata, source art, spec pin and gameplay identities remain unchanged. Spec source: 56a5a5da1d87491d23df86731cc01a5acd868d26, animation-timing-migration.md and acceptance.md BP-003 gate. The active migration remains pending this visual gate and coordinated resource/version/export reconciliation.
