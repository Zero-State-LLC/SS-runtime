# Upgrade choice layout

Read 2026-11-04 from `UpgradeSelectionView` on `5d954be`. No upgrade was added.

The card name, role, effect, and exclusions stay in [upgrade-cards-2026-11-04.md](upgrade-cards-2026-11-04.md). The effect numbers stay in [upgrade-effects-2026-11-03.md](upgrade-effects-2026-11-03.md). The command gate stays in [extraction-and-tick-2026-11-04.md](extraction-and-tick-2026-11-04.md).

The sheet shows while a choice is pending. Its title is `Choose one upgrade`. The next line is `The run is paused while you choose.` The backdrop is red 0.035, green 0.05, blue 0.07. Three columns are used when the width is at least 760 and the type size is not an accessibility size. Otherwise the cards are one column.

`synchronize` clears the submitted flag when the pending flag changes. `submit` accepts an index once, while the sheet is up and `UpgradeID.from` accepts the index. The buttons then disable.

Each button adds a symbol, a numeric line, and a VoiceOver label. Signal Jammer uses `antenna.radiowaves.left.and.right.slash`, prints `Camera gain −1/tick (min 1); Fog/Observation −25%`, and speaks `Signal Jammer. Surveillance control. Reduces camera contact gain by one point per tick, minimum one. Reduces fog and boss observation pulses by twenty-five percent. No Tamper or damage reduction.` Ricochet Pulse uses `arrow.triangle.branch`, prints `One continuation per hit; 160 unit range`, and speaks `Ricochet Pulse. Crowd control. Each civic pulse hit may continue once to a second enemy or camera within one hundred sixty units, excluding the first target, at full damage with clear line of sight. No third hit.` Ghost Step uses `figure.run`, prints `540 u/s for 0.2 s; 1.5 s cooldown; 0.5 s camera concealment; no damage immunity`, and speaks `Ghost Step. Mobility and surveillance evasion. Dodge speed five hundred forty units per second for zero point two seconds, one point five second cooldown, camera concealment for thirty ticks including dodge start, zero point five seconds. No damage immunity. Fog, Observation and Tamper still apply.`

This does not add an upgrade.
