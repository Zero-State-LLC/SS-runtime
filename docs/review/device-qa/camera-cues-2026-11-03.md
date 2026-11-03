# Camera cues

Read 2026-11-03 from `AudioProjector` on `241c167`. No cue was added.

A camera hit is one cue set per camera id on that tick.

| When | Cue | Haptic | Priority | Caption |
|---|---|---|---:|---|
| integrity after is 2 | `camera_hit_01` | light | 6 | Camera hit |
| integrity after is 1 | `camera_hit_02` | light | 6 | Camera hit |
| integrity after is 1 | `camera_critical` | warning | 4 | Camera critical |

Each destroyed camera appends both of these, destroy first.

| Cue | Haptic | Priority | Caption |
|---|---|---:|---|
| `camera_destroy` | rigid | 4 | Camera destroyed |
| `camera_field_off` | none | 4 | Camera field off |

If at least one camera was destroyed, one `camera_network_tamper` follows. Its haptic is rigid and its priority is 4. The variant is `min(3, destroyed count)`. The caption is `Network tamper 3+` when the variant is 3, and `Network tamper 1` or `Network tamper 2` otherwise. A variant above 0 sets the voice rate to `min(2.0, 1.0 + variant * 0.06)`.
