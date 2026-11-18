import CoreImage
import SpriteKit
import UIKit
import XCTest
@testable import SSRuntime
@testable import SurveillanceCore

/// BP-001 owner-authorized isolated trial, November 16 2026 00:38 UTC.
/// New test files only. No source repaint, production mapping, fixture migration,
/// projection selection, dense-play acceptance or faithful-art claim.
final class ReferenceProjectionCaptureTests: XCTestCase {
    private let viewport = CGSize(width: 704, height: 326)

    @MainActor
    func testEightDirectionMathMatchesSpriteKitAndAnalogInverse() throws {
        let scene = SKScene(size: viewport)
        let center = CGPoint(x: 826, y: 724)
        for mapping in ReferenceProjectionTrial.candidates {
            let chain = mapping.groundChain(center: center)
            scene.addChild(chain.root)
            defer { chain.root.removeFromParent() }
            for heading in 0..<8 {
                let angle = CGFloat(heading) * .pi / 4
                for magnitude: CGFloat in [0.25, 0.5, 1, 120] {
                    let delta = CGPoint(x: cos(angle) * magnitude, y: sin(angle) * magnitude)
                    let p = CGPoint(x: center.x + delta.x, y: center.y + delta.y)
                    let actual = chain.coordinates.convert(p, to: scene)
                    let expected = mapping.forward(delta)
                    let tolerance = CGFloat(Float(max(abs(p.x), abs(p.y), 1)).ulp) * 8
                    XCTAssertEqual(actual.x, center.x + expected.x, accuracy: tolerance)
                    XCTAssertEqual(actual.y, center.y + expected.y, accuracy: tolerance)
                    let recovered = scene.convert(actual, to: chain.coordinates)
                    XCTAssertEqual(recovered.x, p.x, accuracy: tolerance)
                    XCTAssertEqual(recovered.y, p.y, accuracy: tolerance)
                    let independentInverse = mapping.inverse(expected)
                    XCTAssertEqual(independentInverse.x, delta.x, accuracy: 1e-9)
                    XCTAssertEqual(independentInverse.y, delta.y, accuracy: 1e-9)
                    if magnitude <= 1 {
                        let world = mapping.analogWorld(delta)
                        XCTAssertEqual(hypot(world.x, world.y), magnitude, accuracy: 1e-9)
                        let screen = mapping.forward(world)
                        XCTAssertEqual(screen.x * delta.y - screen.y * delta.x, 0, accuracy: 1e-9)
                        XCTAssertGreaterThan(screen.x * delta.x + screen.y * delta.y, 0)
                    }
                }
            }
            XCTAssertEqual(mapping.analogWorld(.zero), .zero)
        }
    }

    #if DEBUG
    @MainActor private var alphaSamples: [ObjectIdentifier: (width: Int, height: Int, occupiedHeight: Int)] = [:]

    @MainActor
    private func alphaSample(_ texture: SKTexture) throws -> (width: Int, height: Int, occupiedHeight: Int) {
        let key = ObjectIdentifier(texture)
        if let cached = alphaSamples[key] { return cached }
        let image = texture.cgImage()
        let width = image.width, height = image.height
        var pixels = [UInt8](repeating: 0, count: width * height * 4)
        try pixels.withUnsafeMutableBytes { bytes in
            let context = try XCTUnwrap(CGContext(data: bytes.baseAddress, width: width, height: height,
                bitsPerComponent: 8, bytesPerRow: width * 4, space: CGColorSpaceCreateDeviceRGB(),
                bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue | CGBitmapInfo.byteOrder32Big.rawValue))
            context.draw(image, in: CGRect(x: 0, y: 0, width: width, height: height))
        }
        var first = height, last = -1
        for row in 0..<height {
            if (0..<width).contains(where: { pixels[(row * width + $0) * 4 + 3] > 0 }) {
                first = min(first, row)
                last = row
            }
        }
        let result = (width, height, max(0, last - first + 1))
        alphaSamples[key] = result
        return result
    }

