# Camera field polygon

Read 2026-11-04 from `CameraFieldGeometry` on `86c05bb`. No range was changed.

Contact sampling stays in [camera-contact-2026-11-04.md](camera-contact-2026-11-04.md). The eight placed cameras stay in [placed-cameras-2026-11-04.md](placed-cameras-2026-11-04.md). The segment test stays in [line-of-fire-2026-11-04.md](line-of-fire-2026-11-04.md). This path is the display polygon.

The origin is `fieldOrigin` raw divided by `Q8.scale`, as a double, when that origin is present. Otherwise it is the camera's integer x and y. A range of 0 or an angle of 0 returns an empty path. `base` is `-heading * π / 180_000`. `half` is `angle * π / 360_000`. The arc sample count is `max(1, ceil(angle / 1000))`, and the samples run from `-half` to `+half` inclusive.

Each corner of each solid adds its `atan2` relative to `base`, wrapped with `atan2(sin, cos)`. When `abs(relative + offset)` is within `half`, the offsets −1e-7, 0, and +1e-7 are added. The angles are sorted. Each ray starts at `Double(range)` and keeps the smallest slab entry. An axis-parallel component whose absolute value is below 1e-12 rejects the ray when the origin is outside that slab. The entry is `max(0, near)` when `near <= far` and `far >= 0`. The path closes back at the origin.

This does not decide a contact.
