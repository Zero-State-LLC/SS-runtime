# Offsets inside a layer

Read 2026-11-03 from the runtime sources on `241c167`. No z position was changed. Benchmark ground patches and the field-contrast inner stroke are not in this table.

Each z is relative to the node that owns it.

| What | Owner | z |
|---|---|---:|
| Solid foundation | solids layer | -0.1 |
| Gate barrier root | solids layer | 0.5 |
| Gate warning strip | gate barrier root | 0.1 |
| Ghost silhouette | actors layer | -0.5 |
| Camera damage badge | actors layer | 2 |

A closed gate is added to the solids layer and skips the foundation. The gate root at `0.5` draws above a foundation at `-0.1` and above an upright sprite left at `0`. The warning strip is `0.1` above that root.

The ghost is a silhouette on the actors layer. Its alpha is `0.35` times its fade. The camera damage badge is its own actors-layer node at z `2`, so it draws above an actor left at `0`. Standard cameras with integrity 2 or 1 get the badge. Captain emitters do not.

This does not move a solid, a gate, or a camera.
