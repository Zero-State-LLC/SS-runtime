# Directions that do not copy each other

Measured 2026-11-03 from the runtime asset bytes on `8c37807`. No new frame was added. [player-direction-copies-2026-11-03.md](player-direction-copies-2026-11-03.md) records that `player_hurt`, `player_defeat`, and `player_extraction` are the same bytes in every direction, and that the other clips do not share a south hash.

This note records the rest. The bundle has 940 `actor_*@1x.png` files in 53 clips. Each clip has north, east, south, and west at every frame index it ships. Outside those three clips, that is 50 clips and 876 files: `player_idle`, `player_move`, `player_dodge`, `player_recover`, `player_complete`, and the 45 role-states named in the direction-copies note.

Comparison is the SHA-256 of each PNG file. For each of those 50 clips, a hash from one direction does not appear on another direction, including at a different frame index. North is not a copy of east or of west.

Same bytes are not a facing. Different bytes are not a production admission. This does not close #65, and it does not replace a frame.
