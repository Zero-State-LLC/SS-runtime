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
            while accumulator >= 1.0 / 60.0 {
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
            // #126: tick coverage and observed display coverage are independent.
            if state.tick >= 90 && samples.count > 10 {
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
        let completed = expectation(description: "at least 90 simulation ticks and 11 post-action observations")
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

    func testFullGameSceneCapturesPostActionImagesWithFrameRecords() async throws {
        let window = UIWindow(frame: CGRect(x: 0, y: 0, width: 704, height: 326))
        let controller = UIViewController()
        let view = SKView(frame: window.bounds)
        controller.view = view
        window.rootViewController = controller
        window.makeKeyAndVisible()
        let scene = GameScene(size: view.bounds.size, session: GameSession(seed: 1))
        scene.session.audioSettings = .init(effectsEnabled: false, hapticsEnabled: false, musicEnabled: false)
        let completed = expectation(description: "full GameScene post-action captures")
        var records: [[String: Any]] = []
        var images: [(String, UIImage)] = []
        var capturedPaths: Set<String> = []
        var finished = false
        scene.benchmarkPlaybackObserver = { time, snapshot, position, observed, camera in
            guard !finished else { return }
            let imageName = "BP008-full-scene-tick-\(snapshot.tick)"
            var record: [String: Any] = [
                "displayTime": time, "tick": snapshot.tick,
                "authoritativeRawX": position.x.raw, "authoritativeRawY": position.y.raw,
                "renderedX": observed.position.x, "renderedY": observed.position.y,
                "cameraX": camera.x, "cameraY": camera.y,
                "width": observed.size.width, "height": observed.size.height,
                "anchorX": observed.anchor.x, "anchorY": observed.anchor.y,
                "facing": snapshot.playerDirection, "clip": observed.clipToken ?? "unidentified",
                "framePath": observed.deliveredPath ?? "unidentified",
                "viewportWidth": view.bounds.width, "viewportHeight": view.bounds.height,
                "displayScale": view.contentScaleFactor
            ]
            if let path = observed.deliveredPath, snapshot.playerClipId == "player_move",
               images.count < 4, !capturedPaths.contains(path) {
                let crop = CGRect(x: camera.x - 352, y: camera.y - 163, width: 704, height: 326)
                if let texture = view.texture(from: scene, crop: crop) {
                    images.append((imageName, UIImage(cgImage: texture.cgImage())))
                    capturedPaths.insert(path)
                    record["imageAttachment"] = imageName
                }
            }
            records.append(record)
            if snapshot.tick >= 90 { finished = true; completed.fulfill() }
        }
        view.presentScene(scene)
        defer {
            scene.benchmarkPlaybackObserver = nil
            view.presentScene(nil)
            window.isHidden = true
        }
        let layout = try XCTUnwrap(scene.controlLayout)
        final class Finger {}
        let finger = Finger()
        let token = TouchController.TouchToken(id: ObjectIdentifier(finger))
        // First input dismisses an active intro; a second begins normal steering.
        _ = scene.beginTouch(token: token, atPoints: layout.stickCentre)
        _ = scene.beginTouch(token: token, atPoints: layout.stickCentre)
        scene.moveTouch(token: token, toPoints: CGPoint(x: layout.stickCentre.x,
            y: layout.stickCentre.y - layout.stickRadius))
        await fulfillment(of: [completed], timeout: 30)
        scene.endTouch(token: token)
        XCTAssertGreaterThan(images.count, 1)
        XCTAssertTrue(records.allSatisfy { ($0["framePath"] as? String) != "unidentified" })
        XCTAssertGreaterThan(Set(records.compactMap { $0["authoritativeRawY"] as? Int64 }).count, 1)
        for (name, image) in images {
            let attachment = XCTAttachment(image: image)
            attachment.name = name
            attachment.lifetime = .keepAlways
            add(attachment)
        }
        let data = try JSONSerialization.data(withJSONObject: records, options: [.prettyPrinted, .sortedKeys])
        let attachment = XCTAttachment(data: data, uniformTypeIdentifier: "public.json")
        attachment.name = "BP008-full-scene-post-action-records"
        attachment.lifetime = .keepAlways
        add(attachment)
    }

    static func interruptionCommand(tick: UInt64) -> PlayerCommand {
        let m = PlayerCommand.axisMaximum
        let x: Int16, y: Int16
        switch tick {
        case 1...30: (x, y) = (-m, 0)
        case 31...60: (x, y) = (-m, -m)
        case 61...120, 151...225: (x, y) = (0, -m)
        case 136...150, 241...300: (x, y) = (0, m)
        default: (x, y) = (0, 0)
        }
        return PlayerCommand(tick: tick, moveX: x, moveY: y, dodgePressed: tick == 211)
    }

    /// Isolated ground/contact comparison, not a full benchmark encounter.
    final class PlayerCandidateScene: SKScene {
        let renderer: WorldRenderer
        let session: GameSession
        let axis: Int16
        let reducedMotion: Bool
        let stage: Int
        var simulationSeconds = 0.0
        var renderSeconds = 0.0
        var postActionSeconds = 0.0
        var diagnosticSeconds = 0.0
        private var presentedSnapshot: PresentationSnapshot?
        var snapshotBuildCount = 0
        var frameCosts: [[String: Any]] = []
        var cleanSilhouetteReview = false
        // BP-008 experiment only; shipping renderer cadence remains untouched.
        var reviewLabel = ""
        var distancePhaseComparison = false
        var candidateTextures: [SKTexture] = []
        var moveTicks: UInt64 = 120
        var interruptionRoute = false
        private var pauseUntil: TimeInterval?
        private var pauseCompleted = false
        private var reviewPaused = false
        private var accumulatedTravel = 0.0
        private var distanceSegmentActive = false
        private var sceneConfigured = false
        private var initialDisplayPasses = 0
        private var initialDisplayBegan: TimeInterval?
        var initialDisplaySeconds = 0.0
        private var preparingDisplay = false
        let paths: [String]
        let upright = SKNode()
        var records: [[String: Any]] = []
        var images: [(String, UIImage)] = []
        var seenPaths: Set<String> = []
        var done: (() -> Void)?
        private var previousTime: Double?
        private var accumulator = 0.0
        private var now = 0.0
        private var finished = false

        init(size: CGSize, library: SpriteLibrary, paths: [String], axis: Int16, reducedMotion: Bool, stage: Int) throws {
            var simulation = try Simulation.make(seed: 1)
            simulation.testing_setPlayerPosition(VecI(x: 224, y: 704))
            session = GameSession(simulation: simulation)
            self.axis = axis; self.reducedMotion = reducedMotion; self.stage = stage
            renderer = WorldRenderer(sprites: library)
            self.paths = paths
            if stage >= 1 {
                renderer.benchmarkPlayerRegistration = (CGSize(width: 64, height: 416.0 / 6.0),
                    CGPoint(x: 0.5, y: 1 - 336.0 / 416.0))
            }
            super.init(size: size)
        }
        required init?(coder: NSCoder) { fatalError("init(coder:) unsupported") }
        override func didMove(to view: SKView) { configureScene() }
        func configureScene() {
            guard !sceneConfigured else { return }
            sceneConfigured = true
            addChild(renderer.root)
            renderer.root.yScale = 0.5
            upright.name = "player-source-wrapper"; upright.yScale = 2
            renderer.root.children[WorldRenderer.Layer.actors.rawValue].addChild(upright)
            let camera = SKCameraNode(); addChild(camera); self.camera = camera
            let label = SKLabelNode(fontNamed: "Menlo")
            label.text = reviewLabel; label.fontSize = 11; label.fontColor = .white
            label.horizontalAlignmentMode = .left; label.position = CGPoint(x: -340, y: 145)
            label.zPosition = 10000; camera.addChild(label)
            session.moveY = -axis
        }
        override func update(_ time: TimeInterval) {
            guard !finished else { return }
            now = time
            preparingDisplay = stage >= 4 && initialDisplayPasses < 2
            if preparingDisplay {
                if initialDisplayBegan == nil { initialDisplayBegan = time }
                // Initial presentation is loading, never gameplay catch-up.
                previousTime = nil
            } else if let began = initialDisplayBegan {
                initialDisplaySeconds = time - began
                initialDisplayBegan = nil
            }
            reviewPaused = pauseUntil.map { time < $0 } ?? false
            if pauseUntil != nil && !reviewPaused {
                pauseUntil = nil; pauseCompleted = true; previousTime = nil; accumulator = 0
                renderer.root.isPaused = false
            }
            if reviewPaused { previousTime = nil; accumulator = 0 }
            if let previousTime { accumulator += min(time - previousTime, 0.25) }
            previousTime = preparingDisplay || reviewPaused ? nil : time
            let simulationBegan = CFAbsoluteTimeGetCurrent()
            while accumulator >= 1.0 / 60.0 {
                if interruptionRoute {
                    let command = DisplayedPlaybackTests.interruptionCommand(tick: session.simulation.state.tick + 1)
                    session.moveX = command.moveX; session.moveY = command.moveY
                    session.dodgePressed = command.dodgePressed
                } else {
                    session.moveY = session.simulation.state.tick < moveTicks ? -axis : 0
                }
                let before = session.simulation.state.player.position
                session.step(); accumulator -= 1.0 / 60.0
                if distancePhaseComparison {
                    let after = session.simulation.state.player.position
                    let dx = Double(after.x.raw - before.x.raw) / 256
                    let dy = Double(after.y.raw - before.y.raw) / 256
                    let travel = hypot(dx, dy)
                    if travel > 0 {
                        if distanceSegmentActive { accumulatedTravel += travel }
                        else { distanceSegmentActive = true; accumulatedTravel = 0 }
                    }
                }
                if interruptionRoute && !pauseCompleted && session.simulation.state.tick == 120 {
                    pauseUntil = time + 0.35; reviewPaused = true
                    renderer.root.isPaused = true; previousTime = nil; accumulator = 0
                    break
                }
            }
            let simulationCost = CFAbsoluteTimeGetCurrent() - simulationBegan
            simulationSeconds += simulationCost
            let renderBegan = CFAbsoluteTimeGetCurrent()
            let snap = session.snapshot
            presentedSnapshot = snap
            snapshotBuildCount += 1
            renderer.render(snap, reducedMotion: reducedMotion)
            if distancePhaseComparison { applyDistanceFrameIfSelected() }
            let renderCost = CFAbsoluteTimeGetCurrent() - renderBegan
            renderSeconds += renderCost
            frameCosts.append(["tick": session.simulation.state.tick, "simulationSeconds": simulationCost,
                "renderSeconds": renderCost])
            // Only ground and this actor are in the registration diagnostic.
            // Other upright art must not be flattened into this comparison.
            for (index, layer) in renderer.root.children.enumerated() {
                layer.isHidden = index != WorldRenderer.Layer.ground.rawValue
                    && index != WorldRenderer.Layer.actors.rawValue
                if index == WorldRenderer.Layer.actors.rawValue {
                    for child in layer.children { child.isHidden = child.name != "sprite-player" && child !== upright }
                }
            }
            if let player = renderer.root.childNode(withName: "//sprite-player") as? SKSpriteNode {
                player.size = CGSize(width: 64, height: 416.0 / 6.0)
                player.anchorPoint = CGPoint(x: 0.5, y: 1 - 336.0 / 416.0)
                // Project ground roots, preserving the already elevated artwork.
                if player.parent !== upright {
                    player.removeFromParent(); upright.addChild(player)
                }
                player.yScale = 1
                player.position.y /= 2
            }
            camera?.position = CGPoint(x: snap.player.x, y: snap.player.y / 2)
        }
        @discardableResult
        func applyDistanceFrameIfSelected() -> Bool {
            // Base movement can be obscured by a selected event reaction.
            guard renderer.observePlayerPlayback()?.clipToken == "player_move|s",
                  candidateTextures.count == 16,
                  let player = renderer.root.childNode(withName: "//sprite-player") as? SKSpriteNode else {
                distanceSegmentActive = false; accumulatedTravel = 0
                return false
            }
            let phase = accumulatedTravel.truncatingRemainder(dividingBy: 120) / 120
            player.removeAllActions()
            player.texture = candidateTextures[min(15, Int(floor(phase * 16)))]
            return true
        }
        override func didEvaluateActions() {
            guard !finished else { return }
            // Match GameScene post-action outline synchronization.
            let postBegan = CFAbsoluteTimeGetCurrent()
            renderer.syncOutlines()
            // Visual review only: preserve measured outline preparation controls,
            // but do not show their diagnostic border in the clean art capture.
            if cleanSilhouetteReview {
                renderer.root.enumerateChildNodes(withName: "//" + WorldRenderer.outlineName) { node, _ in
                    node.isHidden = true
                }
            }
            postActionSeconds += CFAbsoluteTimeGetCurrent() - postBegan
            if preparingDisplay {
                initialDisplayPasses += 1
                return
            }
            let diagnosticBegan = CFAbsoluteTimeGetCurrent()
            defer { diagnosticSeconds += CFAbsoluteTimeGetCurrent() - diagnosticBegan }
            guard let snapshot = presentedSnapshot else { return }
            // #130: completion and missing-frame evidence cannot depend on move art.
            defer {
                if session.simulation.state.tick >= moveTicks + 30 {
                    finished = true; done?()
                }
            }
            guard let observed = renderer.observePlayerPlayback(),
                  let path = observed.deliveredPath, let frame = paths.firstIndex(of: path),
                  let player = renderer.root.childNode(withName: "//sprite-player"),
                  let parent = player.parent else {
                records.append(["displayTime": now, "tick": session.simulation.state.tick,
                    "facing": snapshot.playerDirection, "clip": snapshot.playerClipId,
                    "candidateAvailable": false, "inputAxis": axis, "reducedMotion": reducedMotion,
                    "reviewPaused": reviewPaused])
                return
            }
            let position = session.simulation.state.player.position
            let projected = convert(player.position, from: parent)
            let record: [String: Any] = [
                "displayTime": now, "tick": session.simulation.state.tick,
                "inputAxis": axis, "reducedMotion": reducedMotion, "candidateAvailable": true,
                "cameraX": camera?.position.x ?? 0, "cameraY": camera?.position.y ?? 0,
                "viewScale": view?.contentScaleFactor ?? 1,
                "authoritativeRawX": position.x.raw, "authoritativeRawY": position.y.raw,
                "renderedX": projected.x, "renderedY": projected.y,
                "framePath": path, "sourceFrameIndex": frame,
                "facing": snapshot.playerDirection,
                "clip": observed.clipToken ?? "unidentified",
                "width": observed.size.width, "height": observed.size.height,
                "anchorX": observed.anchor.x, "anchorY": observed.anchor.y,
                "groundYScale": 0.5, "artYScaleAfterParent": 1.0,
                "distancePhaseComparison": distancePhaseComparison, "accumulatedTravel": accumulatedTravel,
                "observationWallTime": Date().timeIntervalSince1970, "reviewPaused": reviewPaused
            ]
            // Record texture identity independently of costly GPU image readback.
            seenPaths.insert(path)
            records.append(record)
        }
    }

    func testRevisedPlayerCleanSilhouetteReview() async throws {
        try await capturePlayerCycle(axis: PlayerCommand.axisMaximum, reducedMotion: false,
                                     repetition: 10, cleanSilhouetteReview: true)
    }
    func testRevisedPlayerSourcePlaysWithProjectedSimulationTravel() async throws {
        try await capturePlayerCycle(axis: PlayerCommand.axisMaximum, reducedMotion: false)
    }
    func testRevisedPlayerHalfInputCycle() async throws {
        try await capturePlayerCycle(axis: PlayerCommand.axisMaximum / 2, reducedMotion: false)
    }
    func testRevisedPlayerQuarterInputCycle() async throws {
        try await capturePlayerCycle(axis: PlayerCommand.axisMaximum / 4, reducedMotion: false)
    }
    func testRevisedPlayerReducedMotionCycle() async throws {
        for repetition in 1...3 {
            try await capturePlayerCycle(axis: PlayerCommand.axisMaximum, reducedMotion: true,
                                         repetition: repetition)
        }
    }
    func testCommandDrivenInterruptionRoute() async throws {
        for reduced in [false, true] {
            for distance in [false, true] {
                try await capturePlayerCycle(axis: PlayerCommand.axisMaximum, reducedMotion: reduced,
                    repetition: distance ? 30 : 31, cleanSilhouetteReview: true,
                    distancePhaseComparison: distance, moveTicks: 300, interruptionRoute: true)
            }
        }
    }

    /// Live renderer composition with a real, preflighted SW simulation route.
    /// Other encounter actors are omitted from this art-review snapshot only.
    final class SharedTraversalScene: SKScene {
        let renderer: WorldRenderer
        let session: GameSession
        let reduced: Bool
        let magnification: CGFloat
        let tracksPlayer: Bool
        let textures: [SKTexture]
        let center = CGPoint(x: 706, y: 644)
        let hud = HUDRenderer()
        let squash = SKNode(), rotation = SKNode(), translation = SKNode()
        var originals: [(SKNode, SKNode, CGPoint, CGFloat)] = []
        var player: SKSpriteNode?
        var selectedClip: String?
        var presentedPlayer = CGPoint.zero
        var records: [[String: Any]] = []
        var images: [(Int, UIImage)] = []
        var seen: Set<Int> = []
        var seenImages: Set<Int> = []
        var capturesImages = false
        var done: (() -> Void)?
        var previous: TimeInterval?
        var accumulator = 0.0
        var warmup = 0
        var finished = false
        var worldTrace: [VecQ8] = []
        init(size: CGSize, renderer: WorldRenderer, textures: [SKTexture], reduced: Bool, magnification: CGFloat = 1, tracksPlayer: Bool = false) throws {
            var simulation = try Simulation.make(seed: 1)
            simulation.testing_setPlayerPosition(VecI(x: 736, y: 654))
            session = GameSession(simulation: simulation)
            self.renderer = renderer; self.textures = textures
            self.reduced = reduced
            self.magnification = magnification; self.tracksPlayer = tracksPlayer
            super.init(size: size)
            squash.position = center; squash.yScale = 0.5
            rotation.zRotation = .pi / 4
            translation.position = CGPoint(x: -center.x, y: -center.y)
            addChild(squash); squash.addChild(rotation); rotation.addChild(translation)
            translation.addChild(renderer.root)
            let camera = SKCameraNode(); camera.position = center; addChild(camera); self.camera = camera
            camera.setScale(1 / magnification)
            camera.addChild(hud.root)
            hud.configure(projector: HUDProjector(viewSize: size,
                safeInsets: EdgeInsetsPoints(top: 0, left: 0, bottom: 0, right: 0), sceneSize: size),
                handedness: .right, hudScale: .standard)
            let label = SKLabelNode(fontNamed: "Menlo")
            label.text = "BP008 projected SW / front source / composition only"
            label.fontSize = 9; label.position = CGPoint(x: 0, y: -153)
            label.zPosition = 10000; camera.addChild(label)
        }
        required init?(coder: NSCoder) { fatalError("unsupported") }
        func restoreBillboards() {
            for (node, parent, position, z) in originals {
                node.removeFromParent(); node.position = position; node.zPosition = z; parent.addChild(node)
            }
            originals.removeAll(keepingCapacity: true)
        }
        override func update(_ time: TimeInterval) {
            guard !finished else { return }
            restoreBillboards()
            player = nil
            if warmup >= 2, let previous { accumulator += min(time - previous, 0.25) }
            previous = time
            while accumulator >= 1.0 / 60.0 && session.simulation.state.tick < 90 {
                let moving = session.simulation.state.tick < 75
                session.moveX = moving ? -PlayerCommand.axisMaximum : 0
                session.moveY = moving ? -PlayerCommand.axisMaximum : 0
                session.step(); accumulator -= 1.0 / 60.0
                worldTrace.append(session.simulation.state.player.position)
            }
            var snap = session.snapshot
            // Review composition, not a legal-encounter visibility or camera proof.
            let index = snap.solidIds.firstIndex(of: "solid-03-transit-kiosk")!
            snap.solids = [snap.solids[index]]; snap.solidIds = ["solid-03-transit-kiosk"]
            snap.enemies = []; snap.projectiles = []; snap.telegraphs = []; snap.mines = []
            snap.spawnSockets = []; snap.captainHousings = []; snap.captainField = nil; snap.patrolCones = []
            snap.cameras = Array(snap.cameras.prefix(1))
            snap.cameras[0].x = 846; snap.cameras[0].y = 674
            snap.cameras[0].fieldOrigin = VecI(x: 846, y: 674).asQ8
            snap.cameras[0].headingMilli = 100_000
            renderer.render(snap, reducedMotion: reduced)
            selectedClip = renderer.observePlayerPlayback()?.clipToken
            presentedPlayer = CGPoint(x: snap.player.x, y: snap.player.y)
            hud.render(snap, cameraHUD: session.cameraHUDProjection, paused: false)
            if magnification != 1 {
                let initial = translation.convert(CGPoint(x: 736, y: 654), to: self)
                let current = translation.convert(presentedPlayer, to: self)
                camera?.position = CGPoint(x: center.x + 35 + (tracksPlayer ? current.x - initial.x : 0),
                                           y: center.y + 25 + (tracksPlayer ? current.y - initial.y : 0))
            }

            let names = ["sprite-player", "sprite-camera-\(snap.cameras[0].id.raw)",
                         "benchmark-building", "benchmark-prop-0", "benchmark-prop-1"]
            for name in names {
                guard let node = renderer.root.childNode(withName: "//" + name), let parent = node.parent else { continue }
                let world = renderer.root.convert(node.position, from: parent)
                let point = translation.convert(world, to: self)
                var z = node.zPosition
                var ancestor: SKNode? = parent
                while let current = ancestor, current !== self { z += current.zPosition; ancestor = current.parent }
                originals.append((node, parent, node.position, node.zPosition))
                node.removeFromParent(); node.position = point; node.zPosition = z; addChild(node)
                if name == "sprite-player" { player = node as? SKSpriteNode }
            }
            renderer.root.enumerateChildNodes(withName: "//" + WorldRenderer.outlineName) { node, _ in node.isHidden = true }
            player?.enumerateChildNodes(withName: "//" + WorldRenderer.outlineName) { node, _ in node.isHidden = true }
        }
        override func didEvaluateActions() {
            guard !finished else { return }
            warmup += 1
            guard warmup > 2 else { return }
            defer { if session.simulation.state.tick == 90 { finished = true; done?() } }
            guard let player else { return }
            let frame = textures.firstIndex { $0 === player.texture }
            let world = session.simulation.state.player.position
            let cameraPosition = camera!.position
            let visible = CGRect(x: cameraPosition.x - size.width / magnification / 2,
                                 y: cameraPosition.y - size.height / magnification / 2,
                                 width: size.width / magnification, height: size.height / magnification)
            let emitter = translation.convert(CGPoint(x: 846, y: 674), to: self)
            let record: [String: Any] = ["tick": session.simulation.state.tick,
                "wallTime": Date().timeIntervalSince1970,
                "rawX": world.x.raw, "rawY": world.y.raw,
                "presentationX": presentedPlayer.x, "presentationY": presentedPlayer.y,
                "renderedX": player.position.x, "renderedY": player.position.y,
                "frame": frame ?? -1, "selectedClip": selectedClip ?? "none",
                "worldFacing": session.snapshot.playerDirection, "authoredFacing": "front",
                "reducedMotion": reduced, "magnification": magnification, "tracksPlayer": tracksPlayer,
                "playerCanvasVisible": visible.contains(player.frame), "cameraEmitterVisible": visible.contains(emitter),
                "viewCenterX": cameraPosition.x, "viewCenterY": cameraPosition.y,
                "playerScreenX": (player.position.x - cameraPosition.x) * magnification + size.width / 2,
                "playerScreenY": (player.position.y - cameraPosition.y) * magnification + size.height / 2]
            records.append(record)
            if let frame {
                seen.insert(frame)
                if capturesImages, [0, 4, 8, 12].contains(frame), seenImages.insert(frame).inserted,
                   let image = view?.texture(from: self,
                       crop: CGRect(x: center.x - 352, y: center.y - 163, width: 704, height: 326)) {
                    images.append((frame, UIImage(cgImage: image.cgImage())))
                }
            }
        }
    }

    func testSessionStepStageTimingPreservesAuthority() throws {
        var measurements: [[String: Any]] = []
        for measuredFirst in [false, true] {
            var initial = try Simulation.make(seed: 1)
            initial.testing_setPlayerPosition(VecI(x: 224, y: 704))
            let control = GameSession(simulation: initial), measured = GameSession(simulation: initial)
            measured.benchmarkStepTimingEnabled = true
            control.moveY = -PlayerCommand.axisMaximum; measured.moveY = -PlayerCommand.axisMaximum
            for tick in 1...120 {
                if measuredFirst { measured.step(); control.step() }
                else { control.step(); measured.step() }
                XCTAssertEqual(measured.simulation.state.digest(), control.simulation.state.digest())
                XCTAssertEqual(measured.lastEvents, control.lastEvents)
                XCTAssertTrue(control.benchmarkStepTimings.isEmpty)
                XCTAssertEqual(Set(measured.benchmarkStepTimings.keys), Set([
                    "commandAndFeelBefore", "simulation", "diagnosticsAndCommandLog", "reactions",
                    "hudCaptionsQuietFeel", "audioAndCaptionBoard", "awarenessSnapshotAndHint", "terminalReceipt"
                ]))
                measurements.append(["tick": tick, "measuredFirst": measuredFirst,
                                     "seconds": measured.benchmarkStepTimings])
            }
            XCTAssertEqual(measured.commandLog, control.commandLog)
        }
        let data = try JSONSerialization.data(withJSONObject: measurements, options: [.prettyPrinted, .sortedKeys])
        let attachment = XCTAttachment(data: data, uniformTypeIdentifier: "public.json")
        attachment.name = "BP008-session-step-stage-timings"
        attachment.lifetime = .keepAlways; add(attachment)
    }

    func testSharedProjectedPlayerTraversal() async throws {
        let facing = ClipFrameLibrary.direction(forFacing: VecQ8(unitsX: -1, unitsY: -1))
        var preflight = try Simulation.make(seed: 1)
        preflight.testing_setPlayerPosition(VecI(x: 736, y: 654))
        var expected: [VecQ8] = []
        for tick in 1...90 {
            let before = preflight.state.player.position
            let axis: Int16 = tick <= 75 ? -PlayerCommand.axisMaximum : 0
            _ = preflight.step(command: PlayerCommand(tick: UInt64(tick), moveX: axis, moveY: axis, dodgePressed: false))
            let after = preflight.state.player.position
            if tick <= 75 {
                XCTAssertLessThan(after.x.raw, before.x.raw)
                XCTAssertEqual(after.x.raw - before.x.raw, after.y.raw - before.y.raw)
            }
            expected.append(after)
        }
        let bundle = Bundle(for: Self.self)
        func texture(_ name: String) throws -> SKTexture {
            let url = try XCTUnwrap(bundle.url(forResource: name, withExtension: "png"))
            let image = try XCTUnwrap(UIImage(contentsOfFile: url.path))
            let texture = SKTexture(image: image); texture.filteringMode = .linear; return texture
        }
        let paths = (0..<16).map { String(format: "player-source-s-%02d", $0) }
        let textures = try paths.map(texture)
        // Explicit pilot alias: this world diagonal projects toward the viewer.
        // It is not a new source facing or production metadata migration.
        let ids = (0..<16).map { String(format: "player_move_%@_%02d", facing, $0) }
        let clip = ClipFrameLibrary.Clip(clipId: "player_move", actorRole: "player", directions: [facing],
            framesPerSecond: nil,
            authoredTiming: try ClipTiming(unitsPerSecond: 32, frameUnits: Array(repeating: 1, count: 16)),
            loop: true, anchor: VecI(x: 32, y: 56), frameIds: ids)
        // Build one isolated review library containing the player pilot and the
        // six existing camera timing contracts; no bundled delivery is modified.
        let cameraCandidates = try CameraPlaybackTests.candidateFrames()
        let bundled = try ClipFrameLibrary.bundled()
        var reviewClips = ["player_move": clip]
        var delivered = Dictionary(uniqueKeysWithValues: zip(ids, paths))
        var reviewTextures = Dictionary(uniqueKeysWithValues: zip(paths, textures))
        for (name, candidates) in cameraCandidates {
            let cameraClip = try XCTUnwrap(bundled.clip(name))
            let cameraPaths = try XCTUnwrap(bundled.deliveredFrames(clipId: name, direction: nil))
            XCTAssertEqual(cameraClip.frameIds.count, cameraPaths.count)
            XCTAssertEqual(cameraPaths.count, candidates.count)
            reviewClips[name] = cameraClip
            for (id, path) in zip(cameraClip.frameIds, cameraPaths) { delivered[id] = path }
            for (path, candidate) in zip(cameraPaths, candidates) { reviewTextures[path] = candidate }
        }
        let frames = ClipFrameLibrary(clips: reviewClips, deliveredPaths: delivered)
        for (zoom, tracking): (CGFloat, Bool) in [(1, false), (1.25, false), (1.25, true)] {
        for reduced in [false, true] {
            let library = try XCTUnwrap(SpriteLibrary(benchmarkFrames: frames, benchmarkTextures: reviewTextures))
            let renderer = WorldRenderer(sprites: library)
            var art = BenchmarkReviewArt(player: textures[0], camera: try texture("camera"),
                building: .init(texture: try texture("building-constrained"),
                    size: CGSize(width: 1254 * 128 * sqrt(2.0) / 934, height: 1254 * 128 * sqrt(2.0) / 934),
                    anchor: CGPoint(x: 653.0 / 1254, y: 1 - 1152.0 / 1254), position: CGPoint(x: 512, y: 640)),
                buildingID: "solid-03-transit-kiosk",
                props: [.init(texture: try texture("newsbox"), size: CGSize(width: 20, height: 40),
                              anchor: CGPoint(x: 0.5, y: 0), position: CGPoint(x: 691, y: 639)),
                        .init(texture: try texture("tree"), size: CGSize(width: 50, height: 85),
                              anchor: CGPoint(x: 0.5, y: 0), position: CGPoint(x: 858, y: 780))],
                paving: try XCTUnwrap(EnvironmentTextures().texture(assetId: "env_ground_plaza")))
            art.configureStreetCorner(asphalt: try XCTUnwrap(EnvironmentTextures().texture(assetId: "env_ground_asphalt")))
            art.playerPresentation = .selectedClip
            renderer.installBenchmarkArt(art)
            XCTAssertTrue(renderer.installBenchmarkCameraFrames(cameraCandidates))
            renderer.benchmarkPlayerRegistration = (CGSize(width: 64, height: 416.0 / 6.0),
                CGPoint(x: 0.5, y: 1 - 336.0 / 416.0))
            let scene = try SharedTraversalScene(size: CGSize(width: 704, height: 326), renderer: renderer,
                textures: textures, reduced: reduced, magnification: zoom, tracksPlayer: tracking)
            let windowScene = try XCTUnwrap(UIApplication.shared.connectedScenes.compactMap { $0 as? UIWindowScene }.first)
            let window = UIWindow(windowScene: windowScene)
            window.frame = CGRect(x: 0, y: 0, width: 704, height: 326)
            window.windowLevel = UIWindow.Level(rawValue: UIWindow.Level.alert.rawValue + 1)
            let controller = UIViewController(), view = SKView(frame: window.bounds)
            controller.view = view; window.rootViewController = controller; window.makeKeyAndVisible()
            view.preferredFramesPerSecond = 60
            var preload = Array(reviewTextures.values)
            for (path, texture) in zip(paths, textures) {
                let url = try XCTUnwrap(bundle.url(forResource: path, withExtension: "png"))
                let image = try XCTUnwrap(UIImage(contentsOfFile: url.path)?.cgImage)
                preload.append(try XCTUnwrap(renderer.prepareBenchmarkPlayerOutline(texture: texture,
                    image: image, size: CGSize(width: 64, height: 416.0 / 6.0))))
            }
            // Construct scene resources before its simulation clock starts.
            scene.update(0); scene.previous = nil
            scene.enumerateChildNodes(withName: "//*") { node, _ in
                if let texture = (node as? SKSpriteNode)?.texture { preload.append(texture) }
            }
            await withCheckedContinuation { (continuation: CheckedContinuation<Void, Never>) in
                // SpriteKit may complete on its loading queue. Capture only the
                // Sendable continuation, not this test's MainActor isolation.
                SKTexture.preload(preload) { @Sendable in continuation.resume() }
            }
            renderer.resetBenchmarkOutlineMetrics()
            let complete = expectation(description: "shared projected traversal")
            scene.done = { complete.fulfill() }; view.presentScene(scene)
            await fulfillment(of: [complete], timeout: 30)
            view.presentScene(nil); window.isHidden = true
            XCTAssertEqual(scene.worldTrace, expected, "Presentation must preserve every simulated step")
            XCTAssertEqual(scene.session.simulation.state.digest(), preflight.state.digest())
            XCTAssertEqual(renderer.benchmarkOutlineMetrics.readbacks, 0)
            XCTAssertEqual(scene.seen.count, 16)
            let moving = scene.records.filter { ($0["frame"] as? Int ?? -1) >= 0 }
            for record in moving {
                if tracking { XCTAssertEqual(record["playerCanvasVisible"] as? Bool, true) }

                XCTAssertEqual(record["worldFacing"] as? String, facing)
                XCTAssertEqual(record["selectedClip"] as? String, "player_move|\(facing)")
                let x = Double(try XCTUnwrap(record["presentationX"] as? CGFloat))
                let y = Double(try XCTUnwrap(record["presentationY"] as? CGFloat))
                let r = sqrt(0.5)
                XCTAssertEqual(Double(try XCTUnwrap(record["renderedX"] as? CGFloat)), 706 + r * (x - 706 - y + 644), accuracy: 0.001)
                XCTAssertEqual(Double(try XCTUnwrap(record["renderedY"] as? CGFloat)), 644 + r * (x - 706 + y - 644) / 2, accuracy: 0.001)
            }
            let data = try JSONSerialization.data(withJSONObject: scene.records, options: [.prettyPrinted, .sortedKeys])
            let attachment = XCTAttachment(data: data, uniformTypeIdentifier: "public.json")
            attachment.name = "BP008-shared-traversal-zoom-\(zoom)-tracking-\(tracking)-reduced-\(reduced)-records"
            attachment.lifetime = .keepAlways; add(attachment)
            for (frame, image) in scene.images {
                let attachment = XCTAttachment(image: image)
                attachment.name = "BP008-shared-traversal-zoom-\(zoom)-tracking-\(tracking)-reduced-\(reduced)-frame-\(frame)"
                attachment.lifetime = .keepAlways; add(attachment)
            }
        }
        }
    }

    func testSharedReviewArtPreservesSelectedPlayerClips() throws {
        let library = SpriteLibrary()
        let still = try XCTUnwrap(library.firstTexture(clipId: "player_idle", direction: "s"))
        for reduced in [false, true] {
            for state in ["player_move", "player_idle", "player_dodge", "hurt", "missing-direction"] {
                let control = WorldRenderer(sprites: library)
                let shared = WorldRenderer(sprites: library)
                var art = BenchmarkReviewArt(player: still, camera: still,
                    building: .init(texture: still, size: CGSize(width: 10, height: 10),
                                    anchor: .zero, position: .zero),
                    buildingID: "unused", props: [], paving: still)
            art.playerPresentation = .selectedClip
                shared.installBenchmarkArt(art)
                var snap = PresentationSnapshot(try Simulation.make(seed: 1).state)
                snap.playerClipId = state == "hurt" || state == "missing-direction" ? "player_move" : state
                snap.playerDirection = state == "missing-direction" ? "unsupported" : "s"
                if state == "hurt" {
                    snap.playerReactionClipId = "player_hurt"
                    snap.playerReactionOccurrence = ClipOccurrence(direction: "w", startTick: 100)
                    snap.tick = 106
                }
                for _ in 0..<2 {
                    control.render(snap, reducedMotion: reduced)
                    shared.render(snap, reducedMotion: reduced)
                    let expected = control.root.childNode(withName: "//sprite-player") as? SKSpriteNode
                    let actual = shared.root.childNode(withName: "//sprite-player") as? SKSpriteNode
                    XCTAssertEqual(actual != nil, expected != nil, state)
                    if let expected, let actual {
                        XCTAssertTrue(actual.texture === expected.texture, state)
                        XCTAssertEqual(actual.hasActions(), expected.hasActions(), state)
                        XCTAssertEqual(actual.size, expected.size, state)
                        XCTAssertEqual(actual.anchorPoint, expected.anchorPoint, state)
                    }
                    XCTAssertEqual(shared.observePlayerPlayback()?.clipToken,
                                   control.observePlayerPlayback()?.clipToken, state)
                }
                // Default static composition remains available as its own control.
                art.playerPresentation = .staticComposition
                shared.installBenchmarkArt(art)
                shared.render(snap, reducedMotion: reduced)
                let staticPlayer = try XCTUnwrap(shared.root.childNode(withName: "//sprite-player") as? SKSpriteNode)
                XCTAssertTrue(staticPlayer.texture === still)
                XCTAssertFalse(staticPlayer.hasActions())
            }
        }
    }

    func testDistanceCandidatePreservesSelectedInterruptions() throws {
        let library = SpriteLibrary()
        let scene = try PlayerCandidateScene(size: CGSize(width: 704, height: 326),
            library: library, paths: [], axis: PlayerCommand.axisMaximum,
            reducedMotion: false, stage: 4)
        let candidate = try XCTUnwrap(library.firstTexture(clipId: "player_move", direction: "s"))
        scene.candidateTextures = Array(repeating: candidate, count: 16)
        for reduced in [false, true] {
            for clip in ["player_idle", "player_dodge", "player_defeat", "player_complete"] {
                var snap = PresentationSnapshot(try Simulation.make(seed: 1).state)
                snap.playerClipId = clip; snap.playerDirection = "s"
                scene.renderer.render(snap, reducedMotion: reduced)
                let node = try XCTUnwrap(scene.renderer.root.childNode(withName: "//sprite-player") as? SKSpriteNode)
                let texture = node.texture; let actions = node.hasActions()
                XCTAssertFalse(scene.applyDistanceFrameIfSelected(), clip)
                XCTAssertTrue(node.texture === texture, clip)
                XCTAssertEqual(node.hasActions(), actions, clip)
            }
            var snap = PresentationSnapshot(try Simulation.make(seed: 1).state)
            snap.playerClipId = "player_move"; snap.playerDirection = "s"
            snap.playerReactionClipId = "player_hurt"
            snap.playerReactionOccurrence = ClipOccurrence(direction: "w", startTick: 100)
            snap.tick = 106
            scene.renderer.render(snap, reducedMotion: reduced)
            let node = try XCTUnwrap(scene.renderer.root.childNode(withName: "//sprite-player") as? SKSpriteNode)
            let reaction = node.texture
            XCTAssertFalse(scene.applyDistanceFrameIfSelected())
            XCTAssertTrue(node.texture === reaction)
            snap.playerReactionClipId = nil; snap.playerReactionOccurrence = nil
            snap.playerDirection = "n"
            scene.renderer.render(snap, reducedMotion: reduced)
            let reversed = node.texture
            XCTAssertFalse(scene.applyDistanceFrameIfSelected())
            XCTAssertTrue(node.texture === reversed)
            snap.playerDirection = "s"
            scene.renderer.render(snap, reducedMotion: reduced)
            XCTAssertTrue(scene.applyDistanceFrameIfSelected())
            XCTAssertTrue(node.texture === candidate)
        }
    }

    func testDistancePhaseCandidateAtAllInputLevels() async throws {
        for reduced in [false, true] {
            for axis in [PlayerCommand.axisMaximum, PlayerCommand.axisMaximum / 2, PlayerCommand.axisMaximum / 4] {
                // Same legal 120-tick route length, extended duration for partial input.
                let ticks = UInt64(120 * Int(PlayerCommand.axisMaximum) / Int(axis))
                try await capturePlayerCycle(axis: axis, reducedMotion: reduced,
                    repetition: 21, cleanSilhouetteReview: true, moveTicks: ticks)
                try await capturePlayerCycle(axis: axis, reducedMotion: reduced,
                    repetition: 20, cleanSilhouetteReview: true,
                    distancePhaseComparison: true, moveTicks: ticks)
            }
        }
    }

    func testPlayerPreparationStageComparison() async throws {
        // Controls report coverage; the four final-mode tests below retain strict gates.
        for repetition in 1...2 {
            for stage in 3...4 {
                try await capturePlayerCycle(axis: PlayerCommand.axisMaximum, reducedMotion: false,
                    stage: stage, repetition: repetition, requireCoverage: false)
            }
        }
    }
    private func capturePlayerCycle(axis: Int16, reducedMotion: Bool, stage: Int = 4,
                                    repetition: Int = 0, requireCoverage: Bool = true,
                                    cleanSilhouetteReview: Bool = false,
                                    distancePhaseComparison: Bool = false,
                                    moveTicks: UInt64 = 120, interruptionRoute: Bool = false) async throws {
        // Route is a test initial condition within the real arena; no speed or solid edits.
        var preflight = try Simulation.make(seed: 1)
        preflight.testing_setPlayerPosition(VecI(x: 224, y: 704))
        var preflightY: [Int64] = []
        var blocked = false, slid = false, dodged = false
        for tick in 1...moveTicks {
            let before = preflight.state.player.position
            let command = interruptionRoute ? Self.interruptionCommand(tick: tick)
                : PlayerCommand(tick: tick, moveX: 0, moveY: -axis, dodgePressed: false)
            _ = preflight.step(command: command)
            let after = preflight.state.player.position
            if interruptionRoute {
                if tick <= 30 && before == after { blocked = true }
                if (31...60).contains(tick) && before.x == after.x && before.y != after.y { slid = true }
                dodged = dodged || preflight.state.player.dodgeActiveRemaining > 0
            } else {
                XCTAssertEqual(after.x, before.x)
                XCTAssertLessThan(after.y.raw, before.y.raw,
                                  "Every measured move tick must travel on the preflighted route")
            }
            preflightY.append(after.y.raw)
        }
        if interruptionRoute {
            XCTAssertTrue(blocked, "Must actually stop against the real western solid")
            XCTAssertTrue(slid, "Must actually slide tangentially along that solid")
            XCTAssertTrue(dodged, "Dodge command must activate authoritative Dodge")
        }

        let bundle = Bundle(for: Self.self)
        let paths = (0..<16).map { String(format: "player-source-s-%02d", $0) }
        var textures: [String: SKTexture] = [:]
        var sourceImages: [String: CGImage] = [:]
        for path in paths {
            let url = try XCTUnwrap(bundle.url(forResource: path, withExtension: "png"))
            let image = try XCTUnwrap(UIImage(contentsOfFile: url.path))
            sourceImages[path] = try XCTUnwrap(image.cgImage)
            let texture = SKTexture(image: image)
            XCTAssertEqual(texture.size(), CGSize(width: 384, height: 416))
            texture.filteringMode = .linear; textures[path] = texture
        }
        let ids = (0..<16).map { String(format: "player_move_s_%02d", $0) }
        let clip = ClipFrameLibrary.Clip(clipId: "player_move", actorRole: "player",
            directions: ["s"], framesPerSecond: nil,
            authoredTiming: try ClipTiming(unitsPerSecond: 32, frameUnits: Array(repeating: 1, count: 16)),
            loop: true, anchor: VecI(x: 32, y: 56), frameIds: ids)
        let frames = ClipFrameLibrary(clips: ["player_move": clip],
            deliveredPaths: Dictionary(uniqueKeysWithValues: zip(ids, paths)))
        XCTAssertNil(SpriteLibrary(benchmarkFrames: frames, benchmarkTextures: [:]))
        let library = try XCTUnwrap(SpriteLibrary(benchmarkFrames: frames, benchmarkTextures: textures))
        let windowScene = try XCTUnwrap(UIApplication.shared.connectedScenes.compactMap { $0 as? UIWindowScene }.first)
        let window = UIWindow(windowScene: windowScene)
        window.frame = CGRect(x: 0, y: 0, width: 704, height: 326)
        window.windowLevel = UIWindow.Level(rawValue: UIWindow.Level.alert.rawValue + 1)
        let controller = UIViewController(), view = SKView(frame: window.bounds)
        controller.view = view; window.rootViewController = controller; window.makeKeyAndVisible()
        view.preferredFramesPerSecond = 60
        let scene = try PlayerCandidateScene(size: view.bounds.size, library: library, paths: paths,
                                            axis: axis, reducedMotion: reducedMotion, stage: stage)
        scene.cleanSilhouetteReview = cleanSilhouetteReview
        scene.distancePhaseComparison = distancePhaseComparison
        scene.reviewLabel = "BP008 \(distancePhaseComparison ? "DISTANCE" : "CADENCE") input=\(axis) reduced=\(reducedMotion) rep=\(repetition)"
        scene.candidateTextures = paths.compactMap { textures[$0] }
        scene.moveTicks = moveTicks
        scene.interruptionRoute = interruptionRoute
        let preparationBegan = CFAbsoluteTimeGetCurrent()
        var preloadTextures = paths.compactMap { textures[$0] }
        if stage >= 3 {
            for path in paths {
                let mask = try XCTUnwrap(scene.renderer.prepareBenchmarkPlayerOutline(
                    texture: try XCTUnwrap(textures[path]), image: try XCTUnwrap(sourceImages[path]),
                    size: CGSize(width: 64, height: 416.0 / 6.0)))
                preloadTextures.append(mask)
            }
            XCTAssertEqual(scene.renderer.benchmarkOutlineMetrics.readbacks, 0)
        }
        var scenePreparationSeconds = 0.0
        if stage >= 4 {
            let began = CFAbsoluteTimeGetCurrent()
            scene.configureScene()
            // Construct actual initial scene resources before the simulation clock starts.
            scene.renderer.render(scene.session.snapshot, reducedMotion: reducedMotion)
            scenePreparationSeconds = CFAbsoluteTimeGetCurrent() - began
            scene.renderer.root.enumerateChildNodes(withName: "//*") { node, _ in
                if let texture = (node as? SKSpriteNode)?.texture { preloadTextures.append(texture) }
            }
        }
        if stage >= 2 {
            await withCheckedContinuation { (continuation: CheckedContinuation<Void, Never>) in
                // Explicit on older SDKs that do not import this block as Sendable.
                SKTexture.preload(preloadTextures) { @Sendable in continuation.resume() }
            }
        }
        let preparationSeconds = CFAbsoluteTimeGetCurrent() - preparationBegan
        scene.renderer.resetBenchmarkOutlineMetrics()
        let complete = expectation(description: "revised player live action and travel capture")
        scene.done = { complete.fulfill() }
        view.presentScene(scene)
        defer { view.presentScene(nil); window.isHidden = true }
        await fulfillment(of: [complete], timeout: 45)
        // D-069: locomotion may retain the same clip under Reduced Motion.
        if requireCoverage {
            XCTAssertEqual(scene.seenPaths.count, 16,
                           "Normal playback must actually display every source texture")
        }
        XCTAssertEqual(scene.snapshotBuildCount, scene.frameCosts.count,
                       "Telemetry must reuse the exact snapshot rendered by each callback")
        let metrics = scene.renderer.benchmarkOutlineMetrics
        if stage >= 3 { XCTAssertEqual(metrics.readbacks, 0, "Prepared candidate must not read textures back during playback") }
        let summary: [String: Any] = ["stage": stage, "repetition": repetition, "axis": axis,
            "reducedMotion": reducedMotion, "cleanSilhouetteReview": cleanSilhouetteReview,
            "distancePhaseComparison": distancePhaseComparison, "moveTicks": moveTicks,
            "frames": scene.seenPaths.count,
            "coveragePassed": scene.seenPaths.count == 16, "preparationSeconds": preparationSeconds, "scenePreparationSeconds": scenePreparationSeconds,
            "initialDisplaySeconds": scene.initialDisplaySeconds,
            "frameCosts": scene.frameCosts,
            "simulationSeconds": scene.simulationSeconds, "renderSeconds": scene.renderSeconds,
            "postActionSeconds": scene.postActionSeconds, "diagnosticSeconds": scene.diagnosticSeconds,
            "snapshotBuildCount": scene.snapshotBuildCount, "outlineHits": metrics.hits,
            "outlineMisses": metrics.misses, "outlineReadbacks": metrics.readbacks,
            "outlineBuildSeconds": metrics.buildSeconds, "outlineBytes": scene.renderer.benchmarkOutlineBytes]
        let measurement = XCTAttachment(data: try JSONSerialization.data(withJSONObject: summary, options: [.prettyPrinted, .sortedKeys]), uniformTypeIdentifier: "public.json")
        measurement.name = "BP008-stage-\(stage)-rep-\(repetition)-axis-\(axis)-reduced-\(reducedMotion)-metrics"
        measurement.lifetime = .keepAlways; add(measurement)
        XCTAssertEqual(scene.session.simulation.state.player.position.y.raw, preflightY.last)
        XCTAssertEqual(scene.session.simulation.state.player.position.x, preflight.state.player.position.x)
        if interruptionRoute {
            let paused = scene.records.filter { $0["reviewPaused"] as? Bool == true }
            XCTAssertGreaterThan(paused.count, 2)
            XCTAssertEqual(Set(paused.compactMap { $0["tick"] as? UInt64 }), Set([UInt64(120)]))
            XCTAssertEqual(Set(paused.compactMap { $0["sourceFrameIndex"] as? Int }).count, 1)
            XCTAssertTrue(scene.records.contains { ($0["facing"] as? String) == "n" && ($0["candidateAvailable"] as? Bool) == false })
            XCTAssertTrue(scene.records.contains { ($0["clip"] as? String) == "player_dodge" && ($0["candidateAvailable"] as? Bool) == false })
        }
        let movingRecords = scene.records.filter { $0["sourceFrameIndex"] != nil }
        let wraps = zip(movingRecords, movingRecords.dropFirst()).filter {
            ($0.0["sourceFrameIndex"] as? Int ?? 0) > ($0.1["sourceFrameIndex"] as? Int ?? 0)
        }.count
        XCTAssertGreaterThanOrEqual(wraps, 2, "Repeated live cycles required")
        XCTAssertGreaterThan(Set(scene.records.compactMap { $0["authoritativeRawY"] as? Int64 }).count, 1)
        XCTAssertEqual(scene.records.first?["tick"] as? UInt64, 0)
        XCTAssertEqual(scene.records.first?["clip"] as? String, "player_idle")
        XCTAssertEqual(scene.records.first?["facing"] as? String, "e")
        let lastMovingTick = try XCTUnwrap(scene.records.filter { $0["sourceFrameIndex"] != nil }
            .compactMap { $0["tick"] as? UInt64 }.max())
        XCTAssertTrue(scene.records.contains { ($0["tick"] as? UInt64 ?? 0) > lastMovingTick
            && $0["candidateAvailable"] as? Bool == false && $0["clip"] as? String == "player_idle" })
        for record in scene.records where record["sourceFrameIndex"] != nil {
            XCTAssertEqual(record["facing"] as? String, "s")
            XCTAssertEqual(record["clip"] as? String, "player_move|s")
            XCTAssertEqual(try XCTUnwrap(record["width"] as? CGFloat), CGFloat(64))
            XCTAssertEqual(try XCTUnwrap(record["height"] as? CGFloat), CGFloat(Float(416.0 / 6.0)))
            let rawY = try XCTUnwrap(record["authoritativeRawY"] as? Int64)
            let renderedY = try XCTUnwrap(record["renderedY"] as? CGFloat)
            XCTAssertEqual(Double(renderedY), Double(rawY) / 512, accuracy: 0.51,
                           "Whole-unit presentation rounding must remain bounded")
        }
        for (name, image) in scene.images {
            let attachment = XCTAttachment(image: image); attachment.name = name
            attachment.lifetime = .keepAlways; add(attachment)
        }
        let data = try JSONSerialization.data(withJSONObject: scene.records, options: [.prettyPrinted, .sortedKeys])
        let attachment = XCTAttachment(data: data, uniformTypeIdentifier: "public.json")
        attachment.name = "BP008-stage-\(stage)-rep-\(repetition)-axis-\(axis)-reduced-\(reducedMotion)-post-action-records"
        attachment.lifetime = .keepAlways; add(attachment)
    }

    final class CameraCandidateScene: SKScene {
        let renderer = WorldRenderer()
        var snapshot: PresentationSnapshot
        let candidates: [String: [SKTexture]]
        var stage = 0
        var began: TimeInterval?
        var now: TimeInterval = 0
        var done: (() -> Void)?
        var records: [[String: Any]] = []
        var settled: [Bool] = []
        var observedIdleFrames: Set<String> = []
        var images: [UIImage] = []
        let clips = ["camera_operational_idle", "camera_hit", "camera_critical_enter", "camera_destroyed_idle"]
        init(size: CGSize, snapshot: PresentationSnapshot, candidates: [String: [SKTexture]]) {
            self.snapshot = snapshot
            self.candidates = candidates
            super.init(size: size)
            self.snapshot.cameras = Array(snapshot.cameras.prefix(1))
            addChild(renderer.root)
        }
        required init?(coder: NSCoder) { fatalError("init(coder:) is unsupported") }
        override func update(_ time: TimeInterval) {
            guard stage < 4 else { return }
            now = time
            if began == nil { began = time }
            snapshot.cameras[0].integrity = 3 - stage
            snapshot.cameras[0].fieldVisible = stage < 3
            renderer.render(snapshot)
        }
        override func didEvaluateActions() {
            guard stage < 4, let began,
                let node = renderer.root.childNode(withName: "//sprite-camera-\(snapshot.cameras[0].id.raw)") as? SKSpriteNode else { return }
            let actual = candidates.keys.sorted().flatMap { clip in
                candidates[clip]!.enumerated().compactMap { index, texture in
                    node.texture === texture ? "\(clip)#\(index + 1)" : nil
                }
            }.first ?? "unidentified"
            records.append(["integrity": 3-stage, "displayTime": now, "actualFrame": actual,
                "x": node.position.x, "y": node.position.y,
                "fieldPresent": renderer.root.childNode(withName: "//field-\(snapshot.cameras[0].id.raw)") != nil])
            if stage == 0, actual != "unidentified" { observedIdleFrames.insert(actual) }
            // #127: elapsed time alone cannot establish displayed frame progress.
            // Keep real actions running until both forms of evidence exist.
            let complete = stage == 0 ? now-began >= 0.8 && observedIdleFrames.count > 1
                : !node.hasActions() && now-began > 0.05
            if complete {
                settled.append(stage == 0 || node.texture === candidates[clips[stage]]?.last)
                if let texture = view?.texture(from: node) { images.append(UIImage(cgImage: texture.cgImage())) }
                stage += 1
                self.began = nil
                if stage == 4 { done?() }
            }
        }
    }

    func testCameraCandidatesActuallyPlayAndSettleInPresentedScene() async throws {
        let candidates = try CameraPlaybackTests.candidateFrames()
        let snapshot = PresentationSnapshot(try Simulation.make(seed: 1).state)
        let window = UIWindow(frame: CGRect(x: 0, y: 0, width: 704, height: 326))
        let controller = UIViewController()
        let view = SKView(frame: window.bounds)
        controller.view = view; window.rootViewController = controller; window.makeKeyAndVisible()
        let scene = CameraCandidateScene(size: view.bounds.size, snapshot: snapshot, candidates: candidates)
        XCTAssertTrue(scene.renderer.installBenchmarkCameraFrames(candidates))
        let complete = expectation(description: "candidate camera clips finish under SpriteKit")
        scene.done = { complete.fulfill() }
        view.presentScene(scene)
        defer { view.presentScene(nil); window.isHidden = true }
        await fulfillment(of: [complete], timeout: 30)
        XCTAssertEqual(scene.settled, [true, true, true, true])
        XCTAssertEqual(scene.images.count, 4)
        XCTAssertFalse(scene.records.contains { $0["actualFrame"] as? String == "unidentified" })
        let idleFrames = scene.records.filter { $0["integrity"] as? Int == 3 }.compactMap { $0["actualFrame"] as? String }
        XCTAssertGreaterThan(Set(idleFrames).count, 1)
        XCTAssertTrue(scene.records.filter { $0["integrity"] as? Int == 0 }.allSatisfy { $0["fieldPresent"] as? Bool == false })
        for (index, image) in scene.images.enumerated() {
            let attachment = XCTAttachment(image: image)
            attachment.name = "BP004-candidate-integrity-\(3-index)"
            attachment.lifetime = .keepAlways; add(attachment)
        }
        let data = try JSONSerialization.data(withJSONObject: scene.records, options: [.prettyPrinted, .sortedKeys])
        let attachment = XCTAttachment(data: data, uniformTypeIdentifier: "public.json")
        attachment.name = "BP004-candidate-post-action-records"
        attachment.lifetime = .keepAlways; add(attachment)
    }

}
#endif
