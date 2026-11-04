# Exposure bands

Read 2026-11-03 from `ExposureState` on `3e32d76`. No band was changed.

`DetectionState.projected` maps the exposure integer.

| Exposure | State |
|---|---|
| 0–199 | `hidden` |
| 200–449 | `observed` |
| 450–699 | `tracked` |
| 700–999 | `hunted` |
| 1000 | `lockdown` |

Exposure is clamped to 0 through 1000. While a lockdown is in force, or a tick forces one, exposure is set to 1000. A forced lockdown that is not yet latched also sets the reason to `forcedLockdown`.

Contact from surviving cameras is `min(5, 2 + n - 1)` for `n` cameras, and 0 when `n` is 0. Signal Jammer then subtracts 1, and the result stays at least 1. The upgrade note records the jammer constants.

With no surviving contact and no lockdown, `noContactTicks` increases by 1. After more than 60 such ticks, exposure falls by 2, and it does not fall below `150 * cameras destroyed`. That floor limits recovery. It does not raise exposure.

Each tamper amount is added as given. `tamperSpike` and `tamperFloorPerCamera` are both 150. Fog and observation pulses are added after the contact step, and each is clamped at 1000. Fog is scaled by 75/100 when Signal Jammer is owned. The court release assigns 700 and clears the lockdown latch. The detection state is left for the next resolution.

Reaching 1000 latches lockdown on that tick. This does not change exposure.
