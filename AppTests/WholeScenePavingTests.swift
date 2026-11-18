import CoreImage
import CryptoKit
import SpriteKit
import UIKit
import XCTest
@testable import SSRuntime
@testable import SurveillanceCore

#if DEBUG
/// Muted paving native trial, coordinator 2026-11-16 05:23 UTC. Test-only.
/// ADAPT WholeSceneBenchmarkTests.swift (diagnosticArt ground patches/lines and capture) unchanged.
/// Both arms use identical diagnostic ground composition; ONLY BenchmarkReviewArt.paving differs:
/// env_ground_plaza (control) vs supplied whole-scene-muted-paving.png (trial).
/// Ordinary view only. Building/Camera/props/HUD/fields/outlines unchanged. Not acceptance.
final class WholeScenePavingTests: XCTestCase {
    private let viewport = CGSize(width: 704, height: 326)
    private let id = "solid-03-transit-kiosk"
    static let pavingSHA256 = "c0decdab226512a790ddecf49cf703c9fc736f7943f11bc364b76b111b7c3125"
    private let inputNames = ["painted-player-south", "camera", "building-constrained", "newsbox", "tree", "whole-scene-muted-paving"]

    @MainActor private func data(_ name: String) throws -> Data {
        try Data(contentsOf: try XCTUnwrap(Bundle(for: Self.self).url(forResource: name, withExtension: "png"), name))
    }
    @MainActor private func texture(_ name: String) throws -> SKTexture {
        let texture = SKTexture(image: try XCTUnwrap(UIImage(data: try data(name))))
        texture.filteringMode = .linear
        return texture
    }
    private func sha(_ data: Data) -> String { SHA256.hash(data: data).map { String(format: "%02x", $0) }.joined() }

    /// Identical to WholeSceneBenchmarkTests.diagnosticArt except paving.
    @MainActor private func art(box: AABB, paving: SKTexture) throws -> BenchmarkReviewArt {
        let env = EnvironmentTextures(), x = box.center.x, y = box.center.y
        let canvas = CGFloat(1254) * (CGFloat(128) * CGFloat(2).squareRoot() / 934)
        var art = BenchmarkReviewArt(
            player: try texture("painted-player-south"), camera: try texture("camera"),
            building: .init(texture: try texture("building-constrained"), size: CGSize(width: canvas, height: canvas),
                anchor: CGPoint(x: CGFloat(653) / 1254, y: 1 - CGFloat(1152) / 1254),
                position: CGPoint(x: box.minX, y: box.minY)), buildingID: id,
            props: [
                .init(texture: try texture("newsbox"), size: CGSize(width: 20, height: 40),
                      anchor: CGPoint(x: 0.5, y: 0), position: CGPoint(x: x + 115, y: y - 65)),
                .init(texture: try texture("tree"), size: CGSize(width: 50, height: 85),
                      anchor: CGPoint(x: 0.5, y: 0), position: CGPoint(x: 858, y: 780))
            ], paving: paving)
        let asphalt = try XCTUnwrap(env.texture(assetId: "env_ground_asphalt"))
        art.groundPatches = [
            .init(texture: asphalt, bounds: CGRect(x: 800, y: 0, width: 1504, height: 1536), tileUnits: 128),
            .init(texture: asphalt, bounds: CGRect(x: 0, y: 0, width: 800, height: 600), tileUnits: 128)
        ]
        func line(_ a: CGPoint, _ b: CGPoint, _ width: CGFloat, _ value: CGFloat) -> BenchmarkReviewArt.GroundLine {
            .init(start: a, end: b, width: width, color: SKColor(white: value, alpha: 1))
        }
        art.groundLines = []
        for (width, shade): (CGFloat, CGFloat) in [(8, 0.22), (5, 0.57)] {
            art.groundLines.append(line(CGPoint(x: 796, y: 604), CGPoint(x: 796, y: 1536), width, shade))
            art.groundLines.append(line(CGPoint(x: 0, y: 604), CGPoint(x: 796, y: 604), width, shade))
        }
        for x: CGFloat in [860, 900] {
            art.groundLines.append(line(CGPoint(x: x, y: 0), CGPoint(x: x, y: 1536), 5, 0.12))
            art.groundLines.append(line(CGPoint(x: x, y: 0), CGPoint(x: x, y: 1536), 1.5, 0.55))
        }
        return art
    }

