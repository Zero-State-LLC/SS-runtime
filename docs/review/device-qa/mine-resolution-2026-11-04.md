# Mine resolution

Read 2026-11-04 from the mine loop in `resolvePlayerDeathAndContact` on `fcab4e5`. No mine number was changed.

The content range, arm, life, radius, and damage stay in [standard-enemy-stats-2026-11-04.md](standard-enemy-stats-2026-11-04.md). The drawn mine stays the filled disc that note records.

Each tick sets `armRemaining` to the previous value minus 1, floored at 0, and subtracts 1 from `lifeRemaining` with no floor. `armed` is `armRemaining <= 0`. A mine whose life is still above 0, that is armed, and whose squared distance to the player is at most radius squared, deals `mine.damage` once. The kind is `mine`, the owner is the mine's owner, and the source position is the mine. That mine is then removed. An unarmed mine, or an armed mine that misses, stays while life remains. A life that the decrement has already brought to 0 or below is dropped on that same pass, with no hit test.

The vendor places the mine on the telegraph tick that reaches 0, at the player's position. That placement does not require a clear line, and it does not set `lockPosition`. When that vendor already holds `mine.maximum` mines, the oldest, the lower id, is removed first. The new mine is then appended.
