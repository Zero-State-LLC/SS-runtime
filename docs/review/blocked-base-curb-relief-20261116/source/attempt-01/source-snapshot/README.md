# V9 first source attempt

BP-001/007/012, T1045. Source only. Recommendation and acceptance remain coordinator-only.

Implementation: `author.py`, editable `geometry.json` and `materials.json`, `replay.py`, `preview.py`, `test_source.py`, `freeze.py`. Exact reuse and original material citations: `ADAPT.md`. Integration schema: `API.md` and frozen `manifest.json` (`blocked-base-curb-source-009`).

53 supplemental presentation sprites: one masonry triangular prism covering the exact omitted blocked kiosk corner, height18, plus52 curb blocks height3 within the existing semantic strip. World roots are contact centroids. Each exposes exact XYZ contacts, bounds, height vertices and D108 source-pixel witnesses. Existing 18uprights/24solids remain a separate untouched census. Fixed4source pixels per world unit, native upright draw size=canvas/4. No whole-ground lift, replacement actor, depth boost or changed gameplay height.

First preview: `attempt-01/preview/context-z100.png`, `context-z125.png`, `context-z140.png` (and half/grayscale), `base-curb-detail.png`, `full-benchmark-comparison.png`. These are explicitly synthetic overlays on actual V8 native context. The entire original benchmark is shown uncropped. Native depth must still be checked, especially the kiosk source against its overlapping supplemental base. Root-only synthetic overlay ordering does not certify scene occlusion.

Commands from this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 test_source.py
PYTHONDONTWRITEBYTECODE=1 python3 replay.py --out "$JCODE_SCRATCH_DIR/v9-independent-replay"
```

Replay requires an empty directory and refuses overwrites. `author.py`, `preview.py` and `freeze.py` were run once for first source generation. Do not rerun to overwrite outputs. No second aesthetic pass without a coordinator's precise bounded correction. All first-attempt source and preview files remain immutable.

Tests cover exact blocked triangle and vertical faces, complete selected semantic curb strip, prop-base clearance and retained roots, geometry-derived D108 anchors/draw sizes/height witnesses, source hashes, all frozen V8 files, deterministic source replay and adversarial mutations. They do not certify visual obstruction, source fidelity, owner acceptance, native capture or physical devices. No Swift/native build or git operation belongs to this source lane.
