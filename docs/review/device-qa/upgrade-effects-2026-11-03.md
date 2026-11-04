# Upgrade effects

Read 2026-11-03 from `combat-content-009` and `ExposureState` on `3e32d76`. No upgrade was added. The three ids stay `signalJammer`, `ricochetPulse`, and `ghostStep`.

| Upgrade | Shipped values |
|---|---|
| `signalJammer` | contact reduction 1, minimum contact 1, pulse ratio 75/100, heat reinforcement reduction 2 |
| `ricochetPulse` | 1 continuation, range 160, enemy damage 10, camera damage 1, continuation requires an enemy kill |
| `ghostStep` | dodge speed 540, dodge ticks 12, cooldown 90, camera immunity 18 ticks after the dodge |

Signal Jammer's contact change is applied in `ExposureState.contactDelta`. Its pulse ratio scales fog amounts. Heat reinforcements for M-A and M-B drop by 2, and the count stays at least 0. The content record states the same four numbers.

Ghost Step's dodge speed is in the same units as the content dodge. The post-dodge immunity is `postDodgeCameraImmunity` 18. The cue for selecting any of the three is already in the boss and upgrade cue note.

This does not add a fourth upgrade.
