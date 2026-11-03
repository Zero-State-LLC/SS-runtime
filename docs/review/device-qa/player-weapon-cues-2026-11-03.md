# Player and weapon cues

Read 2026-11-03 from `AudioProjector` on `241c167`. No cue was added.

A larger priority number is dropped first when the voice ceiling is exceeded. The ceiling is in the voice note.

| Cue | Haptic | Priority | Caption | Gate |
|---|---|---:|---|---|
| `weapon_civic_pulse` | none | 6 | Civic Pulse | one `weaponFired` event, then not again for 6 ticks |
| `impact_enemy` | none | 6 | Impact | at most two hits, highest damage first |
| `player_damage` | light | 5 | Player damaged | one `playerDamaged` event, then not again for 15 ticks |
| `player_dodge` | light | 7 | Dodge | one `dodgeStarted` event |

`impact_enemy` skips the player and any camera already counted as a camera hit. Ties in damage keep the lower entity id.
