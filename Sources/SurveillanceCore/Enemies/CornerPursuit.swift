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
    /// D-117: with body clearance, a corner is reached only this close, so the
    /// body stands on it, clear of the box, before the next leg is tested.
    public static let bodyReachedUnits = 2

    /// `target` when the line is clear; otherwise the best corner, or
    /// `target` again when no corner qualifies (the pre-D-114 behaviour).
    public static func waypoint(
        from: VecQ8,
        to target: VecQ8,
        radius: Int,
        solids: [(id: String, box: AABB)],
        bodyClearance: Bool = false
    ) -> VecQ8 {
        guard !Collision.lineOfFireClear(from: from, to: target, solids: solids) else { return target }
        let margin = radius + cornerMarginUnits
        let reached = bodyClearance ? bodyReachedUnits : reachedUnits
        let reachedSq = Int64(reached * reached) * Q8.scale * Q8.scale
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
                      Collision.lineOfFireClear(from: from, to: corner, solids: solids),
                      !bodyClearance || bodyClear(from: from, to: corner, radius: radius, solids: solids)
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

    /// D-117: the path keeps a body of `radius` clear of every solid: the
    /// segment's distance to each box is at least `radius`. Whole units, exact
    /// integer arithmetic.
    public static func bodyClear(from: VecQ8, to: VecQ8, radius: Int, solids: [(id: String, box: AABB)]) -> Bool {
        let a = (Int64(from.x.unitsTruncated), Int64(from.y.unitsTruncated))
        let b = (Int64(to.x.unitsTruncated), Int64(to.y.unitsTruncated))
        let clearance = Int64(radius)
        return !solids.contains { solid in
            distanceSquared(segment: a, b, box: solid.box) < clearance * clearance
        }
    }

    /// Squared distance from segment a→b to `box`, in units²; 0 when they meet.
    static func distanceSquared(segment a: (Int64, Int64), _ b: (Int64, Int64), box: AABB) -> Int64 {
        let minX = Int64(box.minX), maxX = Int64(box.maxX), minY = Int64(box.minY), maxY = Int64(box.maxY)
        if Collision.segmentIntersects(
            VecI(x: Int(a.0), y: Int(a.1)).asQ8, VecI(x: Int(b.0), y: Int(b.1)).asQ8, box: box
        ) { return 0 }
        func pointBox(_ p: (Int64, Int64)) -> Int64 {
            let dx = max(minX - p.0, 0, p.0 - maxX)
            let dy = max(minY - p.1, 0, p.1 - maxY)
            return dx * dx + dy * dy
        }
        // Distance from point p to the segment, squared, as an exact
        // comparison-safe value: cross² / len² rounded up.
        func pointSegment(_ p: (Int64, Int64)) -> Int64 {
            let dx = b.0 - a.0, dy = b.1 - a.1
            let len2 = dx * dx + dy * dy
            if len2 == 0 { return (p.0 - a.0) * (p.0 - a.0) + (p.1 - a.1) * (p.1 - a.1) }
            let dot = (p.0 - a.0) * dx + (p.1 - a.1) * dy
            if dot <= 0 { return (p.0 - a.0) * (p.0 - a.0) + (p.1 - a.1) * (p.1 - a.1) }
            if dot >= len2 { return (p.0 - b.0) * (p.0 - b.0) + (p.1 - b.1) * (p.1 - b.1) }
            let cross = dx * (p.1 - a.1) - dy * (p.0 - a.0)
            return (cross * cross + len2 - 1) / len2
        }
        let corners = [(minX, minY), (maxX, minY), (minX, maxY), (maxX, maxY)]
        return ([pointBox(a), pointBox(b)] + corners.map(pointSegment)).min()!
    }
}

