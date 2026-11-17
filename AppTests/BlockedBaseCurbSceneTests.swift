import CoreImage
import CryptoKit
import SpriteKit
import UIKit
import XCTest
@testable import SSRuntime
@testable import SurveillanceCore

#if DEBUG && SS_SOURCE_SCENE_REVIEW && SS_BLOCKED_BASE_CURB_REVIEW
/// BP-001/007/012/T1045, intent/2026-11-16-blocked-base-curb-relief.md.
/// ADAPT current AppTests/FootprintGroundSceneTests.swift:1-748, not failed2317.
/// Both arms retain the V8 candidate. Only candidate adds explicitly counted supplements.
/// ADAPT: WholeSceneBoundInputsTests.swift:19-44,64-78,185-241.
/// Two quiet ordinary composition arms only. One south-neutral and one Camera-neutral
/// source, NOT a 16-frame family. Missing source preparation is a failure, never a skip.
final class BlockedBaseCurbSceneTests: XCTestCase {
    private let fixtureVersion = "source-scene-base-curb-009-relief"
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
    private struct Building: Decodable, Equatable {
        let role: String
        let nodeName: String
        let solidID: String
        let groundPixelsTopLeft: [[Double]]
    }
    private struct Landmark: Decodable, Equatable {
        let world: [Double]
        let sourcePixelsTopLeft: [Double]
        let provenance: String
    }
    private struct ContactBuilding: Decodable, Equatable {
        let id: String
        let minWorld: [Double]
        let maxWorld: [Double]
        let foundationWorld: [[Double]]
        let actualContactWorld: [[Double]]
        let meshContactStatus: String
        let contactLandmarks: [Landmark]
    }
    private struct Prop: Decodable, Equatable {
        let name: String
        let oldWorldRoot: [Double]
        let worldRoot: [Double]
        let contactRadiusWorld: Double
        let shadowRadiusWorld: Double
        let shadowAlphaMax: Double
    }
    private struct ScenePlan: Decodable, Equatable {
        let props: [Prop]
        let buildings: [ContactBuilding]
    }
    private struct Input: Decodable {
        let schema: String
        let assemblySHA256: String
        let fixtureVersion: String
        let harnessSourceSHA256: String
        let sources: [Source]
        let center: [Double]
        let buildings: [Building]
        let baselineRecordSHA256: String
        let planSHA256: String
        let scenePlan: ScenePlan
        let supplements: [Supplement]
        let supplementalManifestSHA256: String
    }
    private struct Supplement: Decodable {
        let role: String
        let nodeName: String
        let file: String
        let sha256: String
        let registration: Registration
        let verticesWorldXYZ: [[Double]]
        let verticesPixelsTopLeft: [[Double]]
        let footprintWorld: [Double]
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
    @MainActor private func readAuthoritativeScenePlacement() throws {
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
        let packet = repository.appendingPathComponent("docs/review/blocked-base-curb-relief-20261116/scene")
        let prepared = packet.appendingPathComponent("native-inputs-v9")
        let inputURL = prepared.appendingPathComponent("native-inputs.json")
        try require(inputURL.resolvingSymlinksInPath().path == inputURL.path, "Prepared manifest path alias forbidden")
        try require(FileManager.default.fileExists(atPath: inputURL.path),
                    "SOURCE PENDING: run packet/native.py prepare after coordinator recommendations. No fallback or skip.")
        let inputBytes = try Data(contentsOf: inputURL)
        let input = try JSONDecoder().decode(Input.self, from: inputBytes)
        try require(input.schema == "source-scene-native-009" && input.fixtureVersion == fixtureVersion, "Unknown native preparation schema/fixtureVersion")
        let sourceReadSHA256 = sha(try Data(contentsOf: URL(fileURLWithPath: #filePath)))
        let loadedExecutable = try XCTUnwrap(Bundle(for: Self.self).executableURL, "Actual loaded test bundle executable is required")
        let loadedExecutableSHA256 = sha(try Data(contentsOf: loadedExecutable))
        let assembly = try Data(contentsOf: packet.appendingPathComponent("assembly.json"))
        try require(sha(assembly) == input.assemblySHA256, "Stale assembly preparation")
        try require(sourceReadSHA256 == input.harnessSourceSHA256, "Stale harness source preparation, not binary attestation")
        try require(input.sources.count == 10 && Set(input.sources.map(\.role)) == Set(["paving", "camera", "player", "stone", "kiosk", "context-01", "context-02", "context-04", "context-05", "ground-plan"]), "Ten exact source roles required")
        try require(input.buildings.count == 5 && Set(input.buildings.map(\.role)) == Set(["kiosk", "context-01", "context-02", "context-04", "context-05"]), "Five explicit building bindings required")
        let baselineURL = repository.appendingPathComponent("docs/review/footprint-ground-repair-20261116/scene/native-capture-v8/source-scene-records.json")
        try require(input.baselineRecordSHA256 == "f7a8e0119307305fa4cfd15281871f1c852787d3f6c1ba3d0bc2342c421bf762" && sha(try Data(contentsOf: baselineURL)) == input.baselineRecordSHA256, "Immutable v7 baseline drift")
        try require(input.center == [684, 724], "Exact v8 presentation-only center required")
        let assemblyObject = try XCTUnwrap(JSONSerialization.jsonObject(with: assembly) as? [String: Any])
        let supplementBinding = try XCTUnwrap(assemblyObject["supplementalBinding"] as? [String: Any])
        let supplementManifest = try XCTUnwrap(supplementBinding["manifest"] as? [String: Any])
        try verifyDependency(supplementManifest)
        try require(supplementManifest["sha256"] as? String == input.supplementalManifestSHA256, "Supplement manifest drift")
        let supplementalRecommendation = try XCTUnwrap(supplementBinding["recommendation"] as? [String: Any])
        try require(supplementalRecommendation["reviewerRole"] as? String == "coordinator" && supplementalRecommendation["decision"] as? String == "recommended" && supplementalRecommendation["scope"] as? String == "isolated-ordinary-scene" && supplementalRecommendation["manifestSHA256"] as? String == input.supplementalManifestSHA256, "Final exact coordinator supplement recommendation required")
        try verifyDependency(try XCTUnwrap(supplementalRecommendation["evidence"] as? [String: Any]))
        let supplementalData = try JSONSerialization.data(withJSONObject: try XCTUnwrap(assemblyObject["supplements"]), options: [.sortedKeys])
        try require(supplementalData == JSONSerialization.data(withJSONObject: try XCTUnwrap((JSONSerialization.jsonObject(with: inputBytes) as? [String: Any])?["supplements"]), options: [.sortedKeys]), "Prepared supplement drift")
        for dep in try XCTUnwrap(supplementBinding["dependencies"] as? [[String: Any]]) { try verifyDependency(dep) }
        try require(!input.supplements.isEmpty && Set(input.supplements.map(\.nodeName)).count == input.supplements.count, "Missing/duplicate supplemental nodes")
        var supplementalTextures: [String: SKTexture] = [:]
        for item in input.supplements {
            try require(item.nodeName == "supplement-" + item.role && item.file == item.role + ".png", "Unsafe supplement identity")
            try require(!item.role.isEmpty && item.role.allSatisfy { $0.isASCII && ($0.isLetter || $0.isNumber || $0 == "-") }, "Unsafe supplemental path")
            let bytes = try Data(contentsOf: prepared.appendingPathComponent(item.file))
            try require(sha(bytes) == item.sha256, "Supplement source drift")
            let image = try XCTUnwrap(UIImage(data: bytes)?.cgImage)
            let reg = item.registration
            try require([reg.canvasPixels, reg.rootPixelsTopLeft, reg.worldPosition, reg.drawSizeWorld].allSatisfy { $0.count == 2 && $0.allSatisfy(\.isFinite) } && reg.drawSizeWorld.allSatisfy { $0 > 0 }, "Finite positive supplemental registration required")
            try require(item.registration.canvasPixels == [Double(image.width), Double(image.height)], "Supplement canvas mismatch")
            try require(item.verticesWorldXYZ.count >= 6 && item.verticesWorldXYZ.count == item.verticesPixelsTopLeft.count && item.footprintWorld.count == 4, "Explicit supplemental XYZ geometry required")
            supplementalTextures[item.role] = try texture(bytes)
        }
        let assemblySources = try XCTUnwrap(assemblyObject["sources"] as? [[String: Any]])
        try require(assemblySources.count == 10, "Assembly source census mismatch")
        let planBinding = try XCTUnwrap(assemblyObject["planBinding"] as? [String: Any])
        let planDependency = try XCTUnwrap(planBinding["plan"] as? [String: Any])
        try verifyDependency(planDependency)
        try verifyDependency(try XCTUnwrap(planBinding["manifest"] as? [String: Any]))
        let planBytes = try Data(contentsOf: repository.appendingPathComponent(try XCTUnwrap(planDependency["path"] as? String)))
        try require(sha(planBytes) == input.planSHA256, "Stale semantic plan hash")
        try require(try JSONDecoder().decode(ScenePlan.self, from: planBytes) == input.scenePlan, "Prepared semantic plan does not match source plan")
        let planRecommendation = try XCTUnwrap(planBinding["recommendation"] as? [String: Any])
        try require(planRecommendation["reviewerRole"] as? String == "coordinator" && planRecommendation["decision"] as? String == "recommended" && planRecommendation["scope"] as? String == "isolated-ordinary-scene" && planRecommendation["planSHA256"] as? String == input.planSHA256, "Coordinator must bind exact semantic plan")
        try verifyDependency(try XCTUnwrap(planRecommendation["evidence"] as? [String: Any]))
        try require(input.scenePlan.props.map(\.name) == ["benchmark-prop-0", "benchmark-prop-1"], "Exact planned prop census required")
        for dependency in try XCTUnwrap(assemblyObject["contextDependencies"] as? [[String: Any]]) { try verifyDependency(dependency) }
        let buildingData = try JSONSerialization.data(withJSONObject: try XCTUnwrap(assemblyObject["buildings"]), options: [.sortedKeys])
        try require(try JSONDecoder().decode([Building].self, from: buildingData) == input.buildings, "Prepared building geometry drift")
        var textures: [String: SKTexture] = [:]
        var sources: [String: Source] = [:]
        for source in input.sources {
            try require(source.file == source.role + ".png" && source.recommendation == "coordinator-recommended", "Unadmitted source/path")
            let original = try XCTUnwrap(assemblySources.first { $0["role"] as? String == source.role })
            let recommendation = try XCTUnwrap(original["recommendation"] as? [String: Any])
            let originalImage = try XCTUnwrap(original["image"] as? [String: Any])
            try verifyDependency(originalImage)
            if let dependencies = original["dependencies"] as? [[String: Any]] {
                for dependency in dependencies { try verifyDependency(dependency) }
            }
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
        let paving = try XCTUnwrap(sources["paving"]), groundPlan = try XCTUnwrap(sources["ground-plan"])
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
            func propRoot(_ index: Int) -> CGPoint {
                let p = input.scenePlan.props[index]
                let root = p.worldRoot
                return CGPoint(x: root[0], y: root[1])
            }
            let canvas = CGFloat(1254) * (CGFloat(128) * CGFloat(2).squareRoot() / 934)
            var art = BenchmarkReviewArt(player: try XCTUnwrap(controls["painted-player-south"]), camera: try XCTUnwrap(controls["camera"]),
                building: .init(texture: try XCTUnwrap(controls["building-constrained"]), size: CGSize(width: canvas, height: canvas),
                    anchor: CGPoint(x: CGFloat(653) / 1254, y: 1 - CGFloat(1152) / 1254), position: CGPoint(x: box.minX, y: box.minY)),
                buildingID: buildingID, props: [
                    .init(texture: try XCTUnwrap(controls["newsbox"]), size: CGSize(width: 20, height: 40), anchor: CGPoint(x: 0.5, y: 0), position: propRoot(0)),
                    .init(texture: try XCTUnwrap(controls["tree"]), size: CGSize(width: 50, height: 85), anchor: CGPoint(x: 0.5, y: 0), position: propRoot(1))], paving: plaza)
            art.configureStreetCorner(asphalt: asphalt)
            do { // Both arms retain V7 non-ground treatments.
                let buildingSource = try XCTUnwrap(sources["kiosk"])
                art = BenchmarkReviewArt(player: try XCTUnwrap(textures["player"]), camera: try XCTUnwrap(textures["camera"]),
                    building: .init(texture: try XCTUnwrap(textures[buildingSource.role]), size: buildingSource.registration.size,
                                    anchor: buildingSource.registration.anchor, position: buildingSource.registration.position),
                    buildingID: buildingID, props: art.props, paving: plaza)
                let r = groundPlan.registration
                try require(r.drawSizeWorld == [2304, 2304] && r.worldPosition == [0, 0] && r.rootPixelsTopLeft == [0, r.canvasPixels[1]], "Square ground adapter registration drift")
                let arena = snap.arenaBounds
                let bounds = CGRect(x: CGFloat(arena.minX), y: CGFloat(arena.minY), width: CGFloat(arena.maxX - arena.minX), height: CGFloat(arena.maxY - arena.minY))
                try require(bounds == CGRect(x: 0, y: 0, width: 2304, height: 1536), "Authoritative arena ground coverage drift")
                art.groundPatches = [.init(texture: try XCTUnwrap(textures["ground-plan"]), bounds: bounds, tileUnits: r.size.width)]
            }
            // Deliberately NO installBenchmarkCameraFrames: exactly one static neutral texture.
            scene.renderBenchmark(snapshot: snap, art: art, center: CGPoint(x: input.center[0], y: input.center[1]))
            // Register the four replacement context images at unchanged authoritative centers.
            // Never alter parent, scale, depth, visibility, or any non-target context node.
            do { // Both arms preserve all five V7 building images/registrations.
                for binding in input.buildings where binding.role != "kiosk" {
                    let node = try XCTUnwrap(scene.childNode(withName: "//" + binding.nodeName) as? SKSpriteNode)
                    let source = try XCTUnwrap(sources[binding.role])
                    let solid = snap.solids[try XCTUnwrap(snap.solidIds.firstIndex(of: binding.solidID))]
                    try require(source.registration.worldPosition == [Double(solid.center.x), Double(solid.center.y)], "Context must retain authoritative center")
                    let root = node.convert(CGPoint.zero, to: scene)
                    try require(root == source.registration.position, "Context root drift")
                    node.texture = try XCTUnwrap(textures[binding.role])
                    node.size = source.registration.size
                    node.anchorPoint = source.registration.anchor
                }
            }
            let playerNode = try XCTUnwrap(scene.childNode(withName: "//sprite-player") as? SKSpriteNode)
            let cameraNode = try XCTUnwrap(scene.childNode(withName: "//sprite-camera-\(selected.id.raw)") as? SKSpriteNode)
            do { // Both arms retain V7 non-ground treatments.
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
            do { // Both arms retain V7 non-ground treatments.
                // BP-010 comparison only. The source pixels and production border stay unchanged.
                playerOutline.alpha = 0
                let parent = try XCTUnwrap(playerShadow.parent)
                playerShadow.position = parent.convert(player.registration.position, from: scene)
            }
            XCTAssertEqual(playerOutline.alpha, 0)
            XCTAssertTrue(playerShadow.texture === shadowTexture)
            XCTAssertEqual(playerShadow.size, shadowSize)
            let observedShadowRoot = playerShadow.convert(CGPoint.zero, to: scene)
            do { // Both arms retain V7 non-ground treatments.
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
            var buildingHashes: [String: String] = ["benchmark-building": try XCTUnwrap(sources["kiosk"]).sha256]
            for node in environmentNodes {
                let name = try XCTUnwrap(node.name)
                if let binding = input.buildings.first(where: { $0.nodeName == name }) {
                    buildingHashes[name] = try XCTUnwrap(sources[binding.role]).sha256
                } else {
                    let asset = String(name.dropFirst("environment-upright-".count))
                    let path = try XCTUnwrap(try EnvironmentLibrary.bundled().path(for: asset))
                    let url = try XCTUnwrap(RuntimeAssetBundle.url(forFile: path))
                    buildingHashes[name] = sha(try Data(contentsOf: url))
                }
            }
            let actorNodes = try names.map { try XCTUnwrap(scene.childNode(withName: "//" + $0) as? SKSpriteNode) }
            let inventoryNodes = actorNodes + environmentNodes
            for node in inventoryNodes {
                var ancestor: SKNode? = node
                while let current = ancestor {
                    try require(!current.isHidden && current.alpha == 1, "No upright may have a hidden/transparent ancestor")
                    ancestor = current.parent
                }
            }
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
            var supplementalNodes: [SKSpriteNode] = []
            if arm == "candidate" {
                let supplementContainer = SKNode()
                supplementContainer.name = "review-only-supplement-container"
                scene.addChild(supplementContainer)
                for item in input.supplements {
                    let node = SKSpriteNode(texture: try XCTUnwrap(supplementalTextures[item.role]))
                    node.name = item.nodeName
                    node.size = item.registration.size
                    node.anchorPoint = item.registration.anchor
                    node.position = item.registration.position
                    // Zero preprojection Z, no visibility boost. Joint geometry ordering below.
                    node.zPosition = 0
                    supplementContainer.addChild(node)
                    supplementalNodes.append(node)
                    let b = item.footprintWorld
                    footprints[item.nodeName] = .init(minX: b[0], minY: b[1], maxX: b[2], maxY: b[3])
                }
            }
            try require(inventory.count == 18 && supplementalNodes.count == (arm == "candidate" ? input.supplements.count : 0), "Explicit old/new census")
            var discoveredSupplements: [SKSpriteNode] = []
            scene.enumerateChildNodes(withName: "//supplement-*") { node, _ in
                if let sprite = node as? SKSpriteNode { discoveredSupplements.append(sprite) }
            }
            try require(Set(discoveredSupplements.map { ObjectIdentifier($0) }) == Set(supplementalNodes.map { ObjectIdentifier($0) }) && discoveredSupplements.count == supplementalNodes.count, "Independent supplemental extraction census differs")
            uprights += supplementalNodes
            let originalLocalDepths = uprights.map(\.zPosition)
            for zoom: CGFloat in [1, 1.25, 1.4] {
                var record = try capture(scene: scene, view: view, uprights: uprights, footprints: footprints, zoom: zoom,
                                         name: "source-scene-\(arm)-ordinary-z\(Int((zoom * 100).rounded()))",
                                         bindings: input.buildings, sources: sources, plan: input.scenePlan, arm: arm, supplements: arm == "candidate" ? input.supplements : [])
                for (node, originalZ) in zip(uprights, originalLocalDepths) { XCTAssertEqual(node.zPosition, originalZ) }
                XCTAssertEqual(hud.children.map(\.isHidden), hudHidden)
                XCTAssertEqual(field.path, fieldPath)
                XCTAssertEqual(scene.session.simulation.state.digest(), before)
                record["buildingSourceSHA256"] = buildingHashes
                record["comparisonRole"] = arm == "control" ? "BASELINE_V8_CANDIDATE" : "CANDIDATE_V9_BASE_CURB_RELIEF"
                record["preprojectionInventory"] = inventory
                record["expectedEnvironmentNames"] = expectedEnvironmentNames
                record["uprightCount"] = inventory.count
                record["supplementalCount"] = supplementalNodes.count
                record["totalPresentationUprightCount"] = inventory.count + supplementalNodes.count
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
                record["shadowTreatment"] = "ground-root-existing-soft-shadow"
                record["groundBounds"] = [snap.arenaBounds.minX, snap.arenaBounds.minY, snap.arenaBounds.maxX - snap.arenaBounds.minX, snap.arenaBounds.maxY - snap.arenaBounds.minY]
                record["groundSourceWorldSize"] = paving.registration.drawSizeWorld
                record["solidCount"] = snap.solids.count
                captures.append(record)
            }
        }
        XCTAssertEqual(captures.count, 6)
        let record: [String: Any] = ["schema": "source-scene-records-009", "status": "NATIVE_QUIET_SOURCE_COMPARISON_NOT_ACCEPTANCE",
            "fixtureVersion": fixtureVersion, "baselineRecordSHA256": input.baselineRecordSHA256,
            "loadedTestExecutable": ["path": loadedExecutable.path, "sha256": loadedExecutableSHA256],
            "fixture": "south-neutral-camera-neutral", "cameraSourceFrames": 1, "playerSourceFrames": 1,
            "inputSHA256": sha(inputBytes), "assemblySHA256": input.assemblySHA256,
            "harnessSourceReadSHA256": sourceReadSHA256, "planSHA256": input.planSHA256,
            "supplementalManifestSHA256": input.supplementalManifestSHA256,
            "sourceSHA256": Dictionary(uniqueKeysWithValues: input.sources.map { ($0.role, $0.sha256) }),
            "controlSHA256": controlHashes, "runtimeSHA256": runtimeHashes, "captures": captures]
        let attachment = XCTAttachment(data: try JSONSerialization.data(withJSONObject: record, options: [.prettyPrinted, .sortedKeys]), uniformTypeIdentifier: "public.json")
        attachment.name = "source-scene-records"; attachment.lifetime = .keepAlways; add(attachment)
    }

    /// Logical crop coordinates are top-left, x right/y down, never native pixels.
    @MainActor private func framing(scene: GameScene, view: SKView, crop: CGRect,
                                    actors: [SKSpriteNode]) throws -> [String: Any] {
        try require(view.bounds.size == viewport && view.safeAreaInsets == .zero, "Exact offscreen viewport/safe area required")
        let layout = try XCTUnwrap(scene.controlLayout)
        let projector = HUDProjector(viewSize: viewport, safeInsets: .zero, sceneSize: viewport)
        let expectedLayout = ControlLayout.make(projector: projector, handedness: .right)
        try require(layout.stickCentre == expectedLayout.stickCentre && layout.stickRadius == expectedLayout.stickRadius &&
                    layout.dodgeRect == expectedLayout.dodgeRect && layout.pauseRect == expectedLayout.pauseRect,
                    "Production visible control layout changed")
        func values(_ rect: CGRect) -> [CGFloat] { [rect.minX, rect.minY, rect.width, rect.height] }
        func projected(_ rect: CGRect, from node: SKNode) -> CGRect {
            let points = [CGPoint(x: rect.minX, y: rect.minY), CGPoint(x: rect.maxX, y: rect.minY),
                          CGPoint(x: rect.minX, y: rect.maxY), CGPoint(x: rect.maxX, y: rect.maxY)].map { node.convert($0, to: scene) }
            let xs = points.map(\.x), ys = points.map(\.y)
            return CGRect(x: xs.min()! - crop.minX, y: crop.maxY - ys.max()!,
                          width: xs.max()! - xs.min()!, height: ys.max()! - ys.min()!)
        }
        func visible(_ node: SKNode) throws {
            var current: SKNode? = node
            while let value = current {
                try require(!value.isHidden && value.alpha > 0, "Visible control has hidden/transparent ancestor")
                current = value.parent
            }
        }
        func close(_ actual: CGRect, _ expected: CGRect) throws {
            try require(zip(values(actual), values(expected)).allSatisfy { pair in abs(pair.0 - pair.1) <= 0.002 }, "Visible path differs from control layout")
        }
        let stickRect = CGRect(x: layout.stickCentre.x - layout.stickRadius, y: layout.stickCentre.y - layout.stickRadius,
                               width: layout.stickRadius * 2, height: layout.stickRadius * 2)
        let definitions: [(String, String, CGRect)] = [
            ("stick", RuntimeAssetRegistry.HUD.stickBase, stickRect),
            ("dodge", RuntimeAssetRegistry.HUD.dodge, layout.dodgeRect),
            ("pause", RuntimeAssetRegistry.HUD.pause, layout.pauseRect)]
        var controlRecords: [[String: Any]] = []
        var controlBounds: [CGRect] = []
        for (role, name, layoutRect) in definitions {
            let node = try XCTUnwrap(scene.childNode(withName: "//" + name) as? SKShapeNode)
            try visible(node)
            try require(node.glowWidth == 0 && node.lineWidth > 0, "Unexpected control glow/stroke")
            let path = try XCTUnwrap(node.path)
            let pathBounds = projected(path.boundingBoxOfPath, from: node)
            try close(pathBounds, layoutRect)
            // Conservative visible path-plus-stroke bounds, not the invisible activation zone.
            let bounds = projected(path.boundingBoxOfPath.insetBy(dx: -node.lineWidth / 2, dy: -node.lineWidth / 2), from: node)
            try require(CGRect(origin: .zero, size: viewport).contains(bounds), "Visible control clipped")
            if role == "stick" {
                let knob = try XCTUnwrap(scene.childNode(withName: "//" + RuntimeAssetRegistry.HUD.stickKnob) as? SKShapeNode)
                try visible(knob)
                let knobBounds = projected(try XCTUnwrap(knob.path).boundingBoxOfPath.insetBy(dx: -knob.lineWidth / 2, dy: -knob.lineWidth / 2), from: knob)
                try require(bounds.contains(knobBounds), "Stick knob extends beyond recorded visible base")
            } else {
                let parent = try XCTUnwrap(node.parent)
                let label = try XCTUnwrap(parent.children.first { $0.userData?["hudElementKey"] as? String == "control-" + role + "-label" })
                try visible(label)
                try require(bounds.contains(projected(label.calculateAccumulatedFrame(), from: parent)), "Control label extends beyond recorded graphics")
            }
            controlBounds.append(bounds)
            controlRecords.append(["role": role, "nodeName": name, "bounds": values(bounds),
                                   "pathBounds": values(pathBounds), "layoutBounds": values(layoutRect),
                                   "lineWidth": node.lineWidth, "alpha": node.alpha, "hidden": node.isHidden])
        }
        var actorRecords: [[String: Any]] = []
        for node in actors.prefix(2) {
            let canvas = CGRect(x: -node.anchorPoint.x * node.size.width, y: -node.anchorPoint.y * node.size.height,
                                width: node.size.width, height: node.size.height)
            let bounds = projected(canvas, from: node)
            try require(CGRect(origin: .zero, size: viewport).contains(bounds), "Player/Camera canvas clipped")
            for control in controlBounds { try require(!bounds.intersects(control), "Player/Camera canvas overlaps visible control") }
            actorRecords.append(["name": try XCTUnwrap(node.name), "bounds": values(bounds)])
        }
        return ["coordinateSystem": "logical-crop-top-left-704x326", "visibleControls": controlRecords,
                "actorCanvasBounds": actorRecords, "safeAreaInsets": [0, 0, 0, 0]]
    }

    /// ADAPT WholeSceneBoundInputsTests.capture: midpoint world with upright roots,
    /// production camera/HUD outside the projected world, three retained zooms.
    @MainActor private func capture(scene: GameScene, view: SKView, uprights: [SKSpriteNode], footprints: [String: SceneQAReviewDepth.Bounds], zoom: CGFloat, name: String, bindings: [Building], sources: [String: Source], plan: ScenePlan, arm: String, supplements: [Supplement]) throws -> [String: Any] {
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
        // Actual scene conversion of each authoritative ground vertex, not a guessed alpha bound.
        var footprintRecords: [[String: Any]] = []
        for node in uprights.prefix(18) where footprints[node.name ?? ""] != nil {
            let nodeName = try XCTUnwrap(node.name)
            let bounds = try XCTUnwrap(footprints[nodeName])
            let vertices = [[bounds.minX, bounds.minY], [bounds.maxX, bounds.minY],
                            [bounds.maxX, bounds.maxY], [bounds.minX, bounds.maxY]]
            let ground = vertices.map { chain.coordinates.convert(CGPoint(x: $0[0], y: $0[1]), to: scene) }
            var witness: [String: Any] = ["nodeName": nodeName, "worldVertices": vertices,
                "projectedGround": ground.map { [$0.x, $0.y] }, "correspondence": "authority-only-baseline-source-not-rederived"]
            if let binding = bindings.first(where: { $0.nodeName == nodeName }) {
                let source = try XCTUnwrap(sources[binding.role]), reg = source.registration
                try require(binding.groundPixelsTopLeft.count == 4 && binding.groundPixelsTopLeft.allSatisfy { $0.count == 2 && $0.allSatisfy(\.isFinite) }, "Four explicit source ground vertices required")
                let local = binding.groundPixelsTopLeft.map { pixel in
                    CGPoint(x: (pixel[0] - reg.rootPixelsTopLeft[0]) * reg.drawSizeWorld[0] / reg.canvasPixels[0],
                            y: (reg.rootPixelsTopLeft[1] - pixel[1]) * reg.drawSizeWorld[1] / reg.canvasPixels[1])
                }
                let observed = local.map { node.convert($0, to: scene) }
                for (actual, expected) in zip(observed, ground) {
                    XCTAssertEqual(actual.x, expected.x, accuracy: 0.002, "Registered ground vertex X")
                    XCTAssertEqual(actual.y, expected.y, accuracy: 0.002, "Registered ground vertex Y")
                }
                witness["correspondence"] = "explicit-source-geometry"
                witness["role"] = binding.role
                witness["sourceSHA256"] = source.sha256
                witness["groundPixelsTopLeft"] = binding.groundPixelsTopLeft
                witness["localVertices"] = local.map { [$0.x, $0.y] }
                witness["projectedSource"] = observed.map { [$0.x, $0.y] }
            }
            footprintRecords.append(witness)
        }
        let crop = CGRect(x: center.x - 352, y: center.y - 163, width: 704, height: 326)
        var contactRecords: [[String: Any]] = []
        for node in uprights.prefix(18) where footprints[node.name ?? ""] != nil {
            let nodeName = try XCTUnwrap(node.name)
            let canvas = CGRect(x: -node.anchorPoint.x * node.size.width, y: -node.anchorPoint.y * node.size.height,
                                width: node.size.width, height: node.size.height)
            let lower = node.convert(CGPoint(x: canvas.minX, y: canvas.minY), to: scene)
            let upper = node.convert(CGPoint(x: canvas.maxX, y: canvas.maxY), to: scene)
            let bounds = CGRect(x: lower.x, y: lower.y, width: upper.x - lower.x, height: upper.y - lower.y)
            guard bounds.intersects(crop) else { continue }
            let binding = try XCTUnwrap(bindings.first { $0.nodeName == nodeName }, "Visible building lacks source geometry binding")
            let contact = try XCTUnwrap(plan.buildings.first { $0.id == binding.solidID })
            let source = try XCTUnwrap(sources[binding.role]), reg = source.registration
            try require(contact.meshContactStatus == "actual-z0-face-vertices" && contact.contactLandmarks.count >= 3 && contact.actualContactWorld == contact.contactLandmarks.map(\.world), "Actual visible contact contour required, never virtual footprint corners")
            var landmarks: [[String: Any]] = []
            for landmark in contact.contactLandmarks {
                try require(landmark.world.count == 2 && landmark.sourcePixelsTopLeft.count == 2 && landmark.provenance == "actual-z0-mesh-vertex", "Invalid actual source contact")
                let pixel = landmark.sourcePixelsTopLeft
                let local = CGPoint(x: (pixel[0] - reg.rootPixelsTopLeft[0]) * reg.drawSizeWorld[0] / reg.canvasPixels[0],
                                    y: (reg.rootPixelsTopLeft[1] - pixel[1]) * reg.drawSizeWorld[1] / reg.canvasPixels[1])
                let actual = node.convert(local, to: scene)
                let groundPoint = chain.coordinates.convert(CGPoint(x: landmark.world[0], y: landmark.world[1]), to: scene)
                XCTAssertEqual(actual.x, groundPoint.x, accuracy: 0.002, "Actual source contact X")
                XCTAssertEqual(actual.y, groundPoint.y, accuracy: 0.002, "Actual source contact Y")
                landmarks.append(["world": landmark.world, "sourcePixelsTopLeft": pixel, "provenance": landmark.provenance,
                                  "projectedSource": [actual.x, actual.y], "projectedGround": [groundPoint.x, groundPoint.y],
                                  "inCrop": crop.contains(actual)])
            }
            contactRecords.append(["nodeName": nodeName, "solidID": binding.solidID, "sourceSHA256": source.sha256,
                                   "canvasIntersectsCrop": true, "meshContactStatus": contact.meshContactStatus,
                                   "landmarks": landmarks])
        }
        try require(contactRecords.count == 5, "Every visible V7 building must retain actual contact witnesses")
        var patches: [SKSpriteNode] = []
        scene.enumerateChildNodes(withName: "//benchmark-ground-patch-*") { node, _ in
            if let sprite = node as? SKSpriteNode { patches.append(sprite) }
        }
        let patch = try XCTUnwrap(patches.count == 1 ? patches.first : nil, "Exactly one complete ground patch")
        try require(patch.size == CGSize(width: 2304, height: 1536) && patch.anchorPoint == CGPoint(x: 0.5, y: 0.5) && patch.zPosition == CGFloat(Float(0.1)) && !patch.isHidden && patch.alpha == 1, "Ground patch coverage/transform drift: size=\(patch.size), anchor=\(patch.anchorPoint), zPosition=\(patch.zPosition), expectedStoredZ=\(CGFloat(Float(0.1))), hidden=\(patch.isHidden), alpha=\(patch.alpha)")
        let groundCorners = [[0.0, 0.0], [2304.0, 0.0], [2304.0, 1536.0], [0.0, 1536.0]]
        let patchCorners = groundCorners.map { point in patch.convert(CGPoint(x: point[0] - 1152, y: point[1] - 768), to: scene) }
        for (point, observed) in zip(groundCorners, patchCorners) {
            let expected = chain.coordinates.convert(CGPoint(x: point[0], y: point[1]), to: scene)
            XCTAssertEqual(observed.x, expected.x, accuracy: 0.002)
            XCTAssertEqual(observed.y, expected.y, accuracy: 0.002)
        }
        let groundRole = "ground-plan"
        let groundRecord: [String: Any] = ["nodeName": try XCTUnwrap(patch.name), "sourceRole": groundRole,
            "sourceSHA256": try XCTUnwrap(sources[groundRole]).sha256, "planApplied": true,
            "size": [patch.size.width, patch.size.height], "anchor": [patch.anchorPoint.x, patch.anchorPoint.y],
            "zPosition": patch.zPosition, "alpha": patch.alpha, "hidden": patch.isHidden,
            "worldCorners": groundCorners, "projectedCorners": patchCorners.map { [$0.x, $0.y] }]
        let propRecords: [[String: Any]] = try plan.props.map { prop in
            let node = try XCTUnwrap(uprights.first { $0.name == prop.name })
            let index = try XCTUnwrap(uprights.firstIndex { $0 === node })
            let expected = prop.worldRoot
            try require([Double(roots[index].x), Double(roots[index].y)] == expected, "Prop root must match exact plan arm")
            let projected = node.convert(CGPoint.zero, to: scene)
            return ["nodeName": prop.name, "worldRoot": [roots[index].x, roots[index].y],
                    "projectedRoot": [projected.x, projected.y], "planApplied": true,
                    "contactRadiusWorld": prop.contactRadiusWorld, "shadowRadiusWorld": prop.shadowRadiusWorld,
                    "shadowAlphaMax": prop.shadowAlphaMax, "limitsMeaning": "candidate-baked-ground-plan-limits-not-measured-sprite-alpha"]
        }
        let framingRecord = try framing(scene: scene, view: view, crop: crop, actors: Array(uprights.prefix(18)))
        for node in uprights.prefix(2) { XCTAssertTrue(crop.contains(node.convert(CGPoint.zero, to: scene)), "Player/Camera root must be in the ordinary crop") }
        let allActors: [[String: Any]] = saved.enumerated().map { index, entry in
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
        var supplementalWitnesses: [[String: Any]] = []
        for item in supplements {
            let node = try XCTUnwrap(byName[item.nodeName])
            let r = item.registration
            var vertices: [[String: Any]] = []
            for (xyz, pixel) in zip(item.verticesWorldXYZ, item.verticesPixelsTopLeft) {
                try require(xyz.count == 3 && pixel.count == 2 && (xyz + pixel).allSatisfy(\.isFinite), "Finite XYZ/source landmarks required")
                let local = CGPoint(x: (pixel[0] - r.rootPixelsTopLeft[0]) * r.drawSizeWorld[0] / r.canvasPixels[0], y: (r.rootPixelsTopLeft[1] - pixel[1]) * r.drawSizeWorld[1] / r.canvasPixels[1])
                let actual = node.convert(local, to: scene)
                let ground = chain.coordinates.convert(CGPoint(x: xyz[0], y: xyz[1]), to: scene)
                let expected = CGPoint(x: ground.x, y: ground.y + CGFloat(xyz[2]) * zoom)
                XCTAssertEqual(actual.x, expected.x, accuracy: 0.002, "Supplement XYZ source X")
                XCTAssertEqual(actual.y, expected.y, accuracy: 0.002, "Supplement XYZ source height")
                vertices.append(["worldXYZ": xyz, "sourcePixelsTopLeft": pixel, "projectedSource": [actual.x, actual.y], "projectedWorldXYZ": [expected.x, expected.y]])
            }
            supplementalWitnesses.append(["nodeName": item.nodeName, "role": item.role, "sourceSHA256": item.sha256, "footprintWorld": item.footprintWorld, "vertices": vertices])
        }
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
        return ["name": name, "nativePixels": [image.width, image.height], "pngSHA256": hashes, "actors": Array(allActors.prefix(18)),
                "supplementalActors": Array(allActors.dropFirst(18)), "supplementalSourceWitnesses": supplementalWitnesses,
                "groundFootprints": footprintRecords, "visibleBuildingContacts": contactRecords,
                "groundPlanWitness": groundRecord, "propPlanWitnesses": propRecords,
                "framing": framingRecord,
                "depthOrder": depthOrder, "depthBase": depthBase, "depthBand": 0.5,
                "depthItems": itemRecords, "depthConstraints": constraints,
                "playerShadowProjectedRoot": [shadowProjected.x, shadowProjected.y],
                "centerWorld": [center.x, center.y]]
    }
}
#endif
