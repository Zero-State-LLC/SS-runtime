# Camera frames against the housing anchor

Measured 2026-11-02 from the runtime asset bytes and the renderer on `31345cd`. No pixels were changed. No catalog row was added. This is evidence for issue #117 row 1. It does not redraw the camera and it does not admit a family.

Image coordinates start at the top left of the PNG. Bounds are inclusive. A pixel counts as nontransparent when its alpha is greater than 0. A piece is a 4-connected group of at least 20 such pixels. Smaller groups are specks.

Every camera clip in `clip-metadata-001` has anchor (32, 88) in a 64×96 box, measured from the top left. `WorldRenderer` draws the head and the housing at 64×96 and asks `SpriteLibrary.anchorPoint` for a camera clip id. That point is SpriteKit (32/64, 1 − 88/96), which is (0.5, 8/96). The centered fallback (0.5, 0.5) runs only when the clip id is missing. These clip ids are present, so the housing is not centered. The 2026-10-13 candidate note said the housing used a centered anchor. This renderer does not.

The head clip for each integrity is `camera_operational_idle` (intact, 3), `camera_hit` (hit and the damaged hold, 2), `camera_critical_enter` (critical, 1), and `camera_destroyed_idle` after `camera_destroy` (destroyed, 0). `camera_field_off` is the field-off frame. The housing is one of the five `env_camera_` images, drawn under the head at the same anchor.

## Intact — camera_operational_idle

| Frame | Canvas | Bounds | Span | sha256 |
|---|---|---|---|---|
| `actor_camera_operationalIdle_none_01@1x.png` | 64×96 | x 14–63, y 12–82 | 50×71 | `1f0d6ef053e915666a6c3613e28255cc509b51ac18d7336dd127eb6b458c415d` |
| `actor_camera_operationalIdle_none_02@1x.png` | 64×96 | x 0–63, y 12–82 | 64×71 | `5d9b16e6384df500fee96982797e156ff15345cdf645ee4b338151dc7e79ceec` |
| `actor_camera_operationalIdle_none_03@1x.png` | 64×96 | x 0–63, y 12–82 | 64×71 | `1866a81a7e5973a81737839a84a3fcfdbb714fc2366922835c0869045de37663` |
| `actor_camera_operationalIdle_none_04@1x.png` | 64×96 | x 0–49, y 12–82 | 50×71 | `c81ae71c64a0c6eeebbd65981b33d0df4a79fb1c7cbedb2cd230caf440a05a93` |

Frame 02 has two pieces: 1389 px at x 35–63, y 12–82, and 164 px at x 0–6, y 38–67. Frame 03 has two pieces: 1391 px at x 0–28, y 12–82, and 164 px at x 57–63, y 38–67. Frames 01 and 04 are one piece.

## Hit — camera_hit

| Frame | Canvas | Bounds | Span | sha256 |
|---|---|---|---|---|
| `actor_camera_hit_none_01@1x.png` | 64×96 | x 6–56, y 3–87 | 51×85 | `13dfd8a833bd12123ff257595af36fcd70071bf6a0dcec5774ebcd8bb6ba8d86` |
| `actor_camera_hit_none_02@1x.png` | 64×96 | x 15–48, y 42–72 | 34×31 | `fdcd36cdcbd3a63f7ed809e978e5279dcb5873e45739e9b5c2c9eea98cc958d9` |

Frame 01 is one piece plus 13 specks. Frame 02 is one piece. Its bytes are the same as `actor_camera_criticalEnter_none_01@1x.png`.

## Critical — camera_critical_enter

| Frame | Canvas | Bounds | Span | sha256 |
|---|---|---|---|---|
| `actor_camera_criticalEnter_none_01@1x.png` | 64×96 | x 15–48, y 42–72 | 34×31 | `fdcd36cdcbd3a63f7ed809e978e5279dcb5873e45739e9b5c2c9eea98cc958d9` |
| `actor_camera_criticalEnter_none_02@1x.png` | 64×96 | x 10–52, y 40–72 | 43×33 | `2578299b517e62aa9f1734aa915f156c133ef577939a54d0bbfcac6dec405308` |
| `actor_camera_criticalEnter_none_03@1x.png` | 64×96 | x 11–52, y 40–72 | 42×33 | `d77261682a4da0061f1a0b66bfe5610bf9e20121faa869627533753a49da0875` |

