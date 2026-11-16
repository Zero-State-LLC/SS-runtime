# Stone, directly authored mesh and surface paint

**Review-only source. Coordinator verdict at November 16, 2026 08:44 UTC: NOT RECOMMENDED. Painterly fidelity remains unproven and author self-review is a mismatch. Do not infer acceptance from topology or replay checks.**

Technical publication repair retains immutable inherited inputs locally under `inputs/`, with exact origins and hashes in `inputs/provenance.json`. Current author/replay entrypoints no longer require the unpublished older stone packet. Run `python3 docs/review/stone-surface-authored-20261116/verify_clean_copy.py` for isolated authoring/replay verification with only the tracked benchmark and arena contract available outside this packet. See `COORDINATOR-VERDICT.md` and `clean-copy-verification.log`. Historical attempt directories are immutable evidence, not current replay entrypoints.

Authorized by `intent/2026-11-16-source-to-scene-continuation.md`, owner approval 2026-11-16 08:19:29 UTC, slice 5, BP-001/005/007/012 and T1045. Read `create-game-assets` and trail before implementation. This worker changed only this new directory, with no runtime/App/AppTests/CI/shared documentation edits, native runs, dependencies, commits or pushes.

## Actual samples and changed method

First actual source/native/half comparison was delivered at 08:27 UTC and is immutable under `attempt-01/`. Current root exports are the bounded second authored attempt, delivered at 08:33 UTC. No third visual-design attempt was made. The later area-downsampling correction changes normalization only, with identical full-resolution source pixels.

This is not another procedural-weathering variation:

- Old filled upper shell and narrow window grids were removed. The registered foundation is retained, while a new inset closed core, four broad cavities, individually dimensioned beveled piers, stronger cornice returns and inset doorway are explicit XYZ meshes.
- Window backing planes are 6.1 world units behind the front reveal. The door leaf is on x+y=31.3, behind the entry piers at x+y=18. These are actual source geometry separations, not painted panels over the old solid shell.
- `mesh.json` contains 144 closed components. `author_mesh.py` is the retained one-time editing recipe, not called by either replay entrypoint. Every hidden back/bottom/return is deliberately authored, not recovered from the cropped reference.
- `surface-paint.json` has 51 named, editable surface-paint definitions. Explicit polygon and edge coordinates replace the old random mineral-noise generator. Common underpaint/edge strokes are shared, with named surface-specific additions, not a tiled whole-building texture.
- `brushwork.json` contains individually positioned translucent strokes with explicit paths, colors, widths, opacity and edge softness. There is no random scatter or noise. `surfaces/*.svg` exposes editable paint paths, while `surfaces/*.png` can be hand-painted directly.
- Each face maps its paint once, with no repeating world-space material tile. All geometry uses one normalized directional source light from `model.json`: direction [-0.72,-0.28,0.64], ambient 0.52 and diffuse 0.48. This proves common lighting within this source only, not cross-asset scene-lighting agreement. There is no ray-traced cast-shadow/global-illumination claim.
- The complete roof is retained. A small ventilator is authored from the visible reference subject, with explicitly authored dimensions and hidden surfaces. It is not a measurement of the benchmark roof or a gameplay addition.

## Review now

Open `index.html`, `comparison.png`, `comparison-grayscale.png` and `preview-alpha.png`.

The unchanged original is uniformly fit to 704×396, without cropping. Candidate source is shown at 224×192 logical canvas, 112×96 half canvas and 1.4× diagnostic size. No separate X/Y scaling or roof-hiding crop is used. These are source previews, **not native runtime scene captures**.

Author self-review: deeper openings, larger stone piers and layered cornice are a substantial structural improvement. However roof/glass and pigment shapes still read angular and model-like rather than the benchmark's painterly worn stone. The entry remains compact relative to the reference composition, and no integrated street context has established material cohesion. The half-size image verifies legibility/normalization only. No automated color/geometry metric can grant art acceptance. A third same-method visual pass is stopped pending coordinator method review.

## Editable replay

From the repository root:

```sh
# Read saved mesh and explicit paint sources. Does not regenerate geometry.
python3 docs/review/stone-surface-authored-20261116/replay.py
# Directly consume hand-edited mesh plus hand-painted surface PNGs.
python3 docs/review/stone-surface-authored-20261116/replay_painted.py
# Focused source checks, not a visual-acceptance score.
python3 docs/review/stone-surface-authored-20261116/test_source.py
```

`replay_painted.py --mesh YOUR_MESH.json --surfaces YOUR_PAINT_DIRECTORY --out YOUR_PREVIEW.png` preserves direct mesh/PNG edits. `replay.py` regenerates the surface PNG/SVG exports from JSON paint definitions, so do not use it to preserve unmerged manual PNG changes. SVGs are editable paint exports, not an independently verified browser rasterizer. Exact replay authority is the Python/Pillow implementation.

## Registration and authority

World root (512,640,0), source root (560,885), 1120×960 canvas, 5 source pixels per world unit, uniform scene scale 0.2 and bottom-left sprite anchor (0.5,0.078125) remain unchanged. The mapping is `u=560+5*(x-y)/sqrt(2)`, `v=885-5*((x+y)/(2*sqrt(2))+z)`. Uprights remain vertical. No bitmap perspective warp is involved.

`registration.json` retains the exact original 128×128 rectangle at x=512…640, y=640…768 and distinguishes authored foundation B/C/D corners and E/F chamfer endpoints from virtual collision-only A. The registered foundation, not the new roof, supports those vertices. C and other hidden geometry are explicitly authored. `measuredReferenceGeometry` remains null. Source/world correspondence is verified authorship/projection, not a claim of measured reference 3D geometry.

Separate `stairs-alpha.png` and `building-alpha.png` retain the same root and scale. The three stair meshes remain inside the original blocked rectangle and are separate from the building group. Decorative trim can overhang the registered foundation, but it does not expand collision. The visible chamfer, door and stairs stay blocked by the unchanged rectangular simulation solid. This does not support new chamfer/stair gameplay. Independent group exports are not proof of arbitrary native painter-order/occlusion behavior.

## Honest failures and verification

- `attempt-01/topology-check.log`: the new outward signed-volume guard found inward winding in the inherited stair geometry. The previous source checked paired-edge closure but not outward volume. The new source reverses the stair faces, preserving old packets and assertions. `topology-check.log` records the successful retry.
- `attempt-02-before-alpha-fix/tests.log`: eight of nine tests passed. Strict alpha-margin validation rejected a half-size Lanczos halo touching y=0 despite a raw source top margin of 26 pixels. Root and geometry were not moved. BOX area downsampling removes that negative-lobe halo without an alpha threshold. Full-resolution source pixels remain identical. Original exports and failing log are retained.
- `painted-direct-replay.png` was produced through the actual saved-mesh plus painted-PNG entrypoint and `cmp` confirmed byte equality to `preview-alpha.png`.
- `tests.log`: **9 tests passed in 26.837 seconds**. The guards cover positive closed volumes, actual recess depths, unchanged fixture/reference, exact wall-base correspondence, vertical/ground projection, separate bounded stairs, shared source lighting, alpha on all six source/group/size exports, visible effects of actual mesh/paint edits, and byte-identical replay of views/registration/all paint exports.

Technical source status, coordinator visual recommendation, owner acceptance and production admission remain separate. Owner acceptance, native readiness and production admission are false. No local unfiltered Swift suite or native run was attempted.
