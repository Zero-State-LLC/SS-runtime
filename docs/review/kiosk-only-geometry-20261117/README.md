# Kiosk-only source geometry packet

**Review candidate only. No art acceptance, production admission, native integration, merge or release.** BP-001/007/012, T1045. Only this new directory was authored. No shared-tree commit was made.

## Start here

- `output/comparison-z100.png`, `output/comparison-z125.png`, `output/comparison-z140.png`: original full benchmark, immutable V9 native reference, current kiosk source proxy, and kiosk-only Z candidate. All source proxies are labeled and use unchanged V9 textured neighbors, actors, ground and depth.
- `editable/DIMENSIONS.md`: measured kiosk dimensions, full Z subdivision map and unchanged plan spacing to Player/Camera/neighbors.
- `editable/candidate-indexed-mesh.json`: editable6330-vertex/1582-face original-schema source. All original face indices, UVs, materials and XY coordinates retained. Only vertex Z and declared height change.
- `editable/current-indexed-mesh.json`: byte-identical original mesh.
- `z-map.json`, `build.py`, `export_editable.py`: editable parameter map and reproducible source implementation.
- `output/current-geometry.json`, `output/proposed-geometry.json`: complete current/candidate five-building face geometry. Four neighboring building dictionaries are exact equals, not the earlier multi-building proposal.
- `output/scene-contract.json`: entire retained V9 authority record, source bindings, ground and layer hashes, all71 depth items and nine proven offcrop actors.
- `output/manifest.json` and `editable/manifest.json`: exact input/output SHA256 closure. `reproduction/` retains a second deterministic build, not another aesthetic attempt.

## Why this candidate

Reuses ONLY the inspected earlier kiosk candidate: top132 to104, roof125 to100, parapet7 to4, crown24.217054 to10, entry27.116279..92.775194 to18..80. It addresses a vertically heavy crown and threshold above the retained18-high base without touching the128x128 plan, chamfer39, recess depths, material classes or mesh topology. See `DESIGN.md`, written before the first render.

The fixed Camera root remains16 units west of the kiosk envelope, Player96 units east. The north residence envelope meets the kiosk at[512,768]. This work cannot resolve those horizontal spacing relationships and makes no claim that height is the sole cause of the owner's concern.

## Reproduction and validation commands

Run from repository root, with the existing Python/Pillow environment. No new packages, models, assets or paid calls.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/review/kiosk-only-geometry-20261117/build.py --out docs/review/kiosk-only-geometry-20261117/new-empty-output
PYTHONDONTWRITEBYTECODE=1 python3 docs/review/kiosk-only-geometry-20261117/test_packet.py
swift test --scratch-path docs/review/kiosk-only-geometry-20261117/.swift-build --filter 'CameraMountSolidTests|CameraHousingArtTests|EnvironmentContractTests'
```

`build.py` refuses existing output paths. Fresh packet creation used default `output`, then `--out .../reproduction`, then `export_editable.py` (which likewise refuses to overwrite `editable`). The delivered validation suite checks the frozen output and reproduction directories. `diff -qr output reproduction` was run with full packet paths. Do not delete or overwrite evidence to rerun. Local Swift artifacts are ignored inside this owned directory.

## Artistic assumptions and next decision

Actual comparison PNGs at all three zooms were inspected by the implementing worker. The candidate makes the crown visibly thinner and lowers the visual entry relative to the unchanged Camera. Textured neighbors remain the same, including the northern wall revealed by the lower silhouette. This is a geometry hypothesis, not an independent coordinator verdict or acceptance.

Remaining uncertainty: the kiosk's broad plan, chamfer, narrow corner meeting and blocked base can still read oddly. Lowered doorway/window subdivisions may compress existing painted detail if their retained UV correspondence is later textured. The flat kiosk differs in material treatment from its textured neighbors intentionally. The18-high blocked-base supplement remains untouched and can still resemble a step/landing. Full original benchmark framing is not claimed to be an exact reconstruction.

Proxy omissions: native HUD/touch controls, Player shadow and kiosk raster roof vent. Camera field geometry is retained, but field raster and Pillow sampling are not SpriteKit parity. Original V9 native pixels are displayed only as a separate reference, never underneath a changed silhouette.

**Next:** coordinator inspects the actual three comparison images and decides whether this geometry warrants a separately bounded textured/native integration. No integration was performed or accepted here. Keep every neighbor unchanged in any such next step.
