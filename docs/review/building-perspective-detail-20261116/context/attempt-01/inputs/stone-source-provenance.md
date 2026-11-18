# Stone painted-facade first sample

**Current final roof-layer follow-up:** coordinator authorized the final completeness layer at 09:50 UTC and issue246's bounded alpha repair at 09:57 UTC. See `FINAL-ROOF.md` for explicit 2.5D registration, preserved red evidence and the verified resolution. **All13 building tests +9 roof-layer tests and actual OBJ/MTL mutation checks pass in a clean copied packet.** The first facade-only packet is immutable in `attempt-01/`. Final actual-image coordinator review remains required. No further aesthetic edits are planned.

**Status: FIRST SAMPLE, bounded coordinator recommendation for a neutral ordinary scene diagnostic.** Coordinator inspected the actual comparison at 09:48 UTC and found the material/value structure and tall facade/entry substantially closer than the old squat polygon asset. This is not a finished-building verdict. No owner acceptance, native scene capture, production admission, or runtime readiness is claimed. No additional aesthetic pass.

Open `output/comparison.png` for the full immutable benchmark beside native/half logical source previews. `output/preview-alpha.png` is the full-resolution export. The assembled PNG is an output, **not the editable master**. `mesh.json`, `materials.json` and the three separate image materials are the source. `output/building.obj` + `building.mtl` + `textures/` are a portable editable interchange export.

## Source inspection and provenance

Inspected the actual supplied 1536x1024 opaque atlas before authoring. It contains three complete straight-on painted panels on magenta: two-window facade, complete door/entry facade with painted lamp and steps, and dark slate roof. Separate materials are deterministic crops of this independent generated panel atlas, not benchmark crops and not a flattened assembled building. Provider metadata says `action: edit`; it records the image-generation result and revised prompt, not a full input-request audit. No claim is made that the provider worked without a reference image.

Exact original bytes are retained in `inputs/atlas.png` and `inputs/provider.json`. Atlas SHA256: `efa98063a04e0814a8be533a3cf19fc337b6cc65eb50e3d6d0f0607f09769e75`.

Explicit half-open source rectangles `[left,top,right,bottom]`:

| Material | Authored rectangle | Actual crop size |
| --- | --- | --- |
| facade | `[29,120,552,894]` | 523x774 |
| door | `[594,120,914,894]` | 320x774 |
| roof | `[956,248,1508,796]` | 552x548 |

The requested nominal facade ratio was approximately 524:774. The exact half-open crop is 523:774. No color flood, segmentation, alpha bounds or heuristic inferred geometry is used. The gutters are excluded by these authored rectangles. Crops preserve their pixels without repainting.

The complete benchmark is copied byte-for-byte to `inputs/benchmark.png`, SHA256 `49aa35447230187e3eabe948cdc8eba6d6d465b2605d624e2cf7443f6cb69ffb`. The comparison displays the full image with uniform fit, never a crop or stretch. Reference and source panels are not claimed to be equal camera framing or a runtime comparison.

## New mesh and honest relief limits

This is a newly authored closed chamfered prism: 10 vertices, 7 polygon faces, explicit per-face UVs, floor and roof closure, consistent outward winding. It is not the rejected 144-component flat-color mesh or a retexturing of its 79-unit squat proportions.

- Footprint extent: 128x128 world units. Chamfer `c=39`.
- Visible facade widths: `128-39=89` units. Wall height: **132 units**.
- Facade width/height: `89/132 = 0.67424`, near the nominal `524/774 = 0.67700`.
- Entry width: `39*sqrt(2) = 55.1543` units, width/height `0.41784`, near the door material's `320/774 = 0.41344`.
- All foundation vertices contact `z=0`. No floating wall, stairs-as-contact substitution or apron inference.
- The facade material is explicitly copied upright to south and west. It is **not silently mirrored**. Hidden east and north reuse the same full panel, stretched to their authored 128-unit widths. This is disclosed reuse, not unique painted side art.
- Hidden east, north and floor surfaces are authored construction choices, not measured benchmark facts. `output/hidden-surfaces.png` is a reverse-source diagnostic, not a second candidate.
- The roof is one separately textured real planar closure. Floor reuses roof paint on its hidden underside. UVs on horizontal faces are world-plan coordinates divided by 128.
- **All cornices, pilasters, window trim, entry recess, lamp and stairs are baked image relief on flat mesh faces.** No tread/riser mesh or trim extrusion is claimed. The lamp's glow is baked, not dynamic light.
- Roof ventilator, parapet depth and separate stair geometry are absent benchmark details. The roof silhouette remains simple and planar. These limitations remain visible rather than filled by invented components.

