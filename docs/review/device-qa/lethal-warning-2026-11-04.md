# Lethal warning

Read 2026-11-04 from `LethalWarning` on `aaa7919`. No damage was dealt. The card string stays in [tutorial-timing-2026-11-04.md](tutorial-timing-2026-11-04.md). The digest fields stay in [state-digest-2026-11-04.md](state-digest-2026-11-04.md). The live scale and the three-contact cap stay in [player-integrity-2026-11-04.md](player-integrity-2026-11-04.md). The live attacks stay in [boss-attack-resolve-2026-11-04.md](boss-attack-resolve-2026-11-04.md).

The warning is presentation. It writes nothing, and the digest carries none of it. `isOn` is the discrete prediction or the contact prediction. The simulation stores that in `lethalWarningPreempts`.

Contact gathers living enemies whose awareness is `aware` and whose squared distance to the player is at most the sum of the two radii times the Q8 scale, squared. `isUnaware` is every awareness other than `aware`, so `struck` stays out of this list with `unaware`. The boundary counts. The list sorts by higher `contactDps`, then lower id, and sums the first three. Sixty ticks run on copies: the accumulator adds the summed dps, whole points are the quotient by 60, and the remainder stays. Those points go through `scaleDamageTaken` at the content damage-taken percent. Integrity that starts at or below 0, a dps of 0, or a horizon of 0 stays quiet. The warning is on when a copy reaches integrity at or below 0. The copies leave the player where it was.

A discrete amount is scaled on a fresh remainder copy. It warns when the removed points are at least the current integrity. An amount of 0, or integrity at or below 0, stays quiet.

The boss prediction runs while `telegraphRemaining` is above 0, a current attack is set, and a living `algorithmicModerate` exists. Safety uses the resolve cone and a clear line, then tests 18. Narrow sums 9 for each of the three offsets whose predicted bolt contains the player, at speed 420, radius 7, and lifetime 72. Independent sums 8 for each containing lane from `independentReviewLanes`, at speed 360, radius 7, and lifetime 90. Temporary order stays quiet. The prediction fires nothing.

The elite and witch loop uses that same `aware` filter. The elite prediction runs in `queryTelegraph` and tests `DaemonQuery.damage` of the stored markers. The witch prediction runs in `telegraph` while `stateTicks` is above 0. Its velocity is `Targeting.direct` toward the player at the content shot speed, and the contain test uses that shot's radius, lifetime, and damage. The shot numbers stay in [standard-enemy-stats-2026-11-04.md](standard-enemy-stats-2026-11-04.md).

The predicted bolt starts the way `fire` starts one: position is the origin plus the velocity, previous is the origin, age is 1, and the travelled distance is `isqrt` of the velocity. While age is within the lifetime, an age above 1 takes another step, and then age increases. A bolt outside the arena raw bounds, an age past the lifetime, or travel past 10,000 times the Q8 scale is a miss. A wall entry time at or before the player sweep time is a miss. A player sweep with no earlier wall is a hit. A wall with no player sweep is a miss. The first tick leaves the age-1 bolt where it spawned. The velocity matches `fire`: the heading unit times `speedQ8`, half-away over the Q15 scale. The spawn step is in [projectile-step-2026-11-04.md](projectile-step-2026-11-04.md). The wall time is in [line-of-fire-2026-11-04.md](line-of-fire-2026-11-04.md).

The discrete check is that boss telegraph, the elite query telegraph, and the witch telegraph.

This does not deal the damage.
