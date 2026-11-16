# Context building geometry: final bounded source

Final correction: `repair_roof_density.py` reads preserved `attempt-01/geometry.json` and splits upward roof faces into a shared 128-world-unit material grid. This changes 2682 to 2702 faces without moving ground/contact/height or modifying material input pixels. Both preview filenames retain their historical `first-preview` names but current output is the corrected source. Attempt-01 retains the actual original exports.

Coordinator inspection and limitations are recorded in `COORDINATOR-REVIEW.md`. Eleven strict checks passed in `coordinator-tests-2234.log`, including the two added roof-density regressions. The initial recovery test failure remains in `coordinator-tests-2233.log`: the written repair had not yet executed when context was recovered. No thresholds were changed to obtain passing results.

## Original first-sample documentation

Status: **FIRST SAMPLE, NOT AESTHETIC ACCEPTANCE OR PRODUCTION ADMISSION**. Scope is only four newly authored neighboring building sources. No kiosk, production source, shared gallery, shared handoff, native capture, CI, commit or push is performed here.

## Start here

- `output/first-preview-native.png`: the four sources at 1 output pixel per world unit, not a simulator capture.
- `output/first-preview-half.png`: 0.5 output pixels per world unit.
- `output/solid-*.png`: full 4 pixels per world unit alpha source exports.
- `output/*-footprint-witness.png`: original footprint corner loop in coral, unchanged solid-center root in cyan.
- `registration.json`: list of four role-specific records for the scene coordinator.
- `alignment-verification.json`: independent registration checks bound to the exact registration, geometry and retained v6 authority SHA256 values.

The 24 original solids remain authoritative. Only solid01 residential-west, solid02 residential-north, solid04 civic-west and solid05 civic-dais have new review art. No remaining/offcrop node is removed or replaced by this packet. Whether art is actually visible at the preserved v6 framing must be evaluated in the coordinator's native scene. These source previews do not fabricate scene evidence.

## Diagnosis from actual v6 and actual sources

Inspected the actual v6 z100 native candidate PNG, retained unchanged in `inputs/v6-z100-native.png`, and its `preprojectionInventory` plus complete `solids`, retained unchanged in `inputs/v6-records.json`. These record:

| Solid | Original center | Runtime sprite size | Original anchor |
| --- | --- | --- | --- |
| residential-west | 64,640 | 128x512 | .5,.5 |
| residential-north | 320,864 | 384x192 | .5,.5 |
| civic-west | 832,960 | 192x384 | .5,.5 |
| civic-dais | 1088,704 | 160x96 | .5,.5 |

`App/WorldRenderer.swift:746-769` constructs the foundation from the solid box, then creates a sprite using the same unprojected width/height and center with no source-specific root registration. The actual original PNGs already contain isometric-painted architecture and substantial transparent padding. They are retained for inspection, not sampled or stretched into the new meshes. The old residential source is a small multi-storey townhouse cluster inside a 384x192 canvas. The old civic source has a classical entry and teal skylight inside a 192x384 canvas. A padded canvas center is not a measured architectural ground point.

This packet does not solve the defect by squeezing entire PNGs into projected rectangles. Each new architectural face is built in local world XYZ, relative to the original authoritative solid center, and projected with:

```
u = (x-y)/sqrt(2)
v = (x+y)/(2*sqrt(2)) + z
sourceX = rootX + 4*u
sourceY = rootY - 4*v
```

Four true foundation contact vertices coincide with the unchanged rectangle's four corners. Roof lines use exactly the same ground basis, vertical edges use upright z. All geometry stays within the original XY bounds. New decorative elevation is review-only authored geometry, not new collision or a claim about hidden original architecture.

## Editable source and materials

`geometry.json` is the master: every face has named XYZ vertices, a normal, material ID and four editable affine UV coordinates. Non-parallelogram geometry or UV edits fail closed instead of silently ignoring the fourth corner. Split unsupported shapes into supported affine quads. `materials.json` declares explicit source crop rectangles and optional channel tint. `replay.py` uses per-pixel geometric depth, so raised architecture is not ordered by arbitrary sprite depth or by drawing whole boxes on top of one another. The source PNGs are exports, not the master.

2682 authored quads include the full contact plinths, masonry shells, window bay frames, stone sills, lintels, stringcourses, cornices, parapets, coping, capped brick chimneys, civic pilasters and roof lanterns, and the dais's actual step/rail/baluster geometry. Hidden faces reuse visible material vocabulary instead of claiming unique original paint.

Facade, roof and door materials are copied byte-for-byte from the independently generated `stone-painted-facade-20261116` packet. `provenance.json` records exact original paths and SHA256 values, plus retained provider metadata and its original source explanation. This does not claim a new provider generation or a reconstructed original master. The new brick material combines tinted painted stone with an explicitly authored staggered mortar pattern. It is not a primitive flat-color whole-building substitution and is not recovered original residential brick paint.

Window glazing/recesses and small mullion wear remain painted relief. Cornice, sill, bay, chimney, parapet and rail depths are geometry. Broad flat roofs, repeated windows and material repetition are honest first-sample aesthetic limitations. Original civic pediment/entry character is not fully represented in this first sample. Technical registration success cannot establish artistic equivalence.

## Registration schema

`registration.json` is a JSON list. Each entry includes:

- `nodeName`: exact existing environment-upright node name.
- `source`: PNG path relative to this context directory and `sha256`: exact PNG bytes.
- `canvasPixels`, `rootPixelsTopLeft`, `worldPosition`, `drawSizeWorld` and uniform `pixelsPerWorldUnit`.
- `solidID`, `footprintWorld`: original authority, not alpha-derived bounds.
- `geometryLandmarks`: four exact original footprint corners with local XYZ, world XYZ and source pixels.
- `alignmentCheck`: the separate independent verifier evidence and its required hash binding.

The scene adapter must compute `anchor = [rootX/canvasWidth, 1-rootY/canvasHeight]`, keep `worldPosition` unchanged, use the recorded draw size, and apply the shared projection only to the root. Do not project the already projected image plane again. No center-to-corner root migration is required.

## Replay and verification

Pillow is the only third-party dependency. No NumPy, Blender, repository/sibling lookup or provider request is needed for replay:

```sh
python3 docs/review/building-perspective-detail-20261116/context/replay.py
python3 docs/review/building-perspective-detail-20261116/context/test_context.py
```

For a standalone packet, copy this directory elsewhere and run `python3 replay.py` followed by `python3 test_context.py`. `author.py` is historical one-time construction and provenance collection from this repository. It is not required for standalone replay, and must not be rerun over intentional manual mesh/UV edits.

Nine portable checks cover exact four-role inventory, retained 24-solid authority, unchanged roots, inverse-projected contact alignment, all vertex bounds, all source extents, source alpha and native/half sizes, all input/output/implementation hashes, root/size/landmark mutation rejection, unsupported affine-edit rejection, real UV/geometry/material edits changing pixels, and isolated standalone byte-identical rebuild. Raw first-run evidence is `tests-first.log` (eight checks), then `tests-source-guards.log` (nine checks). The independent checker computes inverse D108 from source coordinates without using the renderer's forward-projection function. No image appearance acceptance is inferred.

A bounded `swift test --skip-build --filter EnvironmentLibraryTests` execution also passed 22 Swift Testing tests in six related suites, as shown by `swift-focused.log`. This used the existing cached test binary, not a fresh build or native/simulator run. The initial XCTest section's zero tests is followed by the actual Swift Testing run and its explicit 22-test result.
