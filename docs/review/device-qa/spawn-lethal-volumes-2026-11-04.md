# Spawn lethal volumes

Read 2026-11-04 from `lethalVolumes` on `fcab4e5`. No socket was moved.

Socket ranking, the viewport, Z-01, the flood, and the player-overlap test stay in [spawn-socket-choice-2026-11-04.md](spawn-socket-choice-2026-11-04.md). That note already requires the center to sit strictly outside every lethal volume. This note names the volumes.

Every mine with `lifeRemaining > 0` is a volume at the mine position with `mine.radius`, armed or not.

A living enemy in `telegraph`, `resolve`, `charge`, `fire`, `throwMine`, `queryTelegraph`, `queryResolve`, `dashTelegraph`, or `dash` adds a volume for each content record it has. A pulse is at the enemy position with `pulse.range`. A charge is at `lockPosition` when one is set, otherwise at the enemy position, with the enemy radius. A mine is added only when `lockPosition` is set, at that mark, with `mine.radius`. Each query marker is a volume of radius 56.

`isFair` rejects a socket when the squared distance from the socket center to the volume center is strictly less than `(archetype radius + volume radius)` squared, in Q8. An equal boundary stays fair.
