# Outline seat

Read 2026-11-05 from `WorldRenderer.syncOutlines` on `344ed78`. No outline weight was changed.

The colour, the dash, and sampling scale 1 stay in [faction-outline-2026-11-04.md](faction-outline-2026-11-04.md).

The logical size is the sprite's size divided by its scale, on each axis, using the absolute value. A missing texture, or a cache miss, hides the outline child. A hit sizes that child to the logical size times `(mask + 2 * pad) / mask` on each axis. `mask` is the entry's unpadded mask side, and that division treats a side of 0 as 1. The anchor divides `(sprite anchor * mask + pad)` by `(mask + 2 * pad)` on each axis. The child sits at the sprite's origin.

This does not change an outline weight.
