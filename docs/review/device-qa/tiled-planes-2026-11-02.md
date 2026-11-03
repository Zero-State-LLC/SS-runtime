# Tiled ground and fog planes

Measured 2026-11-02 from the runtime asset bytes on `7f228ea`. No pixels were changed. This note records the canvas against the square the renderer already draws. It does not close T1046.

Image coordinates start at the top left of the PNG. Bounds are inclusive. A pixel counts as nontransparent when its alpha is greater than 0. The same read of the two published solid footprints matches those notes.

## Ground

`WorldRenderer.groundTileUnits` is 128. Each ground sprite is drawn at 128×128, centered on its tile. The zone map in `zoneSurface` is:

| Zone | Surface |
|---|---|
| Z-01 Residential Wedge | `env_ground_sidewalk` |
| Z-02 Transit Cut | `env_ground_railbed` |
| Z-03 Civic Plaza | `env_ground_plaza` |
| Z-04 Service Seam | `env_ground_service` |
| Z-05 Grid Junction | `env_ground_asphalt` |
| Z-06 Authority Court | `env_ground_plaza` |
| Z-07 Phoenix Steps | `env_ground_steps` |

A point outside every zone uses the first declared ground id. That id is `env_ground_asphalt`, from `presentation-assets-003`.

All six images are 128×128 and every pixel has alpha greater than 0 (16384 pixels). The canvas already matches the tile. One image pixel is one world unit on that tile.

| File | sha256 |
|---|---|
| `env_ground_asphalt@1x.png` | `96774980c0b90535f0edfa263b1f5c4841be0be9778be48feaec27e2fd7c1676` |
| `env_ground_sidewalk@1x.png` | `33a590754f7730d8526af161493f748d99336e23accf6c6514de62341126ff03` |
| `env_ground_plaza@1x.png` | `098bc9dadddd45259cdf76bec9ba0c43835a1cbad14e689440c02780d2711484` |
| `env_ground_railbed@1x.png` | `9b71398b45621cc12d24d963d0be583e487dbba101eda6e5c4a0da4eabbb4c15` |
| `env_ground_service@1x.png` | `eb2bd7750d064716dbf35acbdfad92e800fd52c3de66fffc4c235fa469bad5ef` |
| `env_ground_steps@1x.png` | `738b1a9c6bc8f25861395d07d6661765716c991868b245f8993b5f3daecff6d6` |

Files live in `Sources/SurveillanceCore/Resources/RuntimeAssets/`.

## Fog

`WorldRenderer.fogTileUnits` is 512. Each fog sprite is drawn at 512×512. Both images are 512×512 canvases, so the canvas matches the tile. The ink does not fill the tile. Empty canvas is empty fog.

| File | Bounds | Span | Ink pixels | sha256 |
|---|---|---|---|---|
| `env_fog_low@1x.png` | x 5–507, y 110–418 | 503×309 | 54285 | `f772c650585cfea23972afabb8234fb57de78c17845b8304a41377ee3665856d` |
| `env_fog_high@1x.png` | x 0–511, y 147–381 | 512×235 | 27768 | `17c6ce2595f75fad393c9fd19d50696e989879c7ffc8eecc27acfbef0ccf611c` |

A full 512×512 canvas is 262144 pixels. The low layer leaves a clear band above y 110 and below y 418. The high layer is a full-width band from y 147 through y 381.
