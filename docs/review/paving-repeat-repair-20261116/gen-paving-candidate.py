#!/usr/bin/env python3
"""
Deterministic muted paving candidate generation.
Input: AppTests/WholeSceneAssets/whole-scene-muted-paving.png
       SHA256: c0decdab226512a790ddecf49cf703c9fc736f7943f11bc364b76b111b7c3125
Output: docs/review/paving-repeat-repair-20261116/paving-muted-candidate.png
        SHA256: 01d3d1e2bb9793cf374929c50006ac54cdfcfcb863b894948599c39d435c3008

Method: cosine-ease edge-forced blend, bw=20px.
No randomness, no wall-clock, no unseeded sources.
"""
from PIL import Image
import hashlib, math, os

ORIG_SHA = "c0decdab226512a790ddecf49cf703c9fc736f7943f11bc364b76b111b7c3125"
CAND_SHA = "01d3d1e2bb9793cf374929c50006ac54cdfcfcb863b894948599c39d435c3008"
IN_PATH = "AppTests/WholeSceneAssets/whole-scene-muted-paving.png"
OUT_PATH = "docs/review/paving-repeat-repair-20261116/paving-muted-candidate.png"
BW = 20  # blend half-width in pixels


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    # Verify input
    assert sha256(IN_PATH) == ORIG_SHA, f"Input SHA256 mismatch: {sha256(IN_PATH)}"

    img = Image.open(IN_PATH).convert("RGB")
    w, h = img.size
    px_orig = img.load()
    candidate = img.copy()
    px_c = candidate.load()

    # Pass 1: top/bottom edge blend (from px_orig)
    for x in range(w):
        tp = px_orig[x, 0]
        bp = px_orig[x, h - 1]
        tgt = tuple((int(tp[c]) + int(bp[c])) // 2 for c in range(3))
        for dy in range(BW):
            alpha = 0.5 * (1 - math.cos(math.pi * (BW - dy) / BW))
            px_c[x, dy] = tuple(int(px_orig[x, dy][c] * (1 - alpha) + tgt[c] * alpha) for c in range(3))
            px_c[x, h - 1 - dy] = tuple(int(px_orig[x, h - 1 - dy][c] * (1 - alpha) + tgt[c] * alpha) for c in range(3))

    # Pass 2: left/right edge blend (from px_orig)
    for y in range(h):
        lp = px_orig[0, y]
        rp = px_orig[w - 1, y]
        tgt = tuple((int(lp[c]) + int(rp[c])) // 2 for c in range(3))
        for dx in range(BW):
            alpha = 0.5 * (1 - math.cos(math.pi * (BW - dx) / BW))
            px_c[dx, y] = tuple(int(px_orig[dx, y][c] * (1 - alpha) + tgt[c] * alpha) for c in range(3))
            px_c[w - 1 - dx, y] = tuple(int(px_orig[w - 1 - dx, y][c] * (1 - alpha) + tgt[c] * alpha) for c in range(3))

    # Pass 3: force exact edge equality (cleans up corner interactions)
    for x in range(w):
        t = px_c[x, 0]; b = px_c[x, h - 1]
        edge_val = tuple((int(t[c]) + int(b[c]) + 1) // 2 for c in range(3))
        px_c[x, 0] = edge_val; px_c[x, h - 1] = edge_val

    for y in range(h):
        l = px_c[0, y]; r = px_c[w - 1, y]
        edge_val = tuple((int(l[c]) + int(r[c]) + 1) // 2 for c in range(3))
        px_c[0, y] = edge_val; px_c[w - 1, y] = edge_val

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    candidate.save(OUT_PATH, "PNG")

    result = sha256(OUT_PATH)
    assert result == CAND_SHA, f"Output SHA256 mismatch: {result}"
    print(f"OK: {OUT_PATH}")
    print(f"    SHA256: {result}")


if __name__ == "__main__":
    main()
