import SpriteKit
import UIKit
import XCTest
@testable import SSRuntime
@testable import SurveillanceCore

/// BP-001/BP-006 evidence capture, not visual acceptance or a performance test.
/// Uses the shipping GameScene/renderer/HUD. Images remain in the test result.
final class BenchmarkCaptureTests: XCTestCase {
    @MainActor
    func testCaptureReactionTurningReadability() throws {
        let view = SKView(frame: CGRect(x: 0, y: 0, width: 704, height: 326))
        view.isPaused = true
        let scene = SKScene(size: view.bounds.size)
        scene.anchorPoint = CGPoint(x: 0.5, y: 0.5)
        scene.backgroundColor = UIColor(white: 0.22, alpha: 1)
        view.presentScene(scene)
        defer { view.presentScene(nil) }
        let state = try Simulation.make(seed: 1).state
        let crop = CGRect(x: -352, y: -163, width: 704, height: 326)
        for reduced in [false, true] {
            let renderer = WorldRenderer()
            scene.addChild(renderer.root)
            var tracker = ReactionClipTracker(catalog: try ClipCatalog.bundled())
            tracker.ingest(TickResult(tick: 100, events: [AuthoritativeEvent(
                tick: 100, phase: 10, type: .playerDamaged, primary: EntityID(1), insertion: 0)],
                digest: "", outcome: .playing), previousEnemies: [], currentEnemies: [], playerDirection: "w")
            XCTAssertEqual(tracker.playerReaction?.endTick, 109)
            for tick in UInt64(100)...110 {
                var snap = PresentationSnapshot(state)
                snap.tick = tick
                snap.player.x = 0
                snap.player.y = Int(tick - 100) * 4 - 20
                snap.playerDirection = tick == 100 ? "w" : "n"
                snap.playerClipId = "player_move"
                snap.enemies = []; snap.projectiles = []; snap.telegraphs = []; snap.mines = []
                snap.cameras = []; snap.captainHousings = []; snap.captainField = nil
                snap.patrolCones = []; snap.spawnSockets = []; snap.solids = []; snap.solidIds = []
                tracker.apply(to: &snap)
                renderer.render(snap, reducedMotion: reduced)
                XCTAssertEqual(snap.playerReactionClipId != nil, tick < 109)
                if tick < 109 {
                    XCTAssertEqual(snap.playerReactionOccurrence?.direction, "w")
                }
                let texture = try XCTUnwrap(view.texture(from: scene, crop: crop))
                let attachment = XCTAttachment(image: UIImage(cgImage: texture.cgImage()))
                attachment.name = "BP003-reaction-turn-\(reduced ? "reduced" : "normal")-\(tick)"
                attachment.lifetime = .keepAlways
                add(attachment)
            }
            renderer.root.removeFromParent()
        }
        let evidence = XCTAttachment(string: """
        BP-003 native-size event-facing comparison; not benchmark art acceptance.
        Actual WorldRenderer, bundled v1 player textures, ReactionClipTracker.
        704x326-point SKView, backing scale \(view.contentScaleFactor).
        Synthetic presentation path: player moves north 4 units/tick; live facing
        turns west→north at tick 101. Hurt occurrence begins west at tick 100,
        selects three frames at 20 fps, expires exclusively at tick 109.
        Normal and Reduced Motion captured for every tick 100...110.
        SKView is paused: event frames are tick-sampled; fallback locomotion
        shows its initial/settled pose, not action-time animation evidence.
        No authoritative collision, attack or damage scenario is asserted.
        """)
        evidence.name = "BP003-reaction-turn-record"
        evidence.lifetime = .keepAlways
        add(evidence)
    }

