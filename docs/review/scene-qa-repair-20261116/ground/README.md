# Continuous authored ground, bounded sample 01

Review-only source packet for `intent/2026-11-16-scene-qa-repair.md`. This addresses the finite paving rectangle and surrounding material mismatch, not whole-scene fidelity. No owner acceptance, production admission, native run, shared harness change, collision/actor/field relocation or benchmark modification.

## Diagnosis and algorithm

The retained v4 uses the authored 1152-square corner at world bounds `[448,384,1024,960]`, a 576-square world patch. Its coverage fails the inverse 704x326 crop at **all three actual recorded zooms: 1, 1.25, 1.4**, centered at `[736,672]`. The inverse uses +45-degree rotation and 0.5 ground Y scale, then zoom, as in `AppTests/ReferenceProjectionTrial.swift:4-53` and `AppTests/SourceSceneContinuationTests.swift:314-345`. Coverage is a convex-rectangle corner proof, not a heuristic screenshot color classifier.

`authoritative-placement-1014.json` confirms arena `[0,0]..[2304,1536]`. `build.py` directly imports the SHA-pinned independent authoring module `paving-corner-review-20261116/build.py:16-142` and calls its original `read_source`, `material` and `context`. **Only context worldBounds changes.** No source pigment, color, source grid, material mixture seed, curb/road/rail geometry, feature location or world sampling phase changes. The entire original 1152-square raster must equal the corresponding new interior byte for byte.

The original signed-distance rounded corner is evaluated across the whole arena. The 256-world-unit material supertile repeats only within the paving material region. The curb, crossing, rails, drain, tactile panel and manhole are authored world-coordinate geometry, not a tiled picture of the curb. Road grain remains the original absolute-coordinate deterministic formula. All original dependency SHA256 values are embedded in the generator and manifest, checked before and after each build. No benchmark pixels are read.

## Outputs and registration

- `ground-arena.png`: **4608x3072 RGB**, 2 pixels/world unit, world bottom-left `[0,0]`, draw size `[2304,1536]`. Image top-left maps to `[0,1536]`. Original edge-sample convention: `x=px/2`, `y=1536-py/2`. No alpha holes.
- `ground-patch-square.png`: **4608x4608 RGB**, exact arena in bottom3072rows, top1536rows are edge padding only, not additional world content. This adapter is necessary for existing `groundPatches` semantics, not a stretched arena.
- `diagnostic-preview.png`: one bounded offline diagnostic sheet. Top row shows the three ground-only crop inverses. Bottom repeats the same pixels with the old finite patch boundary in red. No actors, HUD, fields or lighting simulated. This is not a native capture.
- `manifest.json`: original hashes, generator hash, output hashes, registration, old/fixed inverse-crop coverage, algorithm and limitations.
- `test_ground.py`, `tests.log`: portable source validation, not native or aesthetic acceptance.

## Coordinator integration, without changing the renderer

`App/WorldRenderer.swift:458-474` computes both texture axes using the single square `tileUnits`. Therefore **do not pass ground-arena.png directly**: that would sample only the bottom two thirds and stretch it. Use the square adapter:

```swift
// Load ground-patch-square.png as a bound review-only texture.
texture.filteringMode = .linear
art.groundPatches = [
    .init(texture: texture,
          bounds: CGRect(x: 0, y: 0, width: 2304, height: 1536),
          tileUnits: 2304)
]
art.groundLines = [] // authored curb/rails already exist in the ground texture
```

This creates exactly one patch, samples normalized bottom-left rect `[0,0,1,2/3]`, and displays it at `[2304,1536]` world size without geometry repetition or stretching. Replace the prior finite patch and any conflicting review ground-line overlays, not authoritative scene data. The opaque patch covers existing plaza/asphalt base tiles within arena bounds. Keep actor roots, solids, fields, all upright inventory, scene center and projection unchanged. Coordinator must bind the new source SHA and preserve v4 evidence. Native sampling/orientation and texture memory performance still require the coordinator's isolated run.

## Commands

Run from repository root with Python3 and Pillow available:

```sh
python3 -B docs/review/scene-qa-repair-20261116/ground/build.py
python3 -B docs/review/scene-qa-repair-20261116/ground/build.py --probe v4
# Expected exit 1: all three actual crops extend outside the finite v4 patch.
python3 -B docs/review/scene-qa-repair-20261116/ground/build.py --probe fixed
# Expected exit 0: all inverse-crop corners are inside authoritative arena bounds.
python3 -B docs/review/scene-qa-repair-20261116/ground/test_ground.py
```

Tests enforce full original interior equality (including all decorative features), absolute rail registration beyond old edges, no repeated drain motif, opaque coverage, all four old-boundary strips matching independently evaluated original geometry, exact square-adapter UV crop, fail-closed input hashes, negative registration/seam mutations and byte-identical full rebuild. Temporary rebuilds stay inside this owned packet and are removed after comparison. They are repeatability checks of sample01, not further aesthetic samples. No unfiltered Swift/native run is permitted by this work order.

## Remaining fidelity limits

This is an extrapolation of the same authored corner, not a restyling or acceptance of the material. Eight-slab repetition and quilted pigments remain. Road grain and decorative curb are procedural presentation, not gameplay authority. Extending this layout arena-wide does not establish meaningful street adjacency at every other building. Lighting, contact shadows, actor contour/occlusion, Camera readability, benchmark composition and complete scene fidelity remain outside this repair. The square adapter is about81MiB if expanded to RGBA before mipmaps, with no measured GPU cost. Existing nearest edge-sample convention is preserved rather than silently correcting its half-pixel interpretation. One bounded source sample is authored here. Native and owner review remain required.
