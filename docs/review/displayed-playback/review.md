# BP-008 displayed-playback specification adoption

Adopts SS-specs 521aec30cbb926938591d1ffb22233b24102732c across SPEC_BASELINE.md, ContractVersions, SPEC_PIN and asset-catalog specificationCommit. This clarifies evidence requirements, not gait, controller speed, contact tolerance, frame count, new artwork admission or phase behavior. Active clip delivery remains v1.

Source audit at runtime e6db65d:
- SpriteLibrary.texture selects event-driven textures by ClipTiming.frameIndex(atTickOffset:).
- SpriteLibrary.animation builds ordinary playback through sequence(textures:timing:), using SpriteKit action intervals and repeatForever for loops.
- WorldRenderer.playClip replaces actions when the clip/direction token changes. The benchmark review-art branch selects a static texture and removes actions.
- GameScene.renderBenchmark installs art, which resets WorldRenderer, then renders with Reduced Motion. This remains valid composition evidence only.
- GameScene.didEvaluateActions already aligns outlines after action evaluation; the moving evidence path should observe displayed texture there rather than guessing its frame index from simulation ticks.
- GameScene.redraw obtains session.snapshot and passes it to WorldRenderer. Authoritative simulation position and rendered node position must remain separately recorded, especially for diagnostic projected-world comparisons.

Required implementation remains open: optional moving candidate installation once, ordinary action timing, post-action frame identity, simulation/rendered/root records, changing-texture sanity evidence and the existing BP-008 motion-case matrix. No static capture or source solver closes these requirements. Current painted contact key remains a source study, not a cycle.

Parity evidence is in parity.log. Core suite passed: 773 tests in 109 suites, 378.692 seconds; process exit 0. See core-tests.log. Neither check establishes artwork quality, moving capture coverage or device readiness.
