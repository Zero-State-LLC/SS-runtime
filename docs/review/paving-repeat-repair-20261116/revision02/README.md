# Revision02: paired-strip repair

Status: implemented bounded coordinator-approved technical normalization, ready for coordinator source/repeat review, NOT visual acceptance or native integration. Attempt1 and its packet remain unchanged in the parent directory.

## Diagnosed cause and correction
Attempt1 propagated the darkest outer-edge color across the entire 20px strip, making a broad dark frame. This revision uses the corresponding opposite pixel at EACH distance, not edge0:

`weight(d) = (1 + cos(pi*d/20))/2`

`out(a,d) = round(a + weight(d)*((a+b)/2-a))`

The symmetric side uses the same pair and weight. Pass1 blends top/bottom. Pass2 reads an immutable COPY of pass1 and blends left/right, preserving the first pass at corners. There is no separate edge-forcing overwrite. RGB channels are independent. No reflection, rotation, resize or image-generation repaint is used in this bounded algorithm correction.

Candidate: `paving-muted-candidate.png`, 1254 square, SHA256 `7a1f29c7b0f1a0a96e12484de84da21e7ab4ebee10cab2e829ed19309ca17d35`.
Original SHA256 remains `c0decdab226512a790ddecf49cf703c9fc736f7943f11bc364b76b111b7c3125`.

## Reproduce and validate
From repository root, Python with Pillow:

```
python3 docs/review/paving-repeat-repair-20261116/revision02/generate-and-check.py
python3 docs/review/paving-repeat-repair-20261116/verify-packet.py
```

First command tests both passes exhaustively for convex paired bounds and pair-mean preservation within one rounding unit, unchanged 1214-square interior, exact top/bottom and left/right edges, source hash, a synthetic dark-edge nonwidening regression and rejection of a nonconvex pixel mutation. Second command validates the preserved attempt1 packet. Nonwidening is a local paired-bound/sentinel guarantee, NOT a claim that no visual darkening is possible: a pixel can darken toward its corresponding opposite pixel.

Full RGB and full grayscale 3x3 images are 3762 square. Half RGB 3x3 images are 1881 square. Original and candidate each have all three variants. `provenance.json` records their dimensions and SHA256 values.

## Visual inspection
Direct inspection of `repeat-candidate-3x3-half.png` shows that attempt1's broad black/dark frame is no longer apparent. Fine dark slab joints remain. The 4x4 slab layout, warm muted grey-brown concrete and irregular stains/cracks remain faithful to the original. There is no reflected motif or mirrored join introduced by this algorithm.

Remaining repeat defect: the same distinctive mottled stains and cracks recur at every four-slab interval in both axes. This makes the 3x3 repeat recognizable, especially over this large unobstructed area. Some fine boundary joints remain visually distinguishable. Exact edge equality is technical only, not aesthetic approval. Full/half/grayscale previews are supplied for coordinator assessment.

No world tileUnits change: 128 remains fixed, with 32 world units per slab. No native run, AppTests edit, production edit, commit or push. Curb/rail continuity, gameplay-scale appearance and image_gen-authored art repair remain unproven/outstanding. This revision implements only the explicitly approved paired-strip normalization correction.
