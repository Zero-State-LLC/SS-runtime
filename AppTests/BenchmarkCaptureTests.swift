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
    private func captureProjectedLegalEncounter(scene: SKScene, view: SKView,
        snap: PresentationSnapshot, zoom: CGFloat, label: String, prefix: String = "BP010-legal", treatment: String = "control",
        framing: String = "legacy", arena: CGRect? = nil) throws {
        let camera = try XCTUnwrap(scene.camera)
        let originalCamera = camera.position
        var hudExclusions: [CGRect] = []
        var safeRegion: CGRect?
        defer { camera.position = originalCamera }
        if framing != "legacy" {
            let bounds = try XCTUnwrap(arena)
            let player = try XCTUnwrap(scene.childNode(withName: "//sprite-player") as? SKSpriteNode)
            let root = scene.convert(player.position, from: try XCTUnwrap(player.parent))
            let viewport = CGSize(width: 704, height: 326)
            if framing == "contained" {
                camera.position = try XCTUnwrap(BenchmarkProjectionGeometry.containedCenter(
                    desired: originalCamera, bounds: bounds, viewport: viewport, magnification: zoom))
            } else {
                let canvas = CGRect(x: -player.anchorPoint.x * player.size.width,
                    y: -player.anchorPoint.y * player.size.height,
                    width: player.size.width, height: player.size.height)
                if framing == "hud-safe" {
                    // GameScene mounts its HUD at z=1000 on the camera. Measure
                    // rendered nodes, including labels, rather than copying HUD constants.
                    let hudRoots = camera.children.filter { $0.zPosition == 1000 }
                    XCTAssertEqual(hudRoots.count, 1)
                    let hudRoot = try XCTUnwrap(hudRoots.first)
                    hudExclusions = hudRoot.children.filter { !$0.isHidden && $0.alpha > 0 }.compactMap {
                        let frame = $0.calculateAccumulatedFrame()
                        guard !frame.isNull, !frame.isInfinite, frame.width > 0, frame.height > 0 else { return nil }
                        let a = hudRoot.convert(CGPoint(x: frame.minX, y: frame.minY), to: camera)
                        let b = hudRoot.convert(CGPoint(x: frame.maxX, y: frame.maxY), to: camera)
                        return CGRect(x: a.x, y: a.y, width: b.x-a.x, height: b.y-a.y)
                    }
                    XCTAssertFalse(hudExclusions.isEmpty)
                    safeRegion = try XCTUnwrap(BenchmarkProjectionGeometry.unobstructedRegion(
                        viewport: CGRect(x: -352, y: -163, width: 704, height: 326),
                        exclusions: hudExclusions,
                        minimumSize: CGSize(width: canvas.width * zoom, height: canvas.height * zoom)))
                }
                camera.position = try XCTUnwrap(BenchmarkProjectionGeometry.playerVisibleCenter(
                    desired: originalCamera, bounds: bounds, viewport: viewport,
                    magnification: zoom, player: root, canvas: canvas, safeRegion: safeRegion))
            }
        }
        let center = camera.position
        let crop = CGRect(x: center.x - 352, y: center.y - 163, width: 704, height: 326)
        var actors: [SKSpriteNode] = []
        scene.enumerateChildNodes(withName: "//sprite-*") { node, _ in
            if let sprite = node as? SKSpriteNode { actors.append(sprite) }
        }
        XCTAssertFalse(actors.isEmpty)
        scene.enumerateChildNodes(withName: "//environment-upright-*") { node, _ in
            if let sprite = node as? SKSpriteNode { actors.append(sprite) }
        }
        XCTAssertEqual(EnvironmentTextures.projectionPlane(for: "env_prop_rail_strip"), .ground)
        XCTAssertEqual(EnvironmentTextures.projectionPlane(for: "env_prop_utility_covers"), .ground)
        XCTAssertEqual(EnvironmentTextures.projectionPlane(for: "env_prop_street_tree"), .upright)
        XCTAssertEqual(EnvironmentTextures.projectionPlane(for: "env_motif_repair"), .unresolved)
        XCTAssertEqual(EnvironmentTextures.projectionPlane(for: "unknown"), .unresolved)
        // BP-005 source revision: registered slab base, never a collision edit.
        let building = try XCTUnwrap(actors.first {
            $0.name == "environment-upright-env_solid_07_service_yard_b"
        })
        let buildingIndex = try XCTUnwrap(snap.solidIds.firstIndex(of: "solid-07-service-yard-b"))
        let box = snap.solids[buildingIndex]
        let originalBuilding = (building.texture, building.size, building.anchorPoint, building.position)
        let originalBuildingAlpha = building.alpha
        defer {
            building.texture = originalBuilding.0; building.size = originalBuilding.1
            building.anchorPoint = originalBuilding.2; building.position = originalBuilding.3
            building.alpha = originalBuildingAlpha
        }
        let sourceURL = try XCTUnwrap(Bundle(for: Self.self).url(
            forResource: "service-building-v3-registered", withExtension: "png"))
        let sourceImage = try XCTUnwrap(UIImage(contentsOfFile: sourceURL.path))
        XCTAssertEqual(sourceImage.cgImage?.width, 1024)
        XCTAssertEqual(sourceImage.cgImage?.height, 1024)
        building.texture = SKTexture(image: sourceImage)
        building.texture?.filteringMode = .linear
        building.size = CGSize(width: 512, height: 512)
        building.anchorPoint = CGPoint(x: 419.745 / 1024, y: 1 - 858.392 / 1024)
        let front = CGPoint(x: box.center.x - box.halfSize.x, y: box.center.y - box.halfSize.y)
        building.position = try XCTUnwrap(building.parent).convert(front, from: scene)
        let saved = try actors.map { ($0, try XCTUnwrap($0.parent), $0.position, $0.zPosition) }
        func project(_ point: CGPoint) -> CGPoint {
            let x = point.x - center.x, y = point.y - center.y, r = CGFloat(0.5).squareRoot()
            return CGPoint(x: center.x + r * (x-y), y: center.y + r * (x+y)/2)
        }
        for (node, parent, position, _) in saved {
            let point = scene.convert(position, from: parent)
            var depth = node.zPosition, ancestor: SKNode? = parent
            while let a = ancestor, a !== scene { depth += a.zPosition; ancestor = a.parent }
            node.removeFromParent(); node.position = project(point); node.zPosition = depth; scene.addChild(node)
        }
        // Check the actual SpriteKit source-to-scene mapping against independent
        // authoritative corners. This proves placement, not visual contact quality.
        for (pixel, corner) in [
            (CGPoint(x: 148.216, y: 722.627), CGPoint(x: box.center.x - box.halfSize.x, y: box.center.y + box.halfSize.y)),
            (CGPoint(x: 419.745, y: 858.392), front),
            (CGPoint(x: 781.784, y: 677.373), CGPoint(x: box.center.x + box.halfSize.x, y: box.center.y - box.halfSize.y))
        ] {
            let local = CGPoint(x: (pixel.x / 1024 - building.anchorPoint.x) * building.size.width,
                                y: (1 - pixel.y / 1024 - building.anchorPoint.y) * building.size.height)
            let actual = building.convert(local, to: scene), expected = project(corner)
            XCTAssertEqual(actual.x, expected.x, accuracy: 0.002)
            XCTAssertEqual(actual.y, expected.y, accuracy: 0.002)
        }
        // BP-009 bounded comparison, not a production occlusion classifier.
        let player = try XCTUnwrap(actors.first { $0.name == "sprite-player" })
        let playerSaved = try XCTUnwrap(saved.first { $0.0 === player })
        let playerGround = scene.convert(playerSaved.2, from: playerSaved.1)
        let enter = max(0, playerGround.x - CGFloat(box.maxX), playerGround.y - CGFloat(box.maxY))
        let leave = min(playerGround.x - CGFloat(box.minX), playerGround.y - CGFloat(box.minY))
        let occluded = leave > enter && player.frame.intersects(building.frame)
        let cue = SKNode(); cue.zPosition = 10_000
        scene.addChild(cue)
        defer { cue.removeFromParent() }
        if treatment != "control" && occluded {
            player.zPosition = building.zPosition - 0.1
            if treatment == "faded" || treatment == "ground-cue" { building.alpha = 0.35 }
            if treatment == "ground-cue" {
                let outline = SKShapeNode(rectOf: CGSize(width: box.halfSize.x * 2, height: box.halfSize.y * 2))
                outline.position = CGPoint(x: box.center.x, y: box.center.y)
                outline.fillColor = SKColor(white: 0.08, alpha: 0.22)
                outline.strokeColor = SKColor(white: 0.18, alpha: 0.8); outline.lineWidth = 1
                cue.addChild(outline)
                let ring = SKShapeNode(circleOfRadius: CGFloat(PlayerBody.radiusUnits))
                ring.position = playerGround; ring.fillColor = .clear
                ring.strokeColor = SKColor(white: 0.9, alpha: 1); ring.lineWidth = 1.25
                cue.addChild(ring)
            }
        }
        let actorIDs = Set(actors.map(ObjectIdentifier.init))
        let ground = scene.children.filter { $0 !== camera && !actorIDs.contains(ObjectIdentifier($0)) }
        let scale = SKNode(), rotate = SKNode(), translate = SKNode(), world = SKNode()
        scale.position = center; scale.yScale = 0.5; rotate.zRotation = .pi/4
        translate.position = CGPoint(x: -center.x, y: -center.y)
        scene.addChild(world); world.addChild(scale); scale.addChild(rotate); rotate.addChild(translate)
        for node in ground { node.removeFromParent(); translate.addChild(node) }
        for node in actors { node.removeFromParent(); world.addChild(node) }
        world.setScale(zoom)
        let offset: CGFloat = zoom == 1 || framing != "legacy" ? 0 : 1
        world.position = CGPoint(x: center.x - (center.x + 35 * offset) * zoom,
                                 y: center.y - (center.y + 25 * offset) * zoom)
        defer {
            for node in ground { node.removeFromParent(); scene.addChild(node) }
            for (node, parent, position, z) in saved {
                node.removeFromParent(); node.position = position; node.zPosition = z; parent.addChild(node)
            }
            world.removeFromParent()
        }
        var visibility: [[String: Any]] = []
        for actor in actors {
            let frame = actor.frame
            let a = world.convert(CGPoint(x: frame.minX, y: frame.minY), to: scene)
            let b = world.convert(CGPoint(x: frame.maxX, y: frame.maxY), to: scene)
            let rect = CGRect(x: a.x, y: a.y, width: b.x-a.x, height: b.y-a.y)
            if ["player-visible", "hud-safe"].contains(framing) && actor.name == "sprite-player" {
                XCTAssertTrue(crop.insetBy(dx: -0.002, dy: -0.002).contains(rect), "Float transform precision only")
            }
            if framing == "hud-safe" && actor.name == "sprite-player" {
                let local = rect.offsetBy(dx: -center.x, dy: -center.y)
                XCTAssertTrue(try XCTUnwrap(safeRegion).insetBy(dx: -0.002, dy: -0.002).contains(local))
                for exclusion in hudExclusions {
                    let overlap = local.intersection(exclusion)
                    XCTAssertTrue(overlap.isNull || overlap.width <= 0.002 || overlap.height <= 0.002)
                }
            }
            visibility.append(["name": actor.name ?? "unnamed", "intersects": crop.intersects(rect),
                "contained": crop.contains(rect), "bounds": [rect.minX, rect.minY, rect.width, rect.height]])
        }
        let projectiles: [[String: Any]] = snap.projectiles.map {
            let point = translate.convert(CGPoint(x: $0.x, y: $0.y), to: scene)
            return ["id": $0.id.raw, "hostile": $0.hostile, "visibleOrigin": crop.contains(point)]
        }
        XCTAssertEqual(camera.xScale, 1)
        XCTAssertEqual(actors.count, saved.count)
        let texture = try XCTUnwrap(view.texture(from: scene, crop: crop))
        let image = XCTAttachment(image: UIImage(cgImage: texture.cgImage()))
        image.name = "\(prefix)-projected-\(Int(zoom*100))-\(label)"; image.lifetime = .keepAlways; add(image)
        let data = try JSONSerialization.data(withJSONObject: ["zoom": zoom, "actors": visibility,
            "projectiles": projectiles, "enemies": snap.enemies.count, "cameras": snap.cameras.count,
            "tick": snap.tick, "occlusionTreatment": treatment, "occlusionCandidate": occluded,
            "framing": framing, "worldFocus": [center.x,center.y],
            "hudExclusions": hudExclusions.map { [$0.minX,$0.minY,$0.width,$0.height] },
            "safeRegion": safeRegion.map { [$0.minX,$0.minY,$0.width,$0.height] } ?? []], options: [.sortedKeys, .prettyPrinted])
        let record = XCTAttachment(data: data, uniformTypeIdentifier: "public.json")
        record.name = "\(prefix)-visibility-\(Int(zoom*100))-\(label)"; record.lifetime = .keepAlways; add(record)
    }

    @MainActor
    func testRegisteredServiceBuildingContacts() throws {
        let state = try Simulation.make(seed: 1).state
        var snap = PresentationSnapshot(state)
        let id = "solid-07-service-yard-b"
        let index = try XCTUnwrap(snap.solidIds.firstIndex(of: id))
        let box = snap.solids[index]
        snap.solids = [box]; snap.solidIds = [id]
        snap.enemies = []; snap.projectiles = []; snap.telegraphs = []; snap.mines = []
        snap.cameras = []; snap.captainHousings = []; snap.captainField = nil
        snap.patrolCones = []; snap.spawnSockets = []
        let view = SKView(frame: CGRect(x: 0, y: 0, width: 704, height: 326))
        view.isPaused = true
        let scene = SKScene(size: view.bounds.size)
        scene.backgroundColor = .darkGray
        let camera = SKCameraNode()
        camera.position = CGPoint(x: box.center.x, y: box.center.y)
        scene.addChild(camera); scene.camera = camera
        view.presentScene(scene)
        defer { view.presentScene(nil) }
        let renderer = WorldRenderer(); scene.addChild(renderer.root)
        let url = try XCTUnwrap(Bundle(for: Self.self).url(forResource: "painted-player-south", withExtension: "png"))
        let neutral = SKTexture(image: try XCTUnwrap(UIImage(contentsOfFile: url.path)))
        neutral.filteringMode = .linear
        let probes: [(String, Int, Int, Int16, Int16)] = [
            ("west", -194, 0, 32767, 0), ("east", 194, 0, -32767, 0),
            ("south", 0, -162, 0, 32767), ("north", 0, 162, 0, -32767),
            ("near-corner", -194, -162, 32767, 32767),
            ("far-corner", 194, 162, -32767, -32767)
        ]
        var rows = ["probe,tick,xQ8,yQ8"]
        for (label, dx, dy, mx, my) in probes {
            var point = VecI(x: box.center.x + dx, y: box.center.y + dy).asQ8
            for tick in 1...40 {
                let command = PlayerCommand(tick: UInt64(tick), moveX: mx, moveY: my, dodgePressed: false)
                point = Collision.slideCircle(from: point,
                    delta: Movement.displacement(from: command, dodgeActive: false, ghostStep: false),
                    radius: PlayerBody.radiusUnits,
                    bounds: AABB(center: box.center, halfSize: VecI(x: 512, y: 512)),
                    solids: [(id: id, box: box)])
                XCTAssertFalse(Circle(center: point, radiusUnits: PlayerBody.radiusUnits).penetrates(box))
                rows.append("\(label),\(tick),\(point.x.raw),\(point.y.raw)")
            }
            if dy == 0 {
                XCTAssertEqual(abs(point.x.raw - Int64(box.center.x) * Q8.scale),
                               Int64(box.halfSize.x + PlayerBody.radiusUnits) * Q8.scale)
            }
            if dx == 0 {
                XCTAssertEqual(abs(point.y.raw - Int64(box.center.y) * Q8.scale),
                               Int64(box.halfSize.y + PlayerBody.radiusUnits) * Q8.scale)
            }
            snap.player.x = Int(point.x.raw / Q8.scale); snap.player.y = Int(point.y.raw / Q8.scale)
            for reduced in [false, true] {
                renderer.render(snap, reducedMotion: reduced)
                let player = try XCTUnwrap(scene.childNode(withName: "//sprite-player") as? SKSpriteNode)
                player.removeAllActions(); player.texture = neutral
                player.size = CGSize(width: 64, height: 64); player.anchorPoint = CGPoint(x: 0.5, y: 0.125)
                // Preserve Q8 solver position for this placement diagnostic.
                player.position = CGPoint(x: CGFloat(point.x.raw) / CGFloat(Q8.scale),
                                          y: CGFloat(point.y.raw) / CGFloat(Q8.scale))
                let overlay = SKNode(); overlay.zPosition = 10_000
                let boundary = SKShapeNode(rectOf: CGSize(width: box.halfSize.x * 2, height: box.halfSize.y * 2))
                boundary.position = CGPoint(x: box.center.x, y: box.center.y)
                boundary.fillColor = .clear; boundary.strokeColor = .magenta; boundary.lineWidth = 1
                overlay.addChild(boundary)
                let body = SKShapeNode(circleOfRadius: CGFloat(PlayerBody.radiusUnits))
                body.position = player.position; body.fillColor = .clear; body.strokeColor = .cyan; body.lineWidth = 1
                overlay.addChild(body); scene.addChild(overlay)
                defer { overlay.removeFromParent() }
                for geometry in [false, true] {
                    overlay.isHidden = !geometry
                    try captureProjectedLegalEncounter(scene: scene, view: view, snap: snap, zoom: 1,
                        label: "\(label)-reduced-\(reduced)-geometry-\(geometry)", prefix: "BP005-service-contact")
                }
                if ["north", "east", "far-corner"].contains(label) {
                    overlay.isHidden = true
                    for treatment in ["opaque", "faded", "ground-cue"] {
                        try captureProjectedLegalEncounter(scene: scene, view: view, snap: snap, zoom: 1,
                            label: "\(label)-reduced-\(reduced)-\(treatment)",
                            prefix: "BP005-service-contact", treatment: treatment)
                    }
                }
            }
        }
        XCTAssertEqual(state.digest(), try Simulation.make(seed: 1).state.digest())
        let record = XCTAttachment(string: "Isolated solver/renderer contact study; neutral pose, no full simulation or depth acceptance.\n" + rows.joined(separator: "\n"))
        record.name = "BP005-service-contact-q8"; record.lifetime = .keepAlways; add(record)
    }

    @MainActor
    func testCaptureCameraFieldsInReplayableEncounter() throws {
        let session = GameSession(seed: 1)
        session.audioSettings = .init(effectsEnabled: false, hapticsEnabled: false, musicEnabled: false)
        var pilot = try XCTUnwrap(DebugAutopilot(scenario: "run", arena: session.simulation.state.arena))
        var found = false
        for _ in 0..<6000 {
            let before = session.snapshot
            let command = pilot.command(before)
            session.moveX = command.moveX; session.moveY = command.moveY
            session.dodgePressed = command.dodge
            if before.upgradePending { session.pendingUpgradeChoice = pilot.upgradeChoice.selectionIndex }
            session.step()
            let snap = session.snapshot
            let nearby = snap.enemies.filter { abs($0.x - snap.player.x) < 300 && abs($0.y - snap.player.y) < 130 }
            let visibleAttack = snap.projectiles.contains { $0.hostile && abs($0.x - snap.player.x) < 300 && abs($0.y - snap.player.y) < 130 }
            let nearbyField = snap.cameras.contains { $0.fieldVisible && abs($0.x - snap.player.x) < 280 && abs($0.y - snap.player.y) < 120 }
            if nearby.count >= 2 && visibleAttack && nearbyField { found = true; break }
            if session.simulation.isTerminal { break }
        }
        XCTAssertTrue(found, "Pilot must reach an unedited encounter with nearby enemies, hostile projectile and Camera field")
        guard found else { return }
        XCTAssertFalse(session.scenarioSeeded)
        let view = SKView(frame: CGRect(x: 0, y: 0, width: 704, height: 326))
        view.isPaused = true
        let scene = GameScene(size: view.bounds.size, session: session)
        view.presentScene(scene)
        defer { view.presentScene(nil) }
        XCTAssertTrue(scene.installBenchmarkCameraFrames(try CameraPlaybackTests.candidateFrames()))
        scene.skipIntroIfRunning()
        scene.update(0)
        let snap = session.snapshot
        let player = try XCTUnwrap(scene.childNode(withName: "//sprite-player") as? SKSpriteNode)
        let directions = ["n": "north", "s": "south", "e": "east", "w": "west"]
        let facing = directions[snap.playerDirection] ?? snap.playerDirection
        let url = try XCTUnwrap(Bundle(for: Self.self).url(forResource: "painted-player-\(facing)", withExtension: "png"))
        let image = try XCTUnwrap(UIImage(contentsOfFile: url.path))
        let candidate = SKTexture(image: image)
        candidate.filteringMode = .linear
        let camera = try XCTUnwrap(scene.camera)
        let lower = scene.convert(CGPoint(x: -352, y: -163), from: camera)
        let upper = scene.convert(CGPoint(x: 352, y: 163), from: camera)
        let crop = CGRect(x: lower.x, y: lower.y, width: upper.x-lower.x, height: upper.y-lower.y)
        let digest = session.simulation.state.digest()
        for reduced in [false, true] {
            for style in WorldRenderer.BenchmarkFieldContrast.allCases {
                scene.setBenchmarkFieldContrast(style)
                scene.refreshBenchmarkPresentation(reducedMotion: reduced)
                player.removeAllActions(); player.texture = candidate
                player.size = CGSize(width: 64, height: 64)
                player.anchorPoint = CGPoint(x: 0.5, y: 0.125)
                scene.refreshBenchmarkOutlines(samplingScale: 3)
                XCTAssertEqual(session.simulation.state.digest(), digest)
                let texture = try XCTUnwrap(view.texture(from: scene, crop: crop))
                let attachment = XCTAttachment(image: UIImage(cgImage: texture.cgImage()))
                attachment.name = "BP010-field-encounter-\(style.rawValue)-reduced-\(reduced)"
                attachment.lifetime = .keepAlways; add(attachment)
                if style == .paired {
                    for zoom: CGFloat in [1, 1.25] {
                        try captureProjectedLegalEncounter(scene: scene, view: view, snap: snap,
                            zoom: zoom, label: "reduced-\(reduced)")
                        XCTAssertEqual(session.simulation.state.digest(), digest)
                        let bounds = session.simulation.state.arena.boundsUnits
                        let rect = CGRect(x: bounds.minX, y: bounds.minY,
                            width: bounds.maxX - bounds.minX, height: bounds.maxY - bounds.minY)
                        for framing in ["contained", "player-visible", "hud-safe"] {
                            try captureProjectedLegalEncounter(scene: scene, view: view, snap: snap,
                                zoom: zoom, label: "reduced-\(reduced)", prefix: "BP007-camera-\(framing)",
                                framing: framing, arena: rect)
                            XCTAssertEqual(session.simulation.state.digest(), digest)
                        }
                    }
                }

            }
        }
        let state = session.simulation.state
        // BP-004/BP-007: distinguish ground mount, targeting and field emission.
        // Diagnostic overlays only; never relocate authority to fit elevated art.
        var registration: [[String: Any]] = []
        let landmarks = SKNode()
        landmarks.zPosition = 10_000
        scene.addChild(landmarks)
        for device in state.cameras where abs(device.position.x - snap.player.x) < 280
            && abs(device.position.y - snap.player.y) < 120 {
            let mount = CGPoint(x: device.position.x, y: device.position.y)
            let field = CGPoint(x: Double(device.fieldOrigin.x.raw) / Double(Q8.scale),
                                y: Double(device.fieldOrigin.y.raw) / Double(Q8.scale))
            let target = CGPoint(x: Double(device.targetAnchor.x.raw) / Double(Q8.scale),
                                 y: Double(device.targetAnchor.y.raw) / Double(Q8.scale))
            let sprite = try XCTUnwrap(snap.cameras.first { $0.id == device.entityId })
            let key = CameraFieldGeometry.Key(camera: sprite, solids: snap.solids)
            XCTAssertEqual(key.originX, Double(field.x))
            XCTAssertEqual(key.originY, Double(field.y))
            for (label, point, color, offset) in [
                ("M", mount, SKColor.cyan, CGPoint(x: -18, y: -18)),
                ("T", target, SKColor.magenta, CGPoint(x: -20, y: 20)),
                ("F", field, SKColor.yellow, CGPoint(x: 20, y: 20))
            ] {
                let dot = SKShapeNode(circleOfRadius: 2)
                dot.position = point; dot.fillColor = color; dot.strokeColor = .black
                landmarks.addChild(dot)
                let text = SKLabelNode(fontNamed: "Menlo-Bold")
                text.text = label; text.fontSize = 10; text.fontColor = color
                text.position = CGPoint(x: point.x + offset.x, y: point.y + offset.y)
                landmarks.addChild(text)
                let path = CGMutablePath(); path.move(to: point); path.addLine(to: text.position)
                let leader = SKShapeNode(path: path)
                leader.strokeColor = color; leader.lineWidth = 0.5
                landmarks.addChild(leader)
            }
            registration.append([
                "socket": device.socketId, "headingMilliDegrees": device.headingMilliDegrees,
                "mount": [device.position.x, device.position.y],
                "fieldQ8": [device.fieldOrigin.x.raw, device.fieldOrigin.y.raw],
                "targetQ8": [device.targetAnchor.x.raw, device.targetAnchor.y.raw],
                "q8Scale": Q8.scale
            ])
        }
        XCTAssertFalse(registration.isEmpty)
        let alignmentTexture = try XCTUnwrap(view.texture(from: scene, crop: crop))
        let alignment = XCTAttachment(image: UIImage(cgImage: alignmentTexture.cgImage()))
        alignment.name = "BP010-field-encounter-registration"
        alignment.lifetime = .keepAlways; add(alignment)
        landmarks.removeFromParent()
        XCTAssertEqual(session.simulation.state.digest(), digest)
        let coordinates = XCTAttachment(data: try JSONSerialization.data(withJSONObject: registration, options: [.prettyPrinted, .sortedKeys]),
                                        uniformTypeIdentifier: "public.json")
        coordinates.name = "BP010-field-encounter-registration-coordinates"
        coordinates.lifetime = .keepAlways; add(coordinates)
        let replay = GhostRecord(identity: state.identity, seed: state.seed, ticks: state.tick,
                                 digest: state.digest(), commands: session.commandLog)
        let replayData = try JSONEncoder().encode(replay)
        let decoded = try JSONDecoder().decode(GhostRecord.self, from: replayData)
        let replayed = try XCTUnwrap(GhostRun.replay(seed: decoded.seed, commands: decoded.playerCommands, until: decoded.ticks))
        XCTAssertEqual(replayed.state.digest(), state.digest())
        let commands = XCTAttachment(data: replayData, uniformTypeIdentifier: "public.json")
        commands.name = "BP010-field-encounter-commands-seed-1"
        commands.lifetime = .keepAlways; add(commands)
        let record = XCTAttachment(string: """
        Seed 1; normal GameSession commands from DebugAutopilot run; no scenario seeding.
        tick=\(snap.tick), player=\(snap.player.x),\(snap.player.y), facing=\(snap.playerDirection)
        enemies=\(snap.enemies.count), projectiles=\(snap.projectiles.count), telegraphs=\(snap.telegraphs.count)
        Production GameScene/HUD/fog/ground/projection; painted neutral Player and complete Camera candidate family.
        Same unedited snapshot across control/dark/paired and normal/Reduced Motion.
        digest=\(state.digest()); candidate source: docs/review/camera-clips.
        Static paused comparison; not movement-animation, final projection, dense-scene or damage-effect acceptance.
        """)
        record.name = "BP010-field-encounter-record"; record.lifetime = .keepAlways; add(record)
    }

    @MainActor
    func testCapturePaintedPlayerLegalEncounterContrast() throws {
        let session = GameSession(seed: 1)
        session.audioSettings = .init(effectsEnabled: false, hapticsEnabled: false, musicEnabled: false)
        var pilot = try XCTUnwrap(DebugAutopilot(scenario: "run", arena: session.simulation.state.arena))
        var found = false
        for _ in 0..<6000 {
            let before = session.snapshot
            let command = pilot.command(before)
            session.moveX = command.moveX; session.moveY = command.moveY
            session.dodgePressed = command.dodge
            if before.upgradePending { session.pendingUpgradeChoice = pilot.upgradeChoice.selectionIndex }
            session.step()
            let snap = session.snapshot
            let nearby = snap.enemies.filter { abs($0.x - snap.player.x) < 300 && abs($0.y - snap.player.y) < 130 }
            if nearby.count >= 2 && !snap.projectiles.isEmpty { found = true; break }
            if session.simulation.isTerminal { break }
        }
        XCTAssertTrue(found, "Pilot must reach an unedited encounter with nearby enemies and projectiles")
        guard found else { return }
        XCTAssertFalse(session.scenarioSeeded)
        let view = SKView(frame: CGRect(x: 0, y: 0, width: 704, height: 326))
        view.isPaused = true
        let scene = GameScene(size: view.bounds.size, session: session)
        view.presentScene(scene)
        defer { view.presentScene(nil) }
        scene.skipIntroIfRunning()
        scene.update(0)
        let snap = session.snapshot
        let player = try XCTUnwrap(scene.childNode(withName: "//sprite-player") as? SKSpriteNode)
        let directions = ["n": "north", "s": "south", "e": "east", "w": "west"]
        let facing = directions[snap.playerDirection] ?? snap.playerDirection
        let url = try XCTUnwrap(Bundle(for: Self.self).url(forResource: "painted-player-\(facing)", withExtension: "png"))
        let image = try XCTUnwrap(UIImage(contentsOfFile: url.path))
        player.removeAllActions()
        player.texture = SKTexture(image: image)
        player.texture?.filteringMode = .linear
        player.size = CGSize(width: 64, height: 64)
        player.anchorPoint = CGPoint(x: 0.5, y: 0.125)
        scene.refreshBenchmarkOutlines(samplingScale: 3)
        let border = try XCTUnwrap(player.childNode(withName: WorldRenderer.outlineName))
        let camera = try XCTUnwrap(scene.camera)
        let lower = scene.convert(CGPoint(x: -352, y: -163), from: camera)
        let upper = scene.convert(CGPoint(x: 352, y: 163), from: camera)
        let crop = CGRect(x: lower.x, y: lower.y, width: upper.x - lower.x, height: upper.y - lower.y)
        for (label, opacity) in [("full", CGFloat(1)), ("quarter", CGFloat(0.25)), ("none", CGFloat(0))] {
            border.alpha = opacity
            let texture = try XCTUnwrap(view.texture(from: scene, crop: crop))
            let attachment = XCTAttachment(image: UIImage(cgImage: texture.cgImage()))
            attachment.name = "BP010-legal-encounter-\(label)"
            attachment.lifetime = .keepAlways
            add(attachment)
        }
        let state = session.simulation.state
        let replay = GhostRecord(identity: state.identity, seed: state.seed, ticks: state.tick,
                                 digest: state.digest(), commands: session.commandLog)
        let replayData = try JSONEncoder().encode(replay)
        let decoded = try JSONDecoder().decode(GhostRecord.self, from: replayData)
        let replayed = try XCTUnwrap(GhostRun.replay(seed: decoded.seed, commands: decoded.playerCommands, until: decoded.ticks))
        XCTAssertEqual(replayed.state.digest(), state.digest())
        let commands = XCTAttachment(data: replayData, uniformTypeIdentifier: "public.json")
        commands.name = "BP010-legal-encounter-commands-seed-1"
        commands.lifetime = .keepAlways; add(commands)
        let record = XCTAttachment(string: """
        Seed 1; normal GameSession commands from DebugAutopilot run; no scenario seeding.
        tick=\(snap.tick), player=\(snap.player.x),\(snap.player.y), facing=\(snap.playerDirection)
        enemies=\(snap.enemies.count), projectiles=\(snap.projectiles.count), telegraphs=\(snap.telegraphs.count)
        Production GameScene/HUD/fog/ground/projection, painted neutral Player texture only.
        Static paused comparison; not movement-animation, final projection, dense-scene or damage-effect acceptance.
        """)
        record.name = "BP010-legal-encounter-record"; record.lifetime = .keepAlways; add(record)
    }

    /// BP-007 comparison: project ground geometry while preserving upright art.
    /// Restores the tree after capture so repeated state samples cannot accumulate transforms.
    @MainActor
    private func projectedSharedCameraScene(scene: GameScene, view: SKView, center: CGPoint,
                                             crop: CGRect, cameraID: UInt64, box: AABB, magnification: CGFloat = 1) throws -> UIImage {
        let camera = try XCTUnwrap(scene.camera)
        let names = ["sprite-player", "sprite-camera-\(cameraID)", "benchmark-building",
                     "benchmark-prop-0", "benchmark-prop-1"]
        let billboards = try names.map { try XCTUnwrap(scene.childNode(withName: "//" + $0)) }
        let building = try XCTUnwrap(billboards[2] as? SKSpriteNode)
        XCTAssertEqual(box.halfSize, VecI(x: 64, y: 64))
        let canvas = CGFloat(1254) * (CGFloat(128) * CGFloat(2).squareRoot() / 934)
        building.size = CGSize(width: canvas, height: canvas)
        building.anchorPoint = CGPoint(x: CGFloat(653) / 1254, y: 1 - CGFloat(1152) / 1254)
        building.position = CGPoint(x: box.minX, y: box.minY)
        let originals = try billboards.map { node in
            (node, try XCTUnwrap(node.parent), node.position, node.zPosition)
        }
        func projected(_ point: CGPoint) -> CGPoint {
            let x = point.x - center.x, y = point.y - center.y
            let r = CGFloat(0.5).squareRoot()
            return CGPoint(x: center.x + r * (x - y), y: center.y + r * (x + y) / 2)
        }
        for (node, parent, position, _) in originals {
            let point = scene.convert(position, from: parent)
            var z = node.zPosition
            var ancestor: SKNode? = parent
            while let a = ancestor, a !== scene { z += a.zPosition; ancestor = a.parent }
            node.removeFromParent(); node.position = projected(point); node.zPosition = z
            scene.addChild(node)
        }
        let upright = Set(billboards.map(ObjectIdentifier.init))
        let groundNodes = scene.children.filter { $0 !== camera && !upright.contains(ObjectIdentifier($0)) }
        let squash = SKNode(), rotation = SKNode(), translation = SKNode()
        squash.position = center; squash.yScale = 0.5
        rotation.zRotation = .pi / 4; translation.position = CGPoint(x: -center.x, y: -center.y)
        scene.addChild(squash); squash.addChild(rotation); rotation.addChild(translation)
        for node in groundNodes { node.removeFromParent(); translation.addChild(node) }
        defer {
            for node in groundNodes { node.removeFromParent(); scene.addChild(node) }
            for (node, parent, position, z) in originals {
                node.removeFromParent(); node.position = position; node.zPosition = z; parent.addChild(node)
            }
            squash.removeFromParent()
        }
        for point in [CGPoint(x: box.minX, y: box.minY), CGPoint(x: box.maxX, y: box.maxY)] {
            let actual = translation.convert(point, to: scene), expected = projected(point)
            XCTAssertEqual(actual.x, expected.x, accuracy: 0.0001)
            XCTAssertEqual(actual.y, expected.y, accuracy: 0.0001)
        }
        // BP-007: exercise the actual comparison tree in all travel directions,
        // including partial input and a full authored-cycle distance.
        let directions: [(CGFloat, CGFloat)] = [
            (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)
        ]
        for (x, y) in directions {
            for magnitude: CGFloat in [0.25, 0.5, 1, 120] {
                let length = hypot(x, y)
                let point = CGPoint(x: center.x + x / length * magnitude,
                                    y: center.y + y / length * magnitude)
                let actual = translation.convert(point, to: scene)
                let expected = projected(point)
                // Numeric transform bound at SpriteKit's Float storage precision;
                // this is not an art/contact acceptance threshold.
                let tolerance = CGFloat(Float(max(abs(point.x), abs(point.y), 1)).ulp) * 8
                XCTAssertEqual(actual.x, expected.x, accuracy: tolerance)
                XCTAssertEqual(actual.y, expected.y, accuracy: tolerance)
                let recovered = scene.convert(actual, to: translation)
                XCTAssertEqual(recovered.x, point.x, accuracy: tolerance)
                XCTAssertEqual(recovered.y, point.y, accuracy: tolerance)
            }
        }
        let screenDownWorld = scene.convert(CGPoint(x: center.x, y: center.y - 1), to: translation)
        XCTAssertLessThan(screenDownWorld.x, center.x)
        XCTAssertLessThan(screenDownWorld.y, center.y)
        let expectedCorner = projected(CGPoint(x: box.minX, y: box.minY))
        // #129: SKNode's observed stored components use Float precision.
        // Keep exact equality at that representation, separate from the ground transform check.
        XCTAssertEqual(building.position, CGPoint(x: CGFloat(Float(expectedCorner.x)),
                                                 y: CGFloat(Float(expectedCorner.y))))
        XCTAssertEqual(building.size.width, building.size.height)
        XCTAssertEqual(camera.xScale, 1)
        // Camera-owned HUD stays fixed while the complete projected world is
        // reframed. Sprite size/anchor and authoritative geometry remain intact.
        let world = scene.children.filter { $0 !== camera }
        let zoomRoot = SKNode()
        if magnification != 1 {
            let focus = CGPoint(x: center.x + 35, y: center.y + 25)
            zoomRoot.setScale(magnification)
            zoomRoot.position = CGPoint(x: center.x - focus.x * magnification,
                                        y: center.y - focus.y * magnification)
            scene.addChild(zoomRoot)
            for node in world { node.removeFromParent(); zoomRoot.addChild(node) }
        }
        defer {
            if magnification != 1 {
                for node in world { node.removeFromParent(); scene.addChild(node) }
                zoomRoot.removeFromParent()
            }
        }
        XCTAssertEqual(camera.xScale, 1)
        let rendered = try XCTUnwrap(view.texture(from: scene, crop: crop))
        return UIImage(cgImage: rendered.cgImage())
    }

    @MainActor
    func testCaptureCompleteCameraCandidatesInSharedScene() throws {
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
            player: try texture("painted-player-south"), camera: try texture("camera"),
            building: .init(texture: try texture("building-constrained"), size: CGSize(width: 190, height: 217),
                            anchor: CGPoint(x: 0.5, y: 0), position: CGPoint(x: x, y: y - 64)),
            buildingID: id,
            props: [
                .init(texture: try texture("newsbox"), size: CGSize(width: 20, height: 40),
                      anchor: CGPoint(x: 0.5, y: 0), position: CGPoint(x: x + 115, y: y - 65)),
                .init(texture: try texture("tree"), size: CGSize(width: 50, height: 85),
                      anchor: CGPoint(x: 0.5, y: 0), position: CGPoint(x: 858, y: 780))
            ], paving: try XCTUnwrap(env.texture(assetId: "env_ground_plaza")))
        var streetArt = art
        let road = CGRect(x: 900, y: 0, width: 1404, height: 1536)
        streetArt.configureStreetCorner(asphalt: try XCTUnwrap(env.texture(assetId: "env_ground_asphalt")))
        XCTAssertFalse(road.intersects(CGRect(x: box.minX, y: box.minY,
                                             width: box.halfSize.x * 2, height: box.halfSize.y * 2)))
        let candidates = try CameraPlaybackTests.candidateFrames()
        XCTAssertTrue(scene.installBenchmarkCameraFrames(candidates))
        let crop = CGRect(x: center.x - 352, y: center.y - 163, width: 704, height: 326)
        let clips = [3: "camera_operational_idle", 2: "camera_hit",
                     1: "camera_critical_enter", 0: "camera_destroyed_idle"]
        for style in WorldRenderer.BenchmarkFieldContrast.allCases {
        scene.setBenchmarkFieldContrast(style)
        for integrity in stride(from: 3, through: 0, by: -1) {
            snap.cameras[0].integrity = integrity
            snap.cameras[0].fieldVisible = integrity > 0
            scene.renderBenchmark(snapshot: snap, art: art, center: center)
            XCTAssertNil(scene.childNode(withName: "//benchmark-ground-line-0"))
            let sprite = try XCTUnwrap(scene.childNode(withName: "//sprite-camera-\(snap.cameras[0].id.raw)") as? SKSpriteNode)
            XCTAssertTrue(sprite.texture === candidates[clips[integrity]!]!.last)
            XCTAssertFalse(sprite.hasActions())
            let contact = try XCTUnwrap(scene.childNode(withName: "//benchmark-camera-contact-\(snap.cameras[0].id.raw)"))
            XCTAssertEqual(contact.position, CGPoint(x: snap.cameras[0].x, y: snap.cameras[0].y - 2))
            XCTAssertNil(scene.childNode(withName: "//housing-\(snap.cameras[0].id.raw)"))
            if integrity == 0 { XCTAssertNil(scene.childNode(withName: "//field-\(snap.cameras[0].id.raw)")) }
            let result = try XCTUnwrap(view.texture(from: scene, crop: crop))
            let attachment = XCTAttachment(image: UIImage(cgImage: result.cgImage()))
            attachment.name = "BP004-shared-scene-\(style.rawValue)-integrity-\(integrity)"
            attachment.lifetime = .keepAlways; add(attachment)
            let digest = scene.session.simulation.state.digest()
            let projected = try projectedSharedCameraScene(scene: scene, view: view, center: center,
                crop: crop, cameraID: snap.cameras[0].id.raw, box: box)
            XCTAssertEqual(scene.session.simulation.state.digest(), digest)
            let registered = XCTAttachment(image: projected)
            registered.name = "BP004-registered-shared-scene-\(style.rawValue)-integrity-\(integrity)"
            registered.lifetime = .keepAlways; add(registered)
            scene.renderBenchmark(snapshot: snap, art: streetArt, center: center)
            var patchCount = 0
            scene.enumerateChildNodes(withName: "//benchmark-ground-patch-0") { node, _ in
                guard let tile = node as? SKSpriteNode else { XCTFail("Patch must be a surface tile"); return }
                patchCount += 1
                XCTAssertTrue(road.contains(tile.frame))
                XCTAssertEqual(tile.texture?.size(), tile.size, "128px/128-unit source density must survive edge cropping")
            }
            XCTAssertEqual(patchCount, 11 * 12)
            let street = try projectedSharedCameraScene(scene: scene, view: view, center: center,
                crop: crop, cameraID: snap.cameras[0].id.raw, box: box)
            XCTAssertEqual(scene.session.simulation.state.digest(), digest)
            let furnished = XCTAttachment(image: street)
            furnished.name = "BP004-street-shared-scene-\(style.rawValue)-integrity-\(integrity)"
            furnished.lifetime = .keepAlways; add(furnished)
            // Revised source composition only. Keep the old neutral control above.
            if style == .paired && integrity == 3 {
                for frame in [0, 4, 8, 12] {
                    var revised = BenchmarkReviewArt(
                        player: try texture(String(format: "player-source-s-%02d", frame)),
                        camera: streetArt.camera, building: streetArt.building,
                        buildingID: streetArt.buildingID, props: streetArt.props, paving: streetArt.paving)
                    revised.groundPatches = streetArt.groundPatches
                    revised.groundLines = streetArt.groundLines
                    scene.renderBenchmark(snapshot: snap, art: revised, center: center)
                    let player = try XCTUnwrap(scene.childNode(withName: "//sprite-player") as? SKSpriteNode)
                    player.size = CGSize(width: 64, height: 416.0 / 6.0)
                    player.anchorPoint = CGPoint(x: 0.5, y: 1 - 336.0 / 416.0)
                    // Approved clean-review treatment only; restore controls afterward.
                    var outlineVisibility: [(SKNode, Bool)] = []
                    scene.enumerateChildNodes(withName: "//" + WorldRenderer.outlineName) { node, _ in
                        outlineVisibility.append((node, node.isHidden)); node.isHidden = true
                    }
                    defer { for (node, hidden) in outlineVisibility { node.isHidden = hidden } }
                    let composed = try projectedSharedCameraScene(scene: scene, view: view, center: center,
                        crop: crop, cameraID: snap.cameras[0].id.raw, box: box)
                    XCTAssertEqual(scene.session.simulation.state.digest(), digest)
                    XCTAssertEqual(player.size.height, CGFloat(Float(416.0 / 6.0)))
                    let image = XCTAttachment(image: composed)
                    image.name = "BP008-revised-shared-composition-pose-\(frame)"
                    image.lifetime = .keepAlways; add(image)
                    if frame == 0 {
                        for zoom: CGFloat in [1.25, 1.4] {
                            let closer = try projectedSharedCameraScene(scene: scene, view: view, center: center,
                                crop: crop, cameraID: snap.cameras[0].id.raw, box: box, magnification: zoom)
                            XCTAssertEqual(scene.session.simulation.state.digest(), digest)
                            let comparison = XCTAttachment(image: closer)
                            comparison.name = "BP007-street-framing-\(Int(zoom * 100))-percent"
                            comparison.lifetime = .keepAlways; add(comparison)
                        }
                    }
                }
            }
        }
        }
        let record = XCTAttachment(string: """
        Actual GameScene/WorldRenderer/HUD; 704x326 logical viewport. Complete camera
        candidates use the production integrity policy, with Reduced Motion settled
        frames. Painted neutral player and constrained building are review assets.
        Explicit composition placements; not a legal encounter or animation capture.
        Registered variants use the BP007 45-degree rotation/half-height ground comparison,
        unchanged zoom, upright artwork and documented constrained-building corner anchor.
        Control variants retain the old stretched building for direct comparison (issue 128).
        Street variants add asphalt bounds (960,0,1344,1536), 128-unit tiles; curb at
        x=960/957 (width 4/3), rail grooves at x=1020/1060 (width 5, metal 1.5).
        All strips span y=0...1536; these are editable fixture values, not arena placement.
        Geometry mapping and player locomotion remain unaccepted. Native frame scale
        must be read from the exported pixel dimensions. Camera texture filtering is
        nearest; other high-resolution composition sources use linear filtering.
        """)
        record.name = "BP004-shared-scene-record"; record.lifetime = .keepAlways; add(record)
    }

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
                      anchor: CGPoint(x: 0.5, y: 0), position: CGPoint(x: 858, y: 780))
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
            // BP-002 painted neutral source: one logical size and anchor across
            // four real facings. Test-only textures; no clip or art admission.
            let previousPlayerTexture = player.texture
            let previousPlayerAnchor = player.anchorPoint
            for facing in ["south", "east", "north", "west"] {
                let candidate = try texture("painted-player-\(facing)")
                XCTAssertEqual(candidate.size(), CGSize(width: 384, height: 384))
                player.texture = candidate
                player.anchorPoint = CGPoint(x: 0.5, y: 0.125)
                // A paused SKView does not run the post-action outline refresh.
                // Use the normal scene callback so no previous-frame outline leaks.
                scene.didEvaluateActions()
                try capture("BP002-painted-neutral-\(facing)-\(tag)")
                scene.refreshBenchmarkOutlines(samplingScale: 3)
                try capture("BP007-outline-3x-\(facing)-\(tag)")
                // BP-010: change only the added Player border in this paused
                // review fixture. Never modify enemy outlines or source art.
                let border = try XCTUnwrap(player.childNode(withName: WorldRenderer.outlineName))
                let originalAlpha = border.alpha
                let rootPosition = player.position
                let otherChildren = player.children.filter { $0 !== border }.map { ($0, $0.alpha) }
                do {
                    defer { border.alpha = originalAlpha }
                    for (label, opacity) in [("half", CGFloat(0.5)), ("quarter", CGFloat(0.25)), ("none", CGFloat(0))] {
                        border.alpha = opacity
                        try capture("BP010-border-\(label)-\(facing)-\(tag)")
                        XCTAssertEqual(player.position, rootPosition)
                        XCTAssertTrue(player.texture === candidate)
                        for (node, alpha) in otherChildren { XCTAssertEqual(node.alpha, alpha) }
                    }
                }
                XCTAssertEqual(border.alpha, originalAlpha)
                if zoom != 1 {
                    // BP-010 backdrop diagnostic. Reuse bundled level surfaces;
                    // only replace the review paving, not world geometry or art.
                    func pavingNodes(_ node: SKNode) -> [SKSpriteNode] {
                        let own = (node as? SKSpriteNode).flatMap { $0.texture === art.paving ? $0 : nil }
                        return (own.map { [$0] } ?? []) + node.children.flatMap(pavingNodes)
                    }
                    let ground = pavingNodes(scene)
                    XCTAssertFalse(ground.isEmpty)
                    let originals = ground.map { ($0, $0.texture) }
                    do {
                        defer {
                            for (node, original) in originals { node.texture = original }
                            border.alpha = originalAlpha
                        }
                        for surface in ["asphalt", "service"] {
                            let paving = try XCTUnwrap(env.texture(assetId: "env_ground_\(surface)"))
                            for node in ground { node.texture = paving }
                            for (label, opacity) in [("full", CGFloat(1)), ("quarter", CGFloat(0.25)), ("none", CGFloat(0))] {
                                border.alpha = opacity
                                try capture("BP010-ground-\(surface)-\(label)-\(facing)")
                                XCTAssertEqual(player.position, rootPosition)
                                XCTAssertTrue(player.texture === candidate)
                            }
                        }
                    }
                    for (node, original) in originals { XCTAssertTrue(node.texture === original) }
                    XCTAssertEqual(border.alpha, originalAlpha)
                }
                scene.didEvaluateActions()
            }
            player.texture = previousPlayerTexture
            player.anchorPoint = previousPlayerAnchor
            scene.didEvaluateActions()
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
        BP002-painted-neutral captures use four registered 384x384 test-only source
        images at the same 64x64 logical canvas and (32,56) anchor. Both ground
        projection zooms are captured with the constrained building, municipal
        camera and props. Names identify view intent, not calibrated world facings.
        Source registration/hashes: BenchmarkAssets/painted-player-sources.json.
        These are still comparisons, not layered-source or animation acceptance.
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
