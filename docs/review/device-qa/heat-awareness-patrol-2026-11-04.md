# Heat, awareness, and the Transit Patrol

Read 2026-11-04 from `combat-content-009` on `49759ab`. No table value was changed. Signal Jammer's reduction stays in [upgrade-effects-2026-11-03.md](upgrade-effects-2026-11-03.md).

Heat appends `autonomousInformant` to M-A and M-B only. The base counts are hidden 0, observed 0, tracked 1, hunted 2, lockdown 2. The reduction of 2, with a floor of 0, is applied to that base. Reinforcements are the tail of the spawn queue.

Awareness applies to the five standard enemies, not the elite and not the boss. Sight range is 320. Ally alert radius is 128. The surveillance alert state is `tracked`, and a standard enemy spawns aware at that state or above. The first damage an unaware enemy takes is multiplied by 3. M-C spawns aware. Heat reinforcements spawn aware. An unaware encounter enemy drifts toward its trigger centre at 25 percent of its speed and stops within 48.

Patrol integrity is 200 percent of the archetype. Patrol speed is 40 percent. Dwell is 30 ticks. Cone sight is 240, half-angle 45000, which is the exact cosine-squared pair (1, 2). Arrival is within 4 units. Routes stay on `civic-seam-arena-004`.

This does not add a detection state.
