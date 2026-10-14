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
#if DEBUG
    @MainActor
    func testCaptureRevisedBenchmarkComposition() throws {
        let bundle = Bundle(for: Self.self)
        func texture(_ name: String) throws -> SKTexture {
            let url = try XCTUnwrap(bundle.url(forResource: name, withExtension: "png"))
            let image = try XCTUnwrap(UIImage(contentsOfFile: url.path))
            let texture = SKTexture(image: image)
            texture.filteringMode = .linear
            return texture
        }
        let view = SKView(frame: CGRect(x: 0, y: 0, width: 704, height: 326))
        view.isPaused = true
        let scene = GameScene(size: view.bounds.size)
        view.presentScene(scene)
        defer { view.presentScene(nil) }
        scene.session.audioSettings = .init(effectsEnabled: false, hapticsEnabled: false, musicEnabled: false)
        var snap = scene.session.snapshot
        let id = "solid-03-transit-kiosk"
        let index = try XCTUnwrap(snap.solidIds.firstIndex(of: id))
        let box = snap.solids[index]
        let x = box.center.x
        let y = box.center.y
        snap.solids = [box]
        snap.solidIds = [id]
        snap.player.x = x + 160
        snap.player.y = y - 50
        snap.playerDirection = "south"
        snap.enemies = []
        snap.projectiles = []
        snap.telegraphs = []
        snap.mines = []
        snap.spawnSockets = []
        snap.captainHousings = []
        snap.captainField = nil
        snap.patrolCones = []
        snap.cameras = Array(snap.cameras.prefix(1))
        XCTAssertEqual(snap.cameras.count, 1)
        snap.cameras[0].x = x + 270
        snap.cameras[0].y = y + 20
        snap.cameras[0].fieldOrigin = VecI(x: x + 270, y: y + 20).asQ8
        snap.cameras[0].headingMilli = 100_000
        snap.cameras[0].integrity = 3
        snap.cameras[0].fieldVisible = true
        let env = EnvironmentTextures()
        let center = CGPoint(x: x + 130, y: y + 20)
        let art = BenchmarkReviewArt(
            player: try texture("player-south"), camera: try texture("camera"),
            building: .init(texture: try texture("building"), size: CGSize(width: 190, height: 217),
                            anchor: CGPoint(x: 0.5, y: 0), position: CGPoint(x: x, y: y - 64)),
            buildingID: id,
            props: [
                .init(texture: try texture("newsbox"), size: CGSize(width: 20, height: 40),
                      anchor: CGPoint(x: 0.5, y: 0), position: CGPoint(x: x + 115, y: y - 65)),
                .init(texture: try texture("tree"), size: CGSize(width: 50, height: 85),
                      anchor: CGPoint(x: 0.5, y: 0), position: CGPoint(x: x + 355, y: y - 20))
            ], paving: try XCTUnwrap(env.texture(assetId: "env_ground_plaza")))
        scene.renderBenchmark(snapshot: snap, art: art, center: center)
        XCTAssertNil(scene.childNode(withName: "//housing-\(snap.cameras[0].id.raw)"))
        XCTAssertNotNil(scene.childNode(withName: "//sprite-camera-\(snap.cameras[0].id.raw)"))
        XCTAssertNotNil(scene.childNode(withName: "//benchmark-building"))
        let crop = CGRect(x: center.x - 352, y: center.y - 163, width: 704, height: 326)
        func capture(_ name: String) throws {
            let result = try XCTUnwrap(view.texture(from: scene, crop: crop))
            let attachment = XCTAttachment(image: UIImage(cgImage: result.cgImage()))
            attachment.name = name
            attachment.lifetime = .keepAlways
            add(attachment)
        }
        try capture("BP001-revised-composition")
        let overlay = SKShapeNode(rectOf: CGSize(width: box.halfSize.x * 2, height: box.halfSize.y * 2))
        overlay.position = CGPoint(x: x, y: y)
        overlay.strokeColor = .magenta
        overlay.fillColor = .clear
        overlay.lineWidth = 1
        overlay.zPosition = 999
        scene.addChild(overlay)
        try capture("BP001-revised-building-footprint")
        overlay.isHidden = true

        // texture(from:crop:) renders node coordinates rather than a camera viewport.
        // Apply the equivalent world-to-view affine zoom before rasterization, leaving
        // the camera-attached HUD fixed. This is not enlargement of a captured bitmap.
        let camera = try XCTUnwrap(scene.camera)
        let worldChildren = scene.children.filter { $0 !== camera }
        let zoomRoot = SKNode()
        let zoom: CGFloat = 1.25
        zoomRoot.setScale(zoom)
        zoomRoot.position = CGPoint(x: center.x * (1 - zoom), y: center.y * (1 - zoom))
        scene.addChild(zoomRoot)
        for node in worldChildren {
            node.removeFromParent()
            zoomRoot.addChild(node)
        }
        let centerAfterZoom = zoomRoot.convert(center, to: scene)
        XCTAssertEqual(centerAfterZoom.x, center.x, accuracy: 0.001)
        XCTAssertEqual(centerAfterZoom.y, center.y, accuracy: 0.001)
        XCTAssertEqual(camera.xScale, 1)
        try capture("BP007-framing-125-percent")
        overlay.isHidden = false
        try capture("BP007-framing-125-percent-footprint")
        for node in worldChildren {
            node.removeFromParent()
            scene.addChild(node)
        }
        zoomRoot.removeFromParent()
        let record = XCTAttachment(string: """
        Composition fixture, not a legal encounter or animation acceptance.
        Runtime renderer and HUD; test-only candidate textures. 704x326 logical viewport.
        Existing solid \(id) AABB is unchanged: \(box). Other solids omitted for isolated review.
        Player, camera and props are explicitly placed presentation samples; simulation is unchanged.
        One complete camera node. Candidate stills only; no locomotion animation claimed.
        Fog omitted while source strips await replacement. Paving uses existing plaza texture.
        Building mapping: 190x217, bottom-center at (\(x),\(y-64)); not fitted to collision AABB.
        Player mapping: 64x64, anchor (32,56). Camera mapping: 64x96, anchor (32,88).
        Candidate source records are in BenchmarkAssets/sources.json. Linear filtering for high-resolution candidate textures.
        BP007 comparison: identical snapshot, art sizes, center, HUD and 704x326 output viewport.
        Close candidate: 1.25 world-to-view magnification (equivalent camera scale 0.8).
        World nodes transformed before rasterization; camera/HUD unchanged. No bitmap upscaling.
        This comparison reduces visible world area; it does not validate legal encounter readability.
        """)
        record.name = "BP001-revised-composition-record"
        record.lifetime = .keepAlways
        add(record)
    }
#endif

}
