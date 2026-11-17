# Preserved-material textured kiosk candidate

BP-001/007/012, T1045. This is the **textured source for reversible playable-runtime review**, not an accepted asset or a new native capture. The preceding flat native comparison remains frozen under `../capture-01/`.

## Exact integration binding

Use `output/candidate/source-full.png`, SHA256 `5a1c7fa1cf23d7bd85bc5676b4a0e297662071404cbb3ec454c9153a7d97c931`.

- Source canvas:1000x1060 pixels.
- Root from image top-left:[500,1020].
- World root:[512,640], unchanged.
- Draw size at zoom1:[200,212] world units, multiplied uniformly by presentation zoom.
- Sprite anchor bottom-left:[0.5, 1-1020/1060]. Use the exact fraction, not a rounded constant.
- Original blocked rectangle:[512,640]..[640,768]. No collision/target/Camera fields are inferred from these texture dimensions.
- Complete authored ground correspondence and virtual chamfer-corner disclosure: `output/candidate/registration.json`.
- Machine binding: `output/bindings.json`.
- Manifest SHA256: `647ec749a5a87bb1e24135ebc758655a1ccd84ca003020e95b0c3a0f3e199953`.

This1000x1060 canvas is a new correct registration for five source pixels per world unit. Do not pair it with the prior flat568x608 registration, stretch it into the original200x240 draw size, or recenter it from alpha bounds.

## What changed and what did not

The exact previously delivered mesh `../../editable/candidate-indexed-mesh.json` is reused byte-for-byte, SHA256 `e24272946eada65ed0b365ba5462f007bb7a5f9117e4d67e158b78c47d1d55ec`. Every face index, UV, material class, XY coordinate, root, footprint and hidden-surface declaration remains unchanged. Only the already-authored Z map differs from the current mesh. There was no new geometry or aesthetic retry here.

The existing V9 atlas and three explicitly authored material crops are reused without new paint or sampling from benchmark pixels. The same retained per-pixel-depth triangle renderer generates the output. The original separately painted roof vent is restored, with rootXY[78,85] and scale unchanged. Its local anchorZ follows roof surface125 to100. It remains a view-dependent2.5D layer, not a new3D mesh or gameplay entity. Existing exact three-pixel alpha residue normalization remains unchanged and disclosed in the retained roof specification.

`output/current/` is a positive reconstruction control. Its body, vent and full source RGBA match all three retained V9 output images exactly. This is source-image parity, not a claim that the new textured candidate already has native scene evidence.

## Inspection and limitations

At02:48UTC the implementing worker inspected `output/source-comparison.png` against the uncropped original benchmark and opened the full1000x1060 candidate. The candidate has a lower, thinner crown while preserving the same overall facade divisions, door, stone courses and vent. Its real textures now make the diagnostic geometric change assessable as a building rather than a gray block. No visible canvas clipping was found, and an independent alpha-edge check confirms transparent margins.

The lowered crown compresses retained cornice/bracket paint. Broad footprint, repeated window/facade surfaces, baked shading, conspicuous entry steps and unchanged horizontal adjacency remain. The V9 blocked-base supplement is not baked into this source and must remain separately bound in any scene comparison. A new playable/native inspection must evaluate that combined reading. **Overall benchmark NOT MET. No art acceptance or production catalog admission.**

## Validation

`test_textured.py` passed12tests at02:48UTC, including a fresh independent candidate rerender, exact current3-layer parity, full source/output hashes, analytical registration/ground projection, UV/material/XY/Z mutation rejection, unchanged vent parameters except roofZ, real alpha, nonclipping, and existing-output refusal.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/review/kiosk-only-geometry-20261117/native/textured/test_textured.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/review/kiosk-only-geometry-20261117/native/textured/build.py --output NEW_EMPTY_DIRECTORY
```

`output/` is the first successful render. `reproduction/` is the identical deterministic rerun, not a second art attempt. Preserve both and raw logs. No source/render/test assertion failed. The retained renderer emits Pillow `getdata` deprecation warnings, which remain logged. Its immutable code was not edited to suppress those warnings.

Coordinator owns App/resource integration and publication. This worker changed no App, package, test contract, source catalog, neighboring building or existing evidence file. The source is ready for reversible review integration, not merge/release/deployment or physical certification.