## Registration derived from the chosen mesh

`output/registration.json` is freshly computed from actual mesh vertices plus the original virtual corner, not copied from the old source anchor. Projection is `u=rootU+5*(x-y)/sqrt(2)`, `v=rootV-5*((x+y)/(2*sqrt(2))+z)`. Extents are rounded outward to 10-source-pixel boundaries with 40-pixel padding.

| Field | New value |
| --- | --- |
| Source canvas | 1000x1200 px |
| Source root | (500,1160) px |
| Source scale | 5 px/world unit, uniform |
| Logical source size | 200x240 points |
| Half-size preview | 100x120 px |
| Bottom-left anchor | (0.5, 0.033333333333333326) |
| World root | (512,640,0), original virtual corner |
| Authoritative bounds | `[512,640,640,768]`, unchanged |

All ten mesh vertices have local/world/source landmarks. The virtual corner is collision-only: the visible chamfer contact is farther back. **The entire original 128x128 collision rectangle remains blocked, including chamfer and painted stairs.** No production geometry or collider was edited. The registration records review metadata, not runtime integration.

## Replay and checks

Executed on Python 3.14.5 with Pillow 12.3.0. Pillow is the only third-party runtime dependency. No NumPy, Blender, Swift, provider connection, repository lookup or sibling packet is needed for replay.

```sh
python3 docs/review/stone-painted-facade-20261116/replay.py
python3 docs/review/stone-painted-facade-20261116/test_source.py
```

To edit, change vertices/face UVs in `mesh.json`, or crop/material mapping in `materials.json`, or the source material atlas, then replay. `author.py` records the original deliberate mesh construction and can recreate its JSON. Do not rerun it after manual edits unless intentionally restoring that authored construction.

**13 focused tests passed**, see `tests-final.log`. Coverage: exact input/crop/output hashes, closed oriented mesh, UV reuse/orientation, proportions and z0 contact, unchanged collision metadata, independently projected registration/bounds, interior alpha coverage, no magenta, real mesh/UV/each-material mutations affecting rendered pixels, hidden-wall mutation visible only from reverse view, native/half sizes and OBJ counts. A standalone copied packet with only local source inputs executes in an isolated Python subprocess and reproduces all output bytes and the manifest exactly, without importing any repository or sibling files.

The first test run honestly caught transparent seams at texture borders. `attempt-01-before-sampler-fix/` retains the first renderer, outputs and failing log. The final renderer implements clamp-to-edge sampling with replicated edge texels. The alpha assertion was not weakened. This is a raster correctness repair to the same first source proposal, not a second visual design. Final output was inspected at full source scale and in the original/native/half comparison. The test run emits a Pillow `getdata` deprecation warning, not an assertion skip or failure.

No Swift tests, native runs, shared handoff/CI edits, commit or push were performed, as scoped. No production source/assets were touched. Technical success does not certify visual fidelity. Coordinator review must decide whether this first proposal is suitable for an isolated scene trial, particularly baked steps, missing roof details, facade reuse and proportions.

## Coordinator follow-up, 09:49 UTC

`clean-copy-exports.log` records **all 13 tests passing again in a copied packet**, followed by actual exported OBJ/MTL validation. `verify_exports.py` parses the exported OBJ vertex/UV/face records and MTL texture paths, loads the separate exported images, and reproduces the baseline pixels exactly. Mutating an actual OBJ `vt` changes rendered pixels while keeping geometry/alpha unchanged. Mutating an actual MTL texture path changes pixels. Mutating actual OBJ top-vertex heights changes the newly derived canvas. These are export roundtrip checks, not just JSON field tests or an external DCC application certification.

```sh
python3 docs/review/stone-painted-facade-20261116/verify_exports.py --clean-copy
```

The strict interior-coverage guard is unchanged from the red run. Only the renderer's out-of-image texture sampling was repaired, with original failed evidence retained. No hull correction or weakened assertion was needed. Complete mesh, per-face UVs, material maps and fresh sourceCanvas/root/uniformScale are exported. The coordinator's technical follow-up is satisfied for this packet. Remaining visible deficits are painted rather than geometric relief/steps, repeated facade paint, flat roof without ventilator or parapet depth, and no coherent native scene evidence. The recommendation is bounded to a neutral ordinary **scene diagnostic**, not native verification, owner acceptance or production admission.
