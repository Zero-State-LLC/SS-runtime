# Extraction presence

Read 2026-11-04 from `resolveExtraction` on `fcab4e5`. No countdown was changed.

The arm rule, the 300 starting countdown, and the reset event stay in [extraction-and-tick-2026-11-04.md](extraction-and-tick-2026-11-04.md). The drawn box stays in [world-shapes-2026-11-03.md](world-shapes-2026-11-03.md): center `(2048, 192)`, half-size `(96, 64)`.

The function runs when extraction is armed and the outcome is `playing` or `upgradeSelectionPending`. Inside is `extraction.aabb.contains` of the integer point `(unitsTruncated x, unitsTruncated y)`. `unitsTruncated` is the raw Q8 divided by `Q8.scale`. `contains` includes the edges, so that point is inside for x from 1,952 through 2,144 and y from 128 through 256.

While the point is inside and remaining is above 0, remaining decreases by 1 and phase 17 emits `extractionCountdownChanged`. At 0, with the player alive, the run succeeds. An inside tick sets `wasInside`. A later tick outside, after `wasInside` was set, stores the previous remaining, sets remaining back to `countdownTicks`, clears `wasInside`, and emits `extractionReset` with `previousRemainingTicks`.
