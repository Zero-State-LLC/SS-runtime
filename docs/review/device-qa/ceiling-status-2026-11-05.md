# Ceiling status

Read 2026-11-05 from `D021Ceilings.fromSimulation` on `ef68565`. No ceiling was changed.

The scenarios that feed it stay in [peak-density-2026-11-05.md](peak-density-2026-11-05.md). The byte fields that settle a device run stay in [device-run-gates-2026-11-05.md](device-run-gates-2026-11-05.md). The expansion decision stays in [expansion-gate-2026-11-05.md](expansion-gate-2026-11-05.md).

The schema is `d021-ceilings-001`. `fromSimulation` copies the report's aggregate peaks and sets the status to `simulationMeasured`. Resident bytes and atlas bytes stay nil, so `isSettled` is false. `withDeviceProfiling` stores both byte counts and sets the status to `settled`. `pendingDeviceProfiling` is the third status string.

`metricsWithinCeilings` requires each of the seven peaks to be at most the stored ceiling. `sampleWithinSimulationCeilings` uses the same seven comparisons on one sample. `gateC011PassesSimulationBounds` requires every scenario in the report to sit within the ceilings.

This does not settle a device.