    @MainActor
    func testCaptureQuietStreetReferenceAndMidpoint() throws {
        let view = SKView(frame: CGRect(origin: .zero, size: viewport))
        view.isPaused = true
        let scene = GameScene(size: viewport)
        view.presentScene(scene)
        defer { view.presentScene(nil) }
        scene.session.audioSettings = .init(effectsEnabled: false, hapticsEnabled: false, musicEnabled: false)
        var snap = scene.session.snapshot
        let id = "solid-03-transit-kiosk"
        let box = snap.solids[try XCTUnwrap(snap.solidIds.firstIndex(of: id))]
        let x = box.center.x, y = box.center.y
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
        // Identical source registration to the existing BP001 quiet pair, including
        // its known midpoint-oriented baked slab. Do not refit the art to the candidate.
        let canvas = CGFloat(1254) * (CGFloat(128) * CGFloat(2).squareRoot() / 934)
        var art = BenchmarkReviewArt(
            player: try texture("painted-player-south"), camera: try texture("camera"),
            building: .init(texture: try texture("building-constrained"),
                size: CGSize(width: canvas, height: canvas),
                anchor: CGPoint(x: CGFloat(653) / 1254, y: 1 - CGFloat(1152) / 1254),
                position: CGPoint(x: box.minX, y: box.minY)), buildingID: id,
            props: [
                .init(texture: try texture("newsbox"), size: CGSize(width: 20, height: 40),
                      anchor: CGPoint(x: 0.5, y: 0), position: CGPoint(x: x + 115, y: y - 65)),
                .init(texture: try texture("tree"), size: CGSize(width: 50, height: 85),
                      anchor: CGPoint(x: 0.5, y: 0), position: CGPoint(x: 858, y: 780))
            ], paving: try XCTUnwrap(env.texture(assetId: "env_ground_plaza")))
        art.configureStreetCorner(asphalt: try XCTUnwrap(env.texture(assetId: "env_ground_asphalt")))
        XCTAssertTrue(scene.installBenchmarkCameraFrames(try CameraPlaybackTests.candidateFrames()))
        scene.setBenchmarkFieldContrast(.paired)
        scene.renderBenchmark(snapshot: snap, art: art, center: center)
        let names = ["sprite-player", "sprite-camera-\(snap.cameras[0].id.raw)",
                     "benchmark-building", "benchmark-prop-0", "benchmark-prop-1"]
        let uprights = try names.map { try XCTUnwrap(scene.childNode(withName: "//" + $0) as? SKSpriteNode) }
        try captureSweep(scene: scene, view: view, snap: snap, uprights: uprights, fixture: "quiet-street")
    }

    @MainActor
    func testCaptureLegalGhostStep4976AndSameCommandWorldInvariance() throws {
        let session = GameSession(seed: 1)
        session.audioSettings = .init(effectsEnabled: false, hapticsEnabled: false, musicEnabled: false)
        var pilot = try XCTUnwrap(DebugAutopilot(scenario: "run", arena: session.simulation.state.arena, upgrade: .ghostStep))
        var found = false
        for _ in 0..<6000 {
            let before = session.snapshot
            let command = pilot.command(before)
            session.moveX = command.moveX
            session.moveY = command.moveY
            session.dodgePressed = command.dodge
            if before.upgradePending { session.pendingUpgradeChoice = pilot.upgradeChoice.selectionIndex }
            session.step()
            let snap = session.snapshot
            let nearby = snap.enemies.filter { abs($0.x - snap.player.x) < 300 && abs($0.y - snap.player.y) < 130 }
            let attack = snap.projectiles.contains { $0.hostile && abs($0.x - snap.player.x) < 300 && abs($0.y - snap.player.y) < 130 }
            let field = snap.cameras.contains { $0.fieldVisible && abs($0.x - snap.player.x) < 280 && abs($0.y - snap.player.y) < 120 }
            if nearby.count >= 2 && attack && field { found = true; break }
            if session.simulation.isTerminal { break }
        }
        XCTAssertTrue(found)
        XCTAssertFalse(session.scenarioSeeded)
        let view = SKView(frame: CGRect(origin: .zero, size: viewport))
        view.isPaused = true
        let scene = GameScene(size: viewport, session: session)
        view.presentScene(scene)
        defer { view.presentScene(nil) }
        XCTAssertTrue(scene.installBenchmarkCameraFrames(try CameraPlaybackTests.candidateFrames()))
        scene.skipIntroIfRunning()
        scene.update(0)
        let snap = session.snapshot
        XCTAssertEqual(snap.tick, 4976, "Freeze the existing pair after its first GameScene update")
        scene.setBenchmarkFieldContrast(.paired)
        scene.refreshBenchmarkPresentation(reducedMotion: false)
        let player = try XCTUnwrap(scene.childNode(withName: "//sprite-player") as? SKSpriteNode)
        let directions = ["n": "north", "s": "south", "e": "east", "w": "west"]
        player.removeAllActions()
        player.texture = try texture("painted-player-\(directions[snap.playerDirection] ?? snap.playerDirection)")
        player.size = CGSize(width: 64, height: 64)
        player.anchorPoint = CGPoint(x: 0.5, y: 0.125)
        scene.refreshBenchmarkOutlines(samplingScale: 3)
        var uprights: [SKSpriteNode] = []
        for pattern in ["//sprite-*", "//environment-upright-*"] {
            scene.enumerateChildNodes(withName: pattern) { node, _ in
                if let sprite = node as? SKSpriteNode { uprights.append(sprite) }
            }
        }
        XCTAssertFalse(uprights.isEmpty)
        try captureSweep(scene: scene, view: view, snap: snap, uprights: uprights, fixture: "legal-ghost-step-4976")
        let state = session.simulation.state
        let record = GhostRecord(identity: state.identity, seed: state.seed, ticks: state.tick,
                                 digest: state.digest(), commands: session.commandLog)
        attach(data: try JSONEncoder().encode(record), name: "BP001-trial-same-world-commands")
        // Both mappings consume exactly the same world-command stream. No inverse
        // gesture migration is installed, so this is an authoritative digest check.
        for mapping in ReferenceProjectionTrial.candidates {
            let replayed = try XCTUnwrap(GhostRun.replay(seed: record.seed, commands: record.playerCommands, until: record.ticks))
            XCTAssertEqual(replayed.state.digest(), state.digest(), mapping.name)
            XCTAssertEqual(replayed.state.tick, state.tick)
        }
    }

