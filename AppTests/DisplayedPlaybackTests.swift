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

    /// Isolated ground/contact comparison, not a full benchmark encounter.
    final class PlayerCandidateScene: SKScene {
        let renderer: WorldRenderer
        let session = GameSession(seed: 1)
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

        init(size: CGSize, library: SpriteLibrary, paths: [String]) {
            renderer = WorldRenderer(sprites: library)
            self.paths = paths
            super.init(size: size)
        }
        required init?(coder: NSCoder) { fatalError("init(coder:) unsupported") }
        override func didMove(to view: SKView) {
            addChild(renderer.root)
            renderer.root.yScale = 0.5
            upright.name = "player-source-wrapper"; upright.yScale = 2
            renderer.root.children[WorldRenderer.Layer.actors.rawValue].addChild(upright)
            let camera = SKCameraNode(); addChild(camera); self.camera = camera
            session.moveY = -PlayerCommand.axisMaximum
        }
        override func update(_ time: TimeInterval) {
            guard !finished else { return }
            now = time
            if let previousTime { accumulator += min(time - previousTime, 0.25) }
            previousTime = time
            while accumulator >= 1.0 / 60.0 {
                session.step(); accumulator -= 1.0 / 60.0
            }
            let snap = session.snapshot
            renderer.render(snap, reducedMotion: false)
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
        override func didEvaluateActions() {
            guard !finished else { return }
            // #130: completion and missing-frame evidence cannot depend on move art.
            defer {
                if session.simulation.state.tick >= 90 && seenPaths.count > 1 {
                    finished = true; done?()
                }
            }
            guard let observed = renderer.observePlayerPlayback(),
                  let path = observed.deliveredPath, let frame = paths.firstIndex(of: path),
                  let player = renderer.root.childNode(withName: "//sprite-player"),
                  let parent = player.parent else {
                records.append(["displayTime": now, "tick": session.simulation.state.tick,
                    "facing": session.snapshot.playerDirection, "clip": session.snapshot.playerClipId,
                    "candidateAvailable": false])
                return
            }
            let position = session.simulation.state.player.position
            let projected = convert(player.position, from: parent)
            var record: [String: Any] = [
                "displayTime": now, "tick": session.simulation.state.tick,
                "authoritativeRawX": position.x.raw, "authoritativeRawY": position.y.raw,
                "renderedX": projected.x, "renderedY": projected.y,
                "framePath": path, "sourceFrameIndex": frame,
                "facing": session.snapshot.playerDirection,
                "clip": observed.clipToken ?? "unidentified",
                "width": observed.size.width, "height": observed.size.height,
                "anchorX": observed.anchor.x, "anchorY": observed.anchor.y,
                "groundYScale": 0.5, "artYScaleAfterParent": 1.0
            ]
            if !seenPaths.contains(path), let view, let camera,
               let texture = view.texture(from: self, crop: CGRect(
                   x: camera.position.x - 352, y: camera.position.y - 163, width: 704, height: 326)) {
                let name = "BP008-player-source-frame-\(frame)-tick-\(session.simulation.state.tick)"
                images.append((name, UIImage(cgImage: texture.cgImage())))
                record["imageAttachment"] = name
                seenPaths.insert(path)
            }
            records.append(record)
        }
    }

    func testRevisedPlayerSourcePlaysWithProjectedSimulationTravel() async throws {
        let bundle = Bundle(for: Self.self)
        let paths = (0..<16).map { String(format: "player-source-s-%02d", $0) }
        var textures: [String: SKTexture] = [:]
        for path in paths {
            let url = try XCTUnwrap(bundle.url(forResource: path, withExtension: "png"))
            let image = try XCTUnwrap(UIImage(contentsOfFile: url.path))
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
        let window = UIWindow(frame: CGRect(x: 0, y: 0, width: 704, height: 326))
        let controller = UIViewController(), view = SKView(frame: window.bounds)
        controller.view = view; window.rootViewController = controller; window.makeKeyAndVisible()
        let scene = PlayerCandidateScene(size: view.bounds.size, library: library, paths: paths)
        let complete = expectation(description: "revised player live action and travel capture")
        scene.done = { complete.fulfill() }
        view.presentScene(scene)
        defer { view.presentScene(nil); window.isHidden = true }
        await fulfillment(of: [complete], timeout: 45)
        XCTAssertGreaterThan(scene.seenPaths.count, 1)
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
        attachment.name = "BP008-revised-player-post-action-records"
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