    @MainActor
    func testExactAndVariableTimingReachSpriteKit() throws {
        let image = UIGraphicsImageRenderer(size: CGSize(width: 2, height: 2)).image { context in
            UIColor.white.setFill()
            context.fill(CGRect(x: 0, y: 0, width: 2, height: 2))
        }
        let texture = SKTexture(image: image)
        let elite = try ClipTiming(unitsPerSecond: 112, frameUnits: Array(repeating: 3, count: 16))
        let eliteAction = try XCTUnwrap(SpriteLibrary.sequence(textures: Array(repeating: texture, count: 16), timing: elite))
        // #120: SpriteKit stores this action duration at Float precision.
        XCTAssertEqual(eliteAction.duration, Double(Float(3.0 / 7.0)))
        let variable = try ClipTiming(unitsPerSecond: 24, frameUnits: [1, 2, 1, 2])
        let variableAction = try XCTUnwrap(SpriteLibrary.sequence(textures: Array(repeating: texture, count: 4), timing: variable))
        XCTAssertEqual(variableAction.duration, 0.25)
        XCTAssertNil(SpriteLibrary.sequence(textures: [texture], timing: variable))
    }

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
        var art = BenchmarkReviewArt(
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
        art.cameraStates = [3: try texture("camera-state-intact"), 2: try texture("camera-state-damaged"),
                            1: try texture("camera-state-critical"), 0: try texture("camera-state-destroyed")]
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
        overlay.removeFromParent()
        for integrity in stride(from: 3, through: 0, by: -1) {
            snap.cameras[0].integrity = integrity
            snap.cameras[0].fieldVisible = integrity > 0
            scene.renderBenchmark(snapshot: snap, art: art, center: center)
            let sprite = try XCTUnwrap(scene.childNode(withName: "//sprite-camera-\(snap.cameras[0].id.raw)") as? SKSpriteNode)
            XCTAssertTrue(sprite.texture === art.cameraStates[integrity])
            XCTAssertEqual(sprite.position, CGPoint(x: snap.cameras[0].x, y: snap.cameras[0].y))
            XCTAssertNil(scene.childNode(withName: "//housing-\(snap.cameras[0].id.raw)"))
            try capture("BP004-candidate-integrity-\(integrity)")
        }
        // BP-007 review experiment only: transform ground geometry and roots,
        // preserving upright sprite form. This is not a production projection API.
        for zoom in [CGFloat(1), CGFloat(2).squareRoot()] {
            snap.cameras[0].integrity = 3
            snap.cameras[0].fieldVisible = true
            scene.renderBenchmark(snapshot: snap, art: art, center: center)
            let billboardNames = ["sprite-player", "sprite-camera-\(snap.cameras[0].id.raw)",
                                  "benchmark-building", "benchmark-prop-0", "benchmark-prop-1"]
            let billboards = try billboardNames.map { try XCTUnwrap(scene.childNode(withName: "//" + $0)) }
            let originals = try billboards.map { node in
                (node, try XCTUnwrap(node.parent), node.position, node.xScale, node.yScale, node.zPosition)
            }
            func projected(_ p: CGPoint) -> CGPoint {
                let x = p.x - center.x, y = p.y - center.y
                let r = CGFloat(0.5).squareRoot()
                return CGPoint(x: center.x + zoom * r * (x - y),
                               y: center.y + zoom * r * (x + y) / 2)
            }
            for (node, parent, position, _, _, _) in originals {
                let world = scene.convert(position, from: parent)
                var z = node.zPosition
                var ancestor: SKNode? = parent
                while let a = ancestor, a !== scene { z += a.zPosition; ancestor = a.parent }
                node.removeFromParent()
                node.position = projected(world)
                node.xScale *= zoom; node.yScale *= zoom
                node.zPosition = z
                scene.addChild(node)
            }
            let uprightSet = Set(billboards.map(ObjectIdentifier.init))
            let world = scene.children.filter { $0 !== camera && !uprightSet.contains(ObjectIdentifier($0)) }
            let squash = SKNode(), rotation = SKNode(), translation = SKNode()
            squash.position = center; squash.xScale = zoom; squash.yScale = zoom / 2
            rotation.zRotation = .pi / 4
            translation.position = CGPoint(x: -center.x, y: -center.y)
            scene.addChild(squash); squash.addChild(rotation); rotation.addChild(translation)
            for node in world { node.removeFromParent(); translation.addChild(node) }
            let probe = CGPoint(x: x + 64, y: y - 64)
            let converted = translation.convert(probe, to: scene)
            XCTAssertEqual(converted.x, projected(probe).x, accuracy: 0.0001)
            XCTAssertEqual(converted.y, projected(probe).y, accuracy: 0.0001)
            let player = try XCTUnwrap(billboards.first as? SKSpriteNode)
            let expectedSize = CGFloat(Float(64 * zoom))
            XCTAssertEqual(player.size, CGSize(width: expectedSize, height: expectedSize))
            XCTAssertEqual(player.xScale, player.yScale)
            XCTAssertEqual(camera.xScale, 1)
            let tag = zoom == 1 ? "unchanged-zoom" : "equal-area-zoom"
            try capture("BP007-projected-\(tag)")
            let footprintRoot = SKNode(), footprintRotation = SKNode(), footprintTranslation = SKNode()
            footprintRoot.position = center; footprintRoot.xScale = zoom; footprintRoot.yScale = zoom / 2
            footprintRoot.zPosition = 999
            footprintRotation.zRotation = .pi / 4
            footprintTranslation.position = CGPoint(x: -center.x, y: -center.y)
            scene.addChild(footprintRoot); footprintRoot.addChild(footprintRotation)
            footprintRotation.addChild(footprintTranslation)
            let footprint = SKShapeNode(rectOf: CGSize(width: box.halfSize.x * 2, height: box.halfSize.y * 2))
            footprint.position = CGPoint(x: x, y: y)
            footprint.strokeColor = .magenta; footprint.fillColor = .clear; footprint.lineWidth = 1
            footprintTranslation.addChild(footprint)
            try capture("BP007-projected-\(tag)-geometry")
            // New constrained wall source: register the visible near corner to
            // the projected minimum-x/minimum-y world corner, never to the apron.
            let building = try XCTUnwrap(billboards[2] as? SKSpriteNode)
            building.texture = try texture("building-constrained")
            building.xScale = 1; building.yScale = 1
            let canvas = CGFloat(1254) * (CGFloat(128) * CGFloat(2).squareRoot() / 934) * zoom
            building.size = CGSize(width: canvas, height: canvas)
            building.anchorPoint = CGPoint(x: CGFloat(653) / 1254, y: 1 - CGFloat(1152) / 1254)
            building.position = projected(CGPoint(x: x - 64, y: y - 64))
            try capture("BP007-constrained-wall-\(tag)-geometry")
            footprintRoot.isHidden = true
            try capture("BP007-constrained-wall-\(tag)")
            if zoom == 1 {
                // Actual fixed-point slide solver, isolated to this authored solid.
                // These are contact probes, not a full encounter or animation proof.
                let probes: [(String, Int, Int, Int16, Int16)] = [
                    ("west", -130, 0, 32767, 0), ("east", 130, 0, -32767, 0),
                    ("south", 0, -130, 0, 32767), ("north", 0, 130, 0, -32767),
                    ("near-corner", -130, -130, 32767, 32767),
                    ("far-corner", 130, 130, -32767, -32767)
                ]
                // View direction for this candidate is toward decreasing world X/Y.
                // Intersect that ground ray with the box, then require visual overlap.
                // This bounded review classifier is not used by the shipping renderer.
                func isOccluded(_ point: CGPoint) -> Bool {
                    let enter = max(0, point.x - CGFloat(box.maxX), point.y - CGFloat(box.maxY))
                    let leave = min(point.x - CGFloat(box.minX), point.y - CGFloat(box.minY))
                    return leave > enter && player.frame.intersects(building.frame)
                }
                let playerStart = player.position
                let shadow = scene.childNode(withName: "//shadow-player")
                let shadowStart = shadow?.position
                var evidence = ["Isolated movement/collision probes. Radius18; existing obstacle unchanged. Neutral south art; no animation."]
                for (label, dx, dy, mx, my) in probes {
                    var position = VecI(x: x + dx, y: y + dy).asQ8
                    for tick in 1...40 {
                        let command = PlayerCommand(tick: UInt64(tick), moveX: mx, moveY: my, dodgePressed: false)
                        let delta = Movement.displacement(from: command, dodgeActive: false, ghostStep: false)
                        position = Collision.slideCircle(from: position, delta: delta, radius: PlayerBody.radiusUnits,
                            bounds: AABB(center: box.center, halfSize: VecI(x: 512, y: 512)), solids: [(id: id, box: box)])
                        XCTAssertFalse(Circle(center: position, radiusUnits: PlayerBody.radiusUnits).penetrates(box))
                        evidence.append("\(label),\(tick),\(position.x.raw),\(position.y.raw)")
                    }
                    // Four straight approaches end at exact radius contact.
                    if dy == 0 { XCTAssertEqual(abs(position.x.raw - Int64(x) * Q8.scale), Int64(82) * Q8.scale) }
                    if dx == 0 { XCTAssertEqual(abs(position.y.raw - Int64(y) * Q8.scale), Int64(82) * Q8.scale) }
                    let point = CGPoint(x: CGFloat(position.x.raw) / CGFloat(Q8.scale),
                                        y: CGFloat(position.y.raw) / CGFloat(Q8.scale))
                    player.position = projected(point)
                    if let shadowStart {
                        shadow?.position = CGPoint(x: point.x + shadowStart.x - CGFloat(snap.player.x),
                                                   y: point.y + shadowStart.y - CGFloat(snap.player.y))
                    }
                    footprintRoot.isHidden = true
                    try capture("BP005-contact-\(label)")
                    let radius = SKShapeNode(circleOfRadius: CGFloat(PlayerBody.radiusUnits))
                    radius.position = point; radius.strokeColor = .cyan; radius.fillColor = .clear
                    radius.lineWidth = 1
                    footprintTranslation.addChild(radius)
                    footprintRoot.isHidden = false
                    try capture("BP005-contact-\(label)-geometry")
                    radius.removeFromParent()
                    let occluded = isOccluded(point)
                    XCTAssertEqual(occluded, ["east", "north", "far-corner"].contains(label))
                    if occluded {
                        let priorZ = player.zPosition
                        let shadowWasHidden = shadow?.isHidden
                        player.zPosition = building.zPosition - 0.1
                        shadow?.isHidden = true
                        footprintRoot.isHidden = true
                        try capture("BP005-opaque-depth-\(label)")
                        building.alpha = 0.35
                        try capture("BP005-faded-depth-\(label)")
                        // BP-009: compare static projected ground cues with fading.
                        // Review parameters only; not the chosen shipping style.
                        footprint.strokeColor = SKColor(white: 0.85, alpha: 1)
                        footprint.lineWidth = 1.5
                        footprint.fillColor = SKColor(white: 0.1, alpha: 0.16)
                        let contactBacking = SKShapeNode(circleOfRadius: CGFloat(PlayerBody.radiusUnits))
                        contactBacking.position = point
                        contactBacking.fillColor = .clear
                        contactBacking.strokeColor = SKColor(white: 0.08, alpha: 1)
                        contactBacking.lineWidth = 3
                        let contactRing = SKShapeNode(circleOfRadius: CGFloat(PlayerBody.radiusUnits))
                        contactRing.fillColor = .clear
                        contactRing.strokeColor = SKColor(white: 0.95, alpha: 1)
                        contactRing.lineWidth = 1.25
                        contactBacking.addChild(contactRing)
                        footprintTranslation.addChild(contactBacking)
                        footprintRoot.isHidden = false
                        XCTAssertFalse(contactBacking.hasActions())
                        XCTAssertFalse(contactRing.hasActions())
                        try capture("BP009-ground-cue-\(label)")
                        footprint.strokeColor = SKColor(white: 0.18, alpha: 0.8)
                        footprint.lineWidth = 1
                        footprint.fillColor = SKColor(white: 0.08, alpha: 0.22)
                        try capture("BP009-muted-ground-cue-\(label)")
                        contactBacking.removeFromParent()
                        footprintRoot.isHidden = true
                        footprint.strokeColor = .magenta
                        footprint.lineWidth = 1; footprint.fillColor = .clear
                        building.alpha = 1
                        player.zPosition = priorZ
                        if let shadowWasHidden { shadow?.isHidden = shadowWasHidden }
                    }
                }
                // Continuous solver movement around all four sides, with automatic
                // treatment entry/exit. Sample every ten ticks for review playback.
                let normalZ = player.zPosition
                var position = VecI(x: x - 100, y: y - 100).asQ8
                let start = position
                var previousOccluded = false, changes = 0, tick = 0
                let contact = SKShapeNode(circleOfRadius: CGFloat(PlayerBody.radiusUnits))
                contact.fillColor = .clear; contact.strokeColor = SKColor(white: 0.9, alpha: 1)
                contact.lineWidth = 1.25
                footprintTranslation.addChild(contact)
                footprint.strokeColor = SKColor(white: 0.18, alpha: 0.8)
                footprint.lineWidth = 1; footprint.fillColor = SKColor(white: 0.08, alpha: 0.22)
                for (mx, my) in [(Int16(32767), Int16(0)), (0, 32767), (-32767, 0), (0, -32767)] {
                    for _ in 0..<50 {
                        tick += 1
                        let command = PlayerCommand(tick: UInt64(tick), moveX: mx, moveY: my, dodgePressed: false)
                        position = Collision.slideCircle(from: position,
                            delta: Movement.displacement(from: command, dodgeActive: false, ghostStep: false),
                            radius: PlayerBody.radiusUnits,
                            bounds: AABB(center: box.center, halfSize: VecI(x: 512, y: 512)), solids: [(id: id, box: box)])
                        XCTAssertFalse(Circle(center: position, radiusUnits: PlayerBody.radiusUnits).penetrates(box))
                        let point = CGPoint(x: CGFloat(position.x.raw) / CGFloat(Q8.scale), y: CGFloat(position.y.raw) / CGFloat(Q8.scale))
                        player.position = projected(point)
                        let occluded = isOccluded(point)
                        if previousOccluded != occluded { changes += 1 }
                        previousOccluded = occluded
                        building.alpha = occluded ? 0.35 : 1
                        player.zPosition = occluded ? building.zPosition - 0.1 : normalZ
                        footprintRoot.isHidden = !occluded; contact.position = point
                        shadow?.isHidden = occluded
                        if let shadowStart { shadow?.position = CGPoint(x: point.x + shadowStart.x - CGFloat(snap.player.x), y: point.y + shadowStart.y - CGFloat(snap.player.y)) }
                        evidence.append("perimeter,\(tick),\(position.x.raw),\(position.y.raw),occluded=\(occluded)")
                        if tick % 10 == 0 { try capture("BP009-perimeter-\(tick)") }
                    }
                }
                XCTAssertEqual(position, start)
                XCTAssertEqual(changes, 2)
                XCTAssertFalse(previousOccluded)
                XCTAssertEqual(building.alpha, 1)
                contact.removeFromParent(); footprintRoot.isHidden = true
                footprint.strokeColor = .magenta; footprint.lineWidth = 1; footprint.fillColor = .clear
                shadow?.isHidden = false
                player.position = playerStart
                if let shadowStart { shadow?.position = shadowStart }
                let probeRecord = XCTAttachment(string: evidence.joined(separator: "\n"))
                probeRecord.name = "BP005-contact-probes-q8"
                probeRecord.lifetime = .keepAlways; add(probeRecord)
            }
            footprintRoot.removeFromParent()
            for node in world { node.removeFromParent(); scene.addChild(node) }
            for (node, parent, position, sx, sy, z) in originals {
                node.removeFromParent(); parent.addChild(node)
                node.position = position; node.xScale = sx; node.yScale = sy; node.zPosition = z
            }
            squash.removeFromParent()
        }
        let record = XCTAttachment(string: """
        Composition fixture, not a legal encounter or animation acceptance.
        Runtime renderer and HUD; test-only candidate textures. 704x326 logical viewport.
        Existing solid \(id) AABB is unchanged: \(box). Other solids omitted for isolated review.
        Player, camera and props are explicitly placed presentation samples; simulation is unchanged.
        One complete camera node. Candidate settled state captures at integrity3/2/1/0.
        These are four still states, not the six required animated clip deliveries.
        No locomotion animation claimed.
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
