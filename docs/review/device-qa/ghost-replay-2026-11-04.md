# Ghost replay

Read 2026-11-04 from `GhostRun` on `30a2cc6`. The ghost stays presentation only.

A stored ghost is replaced when the seed and replay identity match and the new success used fewer ticks. A record from another seed or identity is not a best for this run, so a candidate with no matching stored record is stored.

`GhostRun` builds when the record's identity is the current one, the seed matches the live seed, the recorded length is greater than 0, and the commands are strictly increasing and fall inside that length. A private replay must reproduce the stored tick and the stored digest. It then steps a second private simulation, one command tick at a time, and stops at the recorded terminal tick. The lead is 0.

Opacity is 1 while the ghost is still running. After it finishes, opacity falls linearly to 0 over 30 live ticks. Reduced motion sets that opacity to 0 on the first live tick after the finish. The live simulation does not read the ghost.
