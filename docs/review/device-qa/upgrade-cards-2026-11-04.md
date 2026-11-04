# Upgrade cards

Read 2026-11-04 from `UpgradePresentation` on `93f6d67`. No upgrade was added, and no effect number was changed.

The cards are index 0 Signal Jammer, "Surveillance control", "Build Exposure more slowly under surveillance.", "No Tamper or damage reduction."; index 1 Ricochet Pulse, "Crowd control", "A hit can continue to one nearby enemy or camera at full damage.", "Requires clear line of sight. No third hit."; index 2 Ghost Step, "Mobility and surveillance evasion", "Dodge faster and briefly disappear from camera detection.", "No damage immunity. Fog, Observation and Tamper still apply." Any other index is not an upgrade.

`applyUpgrade` stores that upgrade, clears the pending flag, sets the outcome back to playing, and emits `upgradeSelected` at phase 2. The effect numbers stay in [upgrade-effects-2026-11-03.md](upgrade-effects-2026-11-03.md). The tick order stays in [extraction-and-tick-2026-11-04.md](extraction-and-tick-2026-11-04.md). The command that passes the gate has both axes at 0 and dodge clear.
