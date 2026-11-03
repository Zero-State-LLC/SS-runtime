# Vendor throw frames in north, east, and west

Measured 2026-11-03 from the runtime asset bytes on `df637da`. No new frame was added. Frame 01 in these directions stays in [enemy-action-facing-frame-01-2026-11-03.md](enemy-action-facing-frame-01-2026-11-03.md). The south frames stay in [enemy-south-action-rest-2026-11-03.md](enemy-south-action-rest-2026-11-03.md) and [enemy-south-commit-rest-2026-11-03.md](enemy-south-commit-rest-2026-11-03.md). The anchor stays the one in the enemy note: (32, 56).

Image coordinates start at the top left of the PNG. Bounds are inclusive. A pixel counts as nontransparent when its alpha is greater than 0.

`throw` is frames 02–03. `throwCommit` is frame 02. Every frame below has canvas 64×64. The table is those frames in north, east, and west: 9 files. This does not close #131 or #132.

## Throw

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_victorianVendor_throw_n_02@1x.png` | x 0–56, y 2–56 | 57×55 | `6d73cb8313d96a6fc14fa95dc9f106d0371c7d5db90cda1602f9a6bd59445342` |
| `actor_victorianVendor_throw_e_02@1x.png` | x 17–49, y 5–54 | 33×50 | `9baf9893663a3d18c1f2a128cced39c85cc30ad2bb6147c6dc1659a93664be87` |
| `actor_victorianVendor_throw_w_02@1x.png` | x 13–45, y 5–54 | 33×50 | `87d9a13f2d89c648648f80f717c3449aec8635777c0370588f67099251e2e93c` |
| `actor_victorianVendor_throw_n_03@1x.png` | x 6–50, y 7–56 | 45×50 | `1d6e43731381f6c26cfbfd68e439ebe35dfa8b6ef949a2cafecc3a348bb5102c` |
| `actor_victorianVendor_throw_e_03@1x.png` | x 18–47, y 3–52 | 30×50 | `b45343fe718f8c9294a4fff9b313cc3d9e55020863095c451281eba78b77363e` |
| `actor_victorianVendor_throw_w_03@1x.png` | x 15–44, y 3–52 | 30×50 | `92e6729248cad14be3b82c22a904f84a60db844716d45160e8000d7a46747086` |

## Throw commit

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_victorianVendor_throwCommit_n_02@1x.png` | x 6–43, y 18–55 | 38×38 | `23a9f4800851e5f6796cfb49f0bf2aa992baee90185adaa641138e33bb2db0c5` |
| `actor_victorianVendor_throwCommit_e_02@1x.png` | x 14–52, y 6–53 | 39×48 | `e543a39c69a8a22fc1c967d90327b323fa12dbbcf0811e656b9195009a0b2b7f` |
| `actor_victorianVendor_throwCommit_w_02@1x.png` | x 11–49, y 6–53 | 39×48 | `48ef62f64bfe59944ccb5d69ffeda1506a609f85b575ce676a4f2c981ef970fa` |
