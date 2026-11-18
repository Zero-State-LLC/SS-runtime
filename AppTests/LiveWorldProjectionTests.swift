import SpriteKit
import UIKit
import XCTest
@testable import SSRuntime
@testable import SurveillanceCore

#if DEBUG
@MainActor
final class LiveWorldProjectionTests: XCTestCase {
    private let viewport = CGSize(width: 704, height: 326)
    private func project(_ point: CGPoint) -> CGPoint {
        CGPoint(x: (point.x - point.y) / sqrt(2), y: (point.x + point.y) / (2 * sqrt(2)))
    }
    private func equal(_ actual: CGPoint, _ expected: CGPoint, file: StaticString = #filePath, line: UInt = #line) {
        XCTAssertEqual(actual.x, expected.x, accuracy: 0.001, file: file, line: line)
        XCTAssertEqual(actual.y, expected.y, accuracy: 0.001, file: file, line: line)
    }
    private func review(_ arm: KioskPlayableReview.Arm = .candidate) throws -> KioskPlayableReview {
        let root = URL(fileURLWithPath: #filePath).deletingLastPathComponent().deletingLastPathComponent()
            .appendingPathComponent("docs/review/kiosk-only-geometry-20261117/native/playable/resources")
        return try KioskPlayableReview.load(.init(arm: arm, root: root))
    }
    private func scene() -> (GameScene, SKView) {
        let view = SKView(frame: CGRect(origin: .zero, size: viewport))
        view.isPaused = true
        let scene = GameScene(size: viewport)
        view.presentScene(scene)
        scene.session.audioSettings = .init(effectsEnabled: false, hapticsEnabled: false, musicEnabled: false)
        scene.skipIntroIfRunning()
        return (scene, view)
    }
    private func node(_ scene: SKNode, _ name: String) throws -> SKNode {
        try XCTUnwrap(scene.childNode(withName: "//" + name))
    }

    func testExplicitFlagRequiresValidatedReviewAndRejectsPartialOrDuplicate() throws {
        XCTAssertFalse(try LiveWorldProjection.requested(arguments: [], hasReview: false))
        XCTAssertFalse(try LiveWorldProjection.requested(arguments: [], hasReview: true))
        XCTAssertTrue(try LiveWorldProjection.requested(arguments: ["-SSKioskProjection", "midpoint"], hasReview: true))
        for args in [["-SSKioskProjection"], ["-SSKioskProjection", "unknown"],
                     ["-SSKioskProjection", "midpoint", "-SSKioskProjection", "midpoint"]] {
            XCTAssertThrowsError(try LiveWorldProjection.requested(arguments: args, hasReview: true))
        }
        XCTAssertThrowsError(try LiveWorldProjection.requested(arguments: ["-SSKioskProjection", "midpoint"], hasReview: false))
        let (scene, view) = scene()
        defer { view.presentScene(nil) }
        XCTAssertThrowsError(try scene.installLiveWorldProjection(true))
        XCTAssertFalse(scene.liveProjectionEnabled)
        XCTAssertNil(scene.childNode(withName: "//live-midpoint-ground"))
    }

    func testInverseEightDirectionsPreservesMagnitudeAndScreenHeading() {
        for index in 0..<8 {
            let angle = CGFloat(index) * .pi / 4
            for magnitude: CGFloat in [0, 0.1, 0.25, 0.5, 1, 32767] {
                let screen = CGPoint(x: cos(angle) * magnitude, y: sin(angle) * magnitude)
                let world = LiveWorldProjection.analogWorld(screen)
                XCTAssertEqual(hypot(world.x, world.y), magnitude, accuracy: 1e-8)
                let mapped = project(world)
                XCTAssertEqual(mapped.x * screen.y - mapped.y * screen.x, 0, accuracy: 1e-6)
                XCTAssertGreaterThanOrEqual(mapped.x * screen.x + mapped.y * screen.y, 0)
            }
        }
    }

    func testRendererGroundGeometryUprightsAndRestorationUseOneMapping() throws {
        let scene = SKScene(size: viewport)
        let camera = SKCameraNode()
        scene.addChild(camera)
        camera.position = CGPoint(x: 704, y: 640)
        let renderer = WorldRenderer()
        scene.addChild(renderer.root)
        let snapshot = PresentationSnapshot(try Simulation.make(seed: 1).state)
        try renderer.installKioskPlayableReview(review(), snapshot: snapshot)
        renderer.render(snapshot)
        let uprights = renderer.liveProjectionUprights(snapshot)
        XCTAssertGreaterThan(uprights.count, 15)
        let originals = uprights.map { ($0.node, $0.node.parent!, $0.node.position, $0.node.zPosition, $0.node.xScale, $0.node.yScale, $0.node.zRotation) }
        let kiosk = try node(scene, "kiosk-playable-review")
        let building = try XCTUnwrap(kiosk.childNode(withName: "kiosk-review-building") as? SKSpriteNode)
        let texture = building.texture
        let anchor = building.anchorPoint
        let size = building.size
        let foundation = try node(scene, "solid-footprint-solid-03-transit-kiosk")
        let field = try XCTUnwrap(node(scene, "field-3") as? SKShapeNode)
        let originalPath = field.path
        let shadow = try node(scene, "shadow-player")
        let shadowRoot = shadow.convert(CGPoint.zero, to: scene)
        let chain = LiveWorldProjection(scene: scene, camera: camera, worldRoots: [renderer.root])
        for _ in 0..<30 {
            chain.apply(uprights: uprights)
            chain.apply(uprights: uprights) // Idempotent, never double-project.
            for corner in [CGPoint(x: -64, y: -64), CGPoint(x: 64, y: 64), CGPoint(x: 64, y: -64), CGPoint(x: -64, y: 64)] {
                equal(foundation.convert(corner, to: scene), project(CGPoint(x: 576 + corner.x, y: 704 + corner.y)))
            }
            XCTAssertFalse(foundation.isHidden)
            XCTAssertGreaterThan(foundation.alpha, 0)
            equal(kiosk.convert(CGPoint.zero, to: scene), project(CGPoint(x: 512, y: 640)))
            equal(field.convert(CGPoint(x: 496, y: 672), to: scene), project(CGPoint(x: 496, y: 672)))
            equal(shadow.convert(CGPoint.zero, to: scene), project(shadowRoot))
            equal(camera.position, project(CGPoint(x: 704, y: 640)))
            XCTAssertEqual(field.path, originalPath)
            XCTAssertTrue(building.texture === texture)
            XCTAssertEqual(building.size, size)
            XCTAssertEqual(building.anchorPoint, anchor)
            for old in originals {
                XCTAssertEqual(old.0.xScale, old.4)
                XCTAssertEqual(old.0.yScale, old.5)
                XCTAssertEqual(old.0.zRotation, old.6)
            }
            chain.restore()
            chain.restore()
            for old in originals {
                XCTAssertTrue(old.0.parent === old.1)
                XCTAssertEqual(old.0.position, old.2)
                XCTAssertEqual(old.0.zPosition, old.3)
            }
        }
        chain.remove()
        XCTAssertTrue(renderer.root.parent === scene)
        equal(camera.position, CGPoint(x: 704, y: 640))
    }

    func testWorldEffectsAndGroundVectorsProjectWhileHUDDoesNot() throws {
        let scene = SKScene(size: viewport)
        let camera = SKCameraNode()
        scene.addChild(camera)
        let world = SKNode(), effects = SKNode(), hud = SKNode()
        scene.addChild(world)
        scene.addChild(effects)
        camera.addChild(hud)
        hud.position = CGPoint(x: 80, y: 40)
        camera.position = CGPoint(x: 200, y: 300)
        let effect = SKShapeNode(rectOf: CGSize(width: 30, height: 40))
        effect.position = CGPoint(x: 250, y: 350)
        effect.zRotation = .pi / 6
        effects.addChild(effect)
        let points = [CGPoint.zero, CGPoint(x: 10, y: 20), CGPoint(x: -15, y: -20)]
        let before = points.map { effect.convert($0, to: scene) }
        let chain = LiveWorldProjection(scene: scene, camera: camera, worldRoots: [world, effects])
        chain.apply(uprights: [])
        for (point, original) in zip(points, before) { equal(effect.convert(point, to: scene), project(original)) }
        equal(hud.position, CGPoint(x: 80, y: 40))
        equal(hud.convert(CGPoint(x: 5, y: 7), to: camera), CGPoint(x: 85, y: 47))
        chain.remove()
        for (point, original) in zip(points, before) { equal(effect.convert(point, to: scene), original) }
    }

    func testManualInputIsMappedOnceAndDodgeLayoutPauseRemainIntact() throws {
        final class Finger {}
        let (scene, view) = scene()
        defer { view.presentScene(nil) }
        try scene.installKioskPlayableReview(review())
        let layout = try XCTUnwrap(scene.controlLayout)
        try scene.installLiveWorldProjection(true)
        XCTAssertEqual(scene.controlLayout?.stickCentre, layout.stickCentre)
        XCTAssertEqual(scene.controlLayout?.dodgeRect, layout.dodgeRect)
        let finger = Finger(), dodge = Finger()
        let token = TouchController.TouchToken(id: ObjectIdentifier(finger))
        let dodgeToken = TouchController.TouchToken(id: ObjectIdentifier(dodge))
        scene.beginTouch(token: token, atPoints: layout.stickCentre)
        scene.moveTouch(token: token, toPoints: CGPoint(x: layout.stickCentre.x + layout.stickRadius * 0.6, y: layout.stickCentre.y))
        scene.beginTouch(token: dodgeToken, atPoints: CGPoint(x: layout.dodgeRect.midX, y: layout.dodgeRect.midY))
        scene.update(1)
        scene.didEvaluateActions()
        let command = try XCTUnwrap(scene.session.commandLog.last)
        XCTAssertGreaterThan(command.moveX, 0)
        XCTAssertEqual(command.moveX, -command.moveY)
        XCTAssertTrue(command.dodgePressed)
        let expectedMagnitude = (0.6 - 0.15) / 0.85 * Double(PlayerCommand.axisMaximum)
        XCTAssertEqual(hypot(Double(command.moveX), Double(command.moveY)), expectedMagnitude, accuracy: 2)
        scene.setPaused(true)
        let tick = scene.currentTick
        scene.update(2)
        scene.didEvaluateActions()
        XCTAssertEqual(scene.currentTick, tick)
        scene.setPaused(false)
        scene.update(3)
        scene.didEvaluateActions()
        XCTAssertEqual(scene.session.commandLog.last?.moveX, 0)
        XCTAssertEqual(scene.session.commandLog.last?.moveY, 0)
        XCTAssertEqual(scene.session.commandLog.last?.dodgePressed, false)
    }

    func testEqualLegalWorldCommandsKeepFullSnapshotsAndDigests() throws {
        let (scene, view) = scene()
        defer { view.presentScene(nil) }
        let control = GameSession(seed: 1)
        control.audioSettings = scene.session.audioSettings
        try scene.installKioskPlayableReview(review())
        try scene.installLiveWorldProjection(true)
        for tick in 0..<120 {
            let x: Int16 = tick < 60 ? 16000 : -16000
            scene.session.moveX = x
            control.moveX = x
            scene.session.step()
            control.step()
            scene.redrawBenchmarkPresentation()
            XCTAssertEqual(scene.session.simulation.state.digest(), control.simulation.state.digest())
            XCTAssertEqual(scene.session.snapshot, control.snapshot)
        }
    }

    func testPausedRedrawToggleRestartAndRemovalNeverDuplicateOrResurrectNodes() throws {
        let (scene, view) = scene()
        defer { view.presentScene(nil) }
        try scene.installKioskPlayableReview(review(.current))
        let initial = scene.session.simulation.state.digest()
        for _ in 0..<5 {
            try scene.installLiveWorldProjection(true)
            scene.setPaused(true)
            for _ in 0..<4 { scene.redrawBenchmarkPresentation() }
            equal(try node(scene, "kiosk-playable-review").convert(CGPoint.zero, to: scene), project(CGPoint(x: 512, y: 640)))
            XCTAssertEqual(scene.session.simulation.state.digest(), initial)
            scene.restartRun()
            equal(try node(scene, "kiosk-playable-review").convert(CGPoint.zero, to: scene), project(CGPoint(x: 512, y: 640)))
            try scene.installLiveWorldProjection(false)
            XCTAssertNil(scene.childNode(withName: "//live-midpoint-ground"))
            equal(try node(scene, "kiosk-playable-review").position, CGPoint(x: 512, y: 640))
        }
        try scene.installLiveWorldProjection(true)
        try scene.installKioskPlayableReview(nil)
        XCTAssertFalse(scene.liveProjectionEnabled)
        XCTAssertNil(scene.childNode(withName: "//kiosk-playable-review"))
        XCTAssertNil(scene.childNode(withName: "//live-midpoint-uprights"))
        XCTAssertEqual(scene.session.simulation.state.digest(), initial)
        XCTAssertNotNil(scene.childNode(withName: "//sprite-player"))
    }

    func testLegalAutopilotCommandsBypassManualInverseMapping() throws {
        let (scene, view) = scene()
        defer { view.presentScene(nil) }
        let control = GameSession(seed: 1)
        control.audioSettings = scene.session.audioSettings
        let args = ["-SSAutopilot", "run"]
        var pilot = try XCTUnwrap(DebugAutopilot.fromLaunchArguments(args, arena: control.simulation.state.arena))
        scene.configureAutopilot(arguments: args)
        try scene.installKioskPlayableReview(review())
        try scene.installLiveWorldProjection(true)
        for tick in 0..<90 {
            let before = scene.currentTick
            scene.update(Double(tick) / 60)
            scene.didEvaluateActions()
            guard scene.currentTick > before else { continue }
            let expected = pilot.command(control.snapshot)
            control.moveX = expected.moveX
            control.moveY = expected.moveY
            control.dodgePressed = expected.dodge
            control.step()
            XCTAssertEqual(scene.session.commandLog.last?.moveX, expected.moveX)
            XCTAssertEqual(scene.session.commandLog.last?.moveY, expected.moveY)
            XCTAssertEqual(scene.session.simulation.state.digest(), control.simulation.state.digest())
            XCTAssertEqual(scene.session.snapshot, control.snapshot)
        }
        XCTAssertGreaterThan(scene.currentTick, 60)
    }

    func testRemovedUprightStaysRemovedAndNewNodeProjectsWithoutDrift() {
        let scene = SKScene(size: viewport), world = SKNode(), camera = SKCameraNode()
        scene.addChild(world)
        scene.addChild(camera)
        let old = SKNode()
        old.position = CGPoint(x: 100, y: 200)
        world.addChild(old)
        let adapter = LiveWorldProjection(scene: scene, camera: camera, worldRoots: [world])
        adapter.apply(uprights: [.init(node: old)])
        old.removeFromParent()
        adapter.restore()
        XCTAssertNil(old.parent)
        let fresh = SKNode()
        fresh.position = CGPoint(x: 300, y: 400)
        world.addChild(fresh)
        adapter.apply(uprights: [.init(node: old), .init(node: fresh)])
        equal(fresh.position, project(CGPoint(x: 300, y: 400)))
        adapter.remove()
        XCTAssertTrue(fresh.parent === world)
        equal(fresh.position, CGPoint(x: 300, y: 400))
        XCTAssertNil(old.parent)
    }

    func testActualSKViewCallbacksRestoreBeforeActionsAndProjectAfterward() async throws {
        final class Finger {}
        let window = UIWindow(frame: CGRect(origin: .zero, size: viewport))
        let controller = UIViewController()
        let view = SKView(frame: window.bounds)
        controller.view = view
        window.rootViewController = controller
        window.makeKeyAndVisible()
        let scene = GameScene(size: viewport)
        view.isPaused = true
        view.presentScene(scene)
        defer { view.presentScene(nil); window.isHidden = true }
        scene.session.audioSettings = .init(effectsEnabled: false, hapticsEnabled: false, musicEnabled: false)
        scene.skipIntroIfRunning()
        try scene.installKioskPlayableReview(review())
        let player = try node(scene, "sprite-player")
        try scene.installLiveWorldProjection(true)
        let layout = try XCTUnwrap(scene.controlLayout)
        let finger = Finger()
        let token = TouchController.TouchToken(id: ObjectIdentifier(finger))
        scene.beginTouch(token: token, atPoints: layout.stickCentre)
        scene.moveTouch(token: token, toPoints: CGPoint(x: layout.stickCentre.x + layout.stickRadius, y: layout.stickCentre.y))
        var actionCalls = 0, callbacks = 0
        var textures: Set<ObjectIdentifier> = []
        var worldPosition = CGPoint.zero, worldCamera = CGPoint.zero
        scene.benchmarkPlaybackObserver = { _, _, _, observed, camera in
            worldPosition = observed.position
            worldCamera = camera
        }
        let actionProbe = SKNode()
        actionProbe.name = "projection-action-probe-owner"
        player.addChild(actionProbe)
        actionProbe.run(.repeatForever(.sequence([.run {
            MainActor.assumeIsolated {
                actionCalls += 1
                XCTAssertTrue(actionProbe.parent === player)
                XCTAssertNotEqual(player.parent?.name, "live-midpoint-uprights")
                XCTAssertEqual(scene.childNode(withName: "//live-midpoint-ground")?.yScale, 1)
            }
        }, .wait(forDuration: 1.0 / 60)])), withKey: "projection-action-probe")
        let done = expectation(description: "60 real projected display callbacks")
        scene.liveProjectionObserver = {
            callbacks += 1
            self.equal(player.convert(CGPoint.zero, to: scene), self.project(worldPosition))
            self.equal(scene.camera!.position, self.project(worldCamera))
            XCTAssertEqual(player.parent?.name, "live-midpoint-uprights")
            if let texture = (player as? SKSpriteNode)?.texture { textures.insert(ObjectIdentifier(texture)) }
            if callbacks == 60 { done.fulfill() }
        }
        view.isPaused = false
        await fulfillment(of: [done], timeout: 20)
        view.isPaused = true
        XCTAssertGreaterThan(actionCalls, 10)
        XCTAssertGreaterThan(scene.currentTick, 30)
        XCTAssertGreaterThan(textures.count, 1)
    }
}
#endif
