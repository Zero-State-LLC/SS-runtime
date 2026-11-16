# South garment correspondence pilot 01

**Source-only, awaiting coordinator review. No family expansion or scene admission.**
Authority: `intent/2026-11-16-scene-method-approval.md` (owner approval09:31UTC), BP-002/007/012 and T1045. Work is confined to this directory. No source originals, production files, shared handoff, CI, Swift, commits or pushes changed by this worker.

## First preview and visual assessment

First preview was sent to the coordinator at09:36UTC, before additional visual work. `comparison.png` shows original neutral, tracked baggy target, and the new panel correspondence, with native/half raster approximations below. `index.html` preserves the exact source aspect at64x69.333333 and32x34.666667 CSS pixels. The source canvas is384x416 with six source pixels per logical point. Only one pilot exists.

Worker inspection of the actual comparison confirms the baggy folds, anatomical-left thigh patch (screen right), coat/hood/equipment appearance, and boots match the tracked baggy proposal. Output PNG SHA256 is exactly `a4ff7035ec256c613bc96eaf65b59a64e837c81adc895bcd4e5cd42e6f18a2a3`, identical to that target. This is deliberate exact front correspondence, not evidence of recovered depth. The patch remains vertically proportioned instead of stretched over the rejected inflated thigh shell. The baggy target's narrower shins relative to its north preference remain unchanged. No visual acceptance is inferred.

The strict **original-frame** identity test is honestly red. Nine of ten checks passed. The copied upper layer itself is byte-exact and the pilot exactly matches the tracked baggy target, but that inherited upper composition already differs from the original neutral frame at157 pixels above garment row200. See `IDENTITY-DEFECT.md`. This is not waived by the attractive preview or other green tests.

## Materially different method

The rejected repair tried to project mismatched paint onto enlarged thigh/calf and knee-shell volumes. This pilot does not import any of that renderer, mesh, material sampling profile or shell code.

Instead, `garment.json` defines four independently owned **front surface parameter domains**, each with35 editable vertices and48 explicit triangles. Every vertex has separate root-relative `position=[x,up]` and normalized material `uv=[u,v]`. Total:140 vertices and192 triangles. These are actual inputs to barycentric rasterization in `render.py`. The triangle-owner maps in `diagnostics/` identify every garment pixel's surface triangle. Real position and UV mutations change the rendered garment while preserving unrelated surfaces.

The input paint is the four tracked alpha-separated baggy components, exact crops of the tracked generated trouser sheet. They are not crops of the final character or benchmark. Each source material is Lanczos-rasterized at its registered part size, then sampled by the mesh with premultiplied bilinear interpolation. Neutral UV registration is exact, so interpolation does not widen or foreshorten the patch. Mesh edges bound parameter domains, while the material alpha supplies the irregular front silhouette. This is a textured front-panel mesh, not a watertight cloth volume.

**Honest authorship:** all panel topology and UV registrations here are newly authored from known front-component placement. Existing front paint is generated source paint, not original recovered trousers. There are no new painted regions, no procedural repainting, no image-editing service call, and no newly invented hidden paint. `hiddenSurfaces=[]` is explicit. Side, rear, cloth thickness, unseen folds and full rotation are unknown and not recovered. Upper body remains copied layered paint. This is not a finished whole-character volumetric master.

## Explicit source-to-root correspondence

Root: `(192,336)` in source pixels, equivalent to `(32,56)` logical points. Projection is `screen.x=root.x+position.x`, `screen.y=root.y-position.up`. This root is registration, not the bottom of the visible boots. Source alpha extends to row358. No contact shadow, terrain height or collision field is inferred.

| Owned front surface | Exact sheet crop, x0/y0/x1/y1 | Neutral screen rectangle | Material raster |
| --- | --- | --- | --- |
| anatomical right thigh |208,67,529,683|146,200 to194,292|48x92|
| anatomical left thigh, patch |614,69,943,685|189,200 to238,292|49x92|
| anatomical right shin/kneepad |221,747,487,1295|150,252 to186,326|36x74|
| anatomical left shin/kneepad |646,747,919,1293|194,252 to231,326|37x74|

Draw order is that table, then exact retained boots, then exact retained upper layer. Kneepads belong to the shin front material, not a hidden shell forced into view. The anatomical-left patch belongs only to the left thigh material. Upper/boot copied-layer SHA256 values are pinned in `provenance.json`.

Inspected tracked sources: baggy README/manifest/three-way comparison; bounded-neutral original frame through its exact tracked baggy copy; bounded-proportions README and `frames/00.png`; current south-repair README/verdict and ADAPT record. The proportion source uses12.5/14.5 segments at27 reach and is a moving pose, not this neutral's geometry. This front-only pilot makes no recovered3D segment-length, rig, motion, settle or release-frame claim. Existing releases05/13 are not touched or exercised.

## Editing and replay

Use an existing Python environment with Pillow and NumPy. Validated here with Python3.11.15 in the existing video-use environment. No dependency installation or paid service was used.

```sh
P=/Users/appliedalchemylabs/Developer/video-use/.venv/bin/python
D=docs/review/player-garment-correspondence-20261116
"$P" -B "$D/render.py"
"$P" -B -W error::ResourceWarning "$D/test_correspondence.py"
"$P" -B "$D/diagnose_identity.py"
```

The test command currently exits1 for the retained original-frame identity defect. `tests.log` is the original honest ten-test run, not an expected-failure disguise. Do not advertise this suite as passing.

Edit `surfaces[n].vertices[k].position` to change mesh contour/correspondence, or `.uv` to change material assignment. For example, the geometry mutation test moves left-thigh vertices20..24 right by5 source pixels, while the UV test changes left-thigh vertices10..19 by+0.12 in material U. These are isolated in-memory diagnostics, not additional published visual candidates. Material paths, raster sizes, triangles and ownership are also explicit editable inputs. `south-neutral.png` is an export and is never a rendering input.

`capture_inputs.py` was run once to copy exact files from a pinned git commit and construct the starting panel registration. Do not rerun it over hand edits. `provenance.json` pins every copied file's repository path, commit and SHA256. Ordinary replay needs neither git nor any repository siblings or external original directories. The standalone test deletes both flattened character references and still renders the exact south output from only component materials and retained layers, then restores comparison-only copies and byte-replays all gallery exports.

## Validation and gates

- Passed: exact baggy/patch correspondence, all source-copy hashes and sheet crops, boots/root/visible contact, every garment alpha pixel owned by a triangle, alpha-correct sampling, independent geometry mutation, independent UV mutation, unknown-version/degenerate-triangle rejection, standalone replay without flattened character inputs.
- Failed, preserved: strict original-neutral upper-frame identity. Inherited source mismatch, not a renderer sampling change. Coordinator notified to file a defect issue before resolving source authority.
- Actual browser opened this gallery in Brave. Jev handoff failed with provider401, then two direct measurement calls returned undefined. **Browser measured-size/grayscale verification is not claimed.** CSS specifies native/half aspect correctly, and actual raster comparison was inspected. No further browser retry after the repeated failure.
- No second visual attempt, family, side/rear, scene capture, animation, physical device, production or owner-acceptance claim.
- Coordinator must decide whether this honest front-only surface correspondence is suitable for the next review stage and resolve the original-frame versus copied-layer identity discrepancy. Do not populate the scene or expand the family before that review.
