# The body clearance

Read 2026-11-05 from `CornerPursuit.bodyClear` on `ef68565`. No corner was moved.

The live call stays in [corner-pursuit-2026-11-04.md](corner-pursuit-2026-11-04.md). That call leaves body clearance off, so its reached distance stays 8.

When clearance is requested, a corner within 2 units is skipped, and the corner must also pass `bodyClear`. The ends are truncated to units. A segment that meets the box has distance 0. Otherwise the squared distance is the minimum of each end's squared distance to the box and each of the four corners' squared distance to the segment. An end outside the box uses the outside deltas. A point whose projection falls at or before the start uses the start, and one at or past the end uses the end. Between them the square is `(cross² + len² − 1) / len²`. The path is clear when every solid's squared distance is at least the radius squared.

This does not turn clearance on.
