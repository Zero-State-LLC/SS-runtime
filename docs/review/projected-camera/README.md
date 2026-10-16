# Projected camera boundary comparison

Focused iOS Simulator test passed: 1 test, 0 failures, 39.824 seconds. Result: Test-SSRuntime-2026.10.15_22-59-28--0700.xcresult. Initial build failed because the new harness used `arena.bounds`; corrected to the existing `boundsUnits` API before this run.

Twelve projected captures: legacy, strict containment and player-visible policies × 1x/1.25x × both motion settings. The seeded legal encounter and simulation digest are preserved. These are paused neutral-pose captures, not moving camera or device validation.

Findings from inspected 1x captures: strict containment clips the Player above the image. Player-visible framing preserves the full canvas within the 0.002-unit numerical tolerance but places it underneath the health bar. The raw exact `contained` flag is false at 1x due to floating-point edge precision; the explicitly tolerance-bounded assertion passes. This is not HUD clearance or visual acceptance. Diagnostic outlines remain visible; this is not a clean art approval capture. Old environment registration, scale and depth defects remain visible.

The host geometry check also passed 784 independent SpriteKit viewport-corner conversions, invalid-input checks and six player-visibility probes. It exposes the required presentation-only background overshoot at world boundaries. Host evidence is separate from simulator evidence.

Next: define and test a player-safe screen region excluding actual HUD/control rectangles; compare camera continuity during legal traversal and threat visibility; provide presentation-only boundary dressing. Do not change collision bounds, rules viewport or adopt zoom to hide these failures. Neither new camera policy is admitted to gameplay.
