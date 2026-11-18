#if DEBUG
import CryptoKit
import SpriteKit
import UIKit
import XCTest
@testable import SSRuntime
@testable import SurveillanceCore

/// BP-008/BP-009, accepted benchmark-faithful-scene slice8.
/// Existing shipping art only. No repaired-source or visual-acceptance claim.
@MainActor
final class ExistingArtTraversalTests: XCTestCase {
    private struct Leg {
        let name: String
        let end: UInt64
        let x: CGFloat
        let y: CGFloat
    }
    private let legs = [
        Leg(name: "quarter-west", end: 20, x: -0.25, y: 0),
        Leg(name: "half-west", end: 40, x: -0.5, y: 0),
        Leg(name: "approach-west", end: 55, x: -1, y: 0),
        Leg(name: "reverse-east", end: 75, x: 1, y: 0),
        Leg(name: "collision-west", end: 105, x: -1, y: 0),
        Leg(name: "slide-northwest", end: 155, x: -1, y: 1),
        Leg(name: "rear-west", end: 190, x: -1, y: 0),
        Leg(name: "rear-south-collision", end: 220, x: 0, y: -1),
        Leg(name: "return-east", end: 265, x: 1, y: 0),
        Leg(name: "front-south", end: 325, x: 0, y: -1),
        Leg(name: "front-west", end: 355, x: -1, y: 0),
        Leg(name: "release", end: 380, x: 0, y: 0)
    ]
    private let viewport = CGSize(width: 704, height: 326)
    private let start = VecI(x: 736, y: 654)
    private let kioskID = "solid-03-transit-kiosk"

    private func sha(_ data: Data) -> String {
        SHA256.hash(data: data).map { String(format: "%02x", $0) }.joined()
    }
    private func attach(_ data: Data, name: String, type: String) {
        let attachment = XCTAttachment(data: data, uniformTypeIdentifier: type)
        attachment.name = name
        attachment.lifetime = .keepAlways
        add(attachment)
    }
    /// Same actual-bundle inventory convention as ExistingArtEncounterTests.
    /// Superset of reachable resources, not per-pixel attribution or executed-code attestation.
    private func resourceInventory() throws -> [[String: Any]] {
        let catalog = try AssetCatalog.bundled()
        let eligible = Set(RuntimeBundleFilter.project(catalog: catalog,
            reachable: try RuntimeBundleFilter.reachableAssetIds()).bundleAssetIds)
        var result: [[String: Any]] = []
        for entry in catalog.entries.sorted(by: { $0.record.assetId < $1.record.assetId }) {
            guard eligible.contains(entry.record.assetId) else { continue }
            let path = try XCTUnwrap(entry.record.runtimePath, entry.record.assetId)
            let url = try XCTUnwrap(RuntimeAssetBundle.url(forFile: path), path)
            XCTAssertFalse(url.path.contains("/Sources/"), "Source fallback is not actual-bundle provenance")
            let bytes = try Data(contentsOf: url)
            result.append(["assetId": entry.record.assetId, "path": path,
                           "sha256": sha(bytes), "bytes": bytes.count])
        }
        XCTAssertFalse(result.isEmpty)
        return result
    }

    func testExistingArtLiveTraversalReversalCollisionPauseAndReducedMotion() async throws {
        let resources = try resourceInventory()
        var arms: [[String: Any]] = []
        for reduced in [false, true] { arms.append(try await captureRun(reduced: reduced)) }
        XCTAssertEqual(arms[0]["finalDigest"] as? String, arms[1]["finalDigest"] as? String,
                       "Presentation setting must not change the same authoritative command stream")
        let packet: [String: Any] = [
            "schema": "existing-art-traversal-001", "status": "DIAGNOSTIC_NOT_ACCEPTANCE",
            "testIdentity": "ExistingArtTraversalTests/testExistingArtLiveTraversalReversalCollisionPauseAndReducedMotion()",
            "viewportPoints": [704, 326], "seed": 1, "initialPosition": [start.x, start.y],
            "initialPositionIsTestFixture": true, "resourceInventory": resources,
            "resourceScope": "reachable runtime asset superset loaded from actual bundle; not per-pixel use or complete build-source attestation",
            "captureSemantics": "GameScene didEvaluateActions observer; shipping live tree and reversible midpoint post-action still of same chosen textures",
            "unsupported": ["coherent repaired scene", "source fidelity acceptance", "all sixteen poses or all facings",
                            "exhaustive front/rear/corner visible-pixel occlusion", "dodge", "physical device",
                            "display scanout or performance acceptance", "SwiftUI pause overlay"],
            "arms": arms]
        attach(try JSONSerialization.data(withJSONObject: packet, options: [.prettyPrinted, .sortedKeys]),
               name: "eat-records", type: "public.json")
    }

