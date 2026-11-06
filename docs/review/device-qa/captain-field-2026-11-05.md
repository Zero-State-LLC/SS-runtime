# The captain field sprite

Read 2026-11-05 from `PresentationSnapshot` on `ef68565`. No field was added.

The fill stays in [world-shapes-2026-11-03.md](world-shapes-2026-11-03.md). The housing art and the three emitter points stay in [captain-housing-bounds-2026-11-03.md](captain-housing-bounds-2026-11-03.md). The wall target that uses `EntityID(0)` stays in [hit-order-2026-11-04.md](hit-order-2026-11-04.md).

While an active emitter exists and `fieldRemaining` is above 0, `captainField` is a camera sprite whose id is `EntityID(0)`. Its position, heading, range, and field angle are that emitter's. Integrity is 1. Detecting is true. The presentation state is `critical`. The field is visible. The clip is the clip for `critical`. The housing family is nil. Otherwise the field is nil.

A housing is active when its id is that live emitter's id. The live id is the active emitter's id only while `fieldRemaining` is above 0. Otherwise the live id is nil, and every housing is inactive.

This does not change the field colour.
