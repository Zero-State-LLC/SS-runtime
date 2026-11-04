# Elite cycle and boss attacks

Read 2026-11-04 from `combat-content-009`, `civic-seam-arena-004`, and `Simulation` on `49759ab`. No attack number was changed. Cue ids stay in [boss-upgrade-cues-2026-11-03.md](boss-upgrade-cues-2026-11-03.md).

## Elite

`improperSearchDaemon` has hp 450, radius 26, speed 108, contact 14. The arena spawns it at (1792, 832). It spawns when M-A, M-B, and M-C are complete, it is not already defeated, none is alive, and the player is inside `trigger-elite` (center (1792, 768), half-size (80, 80)). The body starts in `pursue` with `stateTicks` 120. `nextSpecialTick` is the spawn tick plus `spawnDelay` 90. `eliteActivated` is phase 16.

The content cycle is pursuit 120, query telegraph 45, query resolve 0, dash telegraph 36, dash 30, recover 60.

## Boss

`algorithmicModerate` has hp 1600, radius 30, base speed 96, base contact 10, initial delay 90, transition recovery 45. The arena spawns it at (2048, 768). It spawns when the elite is defeated, the boss is not, none is alive, and the player is inside `trigger-boss` (center (1984, 640), half-size (96, 96)). The live step passes `content.bossSpeed`. `IsolatedKernel` still passes base speed 120 into its own boss step. The body starts in `pursue` with `stateTicks` 0, and `nextSpecialTick` is the spawn tick plus 90. `BossRuntime` starts `recoveryRemaining` at 90, and a phase change sets it to 45. Those match `initialDelay` and `transitionRecovery`. The assignments are the literals in `BossSystem`, not a read of the content fields. The phase starts at `publicSafety`. `bossActivated` is phase 16, and it closes `gate-mc-forward`. The court floor on that tick is in [player-integrity-2026-11-04.md](player-integrity-2026-11-04.md).

Phase speed is `baseSpeed * numerator / 100`, half away, then the same per-second conversion as a standard enemy. The content floors and ratios are:

| Phase | Min HP | Observation | Speed | Contact | Orbit | Sequence |
|---|---|---|---|---|---|---|
| `publicSafety` | 1200 | 105/100 | 100/100 | 100/100 | 0/100 | `safetyRationale`, `narrowTailoring` |
| `civilLiberties` | 800 | 108/100 | 90/100 | 104/100 | 72/100 | `narrowTailoring`, `safetyRationale`, `temporaryOrder` |
| `temporarySafeguard` | 400 | 112/100 | 118/100 | 110/100 | 18/100 | `temporaryOrder`, `narrowTailoring`, `safetyRationale` |
| `independentReview` | 1 | 116/100 | 104/100 | 116/100 | −55/100 | `independentReview`, `narrowTailoring`, `temporaryOrder` |

| Attack | Shipped values |
|---|---|
| `safetyRationale` | telegraph 45, range 260, angle 70000, damage 18, cooldown 90 |
| `narrowTailoring` | telegraph 30, angles −12000, 0, 12000, speed 420, radius 7, lifetime 72, damage 9, cooldown 75 |
| `temporaryOrder` | telegraph 48, active 180, pulse every 30, exposure 10, cooldown 120 |
| `independentReview` | telegraph 60, 6 lanes, 5 projectiles, speed 360, radius 7, lifetime 90, damage 8, cooldown 105 |

This does not change the Captain's content speed or the isolated kernel's 120.