Frame 02 has a second piece of 23 px at x 10–18, y 41–47, plus 9 specks. Frames 01 and 03 are one piece. Frame 03 also has 12 specks.

## Destroyed — camera_destroy, then camera_destroyed_idle

| Frame | Canvas | Bounds | Span | sha256 |
|---|---|---|---|---|
| `actor_camera_destroy_none_01@1x.png` | 64×96 | x 13–63, y 37–95 | 51×59 | `df332805bfc2492049d634ef6d008ae80686a258cd45ef86951aaacd18d47e52` |
| `actor_camera_destroy_none_02@1x.png` | 64×96 | x 0–63, y 37–95 | 64×59 | `1360b22b542a32abc9424c37e6ced0c8b236bc7c65cd27d51be15f045d8faa3f` |
| `actor_camera_destroy_none_03@1x.png` | 64×96 | x 0–62, y 12–95 | 63×84 | `4f7832c2e4e154ab8e8c18d21bc71a90d58ba0dc1ede98e0c32031753c4ef4ac` |
| `actor_camera_destroy_none_04@1x.png` | 64×96 | x 20–49, y 13–95 | 30×83 | `f23aa4adcfc7acb0d3207bf37df53e050daf6a3eaf76a7ee1be2aa6e8c48fc52` |
| `actor_camera_destroyedIdle_none_01@1x.png` | 64×96 | x 4–59, y 12–87 | 56×76 | `9822d27f6699726461c6447505e34bedaed60cf53b9a4420a7ff7671c500f680` |
| `actor_camera_destroyedIdle_none_02@1x.png` | 64×96 | x 15–50, y 40–71 | 36×32 | `9d79cb23a274c309834eb2733e6b56a4a402316e248f79998ad19fdec3007c00` |

Separated pieces:

- destroy 01: 711 px at x 13–43, y 37–95, and 44 px at x 61–63, y 51–67.
- destroy 02: 679 px at x 0–27, y 37–95, and 545 px at x 45–63, y 37–95.
- destroy 03: 933 px at x 34–62, y 16–95, and 193 px at x 0–11, y 41–71.
- destroy 04 and destroyed-idle 01 are one piece, plus specks.
- destroyed-idle 02 is one piece. Its bytes are the same as `actor_camera_fieldOff_none_01@1x.png`.

## Field off — camera_field_off

`actor_camera_fieldOff_none_01@1x.png` is 64×96, bounds x 15–50, y 40–71, span 36×32, one piece. sha256 `9d79cb23a274c309834eb2733e6b56a4a402316e248f79998ad19fdec3007c00`.

## Housings

Drawn at 64×96 under the head, same anchor.

| File | Canvas | Bounds | Span | sha256 |
|---|---|---|---|---|
| `env_camera_municipal_dome@1x.png` | 64×96 | x 13–50, y 4–88 | 38×85 | `98145d19642da2f03f1aa8bf0dfece0260b199a37e37584c495b0542684c1719` |
| `env_camera_storefront@1x.png` | 64×96 | x 13–49, y 8–77 | 37×70 | `f76c5e1bb53ef8d8898df6ae028a3f88350fcff1b347aecd0889696d0666bcc1` |
| `env_camera_traffic_reader@1x.png` | 64×96 | x 8–54, y 4–75 | 47×72 | `eed3177293c813f44045723955c6c7ff7e226f46355abb2ccee290f5236aebed` |
| `env_camera_ornamental_civic@1x.png` | 64×96 | x 12–51, y 4–91 | 40×88 | `025727dd9ef318a6e4cbb4a4cda3f707eb6d064265bcbea04983e5a7165409b8` |
| `env_camera_temporary_mast@1x.png` | 64×96 | x 13–49, y 4–90 | 37×87 | `b9e3d159ab8ba08640f6e88b6d3d4451a0ba980c295925de1f8eee8f1c095b58` |

Municipal dome, storefront, and traffic reader are one piece plus specks. Ornamental civic has a second piece of 89 px at x 12–21, y 27–39. The temporary mast has a second piece of 202 px at x 13–24, y 28–56.
