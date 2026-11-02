# Two solid footprints

Measured 2026-11-01 from the runtime asset bytes on `aed7bff`. No pixels were changed. No collision rectangle was changed. This is evidence for issue #117 row 2. It does not repair the art and it does not admit a family.

Image coordinates start at the top left of the PNG. The bounds below are inclusive. A pixel counts as nontransparent when its alpha is greater than 0, including partial coverage. The corner of the box is not always an inked pixel; the box is the axis-aligned extent.

The canvas is the size `admit_environment_art.py` requires for that solid: twice the arena `halfSize`. The image is drawn over the whole blocking rectangle, so empty canvas is empty blocker.

## env_solid_01_residential_west

File: `Sources/SurveillanceCore/Resources/RuntimeAssets/env_solid_01_residential_west@1x.png`

sha256: `1171bd8f9ff905b96e54cb33aac6ea98779b712f4119d2fa76593a2c693bdf6e`

Canvas: 128×512.

Nontransparent bounds: x 4–123, y 181–329. Span 120×149.

Blocking rectangle, `civic-seam-arena-004` solid `solid-01-residential-west`: center (64, 640), halfSize (64, 256). The rectangle runs x 0–128, y 384–896.

The 2026-10-13 candidate note wrote (4,181)–(124,330). That far corner is the exclusive edge of this inclusive box.

## env_solid_13_phoenix_west

File: `Sources/SurveillanceCore/Resources/RuntimeAssets/env_solid_13_phoenix_west@1x.png`

sha256: `7c53e2d05db5fd65af539183908dd7c8651e5d256b170dc9ed2db5c10e6d559a`

Canvas: 64×256.

Nontransparent bounds: x 5–58, y 102–152. Span 54×51.

Blocking rectangle, solid `solid-13-phoenix-west`: center (1856, 192), halfSize (32, 128). The rectangle runs x 1824–1888, y 64–320.

The candidate note wrote (5,102)–(59,153). That far corner is the exclusive edge of this inclusive box.
