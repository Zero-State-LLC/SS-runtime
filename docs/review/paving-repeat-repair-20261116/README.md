# Paving Repeat Repair Record, 2026-11-16

**Slice:** `slice4` per `intent/2026-11-16-benchmark-faithful-ten-slices.md` (owner 05:56:35 UTC)

**Contract authority:** `d1bfd1c` whole-scene

**Status:** Attempt1 REJECTED and preserved. Separate `revision02/` corrects the diagnosed blending defect but remains unaccepted, with recognizable repetition and no native integration.

**Scope:** Review packet and portable CI guards only. No AppTests or production code changed. Published for diagnostic review, not art admission.

---

## Source material (muted original — preserved byte-for-byte)

| Field | Value |
|---|---|
| Bundle name | `whole-scene-muted-paving.png` |
| Path | `AppTests/WholeSceneAssets/whole-scene-muted-paving.png` |
| SHA256 | `c0decdab226512a790ddecf49cf703c9fc736f7943f11bc364b76b111b7c3125` |
| Pixels | 1254 × 1254, RGB (colortype=2), 8-bit |
| File size | 2 689 986 bytes |
| Design spec | tileUnits=128, 4×4 slabs per tile, 32 world-units per slab |
| Chunk markers | caBX (JUMBF provenance), IDAT (zlib compressed) |

The original file is **not modified**. All generated material is in this folder only.

---

## Seam diagnostics — original

| Edge pair | Mean abs diff (all 3 channels) | Max diff |
|---|---|---|
| Top vs Bottom | 14.28 / 255 | 73 |
| Left vs Right | 12.90 / 255 | 63 |

The original has non-zero opposite-edge differences. At tileUnits=128 this produces a step at every tile boundary when tiled.

---

## Candidate procedure (editable, deterministic)

**Method:** 3-pass cosine-ease edge-forced blend, bw=20 pixels.

**Pass 1 — top/bottom:** For each column x, compute `target[c] = (top_pixel[c] + bottom_pixel[c]) // 2` for each of the three RGB channels. Apply a cosine-ease ramp over rows 0–19 (top) and rows h-20 to h-1 (bottom), blending from fully-target at the outer edge to fully-original at row bw. Source is `px_orig` throughout.

**Pass 2 — left/right:** Same procedure on columns, using `px_orig` as source. This overwrites corner pixels (x<20 or x>w-21) that Pass 1 had already written, since both passes read from `px_orig`.

**Pass 3 — exact edge equality:** For each x, set `px[x, 0]` and `px[x, h-1]` both to `ceil((px_c[x,0][c] + px_c[x,h-1][c]) / 2)` per channel. Same for each y on left/right columns. This resolves the corner interaction left by Pass 2 overwriting Pass 1's work at the shared corner pixels.

The blend zone covers the outer 20 pixels on all 4 sides. The interior `[20, 1234) × [20, 1234)` region is **byte-identical to the original**.

**Averaging is RGB per-channel** (each of R, G, B averaged independently). This is not a luminance-only operation.

**Reproduction:** `gen-paving-candidate.py` in this folder. SHA256-pinned input → output. Deterministic, no randomness, no wall-clock.

---

## Candidate seam diagnostics

| Edge pair | Mean abs diff | Max diff |
|---|---|---|
| Top vs Bottom | 0.000 / 255 | 0 |
| Left vs Right | 0.000 / 255 | 0 |

Opposite edges are exactly equal per pixel. This is a technical measurement only; it does not establish whether the tile boundary is visually undetectable.

| Metric | Value |
|---|---|
| Candidate SHA256 | `01d3d1e2bb9793cf374929c50006ac54cdfcfcb863b894948599c39d435c3008` |
| Pixels changed | 98 611 / 1 572 516 (6.3%) |
| Blend zone mean change (top/bottom rows) | ≈26 / 255 |
| Blend zone mean change (left/right cols) | ≈21 / 255 |
| Interior change | 0.00 / 255 — byte-identical |

---

## Portable guards

The following invariants are verifiable from the files in this folder (no AppTests, no native run):