    @MainActor
    private func texture(_ name: String) throws -> SKTexture {
        let url = try XCTUnwrap(Bundle(for: Self.self).url(forResource: name, withExtension: "png"))
        let image = try XCTUnwrap(UIImage(contentsOfFile: url.path))
        let result = SKTexture(image: image)
        result.filteringMode = .linear
        return result
    }

    @MainActor
    private func captureSweep(scene: GameScene, view: SKView, snap: PresentationSnapshot,
                              uprights: [SKSpriteNode], fixture: String) throws {
        let digest = scene.session.simulation.state.digest()
        let commands = scene.session.commandLog
        for mapping in ReferenceProjectionTrial.candidates {
            for zoom: CGFloat in [1, 1.25, 1.4] {
                try capture(scene: scene, view: view, snap: snap, uprights: uprights,
                            fixture: fixture, mapping: mapping, zoom: zoom)
                XCTAssertEqual(scene.session.simulation.state.digest(), digest)
                XCTAssertEqual(scene.session.commandLog, commands)
            }
        }
    }

    @MainActor
    private func capture(scene: GameScene, view: SKView, snap: PresentationSnapshot,
                         uprights: [SKSpriteNode], fixture: String,
                         mapping: ReferenceProjectionTrial, zoom: CGFloat) throws {
        let camera = try XCTUnwrap(scene.camera)
        let center = camera.position
        let crop = CGRect(x: center.x - 352, y: center.y - 163, width: 704, height: 326)
        let hudBefore = camera.children.map { $0.calculateAccumulatedFrame() }
        let saved = try uprights.map { node in
            (node, try XCTUnwrap(node.parent), node.position, node.zPosition,
             node.size, node.anchorPoint, node.xScale, node.yScale, node.zRotation)
        }
        let worldRoots = saved.map { scene.convert($0.2, from: $0.1) }
        let world = SKNode()
        world.setScale(zoom)
        world.position = CGPoint(x: center.x * (1 - zoom), y: center.y * (1 - zoom))
        let chain = mapping.groundChain(center: center)
        // Capture the complete ground subtree, including fields, attacks, shadows,
        // fog and boundaries. Only explicitly classified upright sprites leave it.
        for (index, entry) in saved.enumerated() {
            let node = entry.0
            var depth = entry.3
            var ancestor: SKNode? = entry.1
            while let current = ancestor, current !== scene {
                depth += current.zPosition
                ancestor = current.parent
            }
            let delta = mapping.forward(CGPoint(x: worldRoots[index].x - center.x, y: worldRoots[index].y - center.y))
            node.removeFromParent()
            node.position = CGPoint(x: center.x + delta.x, y: center.y + delta.y)
            node.zPosition = depth
            world.addChild(node)
        }
        let ground = scene.children.filter { $0 !== camera }
        for node in ground { node.removeFromParent(); chain.coordinates.addChild(node) }
        world.addChild(chain.root)
        scene.addChild(world)
        defer {
            for node in ground { node.removeFromParent(); scene.addChild(node) }
            for entry in saved {
                let node = entry.0
                node.removeFromParent()
                node.position = entry.2
                node.zPosition = entry.3
                entry.1.addChild(node)
            }
            world.removeFromParent()
        }
        var actors: [[String: Any]] = []
        for (index, entry) in saved.enumerated() {
            let node = entry.0
            XCTAssertEqual(node.size, entry.4)
            XCTAssertEqual(node.anchorPoint, entry.5)
            XCTAssertEqual(node.xScale, entry.6)
            XCTAssertEqual(node.yScale, entry.7)
            XCTAssertEqual(node.zRotation, entry.8)
            let actual = node.convert(CGPoint.zero, to: scene)
            let expected = chain.coordinates.convert(worldRoots[index], to: scene)
            XCTAssertEqual(actual.x, expected.x, accuracy: 0.002)
            XCTAssertEqual(actual.y, expected.y, accuracy: 0.002)
            let frame = node.frame
            let a = world.convert(CGPoint(x: frame.minX, y: frame.minY), to: scene)
            let b = world.convert(CGPoint(x: frame.maxX, y: frame.maxY), to: scene)
            let bounds = CGRect(x: a.x, y: a.y, width: b.x - a.x, height: b.y - a.y)
            let source = try alphaSample(XCTUnwrap(node.texture))
            var actor: [String: Any] = ["name": node.name ?? "unnamed"]
            actor["worldRoot"] = [worldRoots[index].x, worldRoots[index].y]
            actor["projectedRoot"] = [actual.x, actual.y]
            actor["bounds"] = [bounds.minX, bounds.minY, bounds.width, bounds.height]
            actor["canvasHeightViewportFraction"] = bounds.height / 326
            actor["anchor"] = [node.anchorPoint.x, node.anchorPoint.y]
            actor["logicalSize"] = [node.size.width, node.size.height]
            actor["sourceTexturePixels"] = [source.width, source.height]
            actor["sourceAlphaOccupiedRows"] = source.occupiedHeight
            actor["sourceAlphaHeightViewportFraction"] = CGFloat(source.occupiedHeight) / CGFloat(source.height) * node.size.height * zoom / 326
            actor["contained"] = crop.contains(bounds)
            actor["intersects"] = crop.intersects(bounds)
            actors.append(actor)
        }
        XCTAssertEqual(camera.xScale, 1)
        XCTAssertEqual(camera.yScale, 1)
        XCTAssertEqual(camera.children.map { $0.calculateAccumulatedFrame() }, hudBefore)
        let prefix = "BP001-trial-\(fixture)-\(mapping.name)-z\(Int(zoom * 100))"
        let natural = try XCTUnwrap(view.texture(from: scene, crop: crop)).cgImage()
        try attachSheets(image: natural, name: prefix)
        let overlay = geometry(snap: snap, project: { chain.coordinates.convert($0, to: scene) })
        scene.addChild(overlay)
        defer { overlay.removeFromParent() }
        try attachSheets(image: try XCTUnwrap(view.texture(from: scene, crop: crop)).cgImage(), name: prefix + "-geometry")
        let corners: [[CGFloat]] = snap.solids.flatMap { box in
            [CGPoint(x: box.minX, y: box.minY), CGPoint(x: box.minX, y: box.maxY),
             CGPoint(x: box.maxX, y: box.maxY), CGPoint(x: box.maxX, y: box.minY)].map { p in
                let s = chain.coordinates.convert(p, to: scene)
                return [p.x, p.y, s.x, s.y]
            }
        }
        let metrics: [String: Any] = [
            "fixture": fixture, "tick": snap.tick, "mapping": mapping.name,
            "referenceImageSHA256": ReferenceProjectionTrial.referenceImageSHA256,
            "landmarksSHA256": ReferenceProjectionTrial.landmarksSHA256,
            "rotationDegrees": mapping.degrees, "yScale": mapping.yScale, "matrixRowMajor": mapping.matrix,
            "zoom": zoom, "viewportPoints": [704, 326], "nativePixels": [natural.width, natural.height],
            "backingScale": CGFloat(natural.width) / 704, "worldFocus": [center.x, center.y],
            "actors": actors, "authoritativeCornersWorldAndScene": corners,
            "digest": String(describing: scene.session.simulation.state.digest()),
            "enemies": snap.enemies.count, "projectiles": snap.projectiles.count, "cameras": snap.cameras.count,
            "hudExcludedFromProjection": true, "buildingRegistrationChangedBetweenMappings": false,
            "limitations": ["Ground fit is not camera recovery or faithful original-reference art.",
                "Upright source pixels, anatomical facings and baked building slab remain unchanged and may disagree with ground mapping.",
                "Canvas bounds include transparent pixels. Source-alpha height is unoccluded authored occupancy, not visible-pixel segmentation.",
                "No new occlusion policy, source repaint, dense encounter, live input integration or acceptance."]
        ]
        attach(data: try JSONSerialization.data(withJSONObject: metrics, options: [.prettyPrinted, .sortedKeys]), name: prefix + "-metrics")
    }

