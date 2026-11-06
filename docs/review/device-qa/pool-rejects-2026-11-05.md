# The pool rejects

Read 2026-11-05 from `CameraPlacement.manifestPoolIsValid` on `ef68565`. No socket was added.

The both-ways ban stays in [camera-legal-set-2026-11-04.md](camera-legal-set-2026-11-04.md). The zone minimums and `requiredByZone` stay in [placed-cameras-2026-11-04.md](placed-cameras-2026-11-04.md).

The check returns false when a socket id is repeated. It returns false when `headingMilliDegrees` is below 0 or above 359_999, when `rangeUnits` is below 1, or when `fieldAngleMilliDegrees` is at or below 0 or above 180_000. An empty housing-family list fails, and so does a list that repeats a family. An enabled socket in Z-01 or Z-07 fails. An enabled socket whose zone is outside the `requiredByZone` zones fails. A socket that lists its own id as incompatible fails. A listed id that is missing from the pool fails.

This does not add a camera.
