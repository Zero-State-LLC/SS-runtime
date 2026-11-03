# Copied player directions, file by file

Measured 2026-11-03 from the runtime asset bytes on `9d4656c`. No new frame was added. `player_hurt`, `player_defeat`, and `player_extraction` ship the same PNG bytes in north, east, and west as the south file of the same frame number. The south rows stay in [player-action-frames-2026-11-03.md](player-action-frames-2026-11-03.md). The byte compare stays in [player-direction-copies-2026-11-03.md](player-direction-copies-2026-11-03.md).

Image coordinates start at the top left of the PNG. Bounds are inclusive. A pixel counts as nontransparent when its alpha is greater than 0. Each row below was hashed from its own file and measured again. The hash and the bounds match the south file of that frame.

Same bytes are not a facing. This does not close #65. The table is the 48 north, east, and west files.

## Hurt

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_player_hurt_n_01@1x.png` | x 23–40, y 15–47 | 18×33 | `a83d382295db881c942d6d2b43185cd67a5aeefa2e397e6ca9599956d06c02d5` |
| `actor_player_hurt_e_01@1x.png` | x 23–40, y 15–47 | 18×33 | `a83d382295db881c942d6d2b43185cd67a5aeefa2e397e6ca9599956d06c02d5` |
| `actor_player_hurt_w_01@1x.png` | x 23–40, y 15–47 | 18×33 | `a83d382295db881c942d6d2b43185cd67a5aeefa2e397e6ca9599956d06c02d5` |
| `actor_player_hurt_n_02@1x.png` | x 21–45, y 10–50 | 25×41 | `67bc8428b344718c820d02d4f94d03566ef96435466fd6279da2319d2e05a796` |
| `actor_player_hurt_e_02@1x.png` | x 21–45, y 10–50 | 25×41 | `67bc8428b344718c820d02d4f94d03566ef96435466fd6279da2319d2e05a796` |
| `actor_player_hurt_w_02@1x.png` | x 21–45, y 10–50 | 25×41 | `67bc8428b344718c820d02d4f94d03566ef96435466fd6279da2319d2e05a796` |
| `actor_player_hurt_n_03@1x.png` | x 21–41, y 15–49 | 21×35 | `8b36a6783d4d4edbdd248971893e7d9fa42e493cf1c56ab08ef7bdc206113c1e` |
| `actor_player_hurt_e_03@1x.png` | x 21–41, y 15–49 | 21×35 | `8b36a6783d4d4edbdd248971893e7d9fa42e493cf1c56ab08ef7bdc206113c1e` |
| `actor_player_hurt_w_03@1x.png` | x 21–41, y 15–49 | 21×35 | `8b36a6783d4d4edbdd248971893e7d9fa42e493cf1c56ab08ef7bdc206113c1e` |

## Defeat

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_player_defeat_n_01@1x.png` | x 16–53, y 24–63 | 38×40 | `af78b84b61fc9b58ccc2c87d69183514d10dcb63668500633b6ad76bfaded22e` |
| `actor_player_defeat_e_01@1x.png` | x 16–53, y 24–63 | 38×40 | `af78b84b61fc9b58ccc2c87d69183514d10dcb63668500633b6ad76bfaded22e` |
| `actor_player_defeat_w_01@1x.png` | x 16–53, y 24–63 | 38×40 | `af78b84b61fc9b58ccc2c87d69183514d10dcb63668500633b6ad76bfaded22e` |
| `actor_player_defeat_n_02@1x.png` | x 10–53, y 25–63 | 44×39 | `cc738f69554bad101a1fb4cbc910dc91bf1bf2e44afa5bd6f29c172dcd3982db` |
| `actor_player_defeat_e_02@1x.png` | x 10–53, y 25–63 | 44×39 | `cc738f69554bad101a1fb4cbc910dc91bf1bf2e44afa5bd6f29c172dcd3982db` |
| `actor_player_defeat_w_02@1x.png` | x 10–53, y 25–63 | 44×39 | `cc738f69554bad101a1fb4cbc910dc91bf1bf2e44afa5bd6f29c172dcd3982db` |
| `actor_player_defeat_n_03@1x.png` | x 10–53, y 26–63 | 44×38 | `a34b0c653fd12d46bb8a1710325ca8acfc94c5b749378cefaef30c4d629d755f` |
| `actor_player_defeat_e_03@1x.png` | x 10–53, y 26–63 | 44×38 | `a34b0c653fd12d46bb8a1710325ca8acfc94c5b749378cefaef30c4d629d755f` |
| `actor_player_defeat_w_03@1x.png` | x 10–53, y 26–63 | 44×38 | `a34b0c653fd12d46bb8a1710325ca8acfc94c5b749378cefaef30c4d629d755f` |
| `actor_player_defeat_n_04@1x.png` | x 10–47, y 30–63 | 38×34 | `3712536e00ffaf6e88a2458e1b1f974f2ad34c2772ab35109fe0af71ddac86dd` |
| `actor_player_defeat_e_04@1x.png` | x 10–47, y 30–63 | 38×34 | `3712536e00ffaf6e88a2458e1b1f974f2ad34c2772ab35109fe0af71ddac86dd` |
| `actor_player_defeat_w_04@1x.png` | x 10–47, y 30–63 | 38×34 | `3712536e00ffaf6e88a2458e1b1f974f2ad34c2772ab35109fe0af71ddac86dd` |
| `actor_player_defeat_n_05@1x.png` | x 16–53, y 0–63 | 38×64 | `891fb31c613bbfacc9a9b160d67f663685ebd456f3fd61fb6bffa61b29e3dc15` |
| `actor_player_defeat_e_05@1x.png` | x 16–53, y 0–63 | 38×64 | `891fb31c613bbfacc9a9b160d67f663685ebd456f3fd61fb6bffa61b29e3dc15` |
| `actor_player_defeat_w_05@1x.png` | x 16–53, y 0–63 | 38×64 | `891fb31c613bbfacc9a9b160d67f663685ebd456f3fd61fb6bffa61b29e3dc15` |

