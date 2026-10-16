# Camera registration evidence — BP-004/BP-007/BP-010

## Observed

The seed-1 encounter at tick 461 now records mount (M, cyan), target (T, magenta), and field emitter (F, yellow) independently in the actual GameScene. The plain captures remain separate; the diagnostic overlay is test-only. The pole base visibly meets M. The field apex meets F. T and F are close but distinct.

The visible socket cam-z02-d has heading 70000 millidegrees. Exact coordinates:

| Landmark | World coordinates | Raw Q8 |
|---|---|---|
| Mount | (496, 672) | integer socket position |
| Target | (501.47265625, 656.96484375) | (128377, 168183) |
| Field | (502.15625, 655.0859375) | (128552, 167702) |

These values follow civic-seam-arena-004's local forward offsets: target 16 units and field 18 units, transformed by CameraPlacement.offsetPoint using the socket heading and fixed-point rounding. The presentation snapshot preserves fieldOrigin; CameraFieldGeometry uses its fractional coordinates. Assertions compare the rendered geometry key against the authoritative field point. Capture and overlay leave the simulation digest unchanged; serialized commands replay to the same digest.

## Disposition

The observed mount-to-apex gap is explained by the existing contract, not a misplaced simulation emitter. Do not translate the Camera or detection geometry merely to remove this gap. This evidence does not establish optical-head registration: an elevated optical head is not itself a ground-plane point, and no authored projection of that head has been supplied. A production solution still needs the shared projection/source landmarks and visual review required by BP-007. No new beam connector, housing rotation, or target behavior is selected here.

The scene still contains legacy opaque building backdrops, inconsistent environment scale, and the conspicuous Player border. This diagnostic is not the approved benchmark scene and does not admit the candidate artwork. Full animation, environment replacement, field readability in motion and device acceptance remain open.

## Verification

Xcode Test-SSRuntime-2026.10.14_22-55-32--0700.xcresult: 106 test executions, no failures; existing EnvironmentLibrary nonthrowing-try warning. `swift test --disable-sandbox --filter CameraPresentationTests`: 3 passed, exit 0. No core implementation or specification contract changed. The earlier full-core result is not represented as a fresh full-suite run.
