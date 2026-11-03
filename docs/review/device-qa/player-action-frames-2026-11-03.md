# Player south action frames

Measured 2026-11-03 from the runtime asset bytes on `c573052`. Those bytes are the same player frames as `c700b82`. No new frame was added. No facing was authored. The south idle and south move tables are in [player-sprite-bounds-2026-11-03.md](player-sprite-bounds-2026-11-03.md). This note tables the other south cycles. It does not close #65, #131, or #132, and it does not prove a live cycle.

Image coordinates start at the top left of the PNG. Bounds are inclusive. A pixel counts as nontransparent when its alpha is greater than 0.

The box, anchor, and radius are the ones in the player note: 64×64, anchor (32, 56), radius 18. Each of these clips also stores directions north, east, south, and west. This table is south only.

Every frame below has canvas 64×64. The span line is the smallest and largest width, and the smallest and largest height, across the south frames of that state. Those four numbers are not one frame.

## Dodge

Clip `player_dodge`. Four south frames.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_player_dodge_s_01@1x.png` | x 7–59, y 19–55 | 53×37 | `bb3a906629ab03077cede402a8f5c28247e3538b2eb718ac49da739ef40c421f` |
| `actor_player_dodge_s_02@1x.png` | x 4–59, y 19–55 | 56×37 | `59d26b408d49f2a376d5081842458f923153833685c65cbd749b9b86cb3de311` |
| `actor_player_dodge_s_03@1x.png` | x 4–59, y 19–55 | 56×37 | `aa258e3ff0bdfe4278a27d6e09e2691f53c6f7929ec66e7463286968598d6e1f` |
| `actor_player_dodge_s_04@1x.png` | x 4–58, y 19–55 | 55×37 | `0770969db20d2bd99514ffb57783fb0a6d8a87d2f50168fbc65e9ccdc948f368` |

Across these south frames, nontransparent width runs 53–56 and height runs 37–37.

## Recover

Clip `player_recover`. Two south frames.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_player_recover_s_01@1x.png` | x 37–56, y 37–53 | 20×17 | `52228fce8e816e3cb14b19d0045d06c0dc602f7fd63746a4fb3b4e6d32e9403e` |
| `actor_player_recover_s_02@1x.png` | x 8–29, y 26–55 | 22×30 | `911bbf57a8c7c08c3bd2e0061c328b1f05497bb9d39a6afe7328fb38649d9514` |

Across these south frames, nontransparent width runs 20–22 and height runs 17–30.

## Hurt

Clip `player_hurt`. Three south frames.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_player_hurt_s_01@1x.png` | x 23–40, y 15–47 | 18×33 | `a83d382295db881c942d6d2b43185cd67a5aeefa2e397e6ca9599956d06c02d5` |
| `actor_player_hurt_s_02@1x.png` | x 21–45, y 10–50 | 25×41 | `67bc8428b344718c820d02d4f94d03566ef96435466fd6279da2319d2e05a796` |
| `actor_player_hurt_s_03@1x.png` | x 21–41, y 15–49 | 21×35 | `8b36a6783d4d4edbdd248971893e7d9fa42e493cf1c56ab08ef7bdc206113c1e` |

Across these south frames, nontransparent width runs 18–25 and height runs 33–41.

## Defeat

Clip `player_defeat`. Five south frames.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_player_defeat_s_01@1x.png` | x 16–53, y 24–63 | 38×40 | `af78b84b61fc9b58ccc2c87d69183514d10dcb63668500633b6ad76bfaded22e` |
| `actor_player_defeat_s_02@1x.png` | x 10–53, y 25–63 | 44×39 | `cc738f69554bad101a1fb4cbc910dc91bf1bf2e44afa5bd6f29c172dcd3982db` |
| `actor_player_defeat_s_03@1x.png` | x 10–53, y 26–63 | 44×38 | `a34b0c653fd12d46bb8a1710325ca8acfc94c5b749378cefaef30c4d629d755f` |
| `actor_player_defeat_s_04@1x.png` | x 10–47, y 30–63 | 38×34 | `3712536e00ffaf6e88a2458e1b1f974f2ad34c2772ab35109fe0af71ddac86dd` |
| `actor_player_defeat_s_05@1x.png` | x 16–53, y 0–63 | 38×64 | `891fb31c613bbfacc9a9b160d67f663685ebd456f3fd61fb6bffa61b29e3dc15` |

Across these south frames, nontransparent width runs 38–44 and height runs 34–64.

## Extraction

Clip `player_extraction`. Eight south frames.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_player_extraction_s_01@1x.png` | x 19–36, y 30–63 | 18×34 | `ccc143c741926fc05e6306315077db4b61e870144f99eab36e0d19f1dcd42fb9` |
| `actor_player_extraction_s_02@1x.png` | x 10–53, y 30–63 | 44×34 | `88ed193fec2a7de98710fc380b11fb0e0fec0f42ef328266d8cea853904e1275` |
| `actor_player_extraction_s_03@1x.png` | x 10–53, y 30–63 | 44×34 | `5ffb8c123452b1e31e78ef5d57fc4ffd675e2c7e2601c1564b9f5c9506689de4` |
| `actor_player_extraction_s_04@1x.png` | x 28–44, y 31–63 | 17×33 | `276648769e0a61ab4aa9c116995a0313bbc234a212fceef75d59510ed4ffed16` |
| `actor_player_extraction_s_05@1x.png` | x 18–53, y 0–63 | 36×64 | `1e301367802f73b79d88814de1edce947a80521a0a7d9e4854673f6effd7bde8` |
| `actor_player_extraction_s_06@1x.png` | x 10–53, y 0–63 | 44×64 | `98cd52dd9b1c90118dcb791bd9d0aa614536bab87870911afd10fd580389cf8d` |
| `actor_player_extraction_s_07@1x.png` | x 10–51, y 0–62 | 42×63 | `751d22c79b691656b83401a59c6c70a19dd61c8df5c2c07ecb690734f352a29a` |
| `actor_player_extraction_s_08@1x.png` | x 30–42, y 0–62 | 13×63 | `64a96c3bfaffaada4ce68cd25f32d035ef9440edcfd02026e6dec4ac9213bdc3` |

Across these south frames, nontransparent width runs 13–44 and height runs 33–64.

## Complete

Clip `player_complete`. Four south frames.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_player_complete_s_01@1x.png` | x 7–59, y 0–55 | 53×56 | `18a1b0bdcaa0a6e810e889b7625ecab1a71902f6790359e495b5a7a7504b1244` |
| `actor_player_complete_s_02@1x.png` | x 4–59, y 0–53 | 56×54 | `ecfbba894aeaded59ad1da44d6819c4f971d5371973ac794ae79f882e6867c07` |
| `actor_player_complete_s_03@1x.png` | x 4–59, y 0–55 | 56×56 | `2ac8b8536b82689eb65a22138681339cc2699bb7f4c03f5d7d784ad251e00255` |
| `actor_player_complete_s_04@1x.png` | x 4–57, y 0–55 | 54×56 | `868467b88e1213c4ffff8f471235243dac1cc5e8bf3d649d8f343a2aba871019` |

Across these south frames, nontransparent width runs 53–56 and height runs 54–56.
