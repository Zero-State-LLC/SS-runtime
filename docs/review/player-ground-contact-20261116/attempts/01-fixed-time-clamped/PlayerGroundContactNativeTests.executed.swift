import XCTest
import CryptoKit
import SpriteKit
import UIKit
@testable import SSRuntime
@testable import SurveillanceCore

#if SS_RENDERER_TEST_SUPPORT
/// BP-008 slice2 native constrained comparison. Static explicit renderer passes,
/// not live display cadence. Reuses actual GameSession/Simulation steps and WorldRenderer.
@MainActor
final class PlayerGroundContactNativeTests: XCTestCase {
    private struct Leg: Decodable { let side: String; let contact: Bool; let toe: [Double] }
    private struct Pose: Decodable { let legs: [Leg] }
    private struct Row: Decodable { let sample: Int; let tick: UInt64; let commandX: Int16; let commandY: Int16
        let dodgePressed: Bool; let paused: Bool; let xRaw: Int64; let yRaw: Int64; let dxRaw: Int64; let dyRaw: Int64
        let dodgeRemaining: Int }
    private struct Trace: Decodable { let name: String; let rows: [Row]; let finalDigest: String }
    private struct Packet: Decodable { let traces: [Trace] }

    private let changed = [5, 6, 7, 13, 14, 15]
    private let expectedCandidate = [
        5: "dbe3821459409537792017ccd52386f7081c2a429a3e18d3c42603f391cc0d6d",
        6: "adb38595fac03147d8d423c5b6ffee967f22065f1d7be1dbecc2ab3b6a92cfb3",
        7: "2b1cbc45c241689934bfe7147fda57a3f6b407ba8b0a648ff5a06ad7c52c9a30",
        13: "eeda35fb7ea65efb6c1d60748f9cf1a8e31f2bda68731fc71d40584913b30325",
        14: "62ba49329f251bfae213d1c4e15fbae40bd299ec9f92767769c4e030bbace155",
        15: "9a407fa31aad599d20745bdbe5fa2042125e1da97a0b3160bafe82bbf55f4979"]

    private func sha(_ data: Data) -> String { SHA256.hash(data: data).map { String(format: "%02x", $0) }.joined() }
    private func data(_ name: String, _ ext: String) throws -> Data {
        try Data(contentsOf: try XCTUnwrap(Bundle(for: Self.self).url(forResource: name, withExtension: ext), name))
    }
    private func texture(_ bytes: Data) throws -> SKTexture {
        let image = try XCTUnwrap(UIImage(data: bytes)); XCTAssertEqual(image.size, CGSize(width: 384, height: 416))
        let texture = SKTexture(image: image); texture.filteringMode = .linear; return texture
    }

