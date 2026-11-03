# Placed decoration canvases

Measured 2026-11-02 from the runtime asset bytes on `7f228ea`. No pixels were changed. No collision rectangle was changed. These sprites are presentation only. This note records the canvas, the ink, and the box the renderer already draws. It does not pick a new ground anchor, and it does not close T1046.

Image coordinates start at the top left of the PNG. The bounds below are inclusive. A pixel counts as nontransparent when its alpha is greater than 0, including partial coverage. The same read of `env_solid_01_residential_west` and `env_solid_13_phoenix_west` matches the bounds already in the solid-footprint notes.

`WorldRenderer.renderDecorations` builds one sprite per placed decoration in `civic-seam-arena-004`. The sprite size is `texture.size()` times `scale / 1000`. The texture comes from `UIImage(contentsOfFile:)`, whose scale is 1, so that point size is the PNG pixel size. The code does not set an anchor, so the sprite keeps SpriteKit's center anchor `(0.5, 0.5)`. The contract center is the center of the canvas. Image y grows downward and is not world y. Empty canvas is empty dressing. There is no blocking rectangle.

`EnvironmentTextures.projectionPlane` labels a prop ground or upright, and the phoenix motif stays unresolved. That label is only the node name. It does not change the size or the anchor.

Scale is 1000 except `dec-20`. The two rail strips are rotated 30 degrees counter-clockwise about the canvas center (`rotationMilliDegrees` 30000). The world boxes below are the canvas before that rotation.

## env_prop_rail_strip

File: `Sources/SurveillanceCore/Resources/RuntimeAssets/env_prop_rail_strip@1x.png`

sha256: `ec777b1efeef80119d9eede73a17b4413c92f40e4afa7e29e2a42c0570b73d2f`

Plane label: ground. Canvas: 512×128. Draw size at scale 1000: 512×128.

Nontransparent bounds: x 0–511, y 0–124. Span 512×125.

| Placement | Center | Canvas box before rotation |
|---|---|---|
| `dec-22` | (766, 328) | x 510–1022, y 264–392 |
| `dec-23` | (1210, 584) | x 954–1466, y 520–648 |

## env_prop_street_tree

File: `Sources/SurveillanceCore/Resources/RuntimeAssets/env_prop_street_tree@1x.png`

sha256: `b75552314acfa9358703e3a29a046421270dbfca23c454e2fc6971fef5d6a915`

Plane label: upright. Canvas: 96×128. Draw size: 96×128.

Nontransparent bounds: x 8–91, y 21–106. Span 84×86.

| Placement | Center | Canvas box |
|---|---|---|
| `dec-01` | (300, 200) | x 252–348, y 136–264 |
| `dec-21` | (1990, 110) | x 1942–2038, y 46–174 |

## env_prop_newsbox

File: `Sources/SurveillanceCore/Resources/RuntimeAssets/env_prop_newsbox@1x.png`

sha256: `4017f1726af55b3b55a81529d2e57a5005b26caf04b1454be928b8950e6b8791`

Plane label: upright. Canvas: 48×64. Draw size: 48×64.

Nontransparent bounds: x 4–43, y 10–51. Span 40×42.

`dec-02` center (392, 320). Canvas box x 368–416, y 288–352.

## env_prop_hydrant_meters

File: `Sources/SurveillanceCore/Resources/RuntimeAssets/env_prop_hydrant_meters@1x.png`

sha256: `ad1cfd8f6142481185c2d31e1a35a6923f9567ce28ea7c3f0f95f7624e6236a7`

Plane label: upright. Canvas: 64×64. Draw size: 64×64.

Nontransparent bounds: x 5–58, y 4–59. Span 54×56.

| Placement | Center | Canvas box |
|---|---|---|
| `dec-03` | (176, 420) | x 144–208, y 388–452 |
| `dec-18` | (1620, 1020) | x 1588–1652, y 988–1052 |

## env_prop_trolley_pole

File: `Sources/SurveillanceCore/Resources/RuntimeAssets/env_prop_trolley_pole@1x.png`

sha256: `59528d523a71b8054fc41a09ba0d414fffe395b51a379a3e562b0c1ee96161b1`

Plane label: upright. Canvas: 32×160. Draw size: 32×160.

Nontransparent bounds: x 2–29, y 52–106. Span 28×55.

`dec-05` center (452, 300). Canvas box x 436–468, y 220–380. The ink is a 55-pixel band inside the 160-pixel canvas.

## env_prop_bus_shelter

File: `Sources/SurveillanceCore/Resources/RuntimeAssets/env_prop_bus_shelter@1x.png`

sha256: `5d3319716842214a4ada7739f30efec05969f5dbe993ba1840aee66c8f50c536`

Plane label: upright. Canvas: 160×96. Draw size: 160×96.

