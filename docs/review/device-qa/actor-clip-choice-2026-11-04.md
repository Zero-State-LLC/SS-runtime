# Actor clip choice

Read 2026-11-04 from `ActorClipProjection` on `006304e`. No clip was added.

`isUnaware` is every awareness other than `aware`, so `unaware` and `struck` both take this idle path. A Fog Analytics Cloud, Cable-Car Correlator, Sutro Signal Witch, Autonomous Informant, or Victorian Vendor on that path presents that archetype's raw value plus `_idle`. The Improper Search Daemon and the Algorithmic Moderate have their own clips.

A daemon in `pursue` presents `improperSearchDaemon_pursuit`. `queryTelegraph`, `queryResolve`, `dashTelegraph`, `dash`, and `recover` present `improperSearchDaemon_` plus that state name. Any other daemon state returns nil.

A Captain with `recoveryRemaining` above 0 presents `algorithmicModerate_phaseTransition`. Otherwise a stored attack whose telegraph timer or attack timer is still positive presents `algorithmicModerate_` plus the attack's raw value. `ClipCatalog.clipId(for:)` is that string. A missing runtime, or a Captain with neither timer running, returns nil.

An aware standard enemy in `telegraph` presents `fogAnalyticsCloud_anticipate`, `cableCarCorrelator_anticipate`, `sutroSignalWitch_anticipate`, or `victorianVendor_anticipate` for those four roles. Cable `charge` presents `cableCarCorrelator_commit`. Cable `recover` presents `cableCarCorrelator_recover`. The Informant has no telegraph clip in this switch.

`pursue`, `orbit`, `keepRange`, and `cooldown` are locomotion. Zero velocity presents the role's raw value plus `_idle`. A moving Informant presents `autonomousInformant_anticipate`. Any other moving standard role presents the role's raw value plus `_move`. Any other state returns nil. Hurt, defeat, and the Fog, Witch, and Vendor commits are [reaction-clips-2026-11-04.md](reaction-clips-2026-11-04.md).
