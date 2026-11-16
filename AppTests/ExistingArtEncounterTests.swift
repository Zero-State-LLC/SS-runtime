#if DEBUG
import CryptoKit
import SpriteKit
import UIKit
import XCTest
@testable import SSRuntime
@testable import SurveillanceCore

/// Accepted benchmark-faithful-scene slice9. Existing shipping art only.
/// Static native diagnostic, not live cadence, midpoint composition or art acceptance.
@MainActor
final class ExistingArtEncounterTests: XCTestCase {
    private let limit = 6000
    private let wanted = Set(["camera-integrity-0", "camera-integrity-1", "camera-integrity-2",
        "camera-integrity-3", "cameraDestroyed", "playerDamaged", "entityDied",
        "dense", "hostile", "mines", "telegraphs", "fieldOcclusion"])

    private func sha(_ data: Data) -> String {
        SHA256.hash(data: data).map { String(format: "%02x", $0) }.joined()
    }

    private func attach(_ data: Data, name: String, type: String = "public.json") {
        let attachment = XCTAttachment(data: data, uniformTypeIdentifier: type)
        attachment.name = name
        attachment.lifetime = .keepAlways
        add(attachment)
    }

    /// A superset inventory of reachable bundle inputs, not per-pixel texture attribution.
    private func resourceInventory() throws -> [[String: Any]] {
        let catalog = try AssetCatalog.bundled()
        let eligible = Set(RuntimeBundleFilter.project(catalog: catalog,
            reachable: try RuntimeBundleFilter.reachableAssetIds()).bundleAssetIds)
        var result: [[String: Any]] = []
        for entry in catalog.entries.sorted(by: { $0.record.assetId < $1.record.assetId }) {
            guard eligible.contains(entry.record.assetId) else { continue }
            let path = try XCTUnwrap(entry.record.runtimePath, entry.record.assetId)
            let url = try XCTUnwrap(RuntimeAssetBundle.url(forFile: path), path)
            // RuntimeAssetBundle has a development source fallback. Do not call that bundled evidence.
            XCTAssertFalse(url.path.contains("/Sources/"), "Resource must resolve in actual runtime bundle")
            let data = try Data(contentsOf: url)
            result.append(["assetId": entry.record.assetId, "path": path,
                           "sha256": sha(data), "bytes": data.count])
        }
        XCTAssertFalse(result.isEmpty)
        return result
    }

    /// Compare clipped/unclipped field paths at an actual solid-directed ray.
    /// No snapshot edits and no sprite bounds used as authoritative geometry.
    private func fieldOcclusion(_ snap: PresentationSnapshot) -> [String: Any]? {
        for camera in snap.cameras where camera.fieldVisible && camera.range > 0 {
            let key = CameraFieldGeometry.Key(camera: camera, solids: snap.solids)
            let clipped = CameraFieldGeometry.path(key)
            let clear = CameraFieldGeometry.path(.init(camera: camera, solids: []))
            for (index, solid) in snap.solids.enumerated() {
                let dx = Double(solid.center.x) - key.originX
                let dy = Double(solid.center.y) - key.originY
                let length = hypot(dx, dy)
                guard length > 0 else { continue }
                let distance = Double(camera.range) * 0.95
                let point = CGPoint(x: key.originX + dx / length * distance,
                                    y: key.originY + dy / length * distance)
                if clear.contains(point) && !clipped.contains(point) {
                    return ["cameraId": camera.id.raw, "solidId": snap.solidIds[index],
                            "x": point.x, "y": point.y,
                            "clearContains": true, "clippedContains": false]
                }
            }
        }
        return nil
    }

