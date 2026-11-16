# First painted Camera assembly

**One actual first painted assembly preview. Review only, not accepted.**

Open `preview-01/comparison.png` or `index.html`. The previous material-mapped `../pilot-01/` is preserved unchanged. This packet implements the coordinator's November 16, 2026 09:40 source-method refinement and 09:47 resume instruction. The first actual assembly was reported to the coordinator at 09:50 UTC before technical test completion.

## What changed

The source is now **three complete independently movable painted raster components**, not new procedural illumination of the sixteen-part construction model:

1. Uninterrupted charcoal pole, finial, collars and stepped base, including paint normally hidden behind attachments.
2. Complete cream bracket, mounting plate, neck, hood and smoked glass assembly.
3. Independent closed cream junction box.

`assembly.json` edits each exact crop, uniform scale, position, visibility and draw order. `inputs/` contains raw provider PNGs and verbatim response JSON. `preview-01/source-layers/` contains pixel-exact rectangular crops with original alpha. `preview-01/layers/` contains transformed component previews on the shared canvas. Removing or moving either attachment reveals the intact pole painting, verified at two actual overlap locations.

Only exact rectangular cropping, **uniform scale plus translation**, premultiplied-alpha resampling and compositing are applied. No source recoloring, contour warp, relighting, noise/dabs, benchmark cutout or manually redrawn paint. The original raw provider images are unchanged. Source images were supplied by the coordinator, generated as image edits with the benchmark as reference. These are not claimed to be independent geometry inferred from a finished-object cutout.

**Limit:** three neutral 2.5D layers, not sixteen independently editable parts or a full 3D master. Finial/collars are painted into the pole layer. Bracket/neck/hood/glass remain painted into the head layer. Internal silhouettes, materials and illumination are baked inside each component. Back faces, physical depth and pan frames are not supplied or inferred. The former sixteen-part vector source remains prior construction only and is not used by this renderer.

## Actual source and alpha inspection

Both provider PNGs are **1254 × 1254 RGBA**, not assumed 1024 square. Real alpha ranges 0–255. Their black appearance in some viewers is transparent background, not a matte. Interior alpha is mostly 252–254 rather than mathematically opaque. No alpha cleanup or thresholding is applied to pixels.

| Component | Exact source crop | Retained source pixels with alpha ≥16 | Outside-crop pixels omitted | Actual omitted alpha |
|---|---|---:|---:|---:|
| Pole | `[250,10,540,1220]` | 164,203 | 460 | 1 only |
| Head | `[680,380,1090,770]` | 89,675 | 592 | 1 only |
| Box | `[425,295,815,930]` | 193,160 | 266 | 1 only |

The diagnostic threshold 16 measures completeness, not a render cutoff. **Every source-region pixel with alpha ≥16 is retained**, and the crop borders contain at most alpha1. Original source padding contains isolated alpha1 dust; cropping omits the counts above while retaining the complete subject paint and all original in-crop alpha. `source-audit.json` records complete counts, exact origins and SHA256 hashes. All four raw PNG/JSON files were also byte-compared directly to the supplied originals on this machine.

## First visual inspection and unresolved limits

Actual `comparison.png` and `alpha-on-white.png` inspected at 09:50–09:51 UTC. Painterly value separation and material structure are visibly stronger than the rejected mapped-material pilot. This is a relative observation, **not source fidelity or acceptance**. The original full reference remains unchanged and is shown beside a clearly labeled comparison-only crop.

- The generated pole base is proportionally wider than benchmark at equal pole height. No nonuniform squeeze disguises this mismatch.
- **The rendered pole reaches the left canvas edge.** Its alpha≥16 geometric bounds begin at X≈0.04465 within the 180-pixel canvas, but resampling leaves left-edge alpha up to215. Source crops are complete; assembled antialias margin is **not satisfied**. The first preview is preserved, not silently repaired or called unclipped. `source-audit.json` records this distinct failure honestly.
- Native/half highlight detail can look stippled. No smoothing retry has been rendered.
- The background image is an offline ordinary paving context, without synthesized shadow, HUD or field. It is not an actual native runtime or whole-scene capture.

Source canvas180×450; exact uniform logical scale96/418 produces rounded canvas42×104 native and21×52 half. The scale is applied with equal X/Y coefficients, not by stretching to rounded dimensions. Ground root `[46,427]` is an inherited review coordinate, not production collision/registration proof.

## Replay and validation

Existing Python3 and Pillow only. No installation or external service. From any directory:

```sh
python3 -W error /path/to/painted-assembly/replay.py --out /path/to/new-replay
python3 -W error /path/to/painted-assembly/test_assembly.py
python3 -W error /path/to/painted-assembly/audit.py
```

To edit a layer, copy `assembly.json`, change `uniformScale`, `position`, `visible` or order, then pass `--model /path/to/edited.json --out /path/to/diagnostic`. Keep first-preview files immutable. `audit.py` regenerates only source evidence JSON, not artwork.

**Actual tests: 12 passed in1.530s with all warnings treated as errors**, `tests.log`. Coverage: actual RGBA/provider metadata, pixel-identical complete source crops, rejection of opaque/RGB substitutes, rejection of clipped source paint, isolated head movement, intact hidden pole under both attachments, rejection of nonuniform transforms/new shading/external source, only the two painted PNGs read by rendering, clean standalone replay, input/output tampering, native/half dimensions and zero RGB under alpha0, and explicit reporting of the unresolved left-edge margin.

Standalone replay copied only `assembly.json`, `replay.py` and six local input files into a new directory without repository or siblings. It reproduced **all14 PNG exports plus manifest bytes exactly** under the same Python/Pillow environment. No image edit variants were published by mutation tests. The parent pilot's original7inputs/16components/38exports also reverified unchanged.

## Gate

No owner/source/production acceptance, 3D completeness, native capture, collision/field change, inferred animation, commit or push. No shared handoff, CI or production edits. One painted assembly preview exists. Coordinator review decides whether a further bounded repair is warranted, especially the base width and left-edge padding.
