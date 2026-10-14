import SpriteKit
import UIKit
import XCTest
@testable import SSRuntime
@testable import SurveillanceCore

/// BP-001/BP-006 evidence capture, not visual acceptance or a performance test.
/// Uses the shipping GameScene/renderer/HUD. Images remain in the test result.
final class BenchmarkCaptureTests: XCTestCase {
    @MainActor
    func testCaptureCurrentRuntimeBaseline() throws {
        let view = SKView(frame: CGRect(x: 0, y: 0, width: 704, height: 326))
        view.isPaused = true
        let scene = GameScene(size: view.bounds.size)
        view.presentScene(scene)
        defer { view.presentScene(nil) }
        scene.session.audioSettings = .init(effectsEnabled: false, hapticsEnabled: false, musicEnabled: false)
        scene.skipIntroIfRunning()
        scene.update(0)
        let camera = try XCTUnwrap(scene.camera)
        let bottomLeft = scene.convert(CGPoint(x: -352, y: -163), from: camera)
        let topRight = scene.convert(CGPoint(x: 352, y: 163), from: camera)
        let crop = CGRect(x: bottomLeft.x, y: bottomLeft.y,
                          width: topRight.x - bottomLeft.x, height: topRight.y - bottomLeft.y)
        let texture = try XCTUnwrap(view.texture(from: scene, crop: crop))
        let image = UIImage(cgImage: texture.cgImage())
        XCTAssertGreaterThan(image.size.width, 0)
        XCTAssertGreaterThan(image.size.height, 0)
        let attachment = XCTAttachment(image: image)
        attachment.name = "BP001-current-runtime-baseline"
        attachment.lifetime = .keepAlways
        add(attachment)
        let snapshot = scene.session.snapshot
        let geometry = SKNode()
        geometry.zPosition = 999
        scene.addChild(geometry)
        for solid in snapshot.solids {
            let outline = SKShapeNode(rectOf: CGSize(width: solid.halfSize.x * 2, height: solid.halfSize.y * 2))
            outline.position = CGPoint(x: solid.center.x, y: solid.center.y)
            outline.strokeColor = .magenta
            outline.fillColor = .clear
            outline.lineWidth = 1
            geometry.addChild(outline)
        }
        let geometryTexture = try XCTUnwrap(view.texture(from: scene, crop: crop))
        let geometryAttachment = XCTAttachment(image: UIImage(cgImage: geometryTexture.cgImage()))
        geometryAttachment.name = "BP001-current-runtime-solid-overlay"
        geometryAttachment.lifetime = .keepAlways
        add(geometryAttachment)
        geometry.removeFromParent()
        let record = """
        Status: CAPTURED, not visually accepted.
        Source: real GameScene, WorldRenderer and HUD; current shipping art only.
        Harness: BenchmarkCaptureTests/testCaptureCurrentRuntimeBaseline.
        Logical viewport: 704 x 326 points. SKView display scale: \(view.contentScaleFactor).
        Export pixels: \(texture.cgImage().width) x \(texture.cgImage().height).
        Simulation tick: \(snapshot.tick). Intro skipped through normal scene method.
        Camera position: \(camera.position). Scale: \(camera.xScale),\(camera.yScale).
        Capture crop in scene coordinates: \(crop).
        Simulation advanced once; SKActions paused. This is a still baseline,
        not animation, dense encounter, new-art admission or device timing proof.
        Device: \(UIDevice.current.model), \(UIDevice.current.systemName) \(UIDevice.current.systemVersion).
        """
        let evidence = XCTAttachment(string: record)
        evidence.name = "BP001-current-runtime-capture-record"
        evidence.lifetime = .keepAlways
        add(evidence)
    }
}
