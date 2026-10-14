# Painted candidate in the real renderer

2026-10-14. BP-002/BP-007 comparison, **not benchmark acceptance or production art admission**.

The existing GameScene/WorldRenderer benchmark fixture now captures all four registered painted neutral views with the constrained building, municipal camera, newsbox and tree. Candidate textures live only in the test bundle. Production sprites, clip metadata, physics and gameplay are unchanged. Both existing projection-review zooms are captured: 1 and square root of 2. This remains a bounded review transform, not a selected shipping projection.

## Evidence and validation

- Final simulator result: `Test-SSRuntime-2026.10.14_16-43-59--0700.xcresult`, action status succeeded, 92 test executions; 86 Swift Testing tests plus four XCTest cases and two additional parameter executions. No test failures.
- Core: 773 tests in 109 suites passed in 448.647 seconds. Full log in the parent folder's core-tests.log.
- Eight final captures: four facings × two zooms, each 2112 × 978 pixels from the 704 × 326-point SKView. The comparison plate reduces each to 704 × 326 for logical-size review; source captures remain intact.
- All eight final views visually inspected on the comparison plate; the closer front view also inspected separately at higher resolution.
- One existing compiler warning remains: EnvironmentLibrary.swift:108, unnecessary `try`. No warning suppression was added.

## Findings

The hood, coat opening, strap and boots read more clearly and coherently than the procedural source model. Front, rear and profiles are distinguishable; the rear no longer substitutes a front silhouette. The profile poses still need validation against the selected ground projection. Static images cannot prove turning, contact or gait quality.

The scene does not yet reach the approved benchmark. Current plaza paving, sparse layout, architectural palette and lack of street/curb treatment differ substantially from the approved reference. The closer view crops the municipal camera and tree at the upper edge. Shared source scale, camera placement and framing need a deliberate scene pass. No legal encounter or occlusion acceptance is claimed.

**New concrete runtime gap: #124.** OutlineTextures rejects sources larger than 256 × 256 and assumes one source pixel per logical unit. At 384 × 384 the player loses its faction outline. The first paused capture retained the preceding source's outline; the harness now calls the normal didEvaluateActions callback after each swap and after restoration, so final evidence honestly shows the missing outline. The final eight PNGs supersede that initial capture. Issue: https://github.com/Zero-State-LLC/SS-runtime/issues/124

Before admitting high-resolution sprites, specify and implement resolution-aware outline thickness and input/memory limits, then verify frame changes and Reduced Motion. Merely raising the source cap does not preserve logical thickness. The painted sheet also still needs editable layers, authored hidden surfaces and animation/world-travel validation.

Physical-device testing remains pending. This simulator review satisfies a comparison step only; it does not close BP-001 through BP-009 or the broader runtime/spec audit.
