# Player movement

Read 2026-11-04 from `PlayerBody` and `Movement` on `49759ab`. No speed was changed.

Walk speed is 4 units per tick. A dodge is 8 units per tick for 12 ticks. The cooldown is 120 ticks. A dodge starts on the rising edge of `dodgePressed`, and only when the tick is at least `dodgeReadyTick` and no dodge is already active. `dodgeReadyTick` starts at 1. A press that is not ready increments `rejectedDodges`.

`displacement` scales the stick by `PlayerCommand.axisMaximum` (32,767). A stick longer than that limit is normalized. A dodge with both axes at 0 continues along the facing, at the dodge speed. Facing updates only when the delta is nonzero. The move is `Collision.slideCircle` with radius 18.

Ghost Step's 9 units per tick, cooldown 90, and camera-invisible-until `start + 29` are the kernel constants. The content record's 18 ticks after the dodge are the same window: 29 covers the 12 active ticks and the 18 after them. The upgrade table stays in [upgrade-effects-2026-11-03.md](upgrade-effects-2026-11-03.md).

This does not add a verb.
