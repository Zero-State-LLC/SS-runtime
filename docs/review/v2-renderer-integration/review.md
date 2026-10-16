# BP-003 v2 timing through the actual renderer

Runtime base: e78f38e. Spec pin: 56a5a5da1d87491d23df86731cc01a5acd868d26. Active production delivery remains v1.

SpriteLibrary and WorldRenderer now accept an explicitly supplied frame library while retaining their existing bundled defaults. This lets the integration test load a strict v2 catalog through the same decoder and use the actual renderer, instead of merely testing ClipTiming arithmetic or calling an isolated action constructor.

The fixture mechanically converts existing metadata to v2 and gives the Player hurt clip independent directional holds at 60 units/second: north [1,2,3], east [2,4,6], south [3,6,9], west [4,8,12]. These are technical fixtures, not newly approved artistic cadence. A west-facing event starts at tick 100 and expires at 124. First rendering at 104 must show actor_player_hurt_w_02; tick 111 remains on that frame; 112 shows w_03. A new west-facing event at 112 restarts at w_01 and expires at 136. Live east-facing movement must not retarget the reaction. Reduced Motion selects w_03; expiry resumes the east-facing state clip; reset removes the node.

Expected pixels come from independently named delivered files rather than calculating the expected frame with the same timing method under test. Repeated renders at the same tick prove phase stability. The test does not use replacement art or change authoritative state. Production construction still loads the same bundled metadata; each supplied SpriteLibrary owns its own immutable frame map and caches.

This closes the v2 data-to-renderer functional test gap. It does not close native-scale visual review of new art, complete 16-frame character delivery, camera clips, active v2 resource/export/version migration or physical-device performance.

Validation: 8 focused core tests in ClipMetadataV2Tests and ClipTimingTests passed in 1.052 seconds. Simulator action succeeded with 91 test executions (including parameterized cases), no test-failure summaries. Swift Testing console reported 86 tests / 13 suites passed in 45.591 seconds; the suite also includes three XCTest benchmark/timing checks. Exact result identity and simulator destination are recorded in ios-summary.json. No core implementation changed in this slice; no new full core run was necessary after the prior full/focused evidence.

Core command: `swift test --disable-sandbox --cache-path ../swift-cache --config-path ../swift-config --security-path ../swift-security --filter 'ClipMetadataV2Tests|ClipTimingTests'`. Simulator tests launched through the existing Xcode scheme. No physical-device test.
