# BP-005 contact and occlusion evidence

Runtime parent8d6dabd; spec c773f960ee8f53ac429828767fcd09f4da0d7cb3. Review-only test change. No shipping collision, rendering or art admission change.

## Collision evidence

Six40-tick probes use Movement.displacement and Collision.slideCircle with the actual128x128 authored kiosk solid and PlayerBody.radiusUnits18. This isolates the solver with broad bounds; it is not a complete Simulation run or legal arena traversal. All240sampled positions remained nonpenetrating. Four cardinal approaches stopped at exactly18units beyond the corresponding obstacle face: west(494,704), east(658,704), south(576,622), north(576,786). Diagonal endpoints were(499.734375,624.90625) and(652.265625,783.09375); no claim of symmetric continuous contact is made. positions-q8.csv preserves every fixed-point sample. Static south-facing art depicts endpoints only, so this evidence does not validate facing, gait or continuous animation.

## Observed visual failure

contacts.png shows the unchanged actor-above-scenery layering makes east/north/far-corner players appear on upper walls or the roof despite solver positions remaining outside the obstacle. The geometric separation is correct for these probes, but presentation communicates false elevation. This fails BP-005 visual truth.

## Treatment comparison

For exactly the three known rear probes, the test compares opaque depth ordering with player below the building and then the same order with building alpha0.35. This manual selection is not a general occlusion classifier. Actor shadow is hidden during rear treatments to avoid projecting a ground shadow on top of the building. Opaque depth hides the player entirely. Fading restores visibility but weakens the obstacle boundary and still needs an explicit ground-contact cue. Neither treatment alone is accepted;0.35 is an experimental value, not a researched acceptance threshold.

Next comparison: preserve a clear ground footprint/contact cue while reducing only obscuring architecture, then check continuous entry/exit and corner transitions with enemies/projectiles. A general classifier must use world/depth relationships and the selected projection, not labels from this test. Do not simply put all actors on top or hide them without a cue.

Research basis: Apple zPosition documentation (https://developer.apple.com/documentation/spritekit/sknode/zposition) establishes draw ordering; it does not choose SS's occlusion treatment. Accessed2026-10-14. The alternatives and visual findings here come from actual SS SpriteKit captures.

## Validation

Initial contact result Test-SSRuntime-2026.10.14_11-59-47--0700.xcresult and final comparison Test-SSRuntime-2026.10.14_12-03-56--0700.xcresult both passed87tests, zero failures/skips. The final result includes84Swift Testing tests plus3XCTest tests (89executions with dynamic cases). iPhone17Pro simulatoriOS26.5. No physical-device run. Green assertions prove only the stated solver and transform invariants; screenshots explicitly document a remaining visual defect.
