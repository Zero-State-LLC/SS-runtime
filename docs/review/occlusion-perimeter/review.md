# BP-009 continuous perimeter review

Spec pin: 00ce027209e6c233bcdd35295f35f0b9bfb9bbe5. Runtime base: 897e952; accompanying test diff adds this probe. Test-only scene; no production occlusion behavior adopted.

## Evidence

- Actual SpriteKit renderer, iPhone 17 Pro iOS 26.5 Simulator. Native attachments are 2112×978; playback copies are 704×326.
- 200 consecutive simulation ticks using Movement.displacement and Collision.slideCircle, radius 18, around the authored 128×128 solid centered at (576,704). Every tick asserts nonpenetration; final Q8 position equals start.
- Geometry-derived eligibility plus projected rectangular sprite overlap. Transitions: [(69, 'occluded=true'), (132, 'occluded=false')]. Exactly one entry and one exit; normal building opacity restored.
- Playback samples every ten ticks, giving 20 images over a 200-tick path. Sampling is not a frame-rate or smoothness measurement.
- Core regression: 764 tests in 108 suites passed in 413.477 seconds using `swift test --disable-sandbox --cache-path ../swift-cache --config-path ../swift-config --security-path ../swift-security`.
- iOS result: 87 tests passed, 0 failed, 0 skipped (89 parameterized executions). See test-summary.json.

## Visual judgment

The muted footprint is less conspicuous than the previous white diagnostic boundary. However, the faded wall still overlaps the player's body and the contact ring is easy to read as a floating marker. This is not accepted benchmark art or a selected production occlusion treatment. The plate also exposes scale/material differences between building, player, camera and paving; increasing source resolution alone will not fix those.

## Limits and next work

The player remains a static south-facing pose on every leg. No gait, directional animation, foot planting or frame fidelity is validated. One isolated solid and rectangular image bounds do not cover multiple occluders, alpha silhouettes, direction reversal, stationary contact, scene edges, restart/removal, upright props, legal hazards or Reduced Motion settings. The route goes around the obstacle with clearance; separate six contact probes exercise contact positions. This fixture uses the runtime movement and collision functions, not a full legal Simulation encounter. Production classification, transitions, encounter readability and device performance remain open.

Next compare the assembled scene at native resolution and selected framing before increasing individual asset exports. Retain authored geometry and avoid changing collision to fit art.
