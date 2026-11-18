# Source implementation verification

Status: **SOURCE IMPLEMENTATION COMPLETE, NOT NATIVE EVIDENCE OR ACCEPTANCE.** BP-001/007/012, T1045. Owner approval authorized one geometry proposal only. All work in this lane is under `docs/review/architectural-scale-20261117/source/`. No commit, push, production edit, native execution, new dependency, texture generation or aesthetic variant was performed.

## Delivered source files

- `build.py`: exact baseline mesh extraction, explicit fixed Z subdivision maps, untextured mesh rasterization, retained scene reconstruction and three zoom comparison sheets.
- `output/current-geometry.json`, `output/proposed-geometry.json`: full editable faces/vertices for kiosk, residential-west, residential-north, civic-west and civic-dais. Every XY coordinate and topology remains unchanged.
- `output/registrations.json`: world roots, source root pixels, canvases and draw sizes for both arms.
- `output/dimensions.json`, `DIMENSIONS.md`, `massing-measurements.json`: all vertical changes, Player-relative ratios, doorway limitations, roof/cornice massing, footprint width/depth and complete Z maps.
- `output/current-z100.png`, `current-z125.png`, `current-z140.png` and matching `proposed-*`: raw2112x978 scene frames, exact704:326 aspect. Separate `*-labeled.png` files carry labels.
- `output/comparison-z100.png`, `comparison-z125.png`, `comparison-z140.png`: current/proposed source proxies alongside full uncropped original benchmark and unchanged V9 native capture.
- `output/scene-contract.json`: retained actors/supplements, all71 depth items/order/constraints, field inputs, source-ground square crop, explicit omissions and offcrop proof.
- `output/manifest.json`:75 immutable input hashes and46 output hashes. Final manifest SHA256 `cfa00dd646449a95a20153626c453e005e43de4c2db548c6a1ae6f7066f5a629`.

## Exact commands and observed results

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/review/architectural-scale-20261117/source/build.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/review/architectural-scale-20261117/source/report_dimensions.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/review/architectural-scale-20261117/source/test_source.py
```

Final full build completed with exit0, recorded in `build-final.log`. Report generation completed. Final test command completed with exit0: **18 tests, all passed**, recorded in `tests-complete.log` (4.563s in this run).

Checks include exact baseline extraction, monotone nonuniform Z-only reauthoring, all five sources, retained roots/footprints, every context face's authoritative normal/culling, independent roof-interior pixels, independent square-ground UV samples, raw aspect, Player/Camera layer identity, full71-item retained depth oracle/order, exact recomposition without native-screenshot substrate, old input hashes, complete benchmark pixels, qualified roof area/cornice volume formulas, and fail-closed output overwrite.

Final geometry documents, dimensions and registrations are byte-identical to the initial aesthetic proposal. The two kiosk mesh rasters and all12 Player/Camera layers are unchanged across every render. Context mesh pixels differ only because the explicit-normal adapter defect was corrected. Corrected ground bytes are unchanged by that normal correction.

No Swift/native command was run by this source-only lane. Coordinator owns broader project validation, gallery, independent image review, publication and handoff. The proxy does not establish native rendering equality, physical scale certification or product acceptance.

## Preserved failures, not aesthetic alternatives

1. `attempt-01-ground-uv/`: first complete output/build/test/log, incorrect square-source Y sampling and labeled-frame packaging.
2. `attempt-02-face-normals/`: ground-corrected intermediate, but context faces incorrectly used winding instead of explicit source normals.
3. `tests-normal-regression-before.log`: independent roof test demonstrably fails on the archived missing-roof intermediate.
4. `probe-failure/`: final-render test initially used a dais pixel actually covered by the retained rail. The red test/log remain. Final analytic rail-ray test checks that occluded pixel stays cornice and a genuinely clear platform point stays roof. No image change was needed.

See `TECHNICAL-CORRECTION.md`. Coordinator filed issue255 for validator gaps. None of these corrections altered the fixed geometric proposal or erased failed evidence.

## Source-proxy boundary and remaining gates

The compositor begins with registered source ground and layers, not painted-over textured buildings. No ghost-building pixels can survive under a reduced silhouette. Ground uses tileUnits2304 and source rect[0,0,1,2/3], as native source code specifies. Retained field geometry is reconstructed, but native field fill/antialiasing and SpriteKit sampling are not byte-proven.

Native HUD/touch controls, runtime Player shadow and raster-only kiosk roof vent are explicitly omitted from both source arms. Their authority is not changed. Untouched V9 native panes retain the real native rendering. Residential and civic meshes have no explicit doorways, so their clearance is not invented. All boundaries are disclosed rather than silently presented as native pixels.

Next gate belongs to coordinator/owner: review the one proposal before any detailed material work or native execution. No automatic aesthetic retry is authorized.
