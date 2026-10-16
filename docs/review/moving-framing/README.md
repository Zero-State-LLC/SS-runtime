# Moving framing comparison

Focused test: Test-SSRuntime-2026.10.15_21-22-34--0700, testSharedProjectedPlayerTraversal. One test passes its explicit assertions across six variants (1× fixed, 1.25× fixed, 1.25× tracking; each standard and Reduced Motion). Every variant matches all 90 independent simulation positions and final digest, preserves clip/facing ownership, observes 16 frames and incurs zero player-outline readbacks. This is not blanket visual acceptance: fixed-view clipping is deliberately reported, not hidden by a shortened route.

1× fixed: complete player canvas and camera emitter stay in view in recorded movement observations. 1.25× fixed: player canvas clips in 19 standard / 22 Reduced Motion distinct sampled ticks and the root eventually leaves the viewport. 1.25× tracking: no player-canvas clipping; root remains stable within floating-point precision. Camera emitter leaves view in 28 distinct sampled ticks in each mode. This does not establish missed warnings, because the scene deliberately filters encounter actors and moves the review camera. It establishes that a closer still cannot be promoted without encounter validation.

Proposed decision: reject fixed 1.25× for this route; retain tracking 1.25× for legal-encounter comparison. No shipping camera/zoom policy changed. Source art, speed, anchors and cadence are unchanged. Unsupported idle source remains an existing coverage gap: visibility observations here require the player sprite and cover movement, not all idle/action states.

Apple SKCameraNode documentation defines viewport ownership; the exact tracking policy/offset is our measured proposal, not an Apple aesthetic recommendation: https://developer.apple.com/documentation/spritekit/skcameranode .

No new video or pixel-contact/seam acceptance in this run. Next: legal camera/attack scene with actual authoritative emitter locations and full encounter rendering, then normal/quarter playback. Keep foreground occlusion/input mapping and missing facings/actions open.
