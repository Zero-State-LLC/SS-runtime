# The awareness block, and the heat table

Read 2026-11-05 from `CombatContent.parseAwareness` on `ef68565`. No alert was added. The rank order and the live alert stay in [awareness-alerts-2026-11-04.md](awareness-alerts-2026-11-04.md). The stored heat counts stay in [heat-awareness-patrol-2026-11-04.md](heat-awareness-patrol-2026-11-04.md).

An unknown awareness key, or a missing required key, fails closed. `appliesTo` must be an array of strings. An unknown name is `unknownArchetype`. `improperSearchDaemon` and `algorithmicModerate` are `wrongType`. Sight must be at least 1. Ally radius, drift percent, and drift stop must be at least 0. The ambush multiplier must be at least 1. A JSON boolean fails those integers. `surveillanceAlertState` must be a `DetectionState` raw value. `awareEncounters` must be an array of strings. `heatReinforcementsSpawnAware` must be a JSON boolean.

`parseHeat` requires a known reinforcement archetype. `encounters` must be an array of strings. `byDetectionState` must name `hidden`, `observed`, `tracked`, `hunted`, and `lockdown`, each an integer at least 0. Any other key in that table is `wrongType`.

This does not change a count.
