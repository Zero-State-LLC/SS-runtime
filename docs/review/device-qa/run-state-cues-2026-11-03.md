# Run-state cues

Read 2026-11-03 from `AudioProjector` on `241c167`. No cue was added.

| Cue | Haptic | Priority | Caption | When |
|---|---|---:|---|---|
| `exposure_state_up` | warning | 3 | Detection, then the new state's raw value | the last detection change on the tick rose |
| `lockdown_enter` | heavy | 3 | Lockdown | `lockdownEntered` |
| `extraction_armed` | success | 2 | Phoenix Steps open | `extractionArmed` |
| `extraction_reset` | warning | 2 | Extraction reset | `extractionReset` |
| `extraction_tick` | light | 7 | Extraction, then the displayed second | the displayed second changed and remaining ticks are above 0 |
| `network_blackout` | success | 4 | Network Blackout 8/8 | `allCamerasDestroyed` |
| `boss_defeated` | success | 2 | Authority defeated: no further questions | `bossDefeated` |
| `run_success` | success | 2 | Run complete | `runSucceeded` |
| `player_death` | heavy | 1 | Player down | `runFailed` |

The displayed extraction second is `(remainingTicks + 59) / 60`. `boss_defeated` uses `CaptainCaptions.defeated`. The blackout cue is also the music-drop cue. The mix note records the delay before that file plays. The haptic still fires on the tick.
