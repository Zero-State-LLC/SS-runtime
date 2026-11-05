# Observation pulse

Read 2026-11-04 from `BossSystem.observationAmount` and `ExposureState.resolveTick` on `aaa7919`. No band was changed. Phase numerators stay in [elite-boss-attacks-2026-11-04.md](elite-boss-attacks-2026-11-04.md). The jammer ratio stays in [upgrade-effects-2026-11-03.md](upgrade-effects-2026-11-03.md). Fog scaling stays in [exposure-bands-2026-11-03.md](exposure-bands-2026-11-03.md).

The amount is a half-away division of the base times the phase numerator, over 100. When the jammer is owned, that result takes a second half-away division by the jammer pulse ratio. The field reports the literal 10 on a pulse tick. The live exposure adds `observationAmount` of that pulse, the current phase numerator, and whether the jammer is owned. A comparison copy passes the jammer flag false.

`resolveTick` adds those observation amounts as given. Fog is scaled inside the same call. A failure tick passes an empty fog list and an empty observation list, so the live pulse and the comparison copy are both omitted.

When the jammer is owned, a second `resolveTick` runs on a copy with the unmodified pulses and the jammer flag false. The copy leaves the live exposure where the first call put it. `jammerReducedExposure` is true when the live result is lower than the copy.

The contract test expects base 10 at numerator 105 to be 11 with the jammer off and 8 with the jammer on.

This does not change an exposure band.
