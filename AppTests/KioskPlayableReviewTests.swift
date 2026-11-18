import SpriteKit
import UIKit
import XCTest
@testable import SSRuntime
@testable import SurveillanceCore

#if DEBUG
final class KioskPlayableReviewTests: XCTestCase {
    private var resources: URL {
        URL(fileURLWithPath: #filePath).deletingLastPathComponent().deletingLastPathComponent()
            .appendingPathComponent("docs/review/kiosk-only-geometry-20261117/native/playable/resources")
    }
    @MainActor private func review(_ arm: KioskPlayableReview.Arm) throws -> KioskPlayableReview {
        try KioskPlayableReview.load(.init(arm: arm, root: resources))
    }
    private func temporaryResources() throws -> URL {
        let root = FileManager.default.temporaryDirectory.resolvingSymlinksInPath().appendingPathComponent(UUID().uuidString)
        try FileManager.default.copyItem(at: resources, to: root)
        addTeardownBlock { try FileManager.default.removeItem(at: root) }
        return root
    }

    @MainActor func testExplicitOptInAndMalformedArgumentsFailClosed() throws {
        XCTAssertNil(try KioskPlayableReview.request(arguments: ["app", "-SSMute"]))
        let valid = ["app", "-SSKioskReview", "candidate", "-SSKioskReviewRoot", resources.path]
        XCTAssertEqual(try KioskPlayableReview.request(arguments: valid), .init(arm: .candidate, root: resources))
        for arguments in [["-SSKioskReview"], ["-SSKioskReview", "bad", "-SSKioskReviewRoot", resources.path],
                          ["-SSKioskReviewRoot", resources.path], valid + ["-SSKioskReview", "current"],
                          ["-SSKioskReview", "current", "-SSKioskReviewRoot", "relative/path"],
                          ["-SSKioskReview", "current", "-SSKioskReviewRoot", "/a/../b"]] {
            XCTAssertThrowsError(try KioskPlayableReview.request(arguments: arguments))
        }
    }

    @MainActor func testBothExactSourceArmsAndV9BaseLoad() throws {
        let current = try review(.current), candidate = try review(.candidate)
        XCTAssertEqual(current.building.size, CGSize(width: 200, height: 240))
        XCTAssertEqual(candidate.building.size, CGSize(width: 200, height: 212))
        XCTAssertEqual(candidate.building.anchor, CGPoint(x: 0.5, y: 1 - CGFloat(1020) / 1060))
        XCTAssertEqual(current.base, candidate.base)
        let node = candidate.makeNode()
        XCTAssertEqual(node.position, CGPoint(x: 512, y: 640))
        let base = try XCTUnwrap(node.childNode(withName: "kiosk-review-v9-base") as? SKSpriteNode)
        let building = try XCTUnwrap(node.childNode(withName: "kiosk-review-building") as? SKSpriteNode)
        XCTAssertEqual(base.size, CGSize(width: 57.5, height: 34))
        XCTAssertEqual(base.position.x, 0, accuracy: 0.000001)
        XCTAssertEqual(base.position.y, 13 / CGFloat(2).squareRoot(), accuracy: 0.000001)
        XCTAssertLessThan(base.zPosition, building.zPosition)
        XCTAssertEqual(building.position, .zero)
    }

    @MainActor func testModifiedSourceBytesRejected() throws {
        let root = try temporaryResources()
        let path = root.appendingPathComponent("candidate.png")
        var bytes = try Data(contentsOf: path)
        bytes.append(0)
        try bytes.write(to: path)
        XCTAssertThrowsError(try KioskPlayableReview.load(.init(arm: .candidate, root: root)))
    }

    @MainActor func testModifiedManifestAndRegistrationRejected() throws {
        let root = try temporaryResources()
        let path = root.appendingPathComponent("manifest.json")
        var object = try XCTUnwrap(JSONSerialization.jsonObject(with: Data(contentsOf: path)) as? [String: Any])
        var sources = try XCTUnwrap(object["sources"] as? [[String: Any]])
        sources[1]["drawSizeWorld"] = [200, 240]
        let source = try JSONDecoder().decode(KioskPlayableReview.Source.self, from: JSONSerialization.data(withJSONObject: sources[1]))
        XCTAssertThrowsError(try KioskPlayableReview.validate(source))
        object["sources"] = sources
        try JSONSerialization.data(withJSONObject: object).write(to: path)
        XCTAssertThrowsError(try KioskPlayableReview.load(.init(arm: .candidate, root: root)))
    }

    @MainActor func testAliasedSourceAndMissingFileRejected() throws {
        let root = try temporaryResources()
        let path = root.appendingPathComponent("base.png")
        try FileManager.default.removeItem(at: path)
        XCTAssertThrowsError(try KioskPlayableReview.load(.init(arm: .candidate, root: root)))
        try FileManager.default.createSymbolicLink(at: path, withDestinationURL: resources.appendingPathComponent("base.png"))
        XCTAssertThrowsError(try KioskPlayableReview.load(.init(arm: .candidate, root: root)))
    }

    @MainActor func testAuthorityMismatchCannotInstall() throws {
        let review = try review(.candidate)
        var snap = PresentationSnapshot(try Simulation.make(seed: 1).state)
        try review.validateAuthority(snap)
        let index = try XCTUnwrap(snap.solidIds.firstIndex(of: KioskPlayableReview.solidID))
        snap.solids[index] = AABB(center: VecI(x: 577, y: 704), halfSize: VecI(x: 64, y: 64))
        XCTAssertThrowsError(try review.validateAuthority(snap))
        let renderer = WorldRenderer()
        XCTAssertThrowsError(try renderer.installKioskPlayableReview(review, snapshot: snap))
        renderer.render(snap)
        XCTAssertNil(renderer.root.childNode(withName: "//kiosk-playable-review"))
    }

    @MainActor private func neighbors(_ root: SKNode) -> [String: String] {
        let excluded = "environment-upright-" + EnvironmentLibrary.solidAssetId(forSolidId: KioskPlayableReview.solidID)
        var result: [String: String] = [:]
        root.enumerateChildNodes(withName: "//environment-upright-*") { node, _ in
            guard let sprite = node as? SKSpriteNode, let name = sprite.name, name != excluded else { return }
            let digest = sprite.texture.flatMap { UIImage(cgImage: $0.cgImage()).pngData() }.map(KioskPlayableReview.digest) ?? "none"
            result[name] = "\(sprite.position)|\(sprite.size)|\(sprite.anchorPoint)|\(sprite.zPosition)|\(sprite.alpha)|\(digest)"
        }
        return result
    }

    @MainActor private func cameraFields(_ root: SKNode) -> [String: CGPath] {
        var paths: [String: CGPath] = [:]
        root.enumerateChildNodes(withName: "//field-*") { node, _ in
            if let field = node as? SKShapeNode, let name = field.name, let path = field.path {
                paths[name] = path
            }
        }
        return paths
    }

    @MainActor func testRendererOverrideIsReversibleAndPreservesNeighborsAndActorNodes() throws {
        let snap = PresentationSnapshot(try Simulation.make(seed: 1).state)
        let renderer = WorldRenderer()
        renderer.render(snap)
        let before = neighbors(renderer.root)
        XCTAssertFalse(before.isEmpty)
        let player = try XCTUnwrap(renderer.root.childNode(withName: "//sprite-player"))
        let fieldPaths = cameraFields(renderer.root)
        XCTAssertFalse(fieldPaths.isEmpty)
        let canonicalName = "environment-upright-" + EnvironmentLibrary.solidAssetId(forSolidId: KioskPlayableReview.solidID)
        XCTAssertNotNil(renderer.root.childNode(withName: "//" + canonicalName))
        for arm in [KioskPlayableReview.Arm.current, .candidate] {
            try renderer.installKioskPlayableReview(review(arm), snapshot: snap)
            renderer.render(snap)
            XCTAssertNotNil(renderer.root.childNode(withName: "//kiosk-playable-review"))
            XCTAssertNil(renderer.root.childNode(withName: "//" + canonicalName))
            XCTAssertNotNil(renderer.root.childNode(withName: "//solid-footprint-" + KioskPlayableReview.solidID))
            XCTAssertEqual(neighbors(renderer.root), before)
            XCTAssertTrue(renderer.root.childNode(withName: "//sprite-player") === player)
            XCTAssertEqual(cameraFields(renderer.root), fieldPaths)
        }
        try renderer.installKioskPlayableReview(nil, snapshot: snap)
        renderer.render(snap)
        XCTAssertNil(renderer.root.childNode(withName: "//kiosk-playable-review"))
        XCTAssertNotNil(renderer.root.childNode(withName: "//" + canonicalName))
        XCTAssertEqual(neighbors(renderer.root), before)
    }

    @MainActor func testLiveSceneToggleAndLegalMovementKeepSimulationParity() throws {
        let session = GameSession(seed: 1)
        let control = GameSession(seed: 1)
        session.audioSettings = .init(effectsEnabled: false, hapticsEnabled: false, musicEnabled: false)
        control.audioSettings = session.audioSettings
        let view = SKView(frame: CGRect(x: 0, y: 0, width: 704, height: 326))
        view.isPaused = true
        let scene = GameScene(size: view.bounds.size, session: session)
        view.presentScene(scene)
        defer { view.presentScene(nil) }
        scene.skipIntroIfRunning()
        let initial = session.simulation.state.digest()
        let layout = scene.controlLayout
        try scene.installKioskPlayableReview(review(.candidate))
        XCTAssertEqual(session.simulation.state.digest(), initial)
        XCTAssertEqual(scene.kioskPlayableReviewState, "candidate:not-accepted:live-projection")
        XCTAssertEqual(scene.controlLayout?.stickCentre, layout?.stickCentre)
        let initialPosition = session.simulation.state.player.position
        var moved = false
        for tick in 0..<120 {
            session.moveX = tick < 60 ? PlayerCommand.axisMaximum : PlayerCommand.axisMinimum
            control.moveX = session.moveX
            session.step()
            control.step()
            scene.redrawBenchmarkPresentation()
            moved = moved || session.simulation.state.player.position != initialPosition
            XCTAssertEqual(session.simulation.state.digest(), control.simulation.state.digest())
        }
        XCTAssertTrue(moved)
        XCTAssertEqual(session.snapshot, control.snapshot)
        try scene.installKioskPlayableReview(nil)
        XCTAssertEqual(scene.kioskPlayableReviewState, "disabled")
        XCTAssertNil(scene.childNode(withName: "//kiosk-review-status"))
        XCTAssertNil(scene.childNode(withName: "//kiosk-playable-review"))
        XCTAssertEqual(session.simulation.state.digest(), control.simulation.state.digest())
    }
}
#endif