    func testNativeRendererContactsAcrossCoreTracesSelectionsAndSourceVariants() throws {
        let traces = try JSONDecoder().decode(Packet.self, from: data("player-groundcontact-core-traces", "json")).traces
        let poses = try JSONDecoder().decode([Pose].self, from: data("player-source-s-poses", "json"))
        XCTAssertEqual(sha(try data("player-source-s-poses", "json")), "376fa7adad571cb96ae275e0d5635c735ada34bef230c1678087ce8f03e03a90")
        var baselineData: [Data] = [], candidateData: [Data] = []
        for index in 0..<16 {
            let base = try data(String(format: "player-source-s-%02d", index), "png")
            baselineData.append(base)
            if changed.contains(index) {
                let proposal = try data(String(format: "player-groundcontact-candidate-%02d", index), "png")
                XCTAssertEqual(sha(proposal), expectedCandidate[index]); XCTAssertNotEqual(proposal, base)
                candidateData.append(proposal)
            } else { candidateData.append(base) }
        }
        // Approved release entries 5/13 are zero-based source indices 4/12 and remain byte-identical.
        XCTAssertEqual(sha(baselineData[4]), "c3a5d87a510040b2ee7ae15db599a0b2c48974ab2b2d851422640cbd4d4f826d")
        XCTAssertEqual(sha(baselineData[12]), "85e869ac7fdad2b981adef08655e1473c2db667cb3d25d36c5126ef01131a7c6")
        XCTAssertEqual(candidateData[4], baselineData[4]); XCTAssertEqual(candidateData[12], baselineData[12])
        let families = [("baseline", try baselineData.map(texture)), ("weight-transfer", try candidateData.map(texture))]
        let selected = ["quarter", "half", "full", "pause"]
        let fixed = try ClipTiming(unitsPerSecond: 32, frameUnits: Array(repeating: 1, count: 16))
        var records: [[String: Any]] = [], excluded: [String: Int] = [:], imageCount = 0
        for trace in traces where !selected.contains(trace.name) { excluded[trace.name] = trace.rows.count }
        let view = SKView(frame: CGRect(x: 0, y: 0, width: 704, height: 326))
        for trace in traces where selected.contains(trace.name) {
            for policy in ["fixed-time", "distance-phase"] {
                for (family, textures) in families {
                    let session = GameSession(simulation: { var s = try! Simulation.make(seed: 1)
                        s.testing_setPlayerPosition(VecI(x: 736, y: 654)); return s }())
                    let direction = ClipFrameLibrary.direction(forFacing: VecQ8(unitsX: -1, unitsY: -1))
                    let ids = (0..<16).map { String(format: "player_move_%@_%02d", direction, $0) }
                    let paths = (0..<16).map { String(format: "groundcontact-%@-%02d", family, $0) }
                    let move = ClipFrameLibrary.Clip(clipId: "player_move", actorRole: "player", directions: [direction],
                        framesPerSecond: nil, authoredTiming: fixed, loop: true, anchor: VecI(x: 32, y: 56), frameIds: ids)
                    let library = try XCTUnwrap(SpriteLibrary(benchmarkFrames: ClipFrameLibrary(clips: ["player_move": move],
                        deliveredPaths: Dictionary(uniqueKeysWithValues: zip(ids, paths))),
                        benchmarkTextures: Dictionary(uniqueKeysWithValues: zip(paths, textures))))
                    let renderer = WorldRenderer(sprites: library)
                    renderer.benchmarkPlayerRegistration = (CGSize(width: 64, height: 416.0 / 6.0), CGPoint(x: 0.5, y: 1 - 336.0 / 416.0))
                    let scene = SKScene(size: view.bounds.size), squash = SKNode(), rotation = SKNode(), translation = SKNode()
                    scene.addChild(squash); squash.addChild(rotation); rotation.addChild(translation); translation.addChild(renderer.root)
                    squash.position = CGPoint(x: 352, y: 163); squash.yScale = 0.5; rotation.zRotation = .pi / 4
                    translation.position = CGPoint(x: -736, y: -654)
                    let upright = SKSpriteNode(); upright.name = "groundcontact-upright-player"; scene.addChild(upright)
                    view.presentScene(scene)
                    var start: UInt64?, travel = 0.0, active: [String: [CGPoint]] = [:]
                    func close(_ side: String) {
                        if let points = active[side], points.count > 1 {
                            let span = points.flatMap { a in points.map { hypot(a.x - $0.x, a.y - $0.y) } }.max() ?? 0
                            records.append(["kind": "segment", "trace": trace.name, "policy": policy, "family": family,
                                "side": side, "samples": points.count, "nativeSceneSpanLogical": span])
                        }
                        active[side] = []
                    }
                    for row in trace.rows {
                        let before = session.simulation.state.player.position
                        if row.sample > 0 && !row.paused {
                            session.moveX = row.commandX; session.moveY = row.commandY; session.dodgePressed = row.dodgePressed
                            session.step()
                        }
                        let after = session.simulation.state.player.position
                        XCTAssertEqual(session.simulation.state.tick, row.tick); XCTAssertEqual(after.x.raw, row.xRaw)
                        XCTAssertEqual(after.y.raw, row.yRaw); XCTAssertEqual(after.x.raw - before.x.raw, row.dxRaw)
                        let snap = session.snapshot
                        renderer.render(snap, reducedMotion: false)
                        let moving = row.dxRaw != 0 || row.dyRaw != 0
                        travel += hypot(Double(row.dxRaw), Double(row.dyRaw)) / 256
                        guard (moving || row.paused), row.dodgeRemaining == 0, snap.playerClipId == "player_move",
                              snap.playerDirection == direction,
                              let sprite = renderer.root.childNode(withName: "//sprite-player") as? SKSpriteNode else {
                            upright.isHidden = true
                            close("left"); close("right"); start = nil; continue
                        }
                        if start == nil { start = row.tick }
                        let frame = policy == "fixed-time"
                            ? fixed.frameIndex(atTickOffset: row.tick - start!)
                            : Int(floor(travel.truncatingRemainder(dividingBy: 120) / 120 * 16))
                        // Same explicit candidate-selection mechanism as the vetted harness; no production policy.
                        sprite.removeAllActions(); sprite.texture = textures[frame]
                        XCTAssertEqual(renderer.observePlayerPlayback()?.clipToken, "player_move|\(direction)")
                        XCTAssertTrue(sprite.texture === textures[frame])
                        // Ground position through actual tree; upright texture attached at projected root,
                        // as the vetted midpoint harness does, never squashed or rotated.
                        let root = scene.convert(sprite.position, from: try XCTUnwrap(sprite.parent))
                        sprite.isHidden = true; upright.isHidden = false
                        upright.texture = sprite.texture; upright.size = sprite.size
                        upright.anchorPoint = sprite.anchorPoint; upright.position = root
                        XCTAssertTrue(upright.texture === textures[frame])
                        // Renderer consumes PresentationSnapshot whole-unit position; record Q8 delta separately.
                        let wx: Double = Double(snap.player.x) - 736
                        let wy: Double = Double(snap.player.y) - 654
                        let qx: Double = Double(row.xRaw) / 256 - Double(snap.player.x)
                        let qy: Double = Double(row.yRaw) / 256 - Double(snap.player.y)
                        // Observed: snapshot uses whole units (not nearest). Bound only to <1 unit.
                        XCTAssertLessThan(abs(qx), 1); XCTAssertLessThan(abs(qy), 1)
                        let r2: Double = 2.0.squareRoot()
                        let expectedRoot = CGPoint(x: 352 + (wx - wy) / r2, y: 163 + (wx + wy) / (2 * r2))
                        XCTAssertEqual(root.x, expectedRoot.x, accuracy: 0.002); XCTAssertEqual(root.y, expectedRoot.y, accuracy: 0.002)
                        XCTAssertEqual(upright.size.width, 64); XCTAssertEqual(upright.size.height, 416.0 / 6.0, accuracy: 0.00001)
                        XCTAssertEqual(upright.anchorPoint.y, 1 - 336.0 / 416.0, accuracy: 0.000001)
                        var contacts: [String: [Double]] = [:]
                        for leg in poses[frame].legs {
                            guard leg.contact else { close(leg.side); continue }
                            XCTAssertEqual(leg.toe[2], 0)
                            // Upright sprite is a child of squashed ground; recover scene pixels via the actual tree.
                            let anchorScene = root
                            let point = CGPoint(x: anchorScene.x + leg.toe[0], y: anchorScene.y - 0.5 * leg.toe[1])
                            active[leg.side, default: []].append(point); contacts[leg.side] = [point.x, point.y]
                        }
                        var record: [String: Any] = ["kind": "sample", "trace": trace.name, "policy": policy, "family": family,
                            "tick": row.tick, "sample": row.sample, "frame": frame, "texturePath": paths[frame],
                            "authoritativeRaw": [row.xRaw, row.yRaw], "snapshotWhole": [snap.player.x, snap.player.y],
                            "q8MinusSnapshot": [qx, qy], "projectedRoot": [root.x, root.y], "contacts": contacts,
                            "evidence": "static explicit WorldRenderer pass; not displayed callback"]
                        if row.sample % 30 == 0, imageCount < 96, let rendered = view.texture(from: scene,
                            crop: CGRect(x: root.x - 80, y: root.y - 30, width: 160, height: 110)) {
                            let attachment = XCTAttachment(image: UIImage(cgImage: rendered.cgImage()))
                            attachment.name = "groundcontact-\(trace.name)-\(policy)-\(family)-sample-\(row.sample)-frame-\(frame)"
                            attachment.lifetime = .keepAlways; add(attachment); record["image"] = attachment.name; imageCount += 1
                        }
                        records.append(record)
                    }
                    close("left"); close("right")
                    XCTAssertEqual(session.simulation.state.digest(), trace.finalDigest)
                    view.presentScene(nil)
                }
            }
        }
        let samples = records.filter { $0["kind"] as? String == "sample" }
        XCTAssertEqual(Set(samples.compactMap { $0["family"] as? String }), ["baseline", "weight-transfer"])
        XCTAssertGreaterThan(samples.count, 2000); XCTAssertGreaterThan(imageCount, 40)
        // Same feet/projection: model contacts are expected identical; pixels differ only in source keys.
        let segments = records.filter { $0["kind"] as? String == "segment" }
        let keyed = Dictionary(grouping: segments) { "\($0["trace"]!)|\($0["policy"]!)" }
        for (_, group) in keyed {
            let base = group.filter { $0["family"] as? String == "baseline" }.compactMap { $0["nativeSceneSpanLogical"] as? Double }
            let proposal = group.filter { $0["family"] as? String == "weight-transfer" }.compactMap { $0["nativeSceneSpanLogical"] as? Double }
            XCTAssertEqual(base, proposal)
        }
        let output: [String: Any] = ["status": "STATIC_NATIVE_RENDERER_NOT_DISPLAY_CADENCE", "threshold": NSNull(),
            "excludedInvalidSouthFacingDodgeOrStationaryTraces": excluded, "records": records]
        let json = try JSONSerialization.data(withJSONObject: output, options: [.prettyPrinted, .sortedKeys])
        let attachment = XCTAttachment(data: json, uniformTypeIdentifier: "public.json")
        attachment.name = "groundcontact-native-records"; attachment.lifetime = .keepAlways; add(attachment)
    }
}
#endif
