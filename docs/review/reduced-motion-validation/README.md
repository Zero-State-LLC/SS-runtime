# Reduced Motion frame coverage repair — 2026-10-15

## Change
The candidate PlayerCandidateScene now retains the exact PresentationSnapshot used for rendering and reuses it for post-action telemetry. Previously telemetry recomputed the full snapshot for facing and clip fields, adding redundant scene projection work during playback. It now records diagnostic time and snapshot construction count. Reduced Motion validation runs three independent captures, each keeping the strict 16-frame assertion, route, source timing, travel checks and repeated-cycle checks.

This is a review-harness repair, not a change to Reduced Motion policy, shipping animation clocks or gameplay. No source frames were removed, slowed, held, synthesized or relabelled. The prior failing capture skipped frame index 3 amid roughly 40–60 ms callbacks; the texture was available and the walking branch uses the same clip with Reduced Motion on and off.

## Verification
- Unrecorded app run: 111 named tests / 113 executions passed; all three Reduced Motion captures displayed all 16 frames. Median/p95 callback intervals 16.67 ms; maxima 16.67–33.33 ms.
- Recording-enabled app run: 111 named tests / 113 executions passed; all three Reduced Motion captures displayed all 16 frames. Median/p95 callback intervals 16.67 ms; maxima 33.33–40.66 ms.
- Five ClipTimingTests passed (0.396 seconds).
- Unchanged core last full run: 773 tests / 109 suites passed in 832.380 seconds, prior to this harness-only change. Not rerun in full this turn.
- git diff --check passed.

The app runs were serial, without concurrent core tests. The older failure had recording and a concurrent full core suite; the repaired runs do not isolate their individual contributions. Six successful repetitions establish the tested review condition, not immunity to arbitrary system load. Callback timestamps are SpriteKit scene-update telemetry, not physical display scanout or device performance certification. Original failed evidence remains in SS-player-clean-review/test-summary.json.

## Evidence
serial-summary.json and recorded-summary.json are the result summaries. serial/ and recorded/ contain per-capture metrics, post-action records and comparison.json. The original new recording is ../SS-player-startup-review/reduced-motion-regression.mov. timing-tests.log contains the focused core timing result.

## Next gate
The user reports twiggy legs. art-feedback.md records a proposed modest increase in calf/trouser and boot-shaft volume, preserving approved narrow stance, arm swing, knee-pad detail and foot-contact roots. No leg pixels changed during this timing validation. Show that refinement at normal and quarter speed before integrating the shared scene. No shipping assets admitted and no device retest performed.