Nontransparent bounds: x 4–155, y 2–93. Span 152×92.

`dec-06` center (629, 415). Canvas box x 549–709, y 367–463.

## env_prop_signal_mast

File: `Sources/SurveillanceCore/Resources/RuntimeAssets/env_prop_signal_mast@1x.png`

sha256: `1a3045c0580d7beb57f3597b553e602a44edd18acfd10c7bf6222ce2930645ec`

Plane label: upright. Canvas: 48×144. Draw size: 48×144.

Nontransparent bounds: x 2–45, y 6–137. Span 44×132.

| Placement | Center | Canvas box |
|---|---|---|
| `dec-07` | (700, 560) | x 676–724, y 488–632 |
| `dec-17` | (1880, 880) | x 1856–1904, y 808–952 |

## env_prop_bike_rack

File: `Sources/SurveillanceCore/Resources/RuntimeAssets/env_prop_bike_rack@1x.png`

sha256: `578f9a6f1a4d6976a9e929273326c2f5599557b5e93403bfb30dee74202e5def`

Plane label: upright. Canvas: 96×48. Draw size: 96×48.

Nontransparent bounds: x 4–91, y 2–45. Span 88×44.

`dec-08` center (472, 600). Canvas box x 424–520, y 576–624.

## env_prop_parklet

File: `Sources/SurveillanceCore/Resources/RuntimeAssets/env_prop_parklet@1x.png`

sha256: `0bb6807826f59be3afb0d37d30e2388685b1aeeeb382f203918a7ac0f46848c6`

Plane label: upright. Canvas: 192×96. Draw size: 192×96.

Nontransparent bounds: x 5–186, y 2–93. Span 182×92.

`dec-09` center (869, 555). Canvas box x 773–965, y 507–603.

## env_prop_utility_covers

File: `Sources/SurveillanceCore/Resources/RuntimeAssets/env_prop_utility_covers@1x.png`

sha256: `71ee6ecb7611862abdf185d84c5cada694ceae987f29d902b4942ff82e2a462c`

Plane label: ground. Canvas: 64×64. Draw size: 64×64.

Nontransparent bounds: x 4–58, y 14–56. Span 55×43.

| Placement | Center | Canvas box |
|---|---|---|
| `dec-10` | (1085, 622) | x 1053–1117, y 590–654 |
| `dec-19` | (2048, 840) | x 2016–2080, y 808–872 |

## env_prop_vent_grate

File: `Sources/SurveillanceCore/Resources/RuntimeAssets/env_prop_vent_grate@1x.png`

sha256: `8675d6b09328bb6102f34231a3ad5147dec05374bdbaec333c64ebbd7458a92f`

Plane label: ground. Canvas: 96×64. Draw size: 96×64.

Nontransparent bounds: x 17–80, y 5–59. Span 64×55.

| Placement | Center | Canvas box |
|---|---|---|
| `dec-11` | (957, 641) | x 909–1005, y 609–673 |
| `dec-13` | (1560, 1180) | x 1512–1608, y 1148–1212 |

## env_prop_barricade

File: `Sources/SurveillanceCore/Resources/RuntimeAssets/env_prop_barricade@1x.png`

sha256: `3c09d384d101935d1af7f93d11ed896dc019c17326e99bd78ac6c6c6b8be9c33`

Plane label: upright. Canvas: 128×48. Draw size: 128×48.

Nontransparent bounds: x 5–121, y 2–45. Span 117×44.

| Placement | Center | Canvas box |
|---|---|---|
| `dec-12` | (1280, 900) | x 1216–1344, y 876–924 |
| `dec-16` | (1770, 590) | x 1706–1834, y 566–614 |

## env_prop_seismic_brace

File: `Sources/SurveillanceCore/Resources/RuntimeAssets/env_prop_seismic_brace@1x.png`

sha256: `4b33ecf6b6bcf77ee9ceb2e784deb9d4a5a8ba4fd8a2afb031d106dbc3f27059`

Plane label: upright. Canvas: 64×128. Draw size: 64×128.

Nontransparent bounds: x 2–61, y 4–123. Span 60×120.

`dec-14` center (1300, 1420). Canvas box x 1268–1332, y 1356–1484.

## env_motif_phoenix

File: `Sources/SurveillanceCore/Resources/RuntimeAssets/env_motif_phoenix@1x.png`

sha256: `a5a4fe20dcfc6733c18fd48477c0d498847700cd15777bce2a447be6a41565a2`

Plane label: unresolved. Canvas: 512×512. `dec-20` uses `scalePermille` 300, so the draw size is 153.6×153.6.

Nontransparent bounds: x 2–509, y 2–509. Span 508×508.

`dec-20` center (2048, 300). Canvas box x 1971.2–2124.8, y 223.2–376.8.
