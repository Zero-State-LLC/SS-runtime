# Remaining dodge, recover, and complete frames in north, east, and west

Measured 2026-11-03 from the runtime asset bytes on `8366209`. No new frame was added. The south frames stay in [player-action-frames-2026-11-03.md](player-action-frames-2026-11-03.md). Frame 01 of north, east, and west stays in [player-action-facing-frame-01-2026-11-03.md](player-action-facing-frame-01-2026-11-03.md). The box and anchor stay the ones in [player-sprite-bounds-2026-11-03.md](player-sprite-bounds-2026-11-03.md): 64×64, anchor (32, 56).

Image coordinates start at the top left of the PNG. Bounds are inclusive. A pixel counts as nontransparent when its alpha is greater than 0.

Every frame below has canvas 64×64. The table is dodge frames 02–04, recover frame 02, and complete frames 02–04, in north, east, and west: 21 files. This does not close #65, #131, or #132, and it does not prove a live cycle.

## Dodge

Clip `player_dodge`. Frame 01 in these directions stays in [player-action-facing-frame-01-2026-11-03.md](player-action-facing-frame-01-2026-11-03.md).

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_player_dodge_n_02@1x.png` | x 4–59, y 21–55 | 56×35 | `e1ae4bbafe38030e642f53964816e0e3a3c52c8b4042de8a845a5719c29c239d` |
| `actor_player_dodge_e_02@1x.png` | x 4–59, y 19–55 | 56×37 | `2586cb1fa6d23b49b093afd4b344785dc9c2a387374b42ba8af41bd2cf4891d1` |
| `actor_player_dodge_w_02@1x.png` | x 4–58, y 19–55 | 55×37 | `dbb666b434bb9bc37bb6371600551a8b0f32213a29d91640f764c9503bb5a63a` |
| `actor_player_dodge_n_03@1x.png` | x 4–59, y 24–55 | 56×32 | `720b4e6ee4336c45f39ecf17a71af733158f5126df5acf12a8e553bd23f4e43c` |
| `actor_player_dodge_e_03@1x.png` | x 4–59, y 19–55 | 56×37 | `28a4d7c178817691eb68d8bc06afebb2f7b104f39a235b11095d48db88200896` |
| `actor_player_dodge_w_03@1x.png` | x 5–59, y 19–53 | 55×35 | `ad47ab5ce58c0a79cd9aa850670b3c3129029151711e427ed5e3694f1698b4ce` |
| `actor_player_dodge_n_04@1x.png` | x 4–58, y 18–55 | 55×38 | `75ec0e22e59a8c9a3c455aaf51a5b0a4238c7c0b712cbfd211b37219ea5a881a` |
| `actor_player_dodge_e_04@1x.png` | x 4–57, y 17–55 | 54×39 | `d3cb8ca8cb7251df5e0580e5c04f331c42c714c4994ef5b412e5e0dfafb323a3` |
| `actor_player_dodge_w_04@1x.png` | x 4–57, y 19–55 | 54×37 | `6eab51465cae973371c9513c1ad1006a2ee05f1198192abe7b196a49a3d0b147` |

## Recover

Clip `player_recover`. Frame 01 in these directions stays in [player-action-facing-frame-01-2026-11-03.md](player-action-facing-frame-01-2026-11-03.md).

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_player_recover_n_02@1x.png` | x 6–31, y 20–55 | 26×36 | `ea19406da9cb48916f931ad676f0e39164fd2604fa7e6ae38c2bea4620a7f2cb` |
| `actor_player_recover_e_02@1x.png` | x 8–27, y 29–55 | 20×27 | `1aa72f1be008c534828559b6a185dcc15524efad070453593770ddcf31faf166` |
| `actor_player_recover_w_02@1x.png` | x 7–38, y 35–55 | 32×21 | `ac3c3ce6df07dcf65b4f20e85be71ec16fd13b4eedc286f8fad11fc8c6b32ba7` |

## Complete

Clip `player_complete`. Frame 01 in these directions stays in [player-action-facing-frame-01-2026-11-03.md](player-action-facing-frame-01-2026-11-03.md).

| Frame | Bounds | Span | sha256 |
|---|---|---|---|
| `actor_player_complete_n_02@1x.png` | x 4–59, y 10–55 | 56×46 | `0df49062db6544ffaadf790d999e1ec3deecf235c1ad9c277edeab6d930362f2` |
| `actor_player_complete_e_02@1x.png` | x 4–59, y 2–53 | 56×52 | `b7acb2e57c95295d78c22a72363f0bddb0c4ea4a0e2bd154ef9781ba13df21a9` |
| `actor_player_complete_w_02@1x.png` | x 4–59, y 1–53 | 56×53 | `25fb76cc62ee8567825105782d586c69340545f9869dfeccdc84b762a4bc6279` |
| `actor_player_complete_n_03@1x.png` | x 4–59, y 3–55 | 56×53 | `4ee3c7021932365fa48519f0da31fa7ecf1b48b8f7a5e8a996f88e7ec25614cd` |
| `actor_player_complete_e_03@1x.png` | x 6–59, y 0–54 | 54×55 | `8267562adc647d0f501737b05473dc54ce6b4f2cb2774ee32f092dbab2f79544` |
| `actor_player_complete_w_03@1x.png` | x 4–59, y 0–55 | 56×56 | `1e90cf22ea3489fed8a7b0e61e62a0e3175cea714e3a5f5d03d9ed322ec4ee0f` |
| `actor_player_complete_n_04@1x.png` | x 5–57, y 0–55 | 53×56 | `90476f7443032dd58f92a59eca43f30d75cb35cd2e03ac18fb702967590443b4` |
| `actor_player_complete_e_04@1x.png` | x 4–57, y 0–55 | 54×56 | `657f216de56edf7a6571d557599a62ecc3719f8046de4314f3416a324c911b6d` |
| `actor_player_complete_w_04@1x.png` | x 4–58, y 0–54 | 55×55 | `f63ccc44dc7f61f8d8cbc3e9b8fa0d682a5ced579b29162bf73b2b233cfedc6a` |
