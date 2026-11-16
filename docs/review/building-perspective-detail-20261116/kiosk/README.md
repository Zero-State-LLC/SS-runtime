# Kiosk architectural relief, first sample

Status: **FIRST SAMPLE, awaiting coordinator visual review. Not visual acceptance, not production admission.**

Scope is `intent/2026-11-16-building-perspective-detail.md`. Every authored file is new under this directory. No native/simulator run, production edit, old packet edit, shared gallery/CI edit, commit or push was performed.

## Review first

- `output/first-sample-comparison.png`: full uncropped benchmark plus exact native 200x240 and half 100x120 source previews. This is a source plate, not a native runtime capture.
- `output/source-full.png`: 1000x1200 RGBA source with transparent background and separately composited existing painted ventilator.
- `output/building-alpha.png`: geometry-only building render, without the ventilator.
- `output/native-alpha.png` and `output/half-alpha.png`: uniformly reduced RGBA previews.
- `output/mesh.json`, `output/building.obj`, `output/building.mtl`, `output/textures/`: editable explicit world-space vertices, face UVs and independently painted material assignments.
- `geometry-controls.json`: authored elevation breakpoints and physically meaningful inset controls.
- `output/registration.json`: registration, canonical footprint and exact projected vertex landmarks.

## Diagnosis and bounded correction

I inspected the actual `scene-qa-framing-20261116/native-capture-v6/source-scene-candidate-ordinary-z100-native.png` and the full `inputs/benchmark.png`, not only a building crop. V6's central building has a flat tiled roof flush with its painted top trim and elevation-painted depth cues. The benchmark visibly distinguishes coping top, roof recess, window reveals and entry depth. The surrounding buildings in v6 have different projected proportions and painterly scale, but they are outside this worker's ownership and are not hidden or altered here.

The existing mesh basis is **not demonstrated wrong**. Its `replay.py:14-17` maps `(x-y)/sqrt(2)`, `(x+y)/(2sqrt(2))`, with upright z and uniform source factor5. This sample preserves that basis exactly. It does not rotate, shear or vertically rescale the building to imitate the benchmark's different view/composition.

The old 132-high, chamfer39 prism is the authority for the sample envelope. The revised geometry remains entirely inside its 128x128 footprint. The roof surface is lowered from132 to125 while coping remains132, with a genuine3.2-wide inset parapet, explicit horizontal coping faces and inner walls. Cornice bands, corbel-depth zones, pilaster/window reveals and door recess now have named geometric returns rather than relying only on the elevation's painted depth. The doorway's three depth transitions create horizontal upward-facing entry treads within the blocked chamfer, not a walkable apron outside the solid.

This corrects the **flat-plane-only architectural correspondence**, not every perspective cue in the paint. The unchanged atlas was authored as front elevations. Fine bevel shading, some tapered painted stair edges, the lamp, mullion bevels and weathering remain baked. The real ledges/reveals now project from world geometry, but this is not a fully relit, perspective-free material or a sculpted historical building model. Cornice details remain regular/repeated and the building is still symmetric compared with the benchmark's cropped corner composition. These are material fidelity limits, not grounds to alter D108.

## Source provenance and honest limits

**ADAPT decision:** reuse the independently painted atlas and explicit original footprint, not legacy gameplay source or benchmark pixels. Exact source: `docs/review/stone-painted-facade-20261116/inputs/atlas.png`, unchanged half-open crops from its `materials.json`. `inputs/baseline-mesh.json` is a byte-identical copy of its `mesh.json`. `baseline_renderer.py` is a byte-identical copy of its `replay.py`, reusing registration/texture/export/vent utilities. Its old CLI is not the supported entry point for this packet. New mesh authoring and depth-buffered rendering are in `replay.py`.

No random texture, generated replacement building or benchmark pixel sampling is used. All texture appearance comes from the preserved source atlas and existing independently painted ventilator. The ventilator remains a separately registered **2.5D raster layer**, not mesh geometry, with anchor z rederived to125. Its existing alpha repair policy is unchanged. It is not included in `building.obj`.

Mesh faces are explicit editable surfaces, not a watertight manufacturing solid. Adjacent elevation corner-return seams are not claimed manifold-certified. Hidden elevations reuse the same atlas stretched over the original128-unit edges. Existing baked shading is not recomputed for new geometric normals. Collision remains the original full blocked128x128 rectangle, including the chamfer and entry.

## Registration

| Field | Value |
| --- | --- |
| canvasPixels | `[1000,1200]` |
| rootPixelsTopLeft | `[500,1160]` |
| worldPosition | `[512,640]` |
| drawSizeWorld | `[200,240]` |
| uniform source scale | `.2` |
| source pixels/world unit | `5` |
| authoritative bounds | `[512,640,640,768]` |
| maximum z / chamfer | `132 / 39` |
| roof z / parapet width | `125 / 3.2` |

Canvas/root are recomputed from projected authored vertices plus virtual origin, 10-pixel outward rounding and40-pixel padding. They are not fitted from raster alpha. Source pixels map to scene points by the same `.2` factor in both axes. Every geometry vertex has a recorded local/world/source landmark. Tests independently derive the formula, canonical ground witnesses, basis slopes and uniform-scale bounds.

## Replay and verification

From any working directory, using Python3 with Pillow:

```sh
python3 docs/review/building-perspective-detail-20261116/kiosk/replay.py
python3 docs/review/building-perspective-detail-20261116/kiosk/test_kiosk.py
```

For a completely isolated replay, copy this directory anywhere and run `python3 replay.py` there. The test suite itself copies only this packet's authored scripts/configuration and `inputs/` into a new directory, with no repository or sibling imports, then compares every manifest output byte. `--out PATH` selects a different output directory. The manifest hashes all operative source/material inputs and every exported output, excluding itself.

`tests.log` records12 passing tests, including independent exact projections, envelope invariants, real upward-facing treads, active geometry/UV/material mutations, pixel-identical exported OBJ roundtrip, actual exported vertex mutation, alpha, native/half dimensions, manifest integrity and isolated output-byte replay. `original-byte-audit.json` records110 original tracked stone-packet/capture files compared byte-for-byte with HEAD. The optional repository-local command `python3 audit_originals.py` refreshes that witness and is intentionally not required for isolated replay.

A return-face winding defect in the initial technical render was found during source-resolution inspection. `attempts/01-return-winding/` preserves its script, full render, comparison and manifest. The corrected first sample fixes signed jamb normals and upward tread normals without a new aesthetic design pass. No assertion was relaxed. No unfiltered Swift retry was run, as prohibited by the active intent and existing failure gate.

**Next gate:** coordinator visual review of this first sample. At most one subsequent bounded aesthetic correction is authorized. No source or scene acceptance is inferred from passing tests.