    @MainActor
    private func geometry(snap: PresentationSnapshot, project: (CGPoint) -> CGPoint) -> SKNode {
        let root = SKNode()
        root.zPosition = 100_000
        for box in snap.solids {
            let corners = [CGPoint(x: box.minX, y: box.minY), CGPoint(x: box.maxX, y: box.minY),
                           CGPoint(x: box.maxX, y: box.maxY), CGPoint(x: box.minX, y: box.maxY)]
            let path = CGMutablePath()
            path.addLines(between: corners.map(project))
            path.closeSubpath()
            let shape = SKShapeNode(path: path)
            shape.strokeColor = .magenta
            shape.lineWidth = 1
            shape.fillColor = .clear
            root.addChild(shape)
        }
        // Project the authoritative circular body, not a sprite-derived hitbox.
        let path = CGMutablePath()
        let body = (0...64).map { i -> CGPoint in
            let angle = CGFloat(i) * 2 * .pi / 64
            return project(CGPoint(x: CGFloat(snap.player.x) + cos(angle) * CGFloat(PlayerBody.radiusUnits),
                                   y: CGFloat(snap.player.y) + sin(angle) * CGFloat(PlayerBody.radiusUnits)))
        }
        path.addLines(between: body)
        let ring = SKShapeNode(path: path)
        ring.strokeColor = .cyan
        ring.lineWidth = 1.25
        root.addChild(ring)
        for camera in snap.cameras {
            let key = CameraFieldGeometry.Key(camera: camera, solids: snap.solids)
            let field = CGPoint(x: key.originX, y: key.originY)
            for (point, color) in [(CGPoint(x: camera.x, y: camera.y), SKColor.cyan), (field, SKColor.yellow)] {
                let dot = SKShapeNode(circleOfRadius: 2)
                dot.position = project(point)
                dot.fillColor = color
                dot.strokeColor = .black
                root.addChild(dot)
            }
        }
        return root
    }

