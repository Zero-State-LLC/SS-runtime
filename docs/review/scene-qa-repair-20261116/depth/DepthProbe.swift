import Foundation

/// Host-only JSON bridge to the actual Swift helper. No SpriteKit/UIKit/simulator.
@main
struct DepthProbe {
    struct Input: Decodable {
        let name: String
        let root: [Double]
        let bounds: [Double]?
        let priority: Double?
    }
    struct Request: Decodable {
        let items: [Input]
        let syntheticCycle: Bool?
    }
    static func edgeJSON(_ edge: SceneQAReviewDepth.Edge) -> [String: Any] {
        ["back": edge.back, "front": edge.front,
         "separations": edge.separations.map {
            ["axis": $0.axis.rawValue, "backMinimum": $0.backMinimum,
             "frontMaximum": $0.frontMaximum] as [String: Any]
         }]
    }
    static func main() throws {
        let requests = try JSONDecoder().decode([Request].self, from: FileHandle.standardInput.readDataToEndOfFile())
        let results: [[String: Any]] = requests.map { request in
            let items = request.items.map { input in
                SceneQAReviewDepth.Item(name: input.name,
                    worldRoot: .init(x: input.root[0], y: input.root[1]),
                    solidBounds: input.bounds.map { .init(minX: $0[0], minY: $0[1], maxX: $0[2], maxY: $0[3]) },
                    projectedRootY: input.priority ?? input.root[0] + input.root[1])
            }
            do {
                if request.syntheticCycle == true {
                    // Deliberately contradictory GRAPH, not a fabricated geometric scene.
                    let edges = [SceneQAReviewDepth.Edge(back: "a", front: "b", separations: []),
                                 SceneQAReviewDepth.Edge(back: "b", front: "a", separations: []),
                                 SceneQAReviewDepth.Edge(back: "b", front: "c", separations: [])]
                    return ["names": try SceneQAReviewDepth.topologicalNames(items: items, edges: edges)]
                }
                let order = try SceneQAReviewDepth.order(items)
                return ["names": order.backToFrontNames, "edges": order.edges.map(edgeJSON)]
            } catch SceneQAReviewDepth.Failure.cyclic(let blocked, let edges) {
                return ["error": "cyclic", "blockedNames": blocked, "edges": edges.map(edgeJSON)]
            } catch SceneQAReviewDepth.Failure.duplicateName(let name) {
                return ["error": "duplicateName", "name": name]
            } catch {
                return ["error": "invalidItem", "detail": String(describing: error)]
            }
        }
        let data = try JSONSerialization.data(withJSONObject: results, options: [.sortedKeys])
        FileHandle.standardOutput.write(data)
    }
}
