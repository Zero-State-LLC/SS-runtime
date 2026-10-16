# BP-008 live displayed-frame capture

Runtime base: 6082a24. Specs: 521aec30cbb926938591d1ffb22233b24102732c.

Implemented DEBUG-only observation of the actual admitted SKTexture identity and rendered player size, anchor, position and active clip token. The test installs WorldRenderer once in a presented, unpaused SKScene, advances the real GameSession at fixed ticks and observes from didEvaluateActions. It uses the normal SpriteLibrary action construction and v1 admitted artwork. It does not manually call the action callback, reset the renderer per observation, derive texture identity from ticks, inject synthetic gameplay positions or admit replacement art.

The first live test records display time, simulation tick, authoritative Q8 position (256 raw units per world unit), rendered position, facing, active clip token, texture path, size and anchor. Unknown textures return nil rather than inventing an identity. The test requires changing movement textures and actual authoritative travel; all observations had identified textures.

## Verified result

Xcode simulator run Test-SSRuntime-2026.10.14_20-53-41--0700.xcresult completed successfully on iPhone 17 Pro / iOS 26.5 simulator. 97 test methods, 99 executions including parameterized cases; zero failures or skips. New live test passed in 2.452 seconds. test-summary.json is the result export. frames.json contains the original test attachment; observations.json summarizes its contents.

Observed: 11 post-action display samples; ticks 0–90; six distinct movement textures; player_idle|e followed by player_move|n. Authoritative raw position moved from (40960,49152) to (40960,141312), i.e. 360 world units north. Rendered player position matched the authoritative whole-unit positions in this run. Display timestamps span about 1.784 seconds. This sparse simulator capture is NOT a 60fps performance result, a smoothness judgment, a full animation video or a foot-contact measurement.

Core is unchanged by these DEBUG observation helpers and app tests. Latest core result remains 773 tests / 109 suites passed at the adopted spec baseline, in docs/review/displayed-playback/core-tests.log. The app suite validates the changed code.

## Scope still open

This is the first moving capture mechanism, not the final benchmark fixture. It uses WorldRenderer and GameSession but not the full GameScene HUD/intro path. Candidate animation installation, video/frame-image output, projection/camera transform records, foot landmark mapping, full stop/analog/collision/reversal/interruption/Reduced Motion matrix and coherent replacement cycles remain outstanding. The existing composition fixture is unchanged. No shipping animation phase policy, controller speed, textures, gameplay state or device-test approval changed.

The initial shell xcodebuild attempt stopped before compiling due sandbox access to SwiftPM cache and Simulator services. The successful run used the existing Xcode simulator workflow. Result export required scoped access to Xcode's TestReport cache. No test assertion was weakened.