1. **Source hash guard:** `sha256(AppTests/WholeSceneAssets/whole-scene-muted-paving.png) == c0decdab...` — original must not be modified.
2. **Candidate size:** `paving-muted-candidate.png` must be 1254 × 1254 pixels.
3. **Interior unchanged:** Every pixel at `x ∈ [20, 1234)`, `y ∈ [20, 1234)` must be byte-identical to the same coordinate in the original.
4. **Exact edge equality:** `px[x, 0] == px[x, h-1]` for all x; `px[0, y] == px[w-1, y]` for all y.
5. **No mirror:** Interior pixels must match the original at the same coordinates, not at mirrored coordinates. Verified by sampling 1000 interior points: original-match = 1000/1000, mirror-match = 5/1000 (from texture self-similarity, not transform).
6. **No mutation of simulation or test state:** This folder contains only review material. No AppTests or production Swift files are present here.

Run `python3 docs/review/paving-repeat-repair-20261116/verify-packet.py` from repository root with Pillow installed. It checks source hash, dimensions, exhaustive interior/orientation, exact edges, all six attachment hashes/sizes, and exact full 3x3 placement. It rejects five deliberate mutations: source bytes, interior pixel, edge pixel, horizontal mirror, and wrong dimensions. The generator itself checks input/output hashes only.

**Visual verdict: candidate fails aesthetic repeat review.** Dark border bands are conspicuous relative to original fine slab joints, not merely a subtle improvement. Earlier messages claiming visual seams eliminated or calling this slice complete were incorrect. No native integration is recommended. Source-only checks do not prove curb/rail continuity. Image-generation editing has not been performed, so the requested image_gen repair remains outstanding.

---

## Repeat preview files

| File | Dimensions | Description | SHA256 |
|---|---|---|---|
| `repeat-original-3x3-full.png` | 3762 × 3762 | Original tiled 3×3, full resolution | `5b6fc76f...` |
| `repeat-original-3x3-half.png` | 1881 × 1881 | Original tiled 3×3, half resolution | `5be5c925...` |
| `repeat-original-3x3-grayscale.png` | 3762 × 3762 | Original tiled 3×3, full res, grayscale | `d3fdbb63...` |
| `repeat-candidate-3x3-full.png` | 3762 × 3762 | Candidate tiled 3×3, full resolution | `c544affb...` |
| `repeat-candidate-3x3-half.png` | 1881 × 1881 | Candidate tiled 3×3, half resolution | `1a74cd42...` |
| `repeat-candidate-3x3-grayscale.png` | 3762 × 3762 | Candidate tiled 3×3, full res, grayscale | `c2343bf7...` |

Full SHA256s in `provenance.json`.

---

## Visual repeat defect assessment (from preview images)

This assessment is from direct inspection of the full-resolution 3×3 previews above.

### Original (repeat-original-3x3-full.png)
- Hard luminance step at every tile boundary: clearly visible as a thin dark joint line at all horizontal and vertical tile seams.
- Content (wash/stain pattern) repeats identically in orientation across all 9 tiles — no mirror.
- The step is consistent with the measured edge diff of 14 / 255 mean.

### Candidate (repeat-candidate-3x3-full.png)
- The hard seam cut of the original is replaced by a **visible softer dark band** at every tile boundary. At full resolution the band is a few pixels wide and darker than the adjacent interior, forming a periodic frame around each tile. This band remains a repeat defect: edge equality is exact by metric, but the blend zone introduces a systematic darkening that traces the tile grid.
- **No mirroring.** Content orientation is identical across all 9 tiles.
- **Content repetition:** The stain pattern itself repeats identically in all 9 tiles (expected — this is a tileable texture, not a unique pattern). No unexpected structural repetition introduced by the blend.
- The candidate exchanges a hard step for a soft band. Whether the soft band is acceptable is a visual judgment for the coordinator; the metric result (edge diff = 0) does not resolve this.

### Open visual question
The 20-pixel cosine blend creates a periodic dark border. This may be more or less acceptable than the original hard step depending on how the paving reads at gameplay zoom levels. The coordinator should inspect the full-res preview at intended display scale before deciding.

---

## What this slice does and does not establish

**Does establish:**
- Original source metadata and seam measurements.
- One deterministic candidate with exact edge equality and byte-identical interior.
- Repeat preview images for coordinator visual review.
- Portable guards covering source integrity, size, interior, edges, and no-mirror.

**Does not establish:**
- Acceptance. No WholeScenePavingTests.swift modification, no native render.
- Curb/rail continuity at paving edges (requires scene render, out of scope here).
- That the soft band defect is acceptable.
- Any change to tileUnits, slab scale, or geometry.

---

## Prior packet preservation

Prior whole-scene-paving captures (18/36 plate packets) are in
`docs/review/whole-scene-paving-20261116/capture/` — untouched.
This folder (`paving-repeat-repair-20261116/`) is new and additive only.