    @MainActor
    private func attachSheets(image: CGImage, name: String) throws {
        func png(_ image: UIImage, _ suffix: String) throws {
            let data = try XCTUnwrap(image.pngData())
            let attachment = XCTAttachment(data: data, uniformTypeIdentifier: "public.png")
            attachment.name = name + suffix
            attachment.lifetime = .keepAlways
            add(attachment)
        }
        try png(UIImage(cgImage: image), "-native")
        let format = UIGraphicsImageRendererFormat()
        format.scale = 1
        let half = UIGraphicsImageRenderer(size: CGSize(width: image.width / 2, height: image.height / 2), format: format).image { _ in
            UIImage(cgImage: image).draw(in: CGRect(x: 0, y: 0, width: image.width / 2, height: image.height / 2))
        }
        try png(half, "-half")
        let filter = try XCTUnwrap(CIFilter(name: "CIColorControls"))
        filter.setValue(CIImage(cgImage: image), forKey: kCIInputImageKey)
        filter.setValue(0, forKey: kCIInputSaturationKey)
        let output = try XCTUnwrap(filter.outputImage)
        let gray = try XCTUnwrap(CIContext().createCGImage(output, from: output.extent))
        try png(UIImage(cgImage: gray), "-grayscale")
    }

    private func attach(data: Data, name: String) {
        let attachment = XCTAttachment(data: data, uniformTypeIdentifier: "public.json")
        attachment.name = name
        attachment.lifetime = .keepAlways
        add(attachment)
    }
    #endif
}
