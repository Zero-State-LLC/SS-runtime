import Foundation

/// D-118 (bosses.md § Captain path search): the Captain finds its way round
/// solids with a shortest-path search over the corners of the live solids.
///
/// Geometry is in whole units (positions truncated), with exact integer
/// arithmetic. A path is a chain of straight legs; every leg keeps the
/// Captain's body clear of every solid, so it never steers into a gap it
/// cannot pass. The search runs from the current position every tick, so the
/// route is consistent from tick to tick without stored state.
public enum CaptainPath {
    /// Nodes sit this far beyond the Captain's radius outside each box corner.
    public static let cornerMarginUnits = 4
    /// A node this close is reached; the next one on the path is the waypoint.
    public static let reachedUnits = 2

    /// Where the Captain steers this tick, and whether it is following a path
    /// (true: no orbit) or has the Player in a body-clear straight line.
    public static func approach(
        from start: VecQ8,
        to target: VecQ8,
        radius: Int,
        bounds: AABB,
        solids: [(id: String, box: AABB)]
    ) -> (point: VecQ8, routing: Bool) {
        let boxes = solids.sorted { $0.id.utf8LessThan($1.id) }.map(\.box)
        let s = units(start)
        let t = units(target)
        if clear(s, t, radius: radius, boxes: boxes) { return (target, false) }
        let graph = Graph.cached(radius: radius, bounds: bounds, boxes: boxes)
        guard let next = graph.firstWaypoint(from: s, to: t, radius: radius, boxes: boxes) else {
            // No path: steer straight at the Player, as before D-116.
            return (target, false)
        }
        return (VecI(x: Int(next.0), y: Int(next.1)).asQ8, true)
    }

    typealias Point = (Int64, Int64)

    static func units(_ p: VecQ8) -> Point {
        (Int64(p.x.unitsTruncated), Int64(p.y.unitsTruncated))
    }

    /// A leg a→b is clear when, for every box, it keeps at least the smaller
    /// of `radius` and its endpoints' own distances to that box. So a body
    /// already touching a wall, or a Player pressed into one, does not block
    /// every leg; a leg through a box (distance 0) is always blocked.
    static func clear(_ a: Point, _ b: Point, radius: Int, boxes: [AABB]) -> Bool {
        let r2 = Int64(radius) * Int64(radius)
        for box in boxes {
            let need = min(r2, pointBox(a, box), pointBox(b, box))
            if segmentBox(a, b, box) < need { return false }
        }
        return true
    }

    /// Squared distance from a point to a box; 0 inside.
    static func pointBox(_ p: Point, _ box: AABB) -> Int64 {
        let dx = max(Int64(box.minX) - p.0, 0, p.0 - Int64(box.maxX))
        let dy = max(Int64(box.minY) - p.1, 0, p.1 - Int64(box.maxY))
        return dx * dx + dy * dy
    }

    /// Squared distance from segment a→b to a box, rounded up; 0 when they meet.
    static func segmentBox(_ a: Point, _ b: Point, _ box: AABB) -> Int64 {
        if Collision.segmentIntersects(
            VecI(x: Int(a.0), y: Int(a.1)).asQ8, VecI(x: Int(b.0), y: Int(b.1)).asQ8, box: box
        ) { return 0 }
        func pointSegment(_ p: Point) -> Int64 {
            let dx = b.0 - a.0, dy = b.1 - a.1
            let len2 = dx * dx + dy * dy
            let ax = p.0 - a.0, ay = p.1 - a.1
            if len2 == 0 { return ax * ax + ay * ay }
            let dot = ax * dx + ay * dy
            if dot <= 0 { return ax * ax + ay * ay }
            if dot >= len2 { return (p.0 - b.0) * (p.0 - b.0) + (p.1 - b.1) * (p.1 - b.1) }
            let cross = dx * ay - dy * ax
            return (cross * cross + len2 - 1) / len2
        }
        let corners: [Point] = [
            (Int64(box.minX), Int64(box.minY)), (Int64(box.maxX), Int64(box.minY)),
            (Int64(box.minX), Int64(box.maxY)), (Int64(box.maxX), Int64(box.maxY)),
        ]
        return ([pointBox(a, box), pointBox(b, box)] + corners.map(pointSegment)).min()!
    }

    static func length(_ a: Point, _ b: Point) -> Int64 {
        IntMath.isqrt((a.0 - b.0) * (a.0 - b.0) + (a.1 - b.1) * (a.1 - b.1))
    }