## Extraction

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_player_extraction_n_01@1x.png` | x 19–36, y 30–63 | 18×34 | `ccc143c741926fc05e6306315077db4b61e870144f99eab36e0d19f1dcd42fb9` |
| `actor_player_extraction_e_01@1x.png` | x 19–36, y 30–63 | 18×34 | `ccc143c741926fc05e6306315077db4b61e870144f99eab36e0d19f1dcd42fb9` |
| `actor_player_extraction_w_01@1x.png` | x 19–36, y 30–63 | 18×34 | `ccc143c741926fc05e6306315077db4b61e870144f99eab36e0d19f1dcd42fb9` |
| `actor_player_extraction_n_02@1x.png` | x 10–53, y 30–63 | 44×34 | `88ed193fec2a7de98710fc380b11fb0e0fec0f42ef328266d8cea853904e1275` |
| `actor_player_extraction_e_02@1x.png` | x 10–53, y 30–63 | 44×34 | `88ed193fec2a7de98710fc380b11fb0e0fec0f42ef328266d8cea853904e1275` |
| `actor_player_extraction_w_02@1x.png` | x 10–53, y 30–63 | 44×34 | `88ed193fec2a7de98710fc380b11fb0e0fec0f42ef328266d8cea853904e1275` |
| `actor_player_extraction_n_03@1x.png` | x 10–53, y 30–63 | 44×34 | `5ffb8c123452b1e31e78ef5d57fc4ffd675e2c7e2601c1564b9f5c9506689de4` |
| `actor_player_extraction_e_03@1x.png` | x 10–53, y 30–63 | 44×34 | `5ffb8c123452b1e31e78ef5d57fc4ffd675e2c7e2601c1564b9f5c9506689de4` |
| `actor_player_extraction_w_03@1x.png` | x 10–53, y 30–63 | 44×34 | `5ffb8c123452b1e31e78ef5d57fc4ffd675e2c7e2601c1564b9f5c9506689de4` |
| `actor_player_extraction_n_04@1x.png` | x 28–44, y 31–63 | 17×33 | `276648769e0a61ab4aa9c116995a0313bbc234a212fceef75d59510ed4ffed16` |
| `actor_player_extraction_e_04@1x.png` | x 28–44, y 31–63 | 17×33 | `276648769e0a61ab4aa9c116995a0313bbc234a212fceef75d59510ed4ffed16` |
| `actor_player_extraction_w_04@1x.png` | x 28–44, y 31–63 | 17×33 | `276648769e0a61ab4aa9c116995a0313bbc234a212fceef75d59510ed4ffed16` |
| `actor_player_extraction_n_05@1x.png` | x 18–53, y 0–63 | 36×64 | `1e301367802f73b79d88814de1edce947a80521a0a7d9e4854673f6effd7bde8` |
| `actor_player_extraction_e_05@1x.png` | x 18–53, y 0–63 | 36×64 | `1e301367802f73b79d88814de1edce947a80521a0a7d9e4854673f6effd7bde8` |
| `actor_player_extraction_w_05@1x.png` | x 18–53, y 0–63 | 36×64 | `1e301367802f73b79d88814de1edce947a80521a0a7d9e4854673f6effd7bde8` |
| `actor_player_extraction_n_06@1x.png` | x 10–53, y 0–63 | 44×64 | `98cd52dd9b1c90118dcb791bd9d0aa614536bab87870911afd10fd580389cf8d` |
| `actor_player_extraction_e_06@1x.png` | x 10–53, y 0–63 | 44×64 | `98cd52dd9b1c90118dcb791bd9d0aa614536bab87870911afd10fd580389cf8d` |
| `actor_player_extraction_w_06@1x.png` | x 10–53, y 0–63 | 44×64 | `98cd52dd9b1c90118dcb791bd9d0aa614536bab87870911afd10fd580389cf8d` |
| `actor_player_extraction_n_07@1x.png` | x 10–51, y 0–62 | 42×63 | `751d22c79b691656b83401a59c6c70a19dd61c8df5c2c07ecb690734f352a29a` |
| `actor_player_extraction_e_07@1x.png` | x 10–51, y 0–62 | 42×63 | `751d22c79b691656b83401a59c6c70a19dd61c8df5c2c07ecb690734f352a29a` |
| `actor_player_extraction_w_07@1x.png` | x 10–51, y 0–62 | 42×63 | `751d22c79b691656b83401a59c6c70a19dd61c8df5c2c07ecb690734f352a29a` |
| `actor_player_extraction_n_08@1x.png` | x 30–42, y 0–62 | 13×63 | `64a96c3bfaffaada4ce68cd25f32d035ef9440edcfd02026e6dec4ac9213bdc3` |
| `actor_player_extraction_e_08@1x.png` | x 30–42, y 0–62 | 13×63 | `64a96c3bfaffaada4ce68cd25f32d035ef9440edcfd02026e6dec4ac9213bdc3` |
| `actor_player_extraction_w_08@1x.png` | x 30–42, y 0–62 | 13×63 | `64a96c3bfaffaada4ce68cd25f32d035ef9440edcfd02026e6dec4ac9213bdc3` |
