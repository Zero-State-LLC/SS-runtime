# Baggy south neutral source, PROPOSED

Owner request 2026-11-16 03:41:04 UTC: make the south trousers match the preferred baggy north silhouette. This packet changes only the proposed silhouette. It does not accept the generated north bag, coat, material or camera. It is not native, simulator, animation or production evidence.

## Deliverables

- `south-baggy-neutral.png`: 384 x 416 RGBA proposal.
- `three-way-comparison.png`: original south, proposed baggy south and baggy north reference (attempt 01), at 2x. Hip y200, knee y265, boot top y318 and ground root (192,336) are annotated.
- `layers/`: four trouser layers plus `original_boots.png` and `original_upper.png`.
- `components/`: exact RGBA crops from the generated trouser sheet.
- `baggy-south.json`: provenance, hashes, transforms, retained pixel counts and width measurements.
- `test_source.py` and `tests.log`: 7 source guards, all passing.

## Method

- Trouser sheet `1794800681673-ig_07cd...a.png` (native image_generation, copied to `source/` with its metadata). It is cut into four alpha-separated crops: upper left anatomical RIGHT thigh, upper right LEFT thigh with the cloth patch, lower left RIGHT shin with knee pad, lower right LEFT shin with knee pad.
- Each part gets one uniform Lanczos scale (thighs 0.15, shins 0.135) and a translation. There is no warping, mirroring, repainting or stretching of the old south bitmap. In the south view, anatomical right is on screen left.
- Boots: the original approved frame-00 pixels inside the original boot-layer alpha, rows y >= 318 only (laces and leather), copied exactly (1,636 px).
- Upper body, coat, hands, hood and equipment: the original editable body-source layers. Every pixel that is opaque in both the layer and frame 00 is copied exactly from frame 00 (21,590 px).
- Thin original trouser pixels are not used. A guard checks that every opaque output pixel belongs to a new trouser layer, the boots or the upper layers.

## Measured widths (opaque runs, px, not thresholds)

| Row | Original south | Proposed baggy south | Baggy north ref |
|---|---|---|---|
| 235 (thigh) | 62 joined (coat overlap) | 49 / 52 | 49 / 48 |
| 255 (lower thigh) | 28 / 28 | 45 / 47 | 49 / 47 |
| 275 (knee/shin) | 33 / 33 | 36 / 41 (pad edges) | 45 / 45 |
| 295 (shin) | 29 / 29 | 35 / 35 | 42 / 42 |
| 310 (cuff) | 22 / 22 | 32 / 32 | 29 / 30 |

The alpha y-range is 39-358 for the original and the proposal. The proposed shins are narrower than the north reference (35 vs 42 at row 295) because one uniform scale has to keep the original pose length from knee to boot top. Buffalo has no restored target metrics, and the north reference is an unaccepted sample, so these numbers are comparison facts only.

With buffalo's convention (opaque means alpha > 128) and the active north attempt 01 (sha `0a6e15bd2aa8…`, the same file as `attempts/01-uniform-0.4`; see `../player-north-source-20261116/baggy-leg-landmarks.json`, PROPOSED):

| Row | Proposed south | North |
|---|---|---|
| 236 | 48 / 56 | 48 / 52 |
| 256 | 41 / 41 | 47 / 43 |
| 276 | 36 / 36 | 41 / 43 |
| 296 | 31 / 31 | 38 / 38 |
| 312 | 28 / 25 | 27 / 27 |

The thighs and cuffs are close. The shins are 5 to 7 px narrower than the north. Widening them with a uniform scale would lengthen the shin and move the knee pad. That trade-off is left for the coordinator's review.

## Reproduce

```sh
PY=/Users/appliedalchemylabs/Developer/video-use/.venv/bin/python
cd docs/review/player-baggy-south-source-20261116
"$PY" -B assemble.py && "$PY" -B test_source.py
```

## Limits

- Neutral only. No animation should be generated until the neutral is reviewed.
- The trouser paint is generated, not original master paint.
- The knee-pad position comes from the generated shins. It is not the original pad position.
- The hip, knee and ankle pivots are 2D annotations.
- Original inputs are read only. No files were modified under the original roots, and originals 5 and 13 are untouched. The packet does not re-run the 1,012-file hash audit.
Nine portable source guards now cover original-copy provenance against the previously published1,012-file inventory, reconstructed upper/boot layers, exact full composition, dimensions, anatomical patch side and retained pixels. The coordinator independently reran all nine successfully on November16 at04:09UTC. This replaces the initial seven-test count above. The original upper and boot inputs required for verification are retained under `source/original-upper/` and `source/original-boots/`; no machine-local original is required by these guards.

Coordinator visual inspection of `three-way-comparison.png` confirms the proposal retains the original upper body and boots while increasing trouser volume. South shins remain visibly narrower than north, and knee-pad placement differs. This is a reviewable proposal, not a consistent-family acceptance verdict or permission to animate it.

No shared production files or original-source bytes were changed.