    /// Render bounds are presentation diagnostics only, never authoritative collision.
    private func nodeEvidence(scene: SKScene, names: [String], x: CGFloat, y: CGFloat,
                              crop: CGRect, kind: String, id: UInt64, nearby: Bool) throws -> [String: Any] {
        let node = try XCTUnwrap(names.compactMap { scene.childNode(withName: "//" + $0) }.first)
        let parent = try XCTUnwrap(node.parent)
        let frame = node.calculateAccumulatedFrame()
        let a = scene.convert(CGPoint(x: frame.minX, y: frame.minY), from: parent)
        let b = scene.convert(CGPoint(x: frame.maxX, y: frame.maxY), from: parent)
        let bounds = CGRect(x: min(a.x, b.x), y: min(a.y, b.y),
                            width: abs(b.x - a.x), height: abs(b.y - a.y))
        let root = scene.convert(CGPoint.zero, from: node)
        var visible = true
        var ancestor: SKNode? = node
        while let current = ancestor {
            if current.isHidden || current.alpha <= 0 { visible = false }
            ancestor = current.parent
        }
        XCTAssertEqual(root.x, x, accuracy: 0.001)
        XCTAssertEqual(root.y, y, accuracy: 0.001)
        return ["kind": kind, "id": id, "node": node.name ?? "", "x": x, "y": y,
                "rootX": root.x, "rootY": root.y, "nearby": nearby, "nodeVisible": visible,
                "rootInCrop": crop.contains(root), "boundsIntersectCrop": bounds.intersects(crop),
                "bounds": ["x": bounds.minX, "y": bounds.minY,
                           "width": bounds.width, "height": bounds.height]]
    }

