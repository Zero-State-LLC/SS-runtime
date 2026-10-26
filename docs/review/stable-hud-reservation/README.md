# Stable HUD reservation — sampled diagnostic

Focused iOS Simulator test passed, 1 test / 0 failures, 78.034 seconds. Result: Test-SSRuntime-2026.10.16_01-14-52--0700.xcresult. Six handedness/scale layouts, 50 samples each at ticks 1...5881 in 120-tick intervals. Seed 1, normal autopilot commands, 6000 ticks total. All 300 player placements fit their fixed reservations without measured HUD overlap. Presentation redraw preserves authoritative digests.

At a fixed player probe, recomputing the reservation from current HUD rectangles produces maximum successive sampled focus displacements of 45.86/57.90/89.87 points (left, 100/115/130%) and 45/52/58 points (right). These are geometry measurements, not observed live jitter or frame-rate measurements.

The reservation unions future sampled bounds offline. This demonstrates feasibility for these samples, not production coverage of all copy, phases, localization or viewports. Production needs authored maxima or another validated stable layout policy. Neutral 64x64 candidate canvas, 1x framing. No art, projection, input or device acceptance.

Next: sampled moving-camera capture using the right/100% reservation, then continuous displayed playback, reversals/dodges and threat-entry review. Preserve known depth and boundary-dressing gaps.
