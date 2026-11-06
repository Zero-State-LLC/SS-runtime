# The gate ids, and the unmapped ones

Read 2026-11-05 from `GateRegistry` on `ef68565`. No gate was closed. The decision stays in [expansion-gate-2026-11-05.md](expansion-gate-2026-11-05.md). The playtest counts stay in [playtest-gates-2026-11-05.md](playtest-gates-2026-11-05.md). The device gates stay in [device-run-gates-2026-11-05.md](device-run-gates-2026-11-05.md).

`allGateIds` concatenates `functional`, `determinism`, `stability`, `visual`, `arena`, `accessibility`, and `playtest`.

`functional` is `A-001` through `A-022`. `determinism` is `B-001` through `B-017`. `stability` is `C-001` through `C-011`. `visual` is `D-001` through `D-021`. `arena` is `E-001` through `E-020`. `accessibility` is `F-001` through `F-017`. `playtest` is `G-001` through `G-007`.

The evidence kinds are `automatedTest`, `deviceCapture`, `manualReview`, and `playtest`. `evidence(for:)` returns the first record with that id. `automatedGateIds`, `deviceGateIds`, and `playtestGateIds` filter by kind. `unmappedGateIds` returns every id in `allGateIds` that the evidence list does not name.

This does not close T902.
