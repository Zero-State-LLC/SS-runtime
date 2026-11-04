# Medal predicates

Read 2026-11-03 from `MedalTracker` on `3e32d76`. No medal number was changed.

A run earns medals only when the outcome is success. The canonical order is `GHOST`, `SHADOW`, `BLACKOUT`, `SURGICAL`, `SWIFT`.

| Medal | Predicate |
|---|---|
| `GHOST` | `quietApproach` is still true |
| `SHADOW` | no Transit Patrol member was alerted before M-A's first `waveStarted` |
| `BLACKOUT` | `networkBlackout` is true |
| `SURGICAL` | `integrity * 2 >= maxIntegrity` |
| `SWIFT` | the tick is under 19,800 |

`quietApproach` starts true. It becomes false when the detection state is `tracked`, `hunted`, or `lockdown` before M-C has activated. From M-C's activation tick on, that check is skipped, so the forced lockdown does not clear it.

Content `player.integrity` is 150. Under that maximum, 75 qualifies for `SURGICAL` and 74 does not. 19,800 ticks is 5:30 at 60 ticks a second. A tick of 19,800 does not qualify, because the test is strict less-than.

An alert on the same tick M-A starts counts as before, because the alert phase is published before the wave. Patrol member ids are learned from enemies that have a patrol.

These medals are presentation. They are not an input to the simulation. This does not retune a medal.
