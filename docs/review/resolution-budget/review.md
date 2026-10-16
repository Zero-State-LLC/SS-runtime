# BP-007 measured resolution budget

OBSERVED: source files measured at runtime 14abe4a against spec pin 00ce027209e6c233bcdd35295f35f0b9bfb9bbe5. Measurements use the existing 704×326-point / 2112×978-pixel test fixture and its zoom-1 and √2 upright-art transforms. These are calculated sampling sizes, not a new performance capture.

| Asset | Source pixels | Source/output density, zoom 1 | Density, √2 zoom | Occupied height, zoom 1 → √2 |
|---|---:|---:|---:|---:|
| player-south | 256×256 | 1.33 | 0.94 | 16.0% → 22.6% |
| player-north | 256×256 | 1.33 | 0.94 | 16.0% → 22.6% |
| player-east | 256×256 | 1.33 | 0.94 | 16.0% → 22.6% |
| player-west | 256×256 | 1.33 | 0.94 | 16.0% → 22.6% |
| camera-state-intact | 256×384 | 1.33 | 0.94 | 24.0% → 33.9% |
| camera-state-damaged | 256×384 | 1.33 | 0.94 | 24.0% → 33.9% |
| camera-state-critical | 256×384 | 1.33 | 0.94 | 24.0% → 33.9% |
| camera-state-destroyed | 256×384 | 1.33 | 0.94 | 24.0% → 33.9% |
| building-constrained | 1254×1254 | 1.72 | 1.22 | 63.5% → 89.8% |
| newsbox | 378×768 | 6.30 | 4.45 | 12.3% → 17.4% |
| tree | 454×768 | 3.01 | 2.13 | 26.1% → 36.9% |

Density below 1 means source texels are magnified. Alpha bounds include any nonzero alpha; they are not anatomical measurements or collision footprints. Canvas padding is accounted for in occupied height.

## Production direction

- PROPOSED: retain a high-detail character/camera master and export only after choosing the framing. At √2 zoom and this 3× capture scale, the no-magnification canvas minimum is 272×272 for the player and 272×408 for the camera. These mathematical minima are not an accepted delivery size or quality threshold. Higher headroom may be appropriate for zoom/device coverage, subject to profiling.
- OBSERVED: the constrained building still has about 1.22 source pixels per output pixel at √2. The newsbox and tree have substantially more. Larger files alone will not repair their material/scale mismatch with the approved reference.
- OBSERVED: the closer candidate consumes about 90% of viewport height for the building alpha bounds before accounting for its position. Earlier full-render captures show cropping. A closer view needs composition and encounter visibility work; it cannot be selected solely because the player looks larger.
- PROPOSED: prioritize coherent high-detail character frames and camera state exports; keep current high-resolution building/prop sources while correcting appearance and placement. Do not upscale the 256-pixel character and describe it as newly authored detail.
- NOT_COMPUTABLE: a final atlas residency/frame-time budget from these PNG dimensions alone. Compression, atlas packing, live clip count, mipmaps and intermediate render targets must be measured on the admitted renderer. Doubling both texture axes gives four times the texel count before those factors.

## Reproduction and limits

Run `python3 docs/review/resolution-budget/measure.py` from the runtime root (Pillow required). The script hashes each input and records canvas, alpha bounds, draw size, zoom and derived output density. It does not modify images or production code. Paving, actual device rendering, intermediate targets, anatomical landmarks and visual-detail quality are outside this calculation.

BP-007 already requires these measurements and native-size comparisons; no new gameplay or resolution acceptance threshold is introduced. BP-003/BP-004 animation, BP-005 geometry, BP-009 occlusion and device gates remain open.

Mechanism references: [Apple sprite size](https://developer.apple.com/documentation/spritekit/skspritenode/init(texture:size:)), [view backing scale](https://developer.apple.com/documentation/uikit/uiview/contentscalefactor), and [texture filtering](https://developer.apple.com/documentation/spritekit/sktexturefilteringmode), researched 2026-10-14. These explain sampling; they do not prescribe an SS artistic resolution.
