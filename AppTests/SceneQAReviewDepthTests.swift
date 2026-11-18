#if DEBUG && SS_SOURCE_SCENE_REVIEW
import XCTest

final class SceneQAReviewDepthTests: XCTestCase {
    private typealias D = SceneQAReviewDepth
    private let box = D.Bounds(minX: 512, minY: 640, maxX: 640, maxY: 768)

    private func point(_ name: String, _ x: Double, _ y: Double, priority: Double? = nil) -> D.Item {
        D.Item(name: name, worldRoot: .init(x: x, y: y), projectedRootY: priority ?? x + y)
    }

    private func kiosk() -> D.Item {
        D.Item(name: "kiosk", worldRoot: .init(x: 512, y: 640), solidBounds: box, projectedRootY: 1152)
    }

    func testOutsideFrontCameraDefeatsOldRootOrder() throws {
        let camera = point("camera3", 496, 672)
        let items = [kiosk(), camera]
        let old = items.sorted { $0.projectedRootY > $1.projectedRootY }.map(\.name)
        XCTAssertEqual(old, ["camera3", "kiosk"], "v4 paints the kiosk over Camera3")
        let result = try D.order(items)
        XCTAssertEqual(result.backToFrontNames, ["kiosk", "camera3"])
        XCTAssertEqual(result.edges, [.init(back: "kiosk", front: "camera3", separations: [
            .init(axis: .x, backMinimum: 512, frontMaximum: 496)
        ])])
    }

    func testNearFarAndMixedQuadrants() throws {
        let cases: [(Double, Double, String?, D.Axis?)] = [
            (496, 672, "kiosk", .x), (560, 624, "kiosk", .y),
            (656, 700, "point", .x), (560, 784, "point", .y),
            (496, 624, "kiosk", nil), (656, 784, "point", nil),
            (496, 784, nil, nil), (656, 624, nil, nil)
        ]
        for (x, y, back, axis) in cases {
            let result = try D.order([point("point", x, y), kiosk()])
            XCTAssertEqual(result.edges.first?.back, back, "point [\(x),\(y)]")
            if let axis { XCTAssertEqual(result.edges.first?.separations.first?.axis, axis) }
            XCTAssertEqual(result.edges.count, back == nil ? 0 : 1)
        }
    }

    func testEqualIntersectingAndContactHaveNoInventedEdges() throws {
        for p in [point("p", 512, 640), point("p", 576, 704), point("p", 640, 768)] {
            XCTAssertTrue(try D.order([kiosk(), p]).edges.isEmpty)
        }
        let same = D.Item(name: "same", worldRoot: .init(x: 512, y: 640),
                          solidBounds: box, projectedRootY: 1152)
        let overlap = D.Item(name: "overlap", worldRoot: .init(x: 600, y: 700),
                             solidBounds: .init(minX: 600, minY: 700, maxX: 700, maxY: 800),
                             projectedRootY: 1300)
        XCTAssertTrue(try D.order([kiosk(), same, overlap]).edges.isEmpty)
    }

    func testSolidSeparationAndPriorityOnlyWhenReady() throws {
        let near = D.Item(name: "near", worldRoot: .init(x: 480, y: 660),
                          solidBounds: .init(minX: 480, minY: 660, maxX: 500, maxY: 700),
                          projectedRootY: 9999)
        let free = point("free", -1000, 1000, priority: 2000)
        let result = try D.order([near, kiosk(), free])
        XCTAssertEqual(result.backToFrontNames, ["free", "kiosk", "near"])
        XCTAssertEqual(result.edges.map(\.back), ["kiosk"])
    }

    func testStableTiesAndPermutationIndependence() throws {
        let a = point("a", 1, 9)
        let z = point("z", 9, 1)
        XCTAssertEqual(try D.order([z, a]).backToFrontNames, ["a", "z"])
        let items = [kiosk(), point("camera3", 496, 672), a, z]
        let expected = try D.order(items)
        XCTAssertEqual(try D.order(Array(items.reversed())), expected)
        XCTAssertEqual(try D.order([items[2], items[0], items[3], items[1]]), expected)
        XCTAssertEqual(try D.order([]).backToFrontNames, [])
    }

    func testInvalidInputsFailClosed() {
        XCTAssertThrowsError(try D.order([point("a", 0, 0), point("a", 1, 1)]))
        XCTAssertThrowsError(try D.order([point("", 0, 0)]))
        XCTAssertThrowsError(try D.order([point("nan", .nan, 0)]))
        XCTAssertThrowsError(try D.order([point("infinite", 0, 0, priority: .infinity)]))
        let inverted = D.Item(name: "bad", worldRoot: .init(x: 0, y: 0),
                              solidBounds: .init(minX: 1, minY: 0, maxX: 0, maxY: 1), projectedRootY: 0)
        XCTAssertThrowsError(try D.order([inverted]))
    }

    func testSyntheticGraphCycleFailsWithDiagnosticNotArbitraryRaise() {
        // This tests the graph mechanism, NOT a claim these constraints arise from
        // three feasible ground footprints. Do not fabricate impossible scene inputs.
        let items = [point("a", 0, 0), point("b", 0, 0), point("c", 0, 0)]
        let edges = [D.Edge(back: "a", front: "b", separations: []),
                     D.Edge(back: "b", front: "a", separations: []),
                     D.Edge(back: "b", front: "c", separations: [])]
        XCTAssertThrowsError(try D.topologicalNames(items: items, edges: edges)) { error in
            XCTAssertEqual(error as? D.Failure, .cyclic(blockedNames: ["a", "b", "c"], edges: edges))
        }
    }
}
#endif
