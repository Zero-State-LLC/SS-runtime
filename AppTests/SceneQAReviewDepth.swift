#if DEBUG && SS_SOURCE_SCENE_REVIEW
/// Review-only BP-001/BP-007/T1045 diagnostic, authorized by
/// intent/2026-11-16-scene-qa-repair.md. No renderer or authority mutations.
enum SceneQAReviewDepth {
    struct Point: Equatable {
        let x: Double
        let y: Double
    }

    struct Bounds: Equatable {
        let minX: Double
        let minY: Double
        let maxX: Double
        let maxY: Double
    }

    struct Item: Equatable {
        let name: String
        let worldRoot: Point
        /// Authoritative world footprint, never a sprite/alpha bounding box.
        let solidBounds: Bounds?
        /// Caller-projected Y under the midpoint view (x-y, y+x).
        let projectedRootY: Double

        init(name: String, worldRoot: Point, solidBounds: Bounds? = nil, projectedRootY: Double) {
            self.name = name
            self.worldRoot = worldRoot
            self.solidBounds = solidBounds
            self.projectedRootY = projectedRootY
        }

        fileprivate var footprint: Bounds {
            solidBounds ?? Bounds(minX: worldRoot.x, minY: worldRoot.y,
                                  maxX: worldRoot.x, maxY: worldRoot.y)
        }
    }

    enum Axis: String, Equatable { case x, y }

    struct Separation: Equatable {
        let axis: Axis
        let backMinimum: Double
        let frontMaximum: Double
    }

    struct Edge: Equatable {
        let back: String
        let front: String
        /// Strict separating planes: backMinimum > frontMaximum.
        /// Each listed axis independently supports this back-to-front edge.
        let separations: [Separation]
    }

    struct Order: Equatable {
        let backToFrontNames: [String]
        let edges: [Edge]
    }

    enum Failure: Error, Equatable {
        case invalidItem(name: String, reason: String)
        case duplicateName(String)
        /// Includes cycle members AND any nodes blocked downstream by the cycle.
        /// Edges retain the complete graph for diagnosis. No partial order is returned.
        case cyclic(blockedNames: [String], edges: [Edge])
    }

    /// Low world X / low world Y are toward the viewer. Greater projected Y
    /// wins only among currently unconstrained nodes, then lexical name.
    static func order(_ items: [Item]) throws -> Order {
        let canonical = items.sorted { $0.name < $1.name }
        var seen = Set<String>()
        for item in canonical {
            guard !item.name.isEmpty else {
                throw Failure.invalidItem(name: item.name, reason: "empty name")
            }
            guard seen.insert(item.name).inserted else { throw Failure.duplicateName(item.name) }
            let b = item.footprint
            guard [item.worldRoot.x, item.worldRoot.y, item.projectedRootY,
                   b.minX, b.minY, b.maxX, b.maxY].allSatisfy({ $0.isFinite }),
                  b.minX <= b.maxX, b.minY <= b.maxY,
                  (b.minX - b.maxY).isFinite, (b.maxX - b.minY).isFinite else {
                throw Failure.invalidItem(name: item.name, reason: "nonfinite or inverted geometry")
            }
        }

        var edges: [Edge] = []
        for i in canonical.indices {
            for j in canonical.indices where j > i {
                let a = canonical[i]
                let b = canonical[j]
                // Ground projection X spans. Disjoint spans cannot share a view ray.
                // Do not invent conflicting constraints for opposite mixed quadrants.
                let af = a.footprint
                let bf = b.footprint
                guard max(af.minX - af.maxY, bf.minX - bf.maxY)
                        <= min(af.maxX - af.minY, bf.maxX - bf.minY) else { continue }
                let aBehind = separations(back: af, front: bf)
                let bBehind = separations(back: bf, front: af)
                if !aBehind.isEmpty && bBehind.isEmpty {
                    edges.append(Edge(back: a.name, front: b.name, separations: aBehind))
                } else if !bBehind.isEmpty && aBehind.isEmpty {
                    edges.append(Edge(back: b.name, front: a.name, separations: bBehind))
                }
                // Intersecting/equal/contact-only footprints have no strict evidence.
            }
        }
        edges.sort { $0.back == $1.back ? $0.front < $1.front : $0.back < $1.back }
        return Order(backToFrontNames: try topologicalNames(items: canonical, edges: edges), edges: edges)
    }

    /// Graph mechanism exposed internally for synthetic cycle tests only. Integration
    /// must call order(_:), which validates inputs and derives geometry-backed edges.
    static func topologicalNames(items: [Item], edges: [Edge]) throws -> [String] {
        var indegree = Dictionary(uniqueKeysWithValues: items.map { ($0.name, 0) })
        var outgoing: [String: [String]] = [:]
        for edge in edges {
            indegree[edge.front, default: 0] += 1
            outgoing[edge.back, default: []].append(edge.front)
        }
        var remaining = items
        var names: [String] = []
        while !remaining.isEmpty {
            let ready = remaining.filter { indegree[$0.name] == 0 }.sorted {
                $0.projectedRootY == $1.projectedRootY
                    ? $0.name < $1.name : $0.projectedRootY > $1.projectedRootY
            }
            guard let next = ready.first else {
                throw Failure.cyclic(blockedNames: remaining.map(\.name).sorted(), edges: edges)
            }
            names.append(next.name)
            remaining.removeAll { $0.name == next.name }
            for front in outgoing[next.name, default: []] { indegree[front, default: 0] -= 1 }
        }
        return names
    }

    private static func separations(back: Bounds, front: Bounds) -> [Separation] {
        var result: [Separation] = []
        if back.minX > front.maxX {
            result.append(Separation(axis: .x, backMinimum: back.minX, frontMaximum: front.maxX))
        }
        if back.minY > front.maxY {
            result.append(Separation(axis: .y, backMinimum: back.minY, frontMaximum: front.maxY))
        }
        return result
    }
}
#endif
