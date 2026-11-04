# Touch command

Read 2026-11-04 from `TouchController` on `93f6d67`. The stick arithmetic was not changed.

The command axes run from −32,767 to 32,767. The stick clamps the finger to its radius, so a diagonal stays inside the unit circle. Magnitude is that clamped length over the radius, in thousandths, rounded to the nearest integer. At 150 or below, both axes are 0. Above 150, the live band remaps linearly onto 0…1 by `(magnitude − 150) / 850`. Point space is y-down, and the command is y-up, so the y unit is negated. Each axis is then quantized half-away-from-zero into the command range.

A dodge touch sets one rising edge. `takeCommand` returns that edge once and clears it. Releasing the stick zeroes both axes. A pause touch is a pause hit and does not claim the stick.

The stick may begin in its half of the safe canvas from 30 percent of the height to the bottom: the right half for the right hand, the left half for the left hand. The knob is centred on the drawn stick. Walk speed and dodge length stay in [player-movement-2026-11-04.md](player-movement-2026-11-04.md).
