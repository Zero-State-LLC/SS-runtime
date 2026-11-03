# HUD images and the shapes the HUD draws

Measured 2026-11-03 from the runtime asset bytes and `HUDRenderer` on `c700b82`. No meter was added. No icon was added. No layout changed.

`HUDRenderer` does not sample these PNGs. It draws `SKShapeNode`s and, for some of them, sets `name` to the asset id. The authored rects below are `HUDLayout` points on the 844×390 reference. `HUDProjector` maps a rect into the safe rectangle and divides by `pointsPerSceneUnit` to get scene units. `HUDRenderer.framingScale` is `PresentationCamera.visibleWidth / 896`, which is 704/896, and it scales stroke width and font size.

Image coordinates start at the top left of the PNG. Bounds are inclusive. A pixel counts as nontransparent when its alpha is greater than 0. Every file below is 128×128.

## Shapes that carry an asset id

| Asset id | Shape | Authored size |
|---|---|---|
| `hud_integrity_frame` | Rectangle frame, clear fill, stroke width `1 * framingScale` | 220×20 (`playerIntegrity`) |
| `hud_exposure_bar` | Same frame treatment | 300×24 (`exposureBar`) |
| `hud_boss_bar` | Same frame treatment | 360×24 (`bossIntegrity`) |
| `hud_extraction_ring` | Arc, clear fill, stroke width `3 * framingScale`, radius half the mapped height | 220×56 (`extractionCountdown`) |
| `hud_upgrade_signal_jammer`, `hud_upgrade_ricochet_pulse`, `hud_upgrade_ghost_step` | Rounded square, corner radius one eighth of the side. The name is the equipped upgrade's id. The PNG is not drawn | 64×64 (`upgradeBadge`) |
| `hud_camera_notch_full`, `hud_camera_notch_empty` | Rectangle. Three notches. Each is `0.6 * step` by `step`, and `step` is 14 points after mapping | Beside `cameraObjective` (180×28) |
| `control_stick_base` | Circle. Radius is half the mapped stick width | Stick rect 144×144, so the authored radius is 72 |
| `control_stick_knob` | Circle. Radius is 0.42 of the base radius | |
| `control_dodge` | Circle. Radius is half the mapped dodge width | 88×88 |
| `control_pause` | Rounded rectangle, corner radius 4 | 44×44 |

`RuntimeAssetRegistry.HUD.cameraCounter` and `HUD.detection(_:)` have no draw call. The detection label on screen is text.

## PNG canvases

| File | Bounds | Span | Ink | sha256 |
|---|---|---|---|---|
| `hud_integrity_frame@1x.png` | x 4–123, y 5–122 | 120×118 | 7957 | `8f7cab5822b4bbbd143d92d047013d2c89d64db9de7db659094b3f3d7030a242` |
| `hud_exposure_bar@1x.png` | x 4–123, y 24–122 | 120×99 | 5591 | `a6cdc8d30ea3583373a3081c166c619ed94974ef63af7eed3e64ceabe7adf143` |
| `hud_boss_bar@1x.png` | x 4–123, y 16–118 | 120×103 | 7133 | `4e36da2a82fcc214aabc137c31f2b3abcae8a7f1a6b6e049a45aa748d3662041` |
| `hud_extraction_ring@1x.png` | x 4–123, y 4–121 | 120×118 | 6586 | `7c24780464eea7dfb5960fd6e170392669268dd959b6a4cd6072be1172507085` |
| `hud_upgrade_signal_jammer@1x.png` | x 4–123, y 4–123 | 120×120 | 10467 | `ccc4f235dff1defe1aa07f14934b887994263d5efd2761c85821291d9403b092` |
| `hud_upgrade_ricochet_pulse@1x.png` | x 4–123, y 4–122 | 120×119 | 9347 | `621a4c4b81c9d51abff9098be3fed388d49fb4becb3a7722f9c5d2e0e484d0b3` |
| `hud_upgrade_ghost_step@1x.png` | x 4–123, y 4–123 | 120×120 | 11033 | `c2162d65a726a00478472ea1113d88ec1f47d46aa645776e4e348ac713ce240a` |
| `hud_camera_notch_full@1x.png` | x 4–123, y 9–117 | 120×109 | 7878 | `28a5ffe0a1b53c87cbd30be782194a0f422f88a85b638a7a176d65edfb0dc151` |
| `hud_camera_notch_empty@1x.png` | x 5–123, y 15–112 | 119×98 | 6807 | `8d6f390de279a11d51230ea17d549dee28f13f9e785843474570cfd8f895ecfd` |
| `hud_camera_counter@1x.png` | x 4–123, y 14–112 | 120×99 | 6981 | `8b4c128c5baa40b7d643c4eef9f2a575edbaa960a91e887300812aa91648db77` |
| `hud_detection_hidden@1x.png` | x 4–123, y 5–122 | 120×118 | 8788 | `03cc259eec0c58240a9e00374ee3d03a52a97dc44affb8cb90b1e2367e06996b` |
| `hud_detection_observed@1x.png` | x 4–123, y 4–123 | 120×120 | 8394 | `9fd9fe10f1f8f9ab928589b2748d4f223ca68f7ab691433fc89df8e6dd7c51ce` |
| `hud_detection_tracked@1x.png` | x 4–123, y 4–122 | 120×119 | 9969 | `b7177f0e6e7b292105710bab9200dea5299e9e3155b41c9148498b537d1a207d` |
| `hud_detection_hunted@1x.png` | x 4–123, y 4–123 | 120×120 | 11162 | `8c4fa7435438ea622f6ad645b4643035a8257544396e6392053e873d5950087d` |
| `hud_detection_lockdown@1x.png` | x 4–123, y 4–123 | 120×120 | 10391 | `4ccf2ab8835a2402a31be4e09022135fcda903e27a541548e878dd0d5a1281c1` |
| `control_stick_base@1x.png` | x 4–123, y 4–123 | 120×120 | 10318 | `6da636a79334ec0a03471d5b9797c19a1f3677d97c4a1e21d291acb98dbe6cd6` |
| `control_stick_knob@1x.png` | x 4–123, y 6–121 | 120×116 | 8807 | `8ac52562bbb93443573648a8e519e0b088822b6a9ba0c8530e3e34236ee9a3b6` |
| `control_dodge@1x.png` | x 4–123, y 4–123 | 120×120 | 9176 | `2787cabab60f899a21c43c2877e14a78de4d382852d1aa4945f47ab173dfadbe` |
| `control_pause@1x.png` | x 4–123, y 4–123 | 120×120 | 9971 | `a80ca918ede6b63bc844394c57400b1f766b76833f96172603842143617f0de8` |
