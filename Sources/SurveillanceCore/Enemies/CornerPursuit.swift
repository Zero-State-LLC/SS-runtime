/// D-114 (enemies-and-encounters.md § Corner pursuit): an aware enemy whose
/// line to its target is blocked steers for a corner of the blocking solid
/// instead of pressing into its face.
///
/// No pathfinding: one waypoint, recomputed every tick from the current
/// position, so it advances corner by corner round a box. Integer only.
public enum CornerPursuit {
    /// Corners sit this far outside the box, beyond the enemy's radius.
    public static let cornerMarginUnits = 4
    /// A corner this close counts as reached and is not a waypoint.
    public static let reachedUnits = 8

    /// `target` when the line is clear; otherwise the best corner, or
    /// `target` again when no corner qualifies (the pre-D-114 behaviour).
    public static func waypoint(
        from: VecQ8,
        to target: VecQ8,
        radius: Int,
        solids: [(id: String, box: AABB)]
    ) -> VecQ8 {
        guard !Collision.lineOfFireClear(from: from, to: target, solids: solids) else { return target }
        let margin = radius + cornerMarginUnits
        let reachedSq = Int64(reachedUnits * reachedUnits) * Q8.scale * Q8.scale
        let blocking = solids
            .filter { !Collision.lineOfFireClear(from: from, to: target, solids: [$0]) }
            .sorted { $0.id.utf8LessThan($1.id) }
        // Rank: a corner that sees the target first, then the shorter path.
        // Strictly-less keeps the earliest corner on ties (solid ID, then
        // corner order), so the choice is deterministic.
        var best: (blind: Bool, length: Int64, corner: VecQ8)?
        for solid in blocking {
            let box = solid.box
            let corners = [
                VecI(x: box.minX - margin, y: box.minY - margin),
                VecI(x: box.maxX + margin, y: box.minY - margin),
                VecI(x: box.minX - margin, y: box.maxY + margin),
                VecI(x: box.maxX + margin, y: box.maxY + margin),
            ]
            for corner in corners.map(\.asQ8) {
                guard from.distanceSquared(to: corner) > reachedSq,
                      Collision.lineOfFireClear(from: from, to: corner, solids: solids)
                else { continue }
                let blind = !Collision.lineOfFireClear(from: corner, to: target, solids: solids)
                let length = IntMath.isqrt(from.distanceSquared(to: corner))
                    + IntMath.isqrt(corner.distanceSquared(to: target))
                if let current = best, (current.blind ? 1 : 0, current.length) <= (blind ? 1 : 0, length) {
                    continue
                }
                best = (blind, length, corner)
            }
        }
        return best?.corner ?? target
    }
}
