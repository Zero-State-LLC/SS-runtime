# Review-only footprint depth ordering

Authorization: `intent/2026-11-16-scene-qa-repair.md`, BP-001/BP-007/T1045. This packet implements a new helper only. It does not edit the published v4 harness, production code, authority, alpha, positions, visibility, CI, shared handoff or commits.

## Integration API

Both new AppTests files are entirely gated by `DEBUG && SS_SOURCE_SCENE_REVIEW`. No app, SpriteKit, UIKit or Core dependency is required by the helper.

```swift
let items: [SceneQAReviewDepth.Item] = [
    .init(name: "solid-03-transit-kiosk",
          worldRoot: .init(x: 512, y: 640),
          solidBounds: .init(minX: 512, minY: 640, maxX: 640, maxY: 768),
          projectedRootY: 1152),
    .init(name: "camera-3", worldRoot: .init(x: 496, y: 672),
          projectedRootY: 1168)
]
let result = try SceneQAReviewDepth.order(items)
// result.backToFrontNames == ["solid-03-transit-kiosk", "camera-3"]
// result.edges[0].back / .front name the precedence relation.
// .separations == [.init(axis: .x, backMinimum: 512, frontMaximum: 496)]
```

`Item` takes a unique nonempty `name`, a `worldRoot: Point(x:y:)`, optional `solidBounds: Bounds(minX:minY:maxX:maxY:)`, and required `projectedRootY: Double`. Geometry is Double-valued and must be finite. Inverted bounds and overflowed projected X ranges fail. Degenerate bounds are legal. Omitting bounds means the item is deliberately modeled as a point, not that the helper guesses a footprint.

`Order` returns `backToFrontNames: [String]` and sorted `edges: [Edge]`. Every edge has `back`, `front`, and one or two explanatory `Separation(axis:backMinimum:frontMaximum:)` values. Their strict inequality is inspectable evidence, not a visibility score. No edge or name depends on input enumeration order.

Coordinator integration must:

1. Supply every classified upright, all associated authoritative environment solid footprints, and actual actor world roots. Preserve the complete classified census. Do not silently model a known solid as a point or infer a footprint from texture size, alpha, rendered nodes or roof extent.
2. Supply projected Y from the same midpoint view for every item. The intended view is `(x-y, y+x)`, with lower world X and Y toward the viewer. Common centering and positive uniform scale do not change the priority order. Do not supply a screen-top-left Y inversion.
3. Call `order` once for the complete set, record names and explanatory edges, then assign distinct monotonically increasing bounded world depths in that order. The helper does not assign Z or assume a parent transform. The harness owns actual world/local Z conversion and bounded-band validation.
4. Treat a thrown failure as a fixture failure. Do not catch it and arbitrarily raise the Camera, remove an actor, change alpha, hide a solid or return the old root order. No actor/field/authority mutations are needed by this API.

## Geometry and deterministic ordering

The v4 root-only sequence draws Camera3 first because `496+672=1168 > 512+640=1152`, then paints the kiosk over it. But Camera X496 is strictly in front of the kiosk's minX512 plane, and its projected X=-176 lies inside the kiosk's authoritative projected ground span [-256,0]. Therefore the geometry-backed edge is **kiosk -> Camera3** regardless of those root priorities.

For each pair:

- Replace a point item by its zero-area root bounds. Project each ground footprint onto X as `[minX-maxY, maxX-minY]`.
- If those closed projected spans do not intersect, add no edge. This matters for opposite mixed quadrants: a point low-X but high-Y outside both sides is laterally clear of the footprint, not simultaneously in front and behind.
- With an intersecting projected span, A is behind B if A.minX > B.maxX or A.minY > B.maxY, provided the reverse relation is absent. Record each supporting strict plane. No floating epsilon or name-derived physical relation is invented.
- Equal, intersecting, contained and contact-only footprints add no strict edge. A separate strict axis can still support an edge when the other axis touches.

