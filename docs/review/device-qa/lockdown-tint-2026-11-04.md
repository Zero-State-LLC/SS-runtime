# Lockdown tint

Read 2026-11-04 from `LockdownTint` on `93f6d67`. The tint was not changed.

While detection is lockdown, the world layer takes a red tint. The base opacity is 0.06 and the peak is 0.10. The period is 120 ticks. Reduced flash or reduced motion holds the opacity at 0.06. Otherwise the opacity is a raised cosine from 0.06 at the start of the period to 0.10 at the middle. The HUD is not tinted.

The multiplier is `(1, 1 − opacity, 1 − opacity)`. Every channel stays at or below 1. The function returns nil when detection is not lockdown. Detection bands stay in [exposure-bands-2026-11-03.md](exposure-bands-2026-11-03.md).
