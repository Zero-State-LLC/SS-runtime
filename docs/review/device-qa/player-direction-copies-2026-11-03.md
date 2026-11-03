# Which player directions are the same file bytes

Measured 2026-11-03 from the runtime asset bytes on `1d9754c`. No new frame was added. Comparison is the SHA-256 of each PNG file, and a byte compare of each north, east, and west file with the south file of the same frame number. The south bounds and hashes for hurt, defeat, and extraction are in [player-action-frames-2026-11-03.md](player-action-frames-2026-11-03.md). Idle and move frame 01 are in [player-facing-frame-01-2026-11-03.md](player-facing-frame-01-2026-11-03.md).

`player_hurt`, `player_defeat`, and `player_extraction` ship the same bytes in north, east, south, and west. Frame 01 of hurt is `a83d382295db881c942d6d2b43185cd67a5aeefa2e397e6ca9599956d06c02d5` in all four directions, which is the south hash already in the action note. The same is true of the other frames of those three clips: each north, east, and west file matches the south file of that frame number.

The other five player clips do not. No north, east, or west file hash appears in the south set.

| Clip | Frames in one direction | North, east, and west |
|---|---|---|
| `player_idle` | 4 | no hash shared with south |
| `player_move` | 6 | no hash shared with south |
| `player_dodge` | 4 | no hash shared with south |
| `player_recover` | 2 | no hash shared with south |
| `player_complete` | 4 | no hash shared with south |
| `player_hurt` | 3 | same bytes as south, same frame order |
| `player_defeat` | 5 | same bytes as south, same frame order |
| `player_extraction` | 8 | same bytes as south, same frame order |

The same comparison across the other 45 role-states in the bundle finds no shared hash. That set is the seven `algorithmicModerate` states, the eight `improperSearchDaemon` states, and every state of the five standard enemies. None of those north, east, or west files repeats a south file from the same state.

Same bytes are not a facing, and different bytes are not a production admission. This does not close #65, #131, or #132, and it does not replace a frame.