    @MainActor
    func testMutedPavingVersusPlazaOrdinaryOnly() throws {
        var inputs: [String: String] = [:]
        for name in inputNames { inputs[name + ".png"] = sha(try data(name)) }
        XCTAssertEqual(inputs["whole-scene-muted-paving.png"], Self.pavingSHA256, "Bundled paving must be byte-exact source")
        let pavingImage = try XCTUnwrap(UIImage(data: try data("whole-scene-muted-paving")))
        XCTAssertEqual(pavingImage.size.width * pavingImage.scale, 1254)
        XCTAssertEqual(pavingImage.size.height * pavingImage.scale, 1254)
        var census: [[String: Any]] = []
        var hiddenCensus: [String: [Bool]] = [:]
        for arm in ["plaza", "muted"] {
            let view = SKView(frame: CGRect(origin: .zero, size: viewport))
            view.isPaused = true
            let scene = GameScene(size: viewport)
            view.presentScene(scene)
            defer { view.presentScene(nil) }
            scene.session.audioSettings = .init(effectsEnabled: false, hapticsEnabled: false, musicEnabled: false)
            var snap = scene.session.snapshot
            let box = snap.solids[try XCTUnwrap(snap.solidIds.firstIndex(of: id))]
            let x = box.center.x, y = box.center.y
            snap.solids = [box]; snap.solidIds = [id]
            snap.player.x = x + 160; snap.player.y = y - 50; snap.playerDirection = "south"
            snap.enemies = []; snap.projectiles = []; snap.telegraphs = []; snap.mines = []
            snap.spawnSockets = []; snap.captainHousings = []; snap.captainField = nil; snap.patrolCones = []
            snap.cameras = Array(snap.cameras.prefix(1))
            XCTAssertEqual(snap.cameras.count, 1)
            snap.cameras[0].x = x + 270; snap.cameras[0].y = y + 20
            snap.cameras[0].fieldOrigin = VecI(x: x + 270, y: y + 20).asQ8
            snap.cameras[0].headingMilli = 100_000; snap.cameras[0].integrity = 3; snap.cameras[0].fieldVisible = true
            let digest = scene.session.simulation.state.digest()
            let paving = arm == "plaza" ? try XCTUnwrap(EnvironmentTextures().texture(assetId: "env_ground_plaza"))
                                         : try texture("whole-scene-muted-paving")
            XCTAssertTrue(scene.installBenchmarkCameraFrames(try CameraPlaybackTests.candidateFrames()))
            scene.setBenchmarkFieldContrast(.paired)
            scene.renderBenchmark(snapshot: snap, art: try art(box: box, paving: paving), center: CGPoint(x: x + 130, y: y + 20))
            let camera = try XCTUnwrap(scene.camera)
            let hudCount = camera.children.count
            XCTAssertGreaterThan(hudCount, 0)
            // Ordinary: the test never sets isHidden. Some HUD nodes are hidden by production state;
            // record that census (compared across arms below) rather than assuming all visible.
            let hudHidden = camera.children.map { $0.isHidden }
            hiddenCensus[arm] = hudHidden
            let names = ["sprite-player", "sprite-camera-\(snap.cameras[0].id.raw)", "benchmark-building",
                         "benchmark-prop-0", "benchmark-prop-1"]
            let uprights = try names.map { try XCTUnwrap(scene.childNode(withName: "//" + $0) as? SKSpriteNode, $0) }
            for zoom: CGFloat in [1, 1.25, 1.4] {
                var record = try capture(scene: scene, view: view, uprights: uprights, zoom: zoom,
                                         name: "paving-\(arm)-ordinary-z\(Int(zoom * 100))")
                record["arm"] = arm; record["mode"] = "ordinary"; record["zoom"] = zoom
                record["hudNodeCount"] = hudCount; record["fieldVisible"] = true
                record["hudHiddenByProduction"] = hudHidden.filter { $0 }.count
                census.append(record)
                XCTAssertEqual(scene.session.simulation.state.digest(), digest, "Capture must not mutate authority")
            }
        }
        XCTAssertEqual(census.count, 6)
        XCTAssertEqual(hiddenCensus["plaza"], hiddenCensus["muted"], "HUD state must be identical across arms")
        let output: [String: Any] = [
            "status": "PAVING_MATERIAL_TRIAL_NOT_ACCEPTANCE",
            "pavingSource": ["bundleName": "whole-scene-muted-paving.png", "sha256": Self.pavingSHA256, "pixels": [1254, 1254],
                             "tileUnits": 128, "slabsPerTile": "4x4 authored", "worldUnitsPerSlab": 32],
            "openItems": ["seam/repetition pending: opposite-edge RGB mean abs difference about 13-14/255, not mathematically seamless",
                          "building NOT SOLVED: building-constrained.png fallback",
                          "soft contact shadows absent",
                          "Camera field and HUD prominence retained"],
            "unboundInputs": ["env_ground_plaza", "env_ground_asphalt", "CameraPlaybackTests.candidateFrames()"],
            "inputSHA256": inputs, "captures": census]
        let attachment = XCTAttachment(data: try JSONSerialization.data(withJSONObject: output, options: [.prettyPrinted, .sortedKeys]),
                                       uniformTypeIdentifier: "public.json")
        attachment.name = "paving-records"; attachment.lifetime = .keepAlways; add(attachment)
    }

