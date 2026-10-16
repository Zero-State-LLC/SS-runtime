# HUD-safe framing candidate

Research and authored policy are recorded in SS-specs benchmark-production.md, “HUD-safe camera composition candidate.” Implementation: BenchmarkProjectionGeometry.unobstructedRegion plus optional safeRegion in playerVisibleCenter; capture harness measures actual visible HUD node bounds in camera coordinates. No gameplay camera adoption or simulation geometry change.

Focused iOS Simulator test: 1 passed, 0 failures, 38.721 seconds; Test-SSRuntime-2026.10.15_23-07-46--0700.xcresult. Four policies × two zooms × two motion settings. HUD-safe captures measure 25 visible HUD nodes and choose camera-local region [-191.36499,-163,418.01498,266]. Full player canvas lies inside, and overlaps no HUD exclusion beyond the 0.002-unit numerical tolerance. Digest/replay invariants pass.

Inspected normal-motion 1x and 1.25x images. Player is clear of the health bar; camera post/character occlusion remains visually wrong. At 1x all four enemy canvases and cameras 5/6/7 are contained. At 1.25x enemy 151 and cameras 6/7 are outside the image. Hostile projectile 163 origin is visible at both zooms. Canvas containment does not prove unoccluded pixels or threat lead time. Dark outside-arena area and legacy props remain unresolved. Diagnostic bright outline remains, not a clean art review.

Host checks pass: 784 independent SpriteKit corner conversions, 36 HUD-safe boundary positions across four zooms, three no-fit/unobstructed edge cases and existing six visibility probes. Synthetic HUD fixtures are geometry tests; simulator captures use actual HUD nodes. Specs validator and runtime diff check pass. A first host compiler invocation hit duplicate module-cache path spelling; rebuilt successfully using its canonical absolute path. Only rebuilt checks are cited.

Next: reserve stable HUD regions across transient states/settings; run continuous legal traversal with reversal/dodge, evaluate camera velocity and threat notice time; fix depth/contact and boundary dressing. The current largest-region calculation is static diagnostic code and may change discontinuously when HUD geometry changes. Neither zoom nor camera policy is admitted.
