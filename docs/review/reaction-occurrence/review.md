# BP-003 event-facing one-shot integration

Runtime base: d96fca0. Adopted specification: 56a5a5da1d87491d23df86731cc01a5acd868d26. Active clip delivery remains v1.

ReactionClipTracker records a ClipOccurrence (event-facing and start tick) for hurt, stagger, held commit and defeat, and derives the exclusive end tick from that facing's timing. GameSession supplies the Player's post-tick facing. Enemy occurrences use the same velocity-facing projection as the body. A new qualifying event creates a new occurrence; rendering or turning does not change it. Checked end-tick addition fails closed on overflow.

PresentationSnapshot carries occurrence data separately from live facing. Held commits retain the base clip for missing-art fallback. Applying the tracker to a reused snapshot clears expired reaction data and restores the base, including an absent base. Defeat and cancellation precedence remain in the tracker.

WorldRenderer samples one-shot textures from elapsed simulation ticks, rather than restarting a full SKAction when facing changes. ClipTiming.frameIndex compares full-width integer products at exact frame boundaries; even a very late sample cannot overflow. Repeated or paused ticks select the same pose; late first render enters the current phase; Reduced Motion selects the final pose. Fallback uses the live direction and normal state animation. SpriteKit actions remain in use for ordinary state/locomotion clips.

Core coverage includes unequal facing lifetimes, suppression without deadline extension, turning, repeat events, reused-snapshot expiry, nil-base restoration, reset, exact rational frame boundaries and large-offset arithmetic. The new iOS test compares actual texture PNG pixels for late rendering, turning, repeated ticks, new occurrence, Reduced Motion and missing-art fallback. Existing pause/restart, cancellation, defeat and session-versus-bare-simulation checks remain relevant.

Test defect #122 was recorded before repairing nested #require macro expansion in the new pixel helper. The fix separates texture and PNG-data requirements; no assertion was weakened: https://github.com/Zero-State-LLC/SS-runtime/issues/122.

This is functional playback infrastructure, not acceptance of current source art. Native-scale review of movement during event-facing reactions, complete new cycles, v2 exporter/resource/version migration, performance and physical-device gates remain open. Current animation art is unchanged.

## Validation

Full core run: 772 tests / 109 suites passed in 633.668 seconds before the final nil-base restoration edge-case fix. After that fix, 31 focused tests across ReactionClipTrackerTests, CommitClipTests, ClipTimingTests, ClipMetadataV2Tests, ContractVersionsTests and AssetCatalogTests passed in 1.144 seconds. The full suite was not repeated after that narrow cleanup change.

Final iOS Simulator build: 88 tests passed, 0 failed, 0 skipped (85 Swift Testing + 3 XCTest). Result Test-SSRuntime-2026.10.14_14-29-29--0700.xcresult; iPhone 17 Pro iOS 26.5 simulator CACB3927-A76E-43A5-9ACA-C389EB38C0C3. Includes actual reaction texture checks and existing session digest, pause/restart and camera interruption checks. No physical-device run.

Core command: `swift test --disable-sandbox --cache-path ../swift-cache --config-path ../swift-config --security-path ../swift-security`; focused follow-up adds `--filter 'ReactionClipTrackerTests|CommitClipTests|ClipTimingTests|ClipMetadataV2Tests|ContractVersionsTests|AssetCatalogTests'`.