    @MainActor
    private func capture(scene: GameScene, view: SKView, uprights: [SKSpriteNode], zoom: CGFloat,
                         name: String) throws -> [String: Any] {
        let mapping = ReferenceProjectionTrial.midpoint
        let camera = try XCTUnwrap(scene.camera)
        let center = camera.position
        let crop = CGRect(x: center.x - 352, y: center.y - 163, width: 704, height: 326)
        let saved = try uprights.map { ($0, try XCTUnwrap($0.parent), $0.position, $0.zPosition) }
        let roots = saved.map { scene.convert($0.2, from: $0.1) }
        let world = SKNode()
        world.setScale(zoom)
        world.position = CGPoint(x: center.x * (1 - zoom), y: center.y * (1 - zoom))
        let chain = mapping.groundChain(center: center)
        for (index, entry) in saved.enumerated() {
            var depth = entry.3; var ancestor: SKNode? = entry.1
            while let current = ancestor, current !== scene { depth += current.zPosition; ancestor = current.parent }
            let delta = mapping.forward(CGPoint(x: roots[index].x - center.x, y: roots[index].y - center.y))
            entry.0.removeFromParent()
            entry.0.position = CGPoint(x: center.x + delta.x, y: center.y + delta.y)
            entry.0.zPosition = depth
            world.addChild(entry.0)
        }
        let ground = scene.children.filter { $0 !== camera }
        for node in ground { node.removeFromParent(); chain.coordinates.addChild(node) }
        world.addChild(chain.root); scene.addChild(world)
        defer {
            for node in ground { node.removeFromParent(); scene.addChild(node) }
            for entry in saved { entry.0.removeFromParent(); entry.0.position = entry.2; entry.0.zPosition = entry.3; entry.1.addChild(entry.0) }
            world.removeFromParent()
        }
        var actors: [[String: Any]] = []
        for (index, entry) in saved.enumerated() {
            let actual = entry.0.convert(CGPoint.zero, to: scene)
            let expected = chain.coordinates.convert(roots[index], to: scene)
            XCTAssertEqual(actual.x, expected.x, accuracy: 0.002); XCTAssertEqual(actual.y, expected.y, accuracy: 0.002)
            actors.append(["name": entry.0.name ?? "", "worldRoot": [roots[index].x, roots[index].y],
                           "projectedRoot": [actual.x, actual.y]])
        }
        let image = try XCTUnwrap(view.texture(from: scene, crop: crop)).cgImage()
        var hashes: [String: String] = [:]
        func png(_ image: UIImage, _ suffix: String) throws {
            let bytes = try XCTUnwrap(image.pngData())
            let attachment = XCTAttachment(data: bytes, uniformTypeIdentifier: "public.png")
            attachment.name = name + suffix; attachment.lifetime = .keepAlways; add(attachment)
            hashes[suffix] = sha(bytes)
        }
        try png(UIImage(cgImage: image), "-native")
        let format = UIGraphicsImageRendererFormat(); format.scale = 1
        let half = UIGraphicsImageRenderer(size: CGSize(width: image.width / 2, height: image.height / 2), format: format).image { _ in
            UIImage(cgImage: image).draw(in: CGRect(x: 0, y: 0, width: image.width / 2, height: image.height / 2))
        }
        try png(half, "-half")
        let filter = try XCTUnwrap(CIFilter(name: "CIColorControls"))
        filter.setValue(CIImage(cgImage: image), forKey: kCIInputImageKey)
        filter.setValue(0, forKey: kCIInputSaturationKey)
        let output = try XCTUnwrap(filter.outputImage)
        try png(UIImage(cgImage: try XCTUnwrap(CIContext().createCGImage(output, from: output.extent))), "-grayscale")
        return ["name": name, "nativePixels": [image.width, image.height], "pngSHA256": hashes, "actors": actors]
    }
}
#endif
