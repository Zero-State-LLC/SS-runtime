# Forward gates

Read 2026-11-04 from `Simulation` on `93f6d67`. No gate was moved.

Activating M-A, M-B, or M-C calls `closeForwardGate`. That closes `gate-ma-forward`, `gate-mb-forward`, or `gate-mc-forward`. It leaves the gate open when the player circle of radius 18 penetrates the gate box.

Killing the elite sets `eliteDefeated`, schedules `eliteGateOpenTick` at the death tick plus 60, emits `eliteDefeated` at phase 16, and calls `releaseForCourt`. That call clears `lockdownEntered` and assigns the court exposure. [exposure-bands-2026-11-03.md](exposure-bands-2026-11-03.md) records that assignment as 700. The detection state is left for the next tick. `openEliteGateIfDue` opens `gate-elite-forward` once the tick has reached the scheduled tick, then clears the schedule.

Killing the boss sets `bossDefeated`, retires the boss field and the boss projectiles, emits `bossDefeated` at phase 16, and opens `gate-boss-extraction` on that same tick. Boss spawn still closes `gate-mc-forward`. That sentence stays in [elite-boss-attacks-2026-11-04.md](elite-boss-attacks-2026-11-04.md).