    /// Corner nodes and the clear legs between them for one radius and one set
    /// of solids. A pure function of its inputs, memoised because the solids
    /// change only when a gate moves or a Camera mount falls.
    final class Graph: @unchecked Sendable {
        let nodes: [Point]
        /// Leg lengths between nodes; nil where the leg is not clear.
        let legs: [[Int64?]]

        init(radius: Int, bounds: AABB, boxes: [AABB]) {
            let m = Int64(radius + CaptainPath.cornerMarginUnits)
            let r2 = Int64(radius) * Int64(radius)
            var nodes: [Point] = []
            for box in boxes {
                let corners: [Point] = [
                    (Int64(box.minX) - m, Int64(box.minY) - m), (Int64(box.maxX) + m, Int64(box.minY) - m),
                    (Int64(box.minX) - m, Int64(box.maxY) + m), (Int64(box.maxX) + m, Int64(box.maxY) + m),
                ]
                for c in corners
                where c.0 >= Int64(bounds.minX + radius) && c.0 <= Int64(bounds.maxX - radius)
                    && c.1 >= Int64(bounds.minY + radius) && c.1 <= Int64(bounds.maxY - radius)
                    && !boxes.contains(where: { CaptainPath.pointBox(c, $0) < r2 })
                {
                    nodes.append(c)
                }
            }
            self.nodes = nodes
            var legs = Array(repeating: [Int64?](repeating: nil, count: nodes.count), count: nodes.count)
            for i in nodes.indices {
                for j in nodes.indices where j > i && CaptainPath.clear(nodes[i], nodes[j], radius: radius, boxes: boxes) {
                    let d = CaptainPath.length(nodes[i], nodes[j])
                    legs[i][j] = d
                    legs[j][i] = d
                }
            }
            self.legs = legs
        }

        /// The first node of the shortest clear path start→target, skipping a
        /// node already reached; nil when the target cannot be reached.
        /// Dijkstra over at most a few dozen nodes; ties go to the lower index.
        func firstWaypoint(from s: Point, to t: Point, radius: Int, boxes: [AABB]) -> Point? {
            let n = nodes.count
            let reached2 = Int64(CaptainPath.reachedUnits * CaptainPath.reachedUnits)
            // Index n is the start, n + 1 the target.
            func point(_ i: Int) -> Point { i < n ? nodes[i] : (i == n ? s : t) }
            func leg(_ i: Int, _ j: Int) -> Int64? {
                if i < n && j < n { return legs[i][j] }
                let a = point(i), b = point(j)
                return CaptainPath.clear(a, b, radius: radius, boxes: boxes) ? CaptainPath.length(a, b) : nil
            }
            var dist = [Int64](repeating: .max, count: n + 2)
            var prev = [Int](repeating: -1, count: n + 2)
            var done = [Bool](repeating: false, count: n + 2)
            dist[n] = 0
            while true {
                var u = -1
                for i in 0..<(n + 2) where !done[i] && dist[i] != .max && (u < 0 || dist[i] < dist[u]) { u = i }
                guard u >= 0 else { return nil }
                if u == n + 1 { break }
                done[u] = true
                for v in 0..<(n + 2) where !done[v] && v != n {
                    // A node the Captain already stands on is skipped, not visited.
                    if v < n && u == n {
                        let dx = nodes[v].0 - s.0, dy = nodes[v].1 - s.1
                        if dx * dx + dy * dy <= reached2 { continue }
                    }
                    guard let d = leg(u, v) else { continue }
                    if dist[u] + d < dist[v] {
                        dist[v] = dist[u] + d
                        prev[v] = u
                    }
                }
            }
            var step = n + 1
            while prev[step] != n { step = prev[step] }
            return point(step)
        }

        private static let lock = NSLock()
        nonisolated(unsafe) private static var memo: [[Int]: Graph] = [:]

        static func cached(radius: Int, bounds: AABB, boxes: [AABB]) -> Graph {
            let key = [radius, bounds.minX, bounds.minY, bounds.maxX, bounds.maxY]
                + boxes.flatMap { [$0.minX, $0.minY, $0.maxX, $0.maxY] }
            lock.lock()
            defer { lock.unlock() }
            if let graph = memo[key] { return graph }
            let graph = Graph(radius: radius, bounds: bounds, boxes: boxes)
            if memo.count >= 16 { memo.removeAll() }
            memo[key] = graph
            return graph
        }
    }
}
