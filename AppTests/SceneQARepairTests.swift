import CoreImage
import CryptoKit
import SpriteKit
import UIKit
import XCTest
@testable import SSRuntime
@testable import SurveillanceCore

#if DEBUG && SS_SOURCE_SCENE_REVIEW
/// BP-001/007/012/T1045, intent/2026-11-16-scene-qa-repair.md.
/// ADAPT: WholeSceneBoundInputsTests.swift:19-44,64-78,185-241.
/// Two quiet ordinary composition arms only. One south-neutral and one Camera-neutral
/// source, NOT a 16-frame family. Missing source preparation is a failure, never a skip.
final class SceneQARepairTests: XCTestCase {
    private let fixtureVersion = "source-scene-qa-005-footprint-ground"
    private let viewport = CGSize(width: 704, height: 326)
    private let buildingID = "solid-03-transit-kiosk"
    private let repository = URL(fileURLWithPath: #filePath).deletingLastPathComponent().deletingLastPathComponent()
    private struct Registration: Decodable {
        let canvasPixels: [Double]
        let rootPixelsTopLeft: [Double]
        let worldPosition: [Double]
        let drawSizeWorld: [Double]
        var size: CGSize { CGSize(width: drawSizeWorld[0], height: drawSizeWorld[1]) }
        var anchor: CGPoint { CGPoint(x: rootPixelsTopLeft[0] / canvasPixels[0], y: 1 - rootPixelsTopLeft[1] / canvasPixels[1]) }
        var position: CGPoint { CGPoint(x: worldPosition[0], y: worldPosition[1]) }
    }
    private struct Source: Decodable {
        let role: String
        let file: String
        let sha256: String
        let registration: Registration
        let recommendation: String
    }
    private struct Input: Decodable {
        let schema: String
        let assemblySHA256: String
        let fixtureVersion: String
        let harnessSourceSHA256: String
        let sources: [Source]
        let center: [Double]
    }
    private func sha(_ data: Data) -> String { SHA256.hash(data: data).map { String(format: "%02x", $0) }.joined() }
    private func require(_ condition: Bool, _ message: String) throws {
        guard condition else {
            XCTFail(message)
            throw NSError(domain: "SourceSceneContinuation", code: 1, userInfo: [NSLocalizedDescriptionKey: message])
        }
    }
    private func verifyDependency(_ record: [String: Any]) throws {
        let path = try XCTUnwrap(record["path"] as? String)
        let digest = try XCTUnwrap(record["sha256"] as? String)
        try require(!path.hasPrefix("/") && !path.contains("\\") && path.split(separator: "/", omittingEmptySubsequences: false).allSatisfy { !$0.isEmpty && $0 != "." && $0 != ".." }, "Dependency path escape")
        let url = repository.resolvingSymlinksInPath().appendingPathComponent(path)
        try require(url.resolvingSymlinksInPath().path == url.path, "Dependency symlink forbidden")
        try require(sha(try Data(contentsOf: url)) == digest, "Dependency hash drift: " + path)
    }
    @MainActor private func texture(_ bytes: Data) throws -> SKTexture {
        let texture = SKTexture(image: try XCTUnwrap(UIImage(data: bytes)))
        texture.filteringMode = .linear
        return texture
    }

    /// Source-free authority probe. Same seed/session construction as the scene fixture,
    /// no stepping, source preparation, art injection, screenshots, or guessed sockets.
    @MainActor func testReadAuthoritativeScenePlacement() throws {
        let session = GameSession(seed: 1)
        let before = session.simulation.state.digest()
        let snap = session.snapshot
        try require(snap.solids.count == snap.solidIds.count, "Authoritative solid ID census mismatch")
        try require(!snap.cameras.isEmpty && !snap.solids.isEmpty, "Seed-1 placement must contain cameras and solids")
        let cameras: [[String: Any]] = snap.cameras.sorted { $0.id.raw < $1.id.raw }.map { camera in
            var row: [String: Any] = ["id": camera.id.raw, "rootWorld": [camera.x, camera.y],
                "headingMilli": camera.headingMilli, "range": camera.range, "fieldAngleMilli": camera.fieldAngleMilli,
                "integrity": camera.integrity, "fieldVisible": camera.fieldVisible, "clipId": camera.clipId,
                "presentationState": String(describing: camera.presentationState)]
            if let origin = camera.fieldOrigin {
                row["fieldOriginQ8"] = [origin.x.raw, origin.y.raw]
                row["fieldOriginWorld"] = [Double(origin.x.raw) / Double(Q8.scale), Double(origin.y.raw) / Double(Q8.scale)]
            } else {
                row["fieldOriginQ8"] = NSNull()
                row["fieldOriginWorld"] = NSNull()
            }
            return row
        }
        let solids: [[String: Any]] = snap.solids.enumerated().map { index, box in
            ["index": index, "id": snap.solidIds[index], "minWorld": [box.minX, box.minY],
             "maxWorld": [box.maxX, box.maxY], "centerWorld": [box.center.x, box.center.y],
             "halfSizeWorld": [box.halfSize.x, box.halfSize.y]]
        }
        let executable = try XCTUnwrap(Bundle(for: Self.self).executableURL)
        XCTAssertEqual(session.simulation.state.digest(), before, "Placement read must not advance authority")
        let record: [String: Any] = ["status": "AUTHORITATIVE_SEED1_PLACEMENT_ONLY_NOT_SCENE_EVIDENCE",
            "placementVersion": "source-scene-seed1-placement-001", "fixtureVersion": fixtureVersion,
            "seed": 1, "tick": snap.tick, "q8Scale": Q8.scale,
            "authorityBefore": String(describing: before), "authorityAfter": String(describing: session.simulation.state.digest()),
            "playerRootWorld": [snap.player.x, snap.player.y],
            "arenaMinWorld": [snap.arenaBounds.minX, snap.arenaBounds.minY],
            "arenaMaxWorld": [snap.arenaBounds.maxX, snap.arenaBounds.maxY],
            "cameraCount": cameras.count, "solidCount": solids.count, "cameras": cameras, "solids": solids,
            "loadedTestExecutable": ["path": executable.path, "sha256": sha(try Data(contentsOf: executable))],
            "harnessSourceReadSHA256": sha(try Data(contentsOf: URL(fileURLWithPath: #filePath)))]
        let attachment = XCTAttachment(data: try JSONSerialization.data(withJSONObject: record, options: [.prettyPrinted, .sortedKeys]), uniformTypeIdentifier: "public.json")
        attachment.name = "source-scene-authoritative-placement"; attachment.lifetime = .keepAlways; add(attachment)
    }

    @MainActor func testQuietSouthNeutralOrdinaryScene() throws {
        let packet = repository.appendingPathComponent("docs/review/scene-qa-repair-20261116")
        let prepared = packet.appendingPathComponent("native-inputs-v5")
        let inputURL = prepared.appendingPathComponent("native-inputs.json")
        try require(FileManager.default.fileExists(atPath: inputURL.path),
                    "SOURCE PENDING: run packet/native.py prepare after coordinator recommendations. No fallback or skip.")
        let inputBytes = try Data(contentsOf: inputURL)
        let input = try JSONDecoder().decode(Input.self, from: inputBytes)
        try require(input.schema == "source-scene-native-005" && input.fixtureVersion == fixtureVersion, "Unknown native preparation schema/fixtureVersion")
        let sourceReadSHA256 = sha(try Data(contentsOf: URL(fileURLWithPath: #filePath)))
        let loadedExecutable = try XCTUnwrap(Bundle(for: Self.self).executableURL, "Actual loaded test bundle executable is required")
        let loadedExecutableSHA256 = sha(try Data(contentsOf: loadedExecutable))
        let assembly = try Data(contentsOf: packet.appendingPathComponent("assembly.json"))
        try require(sha(assembly) == input.assemblySHA256, "Stale assembly preparation")
        try require(sourceReadSHA256 == input.harnessSourceSHA256, "Stale harness source preparation, not binary attestation")
        try require(input.sources.count == 4 && Set(input.sources.map(\.role)) == Set(["paving", "camera", "player", "stone"]), "Four exact source roles required")
        try require(input.center.count == 2 && input.center.allSatisfy(\.isFinite), "Explicit center required")
        let assemblyObject = try XCTUnwrap(JSONSerialization.jsonObject(with: assembly) as? [String: Any])
        let assemblySources = try XCTUnwrap(assemblyObject["sources"] as? [[String: Any]])
        try require(assemblySources.count == 4, "Assembly source census mismatch")
        for dependency in try XCTUnwrap(assemblyObject["contextDependencies"] as? [[String: Any]]) { try verifyDependency(dependency) }
        var textures: [String: SKTexture] = [:]
        var sources: [String: Source] = [:]
        for source in input.sources {
            try require(source.file == source.role + ".png" && source.recommendation == "coordinator-recommended", "Unadmitted source/path")
            let original = try XCTUnwrap(assemblySources.first { $0["role"] as? String == source.role })
            let recommendation = try XCTUnwrap(original["recommendation"] as? [String: Any])
            let originalImage = try XCTUnwrap(original["image"] as? [String: Any])
            try verifyDependency(originalImage)
            try verifyDependency(try XCTUnwrap(recommendation["evidence"] as? [String: Any]))
            try require(recommendation["scope"] as? String == (source.role == "paving" ? "bounded-material-layout" : "isolated-ordinary-scene"), "Wrong recommendation scope")
            try require(original["status"] as? String == "recommended" && recommendation["reviewerRole"] as? String == "coordinator" && recommendation["decision"] as? String == "recommended", "Source still pending/rejected")
            try require(originalImage["sha256"] as? String == source.sha256 && recommendation["sourceSHA256"] as? String == source.sha256, "Unbound source recommendation")
            let originalRegistration = try JSONSerialization.data(withJSONObject: try XCTUnwrap(original["registration"]), options: [.sortedKeys])
            let boundRegistration = try JSONDecoder().decode(Registration.self, from: originalRegistration)
            try require(boundRegistration.canvasPixels == source.registration.canvasPixels && boundRegistration.rootPixelsTopLeft == source.registration.rootPixelsTopLeft && boundRegistration.worldPosition == source.registration.worldPosition && boundRegistration.drawSizeWorld == source.registration.drawSizeWorld, "Prepared registration drift")
            let bytes = try Data(contentsOf: prepared.appendingPathComponent(source.file))
            try require(sha(bytes) == source.sha256, "Source byte drift: " + source.role)
            let image = try XCTUnwrap(UIImage(data: bytes)?.cgImage)
            let reg = source.registration
            try require([reg.canvasPixels, reg.rootPixelsTopLeft, reg.worldPosition, reg.drawSizeWorld].allSatisfy { $0.count == 2 && $0.allSatisfy(\.isFinite) }, "Invalid registration")
            try require(reg.canvasPixels == [Double(image.width), Double(image.height)] && reg.drawSizeWorld.allSatisfy { $0 > 0 }, "Dimensions/scale mismatch")
            try require(zip(reg.rootPixelsTopLeft, reg.canvasPixels).allSatisfy { $0.0 >= 0 && $0.0 <= $0.1 }, "Invalid root")
            textures[source.role] = try texture(bytes)
            sources[source.role] = source
        }
        let player = try XCTUnwrap(sources["player"]), cameraSource = try XCTUnwrap(sources["camera"])
        let stone = try XCTUnwrap(sources["stone"]), paving = try XCTUnwrap(sources["paving"])
        var controls: [String: SKTexture] = [:], controlHashes: [String: String] = [:]
        for name in ["painted-player-south", "camera", "building-constrained", "newsbox", "tree"] {
            let url = try XCTUnwrap(Bundle(for: Self.self).url(forResource: name, withExtension: "png"))
            let bytes = try Data(contentsOf: url)
            controls[name] = SKTexture(image: try XCTUnwrap(UIImage(contentsOfFile: url.path)))
            controls[name]?.filteringMode = .linear
            controlHashes[name + ".png"] = sha(bytes)
        }
        let environment = EnvironmentTextures()
        let plaza = try XCTUnwrap(environment.texture(assetId: "env_ground_plaza"))
        let asphalt = try XCTUnwrap(environment.texture(assetId: "env_ground_asphalt"))
        var runtimeHashes: [String: String] = [:]
        for id in ["env_ground_plaza", "env_ground_asphalt"] {
            let path = try XCTUnwrap(try EnvironmentLibrary.bundled().path(for: id))
            let url = try XCTUnwrap(RuntimeAssetBundle.url(forFile: path))
            runtimeHashes[path] = sha(try Data(contentsOf: url))
        }
        var captures: [[String: Any]] = []
        for arm in ["control", "candidate"] {
            let scene = GameScene(size: viewport, session: GameSession(seed: 1))
            let view = SKView(frame: CGRect(origin: .zero, size: viewport))
            view.isPaused = true
            view.presentScene(scene)
            defer { view.presentScene(nil) }
            scene.session.audioSettings = .init(effectsEnabled: false, hapticsEnabled: false, musicEnabled: false)
            let before = scene.session.simulation.state.digest()
            var snap = scene.session.snapshot
            let box = snap.solids[try XCTUnwrap(snap.solidIds.firstIndex(of: buildingID))]
            // Keep ALL authoritative solids and the selected Camera's original field geometry.
            let selected = try XCTUnwrap(snap.cameras.first { $0.fieldVisible && $0.integrity == 3 &&
                Double($0.x) == cameraSource.registration.worldPosition[0] && Double($0.y) == cameraSource.registration.worldPosition[1] },
                "Camera registration must name an actual seed-1 visible intact Camera root. Never move its field to fit art.")
            snap.cameras = [selected]
            snap.player.x = try XCTUnwrap(Int(exactly: player.registration.worldPosition[0]), "Player X must be integral")
            snap.player.y = try XCTUnwrap(Int(exactly: player.registration.worldPosition[1]), "Player Y must be integral")
            try require(Double(snap.player.x) == player.registration.worldPosition[0] && Double(snap.player.y) == player.registration.worldPosition[1], "Player root must be integral world coordinates")
            snap.playerDirection = "south"
            snap.playerClipId = "player_idle"
            snap.enemies = []; snap.projectiles = []; snap.telegraphs = []; snap.mines = []
            snap.spawnSockets = []; snap.captainHousings = []; snap.captainField = nil; snap.patrolCones = []
            let x = box.center.x, y = box.center.y
            let canvas = CGFloat(1254) * (CGFloat(128) * CGFloat(2).squareRoot() / 934)
            var art = BenchmarkReviewArt(player: try XCTUnwrap(controls["painted-player-south"]), camera: try XCTUnwrap(controls["camera"]),
                building: .init(texture: try XCTUnwrap(controls["building-constrained"]), size: CGSize(width: canvas, height: canvas),
                    anchor: CGPoint(x: CGFloat(653) / 1254, y: 1 - CGFloat(1152) / 1254), position: CGPoint(x: box.minX, y: box.minY)),
                buildingID: buildingID, props: [
                    .init(texture: try XCTUnwrap(controls["newsbox"]), size: CGSize(width: 20, height: 40), anchor: CGPoint(x: 0.5, y: 0), position: CGPoint(x: x + 115, y: y - 65)),
                    .init(texture: try XCTUnwrap(controls["tree"]), size: CGSize(width: 50, height: 85), anchor: CGPoint(x: 0.5, y: 0), position: CGPoint(x: 858, y: 780))], paving: plaza)
            art.configureStreetCorner(asphalt: asphalt)
            if arm == "candidate" {
                art = BenchmarkReviewArt(player: try XCTUnwrap(textures["player"]), camera: try XCTUnwrap(textures["camera"]),
                    building: .init(texture: try XCTUnwrap(textures["stone"]), size: stone.registration.size,
                                    anchor: stone.registration.anchor, position: stone.registration.position),
                    buildingID: buildingID, props: art.props, paving: plaza)
                let r = paving.registration
                try require(r.drawSizeWorld == [2304, 2304] && r.worldPosition == [0, 0] && r.rootPixelsTopLeft == [0, r.canvasPixels[1]], "Square ground adapter registration drift")
                let arena = snap.arenaBounds
                let bounds = CGRect(x: CGFloat(arena.minX), y: CGFloat(arena.minY), width: CGFloat(arena.maxX - arena.minX), height: CGFloat(arena.maxY - arena.minY))
                try require(bounds == CGRect(x: 0, y: 0, width: 2304, height: 1536), "Authoritative arena ground coverage drift")
                art.groundPatches = [.init(texture: try XCTUnwrap(textures["paving"]), bounds: bounds, tileUnits: r.size.width)]
            }
            // Deliberately NO installBenchmarkCameraFrames: exactly one static neutral texture.
            scene.renderBenchmark(snapshot: snap, art: art, center: CGPoint(x: input.center[0], y: input.center[1]))
            let playerNode = try XCTUnwrap(scene.childNode(withName: "//sprite-player") as? SKSpriteNode)
            let cameraNode = try XCTUnwrap(scene.childNode(withName: "//sprite-camera-\(selected.id.raw)") as? SKSpriteNode)
            if arm == "candidate" {
                // Existing static API has fixed actor registration. Apply explicit review-only
                // source registration to these rendered nodes, never collision or Camera fields.
                playerNode.size = player.registration.size; playerNode.anchorPoint = player.registration.anchor
                cameraNode.size = cameraSource.registration.size; cameraNode.anchorPoint = cameraSource.registration.anchor
                XCTAssertTrue(playerNode.texture === textures["player"])
                XCTAssertTrue(cameraNode.texture === textures["camera"])
                scene.refreshBenchmarkOutlines(samplingScale: 3)
            }
            let playerOutline = try XCTUnwrap(playerNode.childNode(withName: WorldRenderer.outlineName))
            let playerShadow = try XCTUnwrap(scene.childNode(withName: "//shadow-player") as? SKSpriteNode)
            let shadowTexture = playerShadow.texture
            let shadowSize = playerShadow.size
            let originalShadowHash = sha(try XCTUnwrap(UIImage(cgImage: try XCTUnwrap(playerShadow.texture).cgImage()).pngData()))
            if arm == "candidate" {
                // BP-010 comparison only. The source pixels and production border stay unchanged.
                playerOutline.alpha = 0
                let parent = try XCTUnwrap(playerShadow.parent)
                playerShadow.position = parent.convert(player.registration.position, from: scene)
            }
            XCTAssertEqual(playerOutline.alpha, arm == "candidate" ? 0 : 1)
            XCTAssertTrue(playerShadow.texture === shadowTexture)
            XCTAssertEqual(playerShadow.size, shadowSize)
            let observedShadowRoot = playerShadow.convert(CGPoint.zero, to: scene)
            if arm == "candidate" {
                XCTAssertEqual(observedShadowRoot.x, player.registration.position.x, accuracy: 0.001)
                XCTAssertEqual(observedShadowRoot.y, player.registration.position.y, accuracy: 0.001)
            }
            let field = try XCTUnwrap(scene.childNode(withName: "//field-\(selected.id.raw)") as? SKShapeNode)
            let fieldPath = try XCTUnwrap(field.path)
            let expectedField = CameraFieldGeometry.path(.init(camera: selected, solids: snap.solids))
            XCTAssertEqual(fieldPath, expectedField)
            XCTAssertFalse(field.isHidden)
            let hud = try XCTUnwrap(scene.camera)
            let hudHidden = hud.children.map(\.isHidden)
            XCTAssertFalse(hudHidden.isEmpty)
            XCTAssertTrue(hudHidden.contains(false))
            _ = try XCTUnwrap(scene.controlLayout)
            // ADAPT BenchmarkCaptureTests.swift:205-213 and WorldRenderer.swift:695-772.
            // Inventory independently BEFORE choosing/extracting any projected nodes.
            try require(snap.solids.count == 24, "Seed1 authoritative24-solid census changed")
            let names = ["sprite-player", "sprite-camera-\(selected.id.raw)", "benchmark-building", "benchmark-prop-0", "benchmark-prop-1"]
            var environmentNodes: [SKSpriteNode] = []
            scene.enumerateChildNodes(withName: "//environment-upright-*") { node, _ in
                if let sprite = node as? SKSpriteNode { environmentNodes.append(sprite) }
            }
            environmentNodes.sort { ($0.name ?? "") < ($1.name ?? "") }
            let expectedEnvironmentNames = snap.solidIds.filter {
                $0 != buildingID && !$0.hasPrefix(SelectedCamera.mountSolidPrefix) && !snap.gateIds.contains($0) && environment.solidTexture(solidId: $0) != nil
            }.map { "environment-upright-" + EnvironmentLibrary.solidAssetId(forSolidId: $0) }.sorted()
            try require(!expectedEnvironmentNames.isEmpty, "Expected environment upright cohort must not be empty")
            try require(environmentNodes.compactMap(\.name) == expectedEnvironmentNames, "Independent environment inventory differs from authoritative backed solids")
            for node in environmentNodes {
                let asset = String(try XCTUnwrap(node.name).dropFirst("environment-upright-".count))
                try require(EnvironmentTextures.projectionPlane(for: asset) == .upright, "Environment classification drift")
            }
            let actorNodes = try names.map { try XCTUnwrap(scene.childNode(withName: "//" + $0) as? SKSpriteNode) }
            let inventoryNodes = actorNodes + environmentNodes
            let inventory: [[String: Any]] = inventoryNodes.map { node in
                let root = node.convert(CGPoint.zero, to: scene)
                var originalDepth = node.zPosition
                var ancestor = node.parent
                while let parent = ancestor, parent !== scene { originalDepth += parent.zPosition; ancestor = parent.parent }
                return ["originalWorldDepth": originalDepth, "originalLocalZ": node.zPosition, "name": node.name ?? "", "worldRoot": [root.x, root.y],
                        "size": [node.size.width, node.size.height], "anchor": [node.anchorPoint.x, node.anchorPoint.y],
                        "scale": [node.xScale, node.yScale], "rotation": node.zRotation,
                        "hidden": node.isHidden, "alpha": node.alpha]
            }
            try require(Set(inventoryNodes.map { ObjectIdentifier($0) }).count == inventoryNodes.count, "Duplicate upright inventory")
            // Extraction is a fresh census, checked against the independent inventory.
            var uprights = actorNodes
            scene.enumerateChildNodes(withName: "//environment-upright-*") { node, _ in
                if let sprite = node as? SKSpriteNode { uprights.append(sprite) }
            }
            uprights = Array(uprights.prefix(5)) + uprights.dropFirst(5).sorted { ($0.name ?? "") < ($1.name ?? "") }
            try require(uprights.map { $0.name ?? "" } == inventoryNodes.map { $0.name ?? "" }, "Extraction census differs from inventory")
            var footprints: [String: SceneQAReviewDepth.Bounds] = [:]
            for (id, solid) in zip(snap.solidIds, snap.solids) {
                let name = id == buildingID ? "benchmark-building" : "environment-upright-" + EnvironmentLibrary.solidAssetId(forSolidId: id)
                if inventoryNodes.contains(where: { $0.name == name }) {
                    try require(footprints[name] == nil, "Ambiguous solid-to-upright footprint mapping")
                    footprints[name] = .init(minX: Double(solid.minX), minY: Double(solid.minY), maxX: Double(solid.maxX), maxY: Double(solid.maxY))
                }
            }
            try require(footprints.count == environmentNodes.count + 1, "Every solid-backed upright needs authoritative footprint")
            let originalLocalDepths = uprights.map(\.zPosition)
            for zoom: CGFloat in [1, 1.25, 1.4] {
                var record = try capture(scene: scene, view: view, uprights: uprights, footprints: footprints, zoom: zoom,
                                         name: "source-scene-\(arm)-ordinary-z\(Int((zoom * 100).rounded()))")
                for (node, originalZ) in zip(uprights, originalLocalDepths) { XCTAssertEqual(node.zPosition, originalZ) }
                XCTAssertEqual(hud.children.map(\.isHidden), hudHidden)
                XCTAssertEqual(field.path, fieldPath)
                XCTAssertEqual(scene.session.simulation.state.digest(), before)
                record["preprojectionInventory"] = inventory
                record["expectedEnvironmentNames"] = expectedEnvironmentNames
                record["uprightCount"] = inventory.count
                record["environmentCount"] = expectedEnvironmentNames.count
                record["arm"] = arm; record["mode"] = "ordinary"; record["zoom"] = zoom
                record["hudVisible"] = true; record["controlsRetained"] = true
                record["fieldVisible"] = true; record["fieldUnchanged"] = true
                record["authorityBefore"] = String(describing: before)
                record["authorityAfter"] = String(describing: scene.session.simulation.state.digest())
                record["cameraRoot"] = [selected.x, selected.y]
                record["cameraRange"] = selected.range; record["cameraHeadingMilli"] = selected.headingMilli
                record["cameraFieldAngleMilli"] = selected.fieldAngleMilli
                record["cameraFieldOrigin"] = String(describing: selected.fieldOrigin)
                record["playerOutlineAlpha"] = playerOutline.alpha
                record["originalPlayerShadowSize"] = [shadowSize.width, shadowSize.height]
                record["playerShadowSize"] = [playerShadow.size.width, playerShadow.size.height]
                record["originalPlayerShadowTextureSHA256"] = originalShadowHash
                record["playerShadowTextureSHA256"] = sha(try XCTUnwrap(UIImage(cgImage: try XCTUnwrap(playerShadow.texture).cgImage()).pngData()))
                record["solids"] = zip(snap.solidIds, snap.solids).map { id, solid in
                    ["id": id, "minWorld": [solid.minX, solid.minY], "maxWorld": [solid.maxX, solid.maxY]] as [String: Any]
                }
                record["playerShadowWorldRoot"] = [observedShadowRoot.x, observedShadowRoot.y]
                record["shadowTreatment"] = arm == "candidate" ? "ground-root-existing-soft-shadow" : "original-offset-soft-shadow"
                record["groundBounds"] = arm == "candidate" ? [snap.arenaBounds.minX, snap.arenaBounds.minY, snap.arenaBounds.maxX - snap.arenaBounds.minX, snap.arenaBounds.maxY - snap.arenaBounds.minY] : []
                record["groundSourceWorldSize"] = arm == "candidate" ? paving.registration.drawSizeWorld : []
                record["solidCount"] = snap.solids.count
                captures.append(record)
            }
        }
        XCTAssertEqual(captures.count, 6)
        let record: [String: Any] = ["schema": "source-scene-records-005", "status": "NATIVE_QUIET_SOURCE_COMPARISON_NOT_ACCEPTANCE",
            "fixtureVersion": fixtureVersion,
            "loadedTestExecutable": ["path": loadedExecutable.path, "sha256": loadedExecutableSHA256],
            "fixture": "south-neutral-camera-neutral", "cameraSourceFrames": 1, "playerSourceFrames": 1,
            "inputSHA256": sha(inputBytes), "assemblySHA256": input.assemblySHA256,
            "harnessSourceReadSHA256": sourceReadSHA256,
            "sourceSHA256": Dictionary(uniqueKeysWithValues: input.sources.map { ($0.role, $0.sha256) }),
            "controlSHA256": controlHashes, "runtimeSHA256": runtimeHashes, "captures": captures]
        let attachment = XCTAttachment(data: try JSONSerialization.data(withJSONObject: record, options: [.prettyPrinted, .sortedKeys]), uniformTypeIdentifier: "public.json")
        attachment.name = "source-scene-records"; attachment.lifetime = .keepAlways; add(attachment)
    }

    /// ADAPT WholeSceneBoundInputsTests.capture: midpoint world with upright roots,
    /// production camera/HUD outside the projected world, three retained zooms.
    @MainActor private func capture(scene: GameScene, view: SKView, uprights: [SKSpriteNode], footprints: [String: SceneQAReviewDepth.Bounds], zoom: CGFloat, name: String) throws -> [String: Any] {
        let camera = try XCTUnwrap(scene.camera), center = camera.position
        let saved = try uprights.map { ($0, try XCTUnwrap($0.parent), $0.position, $0.zPosition) }
        let roots = saved.map { scene.convert($0.2, from: $0.1) }
        let mapping = ReferenceProjectionTrial.midpoint, chain = mapping.groundChain(center: center)
        let world = SKNode()
        world.setScale(zoom)
        world.position = CGPoint(x: center.x * (1 - zoom), y: center.y * (1 - zoom))
        let ground = scene.children.filter { $0 !== camera }
        defer {
            for node in ground { node.removeFromParent(); scene.addChild(node) }
            for entry in saved { entry.0.removeFromParent(); entry.0.position = entry.2; entry.0.zPosition = entry.3; entry.1.addChild(entry.0) }
            world.removeFromParent()
        }
        let originalDepths = saved.map { entry -> CGFloat in
            var depth = entry.3
            var parent: SKNode? = entry.1
            while let node = parent, node !== scene { depth += node.zPosition; parent = node.parent }
            return depth
        }
        let depthBase = try XCTUnwrap(originalDepths.max())
        for (index, entry) in saved.enumerated() {
            let delta = mapping.forward(CGPoint(x: roots[index].x - center.x, y: roots[index].y - center.y))
            entry.0.removeFromParent(); entry.0.position = CGPoint(x: center.x + delta.x, y: center.y + delta.y)
            entry.0.zPosition = originalDepths[index]; world.addChild(entry.0)
        }
        // Issue249: use authoritative footprint separation, never alpha bounds or a visibility Z boost.
        let depthItems = try saved.enumerated().map { index, entry -> SceneQAReviewDepth.Item in
            let name = try XCTUnwrap(entry.0.name)
            return .init(name: name, worldRoot: .init(x: Double(roots[index].x), y: Double(roots[index].y)),
                         solidBounds: footprints[name], projectedRootY: Double(mapping.forward(roots[index]).y))
        }
        let ordered = try SceneQAReviewDepth.order(depthItems)
        let depthOrder = ordered.backToFrontNames
        let byName = Dictionary(uniqueKeysWithValues: uprights.map { ($0.name!, $0) })
        let depthSorted = try depthOrder.map { try XCTUnwrap(byName[$0]) }
        let ranks = Dictionary(uniqueKeysWithValues: depthSorted.enumerated().map { (ObjectIdentifier($0.element), $0.offset) })
        for (rank, node) in depthSorted.enumerated() {
            node.zPosition = depthBase + CGFloat(rank) / CGFloat(depthSorted.count) * 0.5
        }
        try require(Set(depthSorted.map(\.zPosition)).count == depthSorted.count, "Unique upright depth ranks required")
        for (rank, node) in depthSorted.enumerated() {
            XCTAssertEqual(node.zPosition, depthBase + CGFloat(rank) / CGFloat(depthSorted.count) * 0.5, accuracy: 0.00001)
            XCTAssertGreaterThanOrEqual(node.zPosition, depthBase)
            XCTAssertLessThan(node.zPosition, depthBase + 0.5)
            if rank > 0 {
                let previous = depthSorted[rank - 1]
                XCTAssertGreaterThan(node.zPosition, previous.zPosition)
            }
        }
        let rankByName = Dictionary(uniqueKeysWithValues: depthOrder.enumerated().map { ($0.element, $0.offset) })
        for edge in ordered.edges {
            XCTAssertLessThan(try XCTUnwrap(rankByName[edge.back]), try XCTUnwrap(rankByName[edge.front]), "Authoritative footprint separation")
        }
        for node in ground { node.removeFromParent(); chain.coordinates.addChild(node) }
        world.addChild(chain.root); scene.addChild(world)
        for (index, entry) in saved.enumerated() {
            let actual = entry.0.convert(CGPoint.zero, to: scene), expected = chain.coordinates.convert(roots[index], to: scene)
            let basisX = entry.0.convert(CGPoint(x: 1, y: 0), to: scene)
            let basisY = entry.0.convert(CGPoint(x: 0, y: 1), to: scene)
            XCTAssertEqual(basisX.x - actual.x, zoom * entry.0.xScale, accuracy: 0.002)
            XCTAssertEqual(basisX.y - actual.y, 0, accuracy: 0.002)
            XCTAssertEqual(basisY.x - actual.x, 0, accuracy: 0.002)
            XCTAssertEqual(basisY.y - actual.y, zoom * entry.0.yScale, accuracy: 0.002)
            XCTAssertEqual(entry.0.xScale, entry.0.yScale, accuracy: 0.00001)
            XCTAssertEqual(entry.0.zRotation, 0, accuracy: 0.00001)
            XCTAssertFalse(entry.0.isHidden)
            XCTAssertGreaterThan(entry.0.alpha, 0)
            XCTAssertEqual(actual.x, expected.x, accuracy: 0.002); XCTAssertEqual(actual.y, expected.y, accuracy: 0.002)
        }
        let crop = CGRect(x: center.x - 352, y: center.y - 163, width: 704, height: 326)
        for node in uprights.prefix(2) { XCTAssertTrue(crop.contains(node.convert(CGPoint.zero, to: scene)), "Player/Camera root must be in the ordinary crop") }
        let actors: [[String: Any]] = saved.enumerated().map { index, entry in
            let projected = entry.0.convert(CGPoint.zero, to: scene)
            return ["actualZ": entry.0.zPosition, "depthRank": ranks[ObjectIdentifier(entry.0)]!,
             "originalWorldDepth": originalDepths[index], "originalLocalZ": entry.3,
             "name": entry.0.name ?? "", "worldRoot": [roots[index].x, roots[index].y],
             "projectedRoot": [projected.x, projected.y],
             "size": [entry.0.size.width, entry.0.size.height], "anchor": [entry.0.anchorPoint.x, entry.0.anchorPoint.y],
             "scale": [entry.0.xScale, entry.0.yScale], "rotation": entry.0.zRotation,
             "hidden": entry.0.isHidden, "alpha": entry.0.alpha,
             "projectedBasisX": [entry.0.convert(CGPoint(x: 1, y: 0), to: scene).x - projected.x, entry.0.convert(CGPoint(x: 1, y: 0), to: scene).y - projected.y],
             "projectedBasisY": [entry.0.convert(CGPoint(x: 0, y: 1), to: scene).x - projected.x, entry.0.convert(CGPoint(x: 0, y: 1), to: scene).y - projected.y]]
        }
        let itemRecords: [[String: Any]] = depthItems.map { item in
            let footprint: Any
            if let bounds = item.solidBounds { footprint = [bounds.minX, bounds.minY, bounds.maxX, bounds.maxY] }
            else { footprint = NSNull() }
            return ["name": item.name, "worldRoot": [item.worldRoot.x, item.worldRoot.y], "footprint": footprint,
                    "projectedRootY": item.projectedRootY]
        }
        let constraints: [[String: Any]] = ordered.edges.map { edge in
            ["back": edge.back, "front": edge.front, "separations": edge.separations.map {
                ["axis": $0.axis.rawValue, "backMinimum": $0.backMinimum, "frontMaximum": $0.frontMaximum] as [String: Any]
            }]
        }
        let shadow = try XCTUnwrap(scene.childNode(withName: "//shadow-player"))
        let shadowProjected = shadow.convert(CGPoint.zero, to: scene)
        let image = try XCTUnwrap(view.texture(from: scene, crop: crop)).cgImage()
        var hashes: [String: String] = [:]
        func attach(_ image: UIImage, _ suffix: String) throws {
            let bytes = try XCTUnwrap(image.pngData())
            let attachment = XCTAttachment(data: bytes, uniformTypeIdentifier: "public.png")
            attachment.name = name + suffix; attachment.lifetime = .keepAlways; add(attachment); hashes[suffix] = sha(bytes)
        }
        try attach(UIImage(cgImage: image), "-native")
        let format = UIGraphicsImageRendererFormat(); format.scale = 1
        let halfSize = CGSize(width: image.width / 2, height: image.height / 2)
        let half = UIGraphicsImageRenderer(size: halfSize, format: format).image { _ in UIImage(cgImage: image).draw(in: CGRect(origin: .zero, size: halfSize)) }
        try attach(half, "-half")
        let filter = try XCTUnwrap(CIFilter(name: "CIColorControls"))
        filter.setValue(CIImage(cgImage: image), forKey: kCIInputImageKey); filter.setValue(0, forKey: kCIInputSaturationKey)
        let gray = try XCTUnwrap(filter.outputImage)
        try attach(UIImage(cgImage: try XCTUnwrap(CIContext().createCGImage(gray, from: gray.extent))), "-grayscale")
        return ["name": name, "nativePixels": [image.width, image.height], "pngSHA256": hashes, "actors": actors,
                "depthOrder": depthOrder, "depthBase": depthBase, "depthBand": 0.5,
                "depthItems": itemRecords, "depthConstraints": constraints,
                "playerShadowProjectedRoot": [shadowProjected.x, shadowProjected.y],
                "centerWorld": [center.x, center.y]]
    }
}
#endif
