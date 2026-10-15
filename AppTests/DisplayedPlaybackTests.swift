import SpriteKit
import UIKit
import XCTest
@testable import SSRuntime
@testable import SurveillanceCore

#if DEBUG
/// BP-008 harness sanity: real action-time textures and real simulation travel.
/// This does not admit candidate art or close the full movement matrix.
@MainActor
final class DisplayedPlaybackTests: XCTestCase {
    final class CaptureScene: SKScene {
        struct Sample: Codable {
            let displayTime: Double
            let tick: UInt64
            let authoritativeRawX: Int64
            let authoritativeRawY: Int64
            let renderedX: Double
            let renderedY: Double
            let width: Double
            let height: Double
            let anchorX: Double
            let anchorY: Double
            let facing: String
            let clip: String
            let framePath: String?
        }
        let renderer = WorldRenderer()
        let session = GameSession(seed: 1)
        var samples: [Sample] = []
        var done: (() -> Void)?
        private var previousTime: Double?
        private var accumulator = 0.0
        private var displayTime = 0.0
        private var finished = false

        override func didMove(to view: SKView) {
            addChild(renderer.root)
            session.moveY = PlayerCommand.axisMaximum
            let camera = SKCameraNode()
            addChild(camera)
            self.camera = camera
        }
        override func update(_ currentTime: TimeInterval) {
            guard !finished else { return }
            displayTime = currentTime
            if let previousTime { accumulator += min(currentTime - previousTime, 0.25) }
            previousTime = currentTime
            while accumulator >= 1.0 / 60.0 && session.simulation.state.tick < 90 {
                session.step()
                accumulator -= 1.0 / 60.0
            }
            let snap = session.snapshot
            camera?.position = CGPoint(x: snap.player.x, y: snap.player.y)
            renderer.render(snap, reducedMotion: false)
        }
        override func didEvaluateActions() {
            guard !finished, let observed = renderer.observePlayerPlayback() else { return }
            let state = session.simulation.state
            let snap = session.snapshot
            samples.append(Sample(displayTime: displayTime, tick: state.tick,
                authoritativeRawX: state.player.position.x.raw,
                authoritativeRawY: state.player.position.y.raw,
                renderedX: Double(observed.position.x), renderedY: Double(observed.position.y),
                width: Double(observed.size.width), height: Double(observed.size.height),
                anchorX: Double(observed.anchor.x), anchorY: Double(observed.anchor.y),
                facing: snap.playerDirection, clip: observed.clipToken ?? "unidentified",
                framePath: observed.deliveredPath))
            if state.tick >= 90 {
                finished = true
                done?()
            }
        }
    }

    func testLiveActionsExposeChangingDeliveredFramesAndSimulationTravel() async throws {
        let window = UIWindow(frame: CGRect(x: 0, y: 0, width: 704, height: 326))
        let controller = UIViewController()
        let view = SKView(frame: window.bounds)
        controller.view = view
        window.rootViewController = controller
        window.makeKeyAndVisible()
        let scene = CaptureScene(size: view.bounds.size)
        let completed = expectation(description: "90 simulation ticks with post-action observations")
        scene.done = { completed.fulfill() }
        view.presentScene(scene)
        defer { view.presentScene(nil); window.isHidden = true }
        await fulfillment(of: [completed], timeout: 15)
        XCTAssertGreaterThan(scene.samples.count, 10)
        XCTAssertTrue(scene.samples.allSatisfy { $0.framePath != nil })
        let moving = scene.samples.filter { $0.clip.hasPrefix("player_move|") }
        XCTAssertGreaterThan(Set(moving.compactMap(\.framePath)).count, 1,
                             "A static or reset-on-every-frame fixture cannot prove playback")
        let first = try XCTUnwrap(scene.samples.first)
        XCTAssertTrue(scene.samples.contains {
            $0.authoritativeRawX != first.authoritativeRawX || $0.authoritativeRawY != first.authoritativeRawY
        })
        let encoder = JSONEncoder()
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
        let data = try encoder.encode(scene.samples)
        let attachment = XCTAttachment(data: data, uniformTypeIdentifier: "public.json")
        attachment.name = "BP008-live-admitted-player-post-action-frames"
        attachment.lifetime = .keepAlways
        add(attachment)
    }
}
#endif
