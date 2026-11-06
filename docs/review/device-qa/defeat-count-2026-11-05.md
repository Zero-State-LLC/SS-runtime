# The defeat count

Read 2026-11-05 from `Simulation.killEnemy` on `ef68565`. No enemy was added.

The elite gate and the boss gate stay in [forward-gates-2026-11-04.md](forward-gates-2026-11-04.md). The receipt field stays in [run-receipt-2026-11-04.md](run-receipt-2026-11-04.md).

The function emits `entityDied` at phase 10. The primary id is the enemy id. The payload carries `entityId` as that id's decimal string and `archetypeId` as the archetype's raw value. It then adds one to `defeatsByArchetype` for that raw value. When the enemy's encounter id is present, that record's `living` becomes the greater of 0 and the previous living minus 1.

This does not change the gate timing.