    private func captureRun(reduced: Bool) async throws -> [String: Any] {
        let arm = reduced ? "reduced" : "normal"
        var simulation = try Simulation.make(seed: 1)
        simulation.testing_setPlayerPosition(start)
        let session = GameSession(simulation: simulation)
        let initialDigest = session.simulation.state.digest()
        let window = UIWindow(frame: CGRect(origin: .zero, size: viewport))
        let controller = UIViewController()
        let view = SKView(frame: window.bounds)
        controller.view = view
        window.rootViewController = controller
        window.makeKeyAndVisible()
        let scene = GameScene(size: viewport, session: session)
        var settings = PresentationSettings.defaults
        settings.audio = .init(effectsEnabled: false, hapticsEnabled: false, musicEnabled: false)
        settings.ghostEnabled = false
        settings.vfx.reducedMotion = reduced
        scene.apply(settings: settings)
        let completed = expectation(description: "existing art \(arm) post-action traversal")
        var records: [[String: Any]] = []
        var captures: [[String: Any]] = []
        var textures: [ObjectIdentifier: (String, String, Data)] = [:]
        var finished = false
        var callbackFailure: Error?
        var lastTick: UInt64 = 0
        var lastPosition = start.asQ8
        var pauseLeft = 0
        var paused = false
        var pauseStarted = false
        var pauseDigest: String?
        var pauseTexture: String?
        var captured: Set<String> = []
        final class Finger {}
        let finger = Finger()
        let token = TouchController.TouchToken(id: ObjectIdentifier(finger))
        let terminal = try XCTUnwrap(legs.last).end

        func drive(nextTick: UInt64) throws {
            let layout = try XCTUnwrap(scene.controlLayout)
            scene.endTouch(token: token)
            guard let leg = legs.first(where: { nextTick < $0.end }), leg.x != 0 || leg.y != 0 else { return }
            _ = scene.beginTouch(token: token, atPoints: layout.stickCentre)
            scene.moveTouch(token: token, toPoints: CGPoint(
                x: layout.stickCentre.x + leg.x * layout.stickRadius,
                y: layout.stickCentre.y - leg.y * layout.stickRadius))
        }

        scene.benchmarkPlaybackObserver = { time, snap, position, observed, camera in
            guard !finished else { return }
            do {
                let sprite = try XCTUnwrap(scene.childNode(withName: "//sprite-player") as? SKSpriteNode)
                let texture = try XCTUnwrap(sprite.texture)
                let path = try XCTUnwrap(observed.deliveredPath, "Actual post-action texture must have a delivered source")
                let source = try XCTUnwrap(RuntimeAssetBundle.url(forFile: path), path)
                XCTAssertFalse(source.path.contains("/Sources/"))
                let identifier = ObjectIdentifier(texture)
                if textures[identifier] == nil {
                    let png = try XCTUnwrap(UIImage(cgImage: texture.cgImage()).pngData())
                    textures[identifier] = ("eat-\(arm)-texture-\(textures.count)", self.sha(png), png)
                }
                let selected = try XCTUnwrap(textures[identifier])
                let command = session.commandLog.last
                let commandTick = command?.tick ?? 0
                let leg = try XCTUnwrap(self.legs.first(where: { commandTick <= $0.end }))
                let digest = session.simulation.state.digest()
                let deltaX = position.x.raw - lastPosition.x.raw
                let deltaY = position.y.raw - lastPosition.y.raw
                let advanced = lastTick != snap.tick
                XCTAssertEqual(snap.player.x, position.x.unitsTruncated)
                XCTAssertEqual(snap.player.y, position.y.unitsTruncated)
                XCTAssertEqual(observed.position.x, CGFloat(snap.player.x))
                XCTAssertEqual(observed.position.y, CGFloat(snap.player.y))
                for solid in snap.solids {
                    XCTAssertFalse(Circle(center: position, radiusUnits: PlayerBody.radiusUnits).penetrates(solid),
                                   "Actual core position must not penetrate authoritative solid")
                }
                if paused {
                    XCTAssertEqual(snap.tick, 55)
                    XCTAssertEqual(digest, pauseDigest)
                    XCTAssertEqual(selected.1, pauseTexture, "Production pause must freeze the actual selected texture")
                    XCTAssertEqual(deltaX, 0)
                    XCTAssertEqual(deltaY, 0)
                }
                let body = Circle(center: position, radiusUnits: PlayerBody.radiusUnits)
                let box = snap.solids[try XCTUnwrap(snap.solidIds.firstIndex(of: self.kioskID))]
                var record: [String: Any] = [
                    "ordinal": records.count, "tick": snap.tick, "commandTick": commandTick,
                    "displayTime": time, "postActionUptime": ProcessInfo.processInfo.systemUptime,
                    "phase": paused ? "pause" : leg.name, "paused": paused, "advanced": advanced,
                    "rawX": position.x.raw, "rawY": position.y.raw,
                    "deltaRawX": deltaX, "deltaRawY": deltaY,
                    "snapshotX": snap.player.x, "snapshotY": snap.player.y,
                    "renderedX": observed.position.x, "renderedY": observed.position.y,
                    "cameraX": camera.x, "cameraY": camera.y,
                    "clip": observed.clipToken ?? "unidentified", "requestedClip": snap.playerClipId,
                    "facing": snap.playerDirection, "deliveredPath": path,
                    "sourceSHA256": self.sha(try Data(contentsOf: source)),
                    "textureAttachment": selected.0, "texturePNG_SHA256": selected.1,
                    "width": observed.size.width, "height": observed.size.height,
                    "anchorX": observed.anchor.x, "anchorY": observed.anchor.y,
                    "digest": digest, "commandCount": session.commandLog.count,
                    "moveX": command?.moveX ?? 0, "moveY": command?.moveY ?? 0,
                    "bodyRadius": body.radiusUnits, "reducedMotion": reduced,
                    "kioskBounds": [box.minX, box.minY, box.maxX, box.maxY],
                    "solidBounds": snap.solids.map { [$0.minX, $0.minY, $0.maxX, $0.maxY] },
                    "playerZ": sprite.zPosition, "playerHidden": sprite.isHidden, "playerAlpha": sprite.alpha,
                    "scenePoints": [scene.size.width, scene.size.height],
                    "viewportPoints": [view.bounds.width, view.bounds.height], "viewContentScale": view.contentScaleFactor]
                // Geometry relations are not visible-pixel occlusion or a collision proxy.
                record["kioskRelation"] = position.y.raw > Int64(box.maxY) * 256 ? "rear-side-world" :
                    (position.y.raw < Int64(box.minY) * 256 ? "front-side-world" : "side-world")
                let tag = paused ? "pause" : (snap.tick == leg.end ? leg.name : "")
                if !tag.isEmpty, captured.insert(tag).inserted {
                    let prefix = "eat-\(arm)-\(tag)"
                    let pair = try self.capturePair(scene: scene, view: view, name: prefix)
                    captures.append(contentsOf: pair)
                    record["captureNames"] = pair.map { $0["name"] as! String }
                }
                records.append(record)
                lastTick = snap.tick
                lastPosition = position
                if snap.tick == terminal {
                    finished = true
                    scene.setPaused(true)
                    completed.fulfill()
                    return
                }
                if paused {
                    pauseLeft -= 1
                    if pauseLeft == 0 {
                        scene.setPaused(false)
                        paused = false
                        try drive(nextTick: snap.tick)
                    }
                } else if snap.tick == 55, !pauseStarted {
                    pauseStarted = true
                    pauseLeft = 8
                    paused = true
                    pauseDigest = digest
                    pauseTexture = selected.1
                    scene.setPaused(true)
                } else {
                    try drive(nextTick: snap.tick)
                }
            } catch {
                callbackFailure = error
                finished = true
                scene.setPaused(true)
                completed.fulfill()
            }
        }
        view.presentScene(scene)
        defer {
            scene.benchmarkPlaybackObserver = nil
            scene.endTouch(token: token)
            view.presentScene(nil)
            window.isHidden = true
        }
        scene.skipIntroIfRunning()
        try drive(nextTick: 0)
        await fulfillment(of: [completed], timeout: 35)
        if let callbackFailure { throw callbackFailure }
        XCTAssertEqual(session.simulation.state.tick, terminal)
        XCTAssertEqual(session.commandLog.count, Int(terminal))
        XCTAssertEqual(records.filter { $0["paused"] as? Bool == true }.count, 8)
        XCTAssertEqual(captured, Set(legs.map(\.name) + ["pause"]))
        XCTAssertTrue(records.contains { ($0["moveX"] as? Int16 ?? 0) != 0 &&
            ($0["deltaRawX"] as? Int64) == 0 && ($0["advanced"] as? Bool) == true &&
            ($0["phase"] as? String) == "collision-west" }, "Require actual collision stop, not only intended path")
        XCTAssertTrue(records.contains { ($0["phase"] as? String) == "reverse-east" &&
            ($0["deltaRawX"] as? Int64 ?? 0) > 0 })
        XCTAssertTrue(records.contains { ($0["kioskRelation"] as? String) == "rear-side-world" })
        XCTAssertTrue(records.contains { ($0["kioskRelation"] as? String) == "front-side-world" })
        if !reduced {
            XCTAssertGreaterThan(Set(records.filter { ($0["requestedClip"] as? String) == "player_move" }
                .compactMap { $0["deliveredPath"] as? String }).count, 1,
                "Live normal playback must show multiple actual selected textures, not tick-derived frame guesses")
        }
        var replaySimulation = try Simulation.make(seed: 1)
        replaySimulation.testing_setPlayerPosition(start)
        let replay = GameSession(simulation: replaySimulation)
        replay.audioSettings = settings.audio
        var commands: [[String: Any]] = []
        for command in session.commandLog {
            replay.moveX = command.moveX
            replay.moveY = command.moveY
            replay.dodgePressed = command.dodgePressed
            replay.step()
            commands.append(["tick": command.tick, "moveX": command.moveX,
                             "moveY": command.moveY, "dodge": command.dodgePressed])
        }
        XCTAssertEqual(replay.simulation.state.digest(), session.simulation.state.digest())
        for (_, selected) in textures.sorted(by: { $0.value.0 < $1.value.0 }) {
            attach(selected.2, name: selected.0, type: "public.png")
        }
        return ["arm": arm, "reducedMotion": reduced, "records": records, "captures": captures,
                "initialDigest": initialDigest, "finalDigest": session.simulation.state.digest(),
                "replayDigest": replay.simulation.state.digest(), "commands": commands,
                "textureCount": textures.count, "expectedTerminalTick": terminal]
    }