Kahn topological ordering selects the ready item with greatest `projectedRootY`, then lexical name. The priority applies only to nodes currently having no unsatisfied incoming edge, not a post-sort of the complete result. Edge enumeration is canonical by back/front name, explanations by X then Y.

Failures are `invalidItem(name:reason:)`, `duplicateName(String)` or `cyclic(blockedNames:edges:)`. Cyclic blocked names include downstream blocked nodes, not just strongly connected components. The complete edge graph is retained. No partial order is returned. The internal `topologicalNames(items:edges:)` mechanism is exposed solely to test deliberately contradictory synthetic graphs and assumes validated items and known edge endpoints. Integrators must use `order(_:)`, never supply synthetic edges. Cycle coverage does not pretend an impossible three-body scene is a feasible ground placement.

## Semantic limits

This is a conservative ground-footprint painter ordering diagnostic, not a 3D renderer or per-pixel visibility solution. It assumes the stated view and low-X/low-Y viewer orientation. It does not support height volumes, overpasses, rotated/non-axis-aligned solids, view rotation, authored lateral overhangs, actor body widths, sprite splitting or interpenetrating occluders. Laterally disjoint ground spans may still have overlapping painted overhangs, which are deliberately not inferred from art. Unknown or intersecting relations fall back deterministically to projected-root/name priority, without a claim of geometric correctness for the overlap. Root location need not be inside a solid footprint because registration may use a different ground reference.

The helper does not prove Camera visibility percentage, preserve every desired painterly overlap, establish visual acceptance, change collision or make gameplay claims. The coordinator still needs a new all-solids scene capture, bounded distinct Z checks and actual visual review. No native simulator was run by this worker.

## Validation

Run from the repository root:

```sh
python3 docs/review/scene-qa-repair-20261116/depth/test_depth.py
```

Requires Python 3, Swift and, on macOS, the selected Xcode host XCTest framework plus its Swift overlay. The script discovers the platform with `xcrun`, uses `-F .../Developer/Library/Frameworks` and `-I .../Developer/usr/lib`, and bounds subprocess execution. Temporary build artifacts use `JCODE_SCRATCH_DIR` when present. It compiles the actual helper with `DepthProbe.swift`, runs it as a host executable, and independently checks results. No Swift package build, `swift test`, simulator, remote build or dependency download is involved.

Observed November 16, 2026 at 20:55 UTC: **13 tests passed in 5.274s**, exit 0, retained in `validation.log`. Coverage includes the exact v4 failure, eight point quadrants, 1,089 independently calculated ray/box positions, solid/solid relations, contact/equal/intersection, empty/single/invalid inputs, projected overflow, 24 input permutations, ready-node priority, translation/scale invariance, same-column points and explicit synthetic graph cycle failure. Both Swift files typecheck together with flags enabled and in all three excluded flag combinations. The seven XCTest methods were typechecked, not executed in a test host.

The independent oracle intersects the ray `p + t*(1,1)` against the authoritative kiosk box, using an entry/exit parameter interval rather than copying the helper's axis-separation implementation.

Retained attempts:

- `attempt-01-validation.log` and `attempt-01-host-startup-sample.txt`: the first compiled host process stalled at `_dyld_start` before executing the helper and was explicitly terminated. Remaining functional tests passed. XCTest typechecking initially lacked its framework lookup path. The initial shell pipeline lacked pipefail, so its shell exit 0 is **not** a passing result. The unittest log correctly reports two errors.
- `attempt-02-validation.log`: all functional execution passed, but adding only the framework path found the Objective-C XCTest module without its separate Swift assertion overlay. Retained as a failing run.
- Final run adds the discovered Swift overlay path, leaves assertions unchanged, uses pipefail, and passes all 13 checks. Host startup did not stall again. Its underlying first-launch cause is not proven by the dyld sample.

No test assertion was weakened, historical evidence rewritten, or native/integration acceptance inferred.
