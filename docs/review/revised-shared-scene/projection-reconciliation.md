# Projection reconciliation checkpoint

The graph-located `BenchmarkCaptureTests.projectedSharedCameraScene` was checked against current source. Its rotation +45° followed by half-height transform projects world south down-right, not toward the viewer. A straight front-facing source therefore cannot validate world-south travel in this shared fixture.

The specs now distinguish world heading, projected displacement and authored facing, including reaction ownership, inverse input and speed preservation. Screen-down corresponds to world south-west for this comparison. This is a bounded pilot direction, not all-facing art coverage or a production mapping policy.

`python3 scripts/audit_benchmark_projection.py --output docs/review/revised-shared-scene/projection-audit.json` passes eight inverse round trips, the projected diagonal speed ratio and screen-down inverse mapping. This independent algebra diagnostic does not run the Swift helper. Current production behavior is unchanged.

Next implementation evidence: actual node-conversion regression, then a labeled live projected pilot without altering simulation direction or silently overriding reaction selection. Full directional art, input conversion and occlusion integration remain open.

Host SpriteKit follow-up: `swift -module-cache-path /private/tmp/ss-projection-module-cache scripts/check_benchmark_projection.swift` passed 32 forward/inverse samples across eight directions and four magnitudes. Maximum error was 0.00021364472945606394 points. An initial fixed 0.0002 bound failed; the replacement uses eight Float ULPs at coordinate magnitude for composed transform arithmetic, distinct from contact acceptance. The actual shared-scene helper now runs matching assertions. Fresh app run `18-55-43` is pending; prior app results do not validate this edit.

Completed app result: 114 named tests / 116 executions passed, zero failures. The shared comparison now verifies all eight directions and inverse conversion at four magnitudes in its actual SpriteKit hierarchy. This closes numerical mapping verification only; projected animated traversal, facing selection, input migration and visual acceptance remain open.