    /// Vetted reversible projection pattern: ReferenceProjectionCaptureTests.capture, lines226-273.
    /// Action-selected textures are preserved. This extra midpoint still is not midpoint live display evidence.
    private func capturePair(scene: GameScene, view: SKView, name: String) throws -> [[String: Any]] {
        let camera = try XCTUnwrap(scene.camera)
        let center = camera.position
        let crop = CGRect(x: center.x - 352, y: center.y - 163, width: 704, height: 326)
        let digest = scene.session.simulation.state.digest()
        func capture(_ suffix: String) throws -> [String: Any] {
            let image = try XCTUnwrap(view.texture(from: scene, crop: crop)).cgImage()
            let data = try XCTUnwrap(UIImage(cgImage: image).pngData())
            let key = name + "-" + suffix
            attach(data, name: key, type: "public.png")
            let player = try XCTUnwrap(scene.childNode(withName: "//sprite-player"))
            let root = player.convert(CGPoint.zero, to: scene)
            return ["name": key, "mapping": suffix, "sha256": sha(data),
                    "nativePixels": [image.width, image.height], "tick": scene.currentTick,
                    "digest": digest, "captureKind": "actual-post-action-renderer-still",
                    "worldFocus": [center.x, center.y], "observedPlayerSceneRoot": [root.x, root.y]]
        }
        var captures = [try capture("shipping")]
        var uprights: [SKSpriteNode] = []
        for pattern in ["//sprite-*", "//environment-upright-*"] {
            scene.enumerateChildNodes(withName: pattern) { node, _ in
                if let sprite = node as? SKSpriteNode { uprights.append(sprite) }
            }
        }
        XCTAssertFalse(uprights.isEmpty)
        let saved = try uprights.map { ($0, try XCTUnwrap($0.parent), $0.position, $0.zPosition) }
        let mapping = ReferenceProjectionTrial.midpoint
        let chain = mapping.groundChain(center: center)
        let world = SKNode()
        let hudBefore = camera.children.map { $0.calculateAccumulatedFrame() }
        for (node, parent, position, z) in saved {
            let root = scene.convert(position, from: parent)
            let offset = mapping.forward(CGPoint(x: root.x - center.x, y: root.y - center.y))
            var depth = z
            var ancestor: SKNode? = parent
            while let current = ancestor, current !== scene { depth += current.zPosition; ancestor = current.parent }
            node.removeFromParent()
            node.position = CGPoint(x: center.x + offset.x, y: center.y + offset.y)
            node.zPosition = depth
            world.addChild(node)
        }
        let ground = scene.children.filter { $0 !== camera }
        for node in ground { node.removeFromParent(); chain.coordinates.addChild(node) }
        world.addChild(chain.root)
        scene.addChild(world)
        defer {
            for node in ground { node.removeFromParent(); scene.addChild(node) }
            for (node, parent, position, z) in saved {
                node.removeFromParent(); node.position = position; node.zPosition = z; parent.addChild(node)
            }
            world.removeFromParent()
        }
        XCTAssertEqual(camera.children.map { $0.calculateAccumulatedFrame() }, hudBefore)
        captures.append(try capture("midpoint-post-action-still"))
        XCTAssertEqual(scene.session.simulation.state.digest(), digest)
        return captures
    }
}
#endif
