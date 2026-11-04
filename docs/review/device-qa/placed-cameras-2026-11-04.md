# Placed cameras

Read 2026-11-04 from `CameraPlacement` and `civic-seam-arena-004` on `49759ab`. No socket was moved. Captain emitters stay in [captain-housing-bounds-2026-11-03.md](captain-housing-bounds-2026-11-03.md).

`requiredByZone` is Z-02 ×2, Z-03 ×1, Z-04 ×2, Z-05 ×2, and Z-06 ×1. That is eight cameras. The arena enables all 18 sockets. The minimum the search requires is Z-02 ×4, Z-03 ×3, Z-04 ×4, Z-05 ×4, and Z-06 ×3.

The placement seed is `SplitMix64.mix(runSeed ^ 0x4341_4D45_5241_3031)`. The constant is ASCII `CAMERA01`. Housing is the first family after shuffling the socket's allowed families. The set used is the first legal set for that shuffle. Each selected camera keeps its socket heading, range, and field angle.

Shared geometry is mount collision radius 12, hit radius 16, field origin offset (0, 18), and target anchor offset (0, 16). Integrity starts at 3. `Simulation.step` does not change a camera heading.

Civic Pulse damage against that integrity is in [civic-pulse-2026-11-04.md](civic-pulse-2026-11-04.md).

This does not add a camera.
