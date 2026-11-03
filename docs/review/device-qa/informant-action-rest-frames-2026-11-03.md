# Informant pursuit frames in north, east, and west

Measured 2026-11-03 from the runtime asset bytes on `df637da`. No new frame was added. Frame 01 in these directions stays in [enemy-action-facing-frame-01-2026-11-03.md](enemy-action-facing-frame-01-2026-11-03.md). The south frames stay in [enemy-south-action-rest-2026-11-03.md](enemy-south-action-rest-2026-11-03.md) and [enemy-south-commit-rest-2026-11-03.md](enemy-south-commit-rest-2026-11-03.md). The anchor stays the one in the enemy note: (32, 56).

Image coordinates start at the top left of the PNG. Bounds are inclusive. A pixel counts as nontransparent when its alpha is greater than 0.

`autonomousInformant` has no move clip. `pursuit` is frames 02–03. `pursuitCommit` is frame 02. Every frame below has canvas 64×64. The table is those frames in north, east, and west: 9 files. This does not close #131 or #132.

## Pursuit

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_autonomousInformant_pursuit_n_02@1x.png` | x 21–44, y 8–53 | 24×46 | `0d9ffd40209925e1c1c1e7c277037308b5221ad172d727e157537064c61edbd4` |
| `actor_autonomousInformant_pursuit_e_02@1x.png` | x 13–49, y 14–53 | 37×40 | `68ffafed84a207ec2119a637c8dd295d6e9273d7b1798aab0d9220906b64f85d` |
| `actor_autonomousInformant_pursuit_w_02@1x.png` | x 13–49, y 14–53 | 37×40 | `fac1943d671a115bf7cb26afa585128244389c2c002e19e878afd3ca0b750e53` |
| `actor_autonomousInformant_pursuit_n_03@1x.png` | x 10–36, y 8–55 | 27×48 | `155be7241fda886e0fbfd6608fcf6308e2f47146237e215d1d7d53971d41b559` |
| `actor_autonomousInformant_pursuit_e_03@1x.png` | x 10–52, y 7–44 | 43×38 | `05aba389cba7c8891d250a83babfb3a2889a716b7bb439f235f269b4386f9ba9` |
| `actor_autonomousInformant_pursuit_w_03@1x.png` | x 10–52, y 7–44 | 43×38 | `f279ffdc281d8e0b96ca8fc2a27406d7995f23b79cf3ab655ebf50467f81e177` |

## Pursuit commit

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_autonomousInformant_pursuitCommit_n_02@1x.png` | x 6–49, y 14–55 | 44×42 | `38d44c6e6a528ce5fad3b70d71e87432a9c98113b3b0155418d88095e81a3b00` |
| `actor_autonomousInformant_pursuitCommit_e_02@1x.png` | x 5–58, y 11–44 | 54×34 | `6ecf29a0d4d885c04414614380cf4138402b18a14cc5412c398219c8a80799df` |
| `actor_autonomousInformant_pursuitCommit_w_02@1x.png` | x 5–58, y 11–44 | 54×34 | `64c26c9d8a4c836381628a278c26c9f8c098a6ff4b00ddc1a1289768113572ac` |
