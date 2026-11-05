# Outline cache

Read 2026-11-05 from `OutlineTextures` on `c6da67e`. No outline weight was changed.

The faction colours and the dash stay in [faction-outline-2026-11-04.md](faction-outline-2026-11-04.md). Ordinary play stays at sampling scale 1, as that note records.

The cache holds 128 entries, or `4 * 1024 * 1024` bytes of stored masks, whichever limit is reached first. A hit moves that key to the newest end. While the next mask would pass either limit, the oldest key leaves. A mask whose own cost is already over the byte cap is returned and not stored. A miss is stored, including a failed build.

A sampling scale outside 1, 2, or 3 returns nil. Each logical side must be finite, positive, and at most 256. The mask side is that side rounded to the nearest whole pixel, then multiplied by the scale, and it must still be at most 256. The source image side must be at most 1024, and the mask must be at most `256 * 256` pixels.

A source pixel counts as body at alpha 64 or above. The pad is 1 logical pixel times the scale. A clear pixel within that pad of a body pixel is a candidate, and the faction test decides it. The outline texture is built with smoothing off.

This does not select another sampling scale.
