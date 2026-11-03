# Player north, east, and west frame 01

Measured 2026-11-03 from the runtime asset bytes on `bf173ec`. No new frame was added. The south idle and south move tables are in [player-sprite-bounds-2026-11-03.md](player-sprite-bounds-2026-11-03.md). The other south cycles are in [player-action-frames-2026-11-03.md](player-action-frames-2026-11-03.md). This note tables frame 01 of north, east, south, and west for idle and move, and records that the other directions are not copies of the south files.

Image coordinates start at the top left of the PNG. Bounds are inclusive. A pixel counts as nontransparent when its alpha is greater than 0.

The box and anchor are the ones in the player note: 64×64, anchor (32, 56). Every frame below has canvas 64×64. The south frame 01 hashes match that earlier note.

None of the four north, four east, or four west `player_idle` file hashes appears among the four south idle hashes. None of the six north, six east, or six west `player_move` file hashes appears among the six south move hashes. Different file bytes are not a production admission. This does not close #65, #131, or #132, and it does not prove a live cycle. North, east, and west of the dodge, recover, hurt, defeat, extraction, and complete clips are not tabulated here.

## Idle

Clip `player_idle`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_player_idle_n_01@1x.png` | x 22–41, y 8–55 | 20×48 | `bb98b4a578f27e4f0a6397a18555b9dfaacf6d548aff69fd56b1f87a24e4af68` |
| `actor_player_idle_e_01@1x.png` | x 26–37, y 8–55 | 12×48 | `975f700e74ddd28f2e257bd2295c4d0d20da87c2d1faba953d1d4d76b84701cf` |
| `actor_player_idle_s_01@1x.png` | x 20–42, y 5–55 | 23×51 | `f45ca16776f7e4b4475ef8f7cbe7791abbb4b371f24902b600c5d8468a8dd6f4` |
| `actor_player_idle_w_01@1x.png` | x 27–36, y 16–55 | 10×40 | `fac6c5c0aa66ee89a8fffa4b66b4f2a48ade5dcf254bda6653a1b39c69058bf7` |

## Move

Clip `player_move`.

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_player_move_n_01@1x.png` | x 25–38, y 15–55 | 14×41 | `d7596bcdaadad0ce988b8d4ef0711c1b7b60989f2af2ccf8b050cb67ba8b44be` |
| `actor_player_move_e_01@1x.png` | x 19–44, y 18–55 | 26×38 | `1210a72673d5ec47714d87872060d24b50c3cf11c59642c2a1440afe704cb187` |
| `actor_player_move_s_01@1x.png` | x 22–42, y 7–55 | 21×49 | `7b3434af45c8bea2a987866f7041ae0299a65899f54e7c17d5012642f37d0108` |
| `actor_player_move_w_01@1x.png` | x 21–42, y 7–55 | 22×49 | `cb50d35b35964d68843826eedb3dd2ce7b6f2ab256345b17a00abf89950131c9` |