    func testLegalPilotExistingArtEncounterEvidence() throws {
        let inputs = try resourceInventory()
        var contracts: [String: String] = [:]
        for name in ["asset-catalog-001", "presentation-assets-003", "clip-metadata-001"] {
            contracts[name + ".json"] = sha(try SpecBundle.contract(name))
        }
        let session = GameSession(seed: 1)
        session.audioSettings = .init(effectsEnabled: false, hapticsEnabled: false, musicEnabled: false)
        var pilot = try XCTUnwrap(DebugAutopilot(scenario: "run",
            arena: session.simulation.state.arena, upgrade: .ghostStep))
        let view = SKView(frame: CGRect(x: 0, y: 0, width: 704, height: 326))
        view.isPaused = true
        let scene = GameScene(size: view.bounds.size, session: session)
        view.presentScene(scene)
        defer { view.presentScene(nil) }
        scene.skipIntroIfRunning()
        XCTAssertFalse(session.scenarioSeeded)
        XCTAssertEqual(session.simulation.state.tick, 0)
        let library = try ClipFrameLibrary.bundled()
        var seen: Set<String> = []
        var captures: [[String: Any]] = []
        var eventCounts: [String: Int] = [:]
        var captureDigests: [UInt64: String] = [:]

        for _ in 0..<limit {
            if session.simulation.isTerminal { break }
            let before = session.snapshot
            let command = pilot.command(before)
            session.moveX = command.moveX
            session.moveY = command.moveY
            session.dodgePressed = command.dodge
            if before.upgradePending { session.pendingUpgradeChoice = pilot.upgradeChoice.selectionIndex }
            session.step()
            let snap = session.snapshot
            XCTAssertFalse(session.scenarioSeeded)
            let events = session.lastEvents
            for event in events { eventCounts[event.type.rawValue, default: 0] += 1 }
            var tags = Set(snap.cameras.map { "camera-integrity-\($0.integrity)" })
            tags.formUnion(events.map { $0.type.rawValue }.filter { wanted.contains($0) })
            let nearby = snap.enemies.filter {
                abs($0.x - snap.player.x) < 300 && abs($0.y - snap.player.y) < 130
            }
            let localShots = snap.projectiles.filter {
                abs($0.x - snap.player.x) < 352 && abs($0.y - snap.player.y) < 163
            }
            if nearby.count >= 2 && !localShots.isEmpty { tags.insert("dense") }
            if snap.projectiles.contains(where: { $0.hostile }) { tags.insert("hostile") }
            if !snap.mines.isEmpty { tags.insert("mines") }
            if !snap.telegraphs.isEmpty { tags.insert("telegraphs") }
            let occlusion = snap.tick % 120 == 0 && !seen.contains("fieldOcclusion") ? fieldOcclusion(snap) : nil
            if occlusion != nil { tags.insert("fieldOcclusion") }
            let fresh = tags.intersection(wanted).subtracting(seen)
            guard !fresh.isEmpty else { continue }
            seen.formUnion(fresh)
            let digest = session.simulation.state.digest()
            // No GameScene.update call: that would add an unrecorded simulation step.
            scene.ingestBenchmarkEvents()
            scene.redrawBenchmarkPresentation()
            XCTAssertEqual(session.simulation.state.digest(), digest)
            XCTAssertEqual(session.snapshot, snap)
            let camera = try XCTUnwrap(scene.camera)
            // Staged snapshot follow only. This is not GameScene live camera-follow coverage.
            camera.position = CGPoint(x: snap.player.x, y: snap.player.y)
            camera.setScale(1)
            let crop = CGRect(x: camera.position.x - scene.size.width / 2,
                              y: camera.position.y - scene.size.height / 2,
                              width: scene.size.width, height: scene.size.height)
            var renderNodes = [try nodeEvidence(scene: scene, names: ["sprite-player", "player"],
                x: CGFloat(snap.player.x), y: CGFloat(snap.player.y), crop: crop,
                kind: "player", id: 0, nearby: true)]
            for actor in snap.enemies {
                renderNodes.append(try nodeEvidence(scene: scene,
                    names: ["sprite-enemy-\(actor.id.raw)", "enemy-\(actor.id.raw)"],
                    x: CGFloat(actor.x), y: CGFloat(actor.y), crop: crop, kind: "enemy", id: actor.id.raw,
                    nearby: nearby.contains { $0.id == actor.id }))
            }
            for shot in snap.projectiles {
                renderNodes.append(try nodeEvidence(scene: scene, names: ["shot-\(shot.id.raw)"],
                    x: CGFloat(shot.x), y: CGFloat(shot.y), crop: crop,
                    kind: "projectile", id: shot.id.raw, nearby: localShots.contains { $0.id == shot.id }))
            }
            func included(_ row: [String: Any]) -> Bool {
                row["rootInCrop"] as? Bool == true && row["boundsIntersectCrop"] as? Bool == true
                    && row["nodeVisible"] as? Bool == true
            }
            XCTAssertTrue(included(renderNodes[0]), "Player must be included in every staged crop")
            if fresh.contains("dense") {
                XCTAssertGreaterThanOrEqual(renderNodes.filter {
                    $0["kind"] as? String == "enemy" && $0["nearby"] as? Bool == true && included($0)
                }.count, 2)
                XCTAssertTrue(renderNodes.contains { $0["kind"] as? String == "projectile" && included($0) })
            }
            let texture = try XCTUnwrap(view.texture(from: scene, crop: crop))
            let png = try XCTUnwrap(UIImage(cgImage: texture.cgImage()).pngData())
            let imageName = "existing-art-tick-\(snap.tick)"
            attach(png, name: imageName, type: "public.png")
            let cameras: [[String: Any]] = snap.cameras.map { actor in
                let fieldPresent = scene.childNode(withName: "//field-\(actor.id.raw)") != nil
                if !actor.fieldVisible { XCTAssertFalse(fieldPresent, "Field-off must remove the rendered cone") }
                return ["id": actor.id.raw, "integrity": actor.integrity,
                        "state": actor.presentationState.rawValue, "clip": actor.clipId,
                        "fieldVisible": actor.fieldVisible, "fieldNodePresent": fieldPresent,
                        "onScreenRoot": crop.contains(CGPoint(x: actor.x, y: actor.y)),
                        "clipBacked": library.isBacked(clipId: actor.clipId)]
            }
            let enemies: [[String: Any]] = snap.enemies.map { actor in
                ["id": actor.id.raw, "x": actor.x, "y": actor.y, "role": actor.role, "clip": actor.clipId ?? "none",
                 "reaction": actor.reactionClipId ?? "none", "direction": actor.direction,
                 "clipBacked": actor.clipId.map { library.isBacked(clipId: $0, direction: actor.direction) } ?? false]
            }
            var record: [String: Any] = [
                "tick": snap.tick, "digest": digest, "captureDigestAfter": session.simulation.state.digest(),
                "tags": fresh.sorted(), "image": imageName, "pngSHA256": sha(png),
                "width": texture.cgImage().width, "height": texture.cgImage().height,
                "sceneWidth": scene.size.width, "sceneHeight": scene.size.height,
                "cameraX": camera.position.x, "cameraY": camera.position.y,
                "framing": "staged snapshot Player center, not live follow",
                "playerX": snap.player.x, "playerY": snap.player.y,
                "crop": ["x": crop.minX, "y": crop.minY, "width": crop.width, "height": crop.height],
                "renderNodes": renderNodes,
                "cameras": cameras, "enemies": enemies, "nearbyEnemyCount": nearby.count,
                "projectileCount": snap.projectiles.count,
                "hostileProjectileCount": snap.projectiles.filter { $0.hostile }.count,
                "mineCount": snap.mines.count, "armedMineCount": snap.mines.filter { $0.armed }.count,
                "mines": snap.mines.map { ["id": $0.id.raw, "armed": $0.armed,
                    "armRemaining": $0.armRemaining, "lifeRemaining": $0.lifeRemaining,
                    "x": $0.x, "y": $0.y] as [String: Any] },
                "projectiles": snap.projectiles.map { ["id": $0.id.raw, "hostile": $0.hostile,
                    "role": $0.role, "x": $0.x, "y": $0.y] as [String: Any] },
                "telegraphCount": snap.telegraphs.count,
                "events": events.map { ["tick": $0.tick, "type": $0.type.rawValue,
                                         "primary": $0.primaryEntityId?.raw ?? 0] as [String: Any] },
                "playerClip": snap.playerClipId, "playerDirection": snap.playerDirection,
                "playerClipBacked": library.isBacked(clipId: snap.playerClipId, direction: snap.playerDirection)]
            if let occlusion { record["fieldOcclusion"] = occlusion }
            captures.append(record)
            captureDigests[snap.tick] = digest
        }
        let state = session.simulation.state
        let replayRecord = GhostRecord(identity: state.identity, seed: state.seed, ticks: state.tick,
                                       digest: state.digest(), commands: session.commandLog)
        let replayData = try JSONEncoder().encode(replayRecord)
        attach(replayData, name: "existing-art-legal-commands")
        // Independent public replay at the final boundary and each captured prefix.
        let replay = try XCTUnwrap(GhostRun.replay(seed: state.seed,
            commands: replayRecord.playerCommands, until: state.tick))
        XCTAssertEqual(replay.state.digest(), state.digest())
        var prefixes = try Simulation.make(seed: state.seed)
        let commands = replayRecord.playerCommands
        var nextCommand = 0
        while prefixes.state.tick < state.tick && !prefixes.isTerminal {
            let nextTick = prefixes.state.tick + 1
            var command: PlayerCommand?
            if nextCommand < commands.count && commands[nextCommand].tick == nextTick {
                command = commands[nextCommand]
                nextCommand += 1
            }
            _ = prefixes.step(command: command)
            if let expected = captureDigests[prefixes.state.tick] {
                XCTAssertEqual(prefixes.state.digest(), expected)
            }
        }
        XCTAssertEqual(prefixes.state.tick, state.tick)
        XCTAssertEqual(prefixes.state.digest(), state.digest())
        let packet: [String: Any] = [
            "schema": "existing-art-encounters-v2", "seed": state.seed, "tickLimit": limit,
            "terminalTick": state.tick, "finalDigest": state.digest(), "replayDigest": replay.state.digest(),
            "scenarioSeeded": session.scenarioSeeded, "replaySHA256": sha(replayData),
            "driver": "DebugAutopilot run / ghostStep / seed1", "captures": captures,
            "observed": seen.sorted(), "notObserved": wanted.subtracting(seen).sorted(),
            "eventCounts": eventCounts, "runtimeInputs": inputs, "contractSHA256": contracts,
            "resourceScope": "reachable bundled inventory superset, not per-pixel attribution",
            "evidenceKind": "static paused GameScene existing production art and projection",
            "sourceFidelity": "BLOCKED", "ownerAcceptance": "NOT_GRANTED", "productionAdmission": "NOT_GRANTED",
            "unsupported": ["coherent benchmark scene", "selected midpoint composition", "new artwork",
                            "live callback cadence", "physical device", "sprite occlusion ordering proof",
                            "complete attack/animation family coverage"]]
        attach(try JSONSerialization.data(withJSONObject: packet, options: [.sortedKeys, .prettyPrinted]),
               name: "existing-art-encounter-records")
        XCTAssertTrue(seen.contains("dense"), "Existing legal seed1 route must reach the established encounter")
        XCTAssertGreaterThan(captures.count, 1)
        XCTAssertLessThanOrEqual(captures.count, wanted.count)
    }
}
#endif
