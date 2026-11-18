import XCTest
import CryptoKit
import SpriteKit
import UIKit
@testable import SSRuntime
@testable import SurveillanceCore

#if SS_RENDERER_TEST_SUPPORT
/// New south release candidates only. Static renderer evidence, not live cadence,
/// shared-scene fidelity, other facings or production asset admission.
@MainActor
final class AllReleaseSourceTests: XCTestCase {
    private let newPhases = (1...16).filter { ![5, 13].contains($0) }

    private func texture(_ name: String) throws -> SKTexture {
        let url = try XCTUnwrap(Bundle(for: Self.self).url(forResource: name, withExtension: "png"))
        let image = try XCTUnwrap(UIImage(contentsOfFile: url.path))
        XCTAssertEqual(image.size, CGSize(width: 384, height: 416))
        let texture = SKTexture(image: image)
        texture.filteringMode = .linear
        return texture
    }

    private func candidate(_ phase: Int) throws -> (WorldRenderer, [SKTexture], [String]) {
        let entry = String(format: "player-source-s-%02d", phase - 1)
        let names = [entry] + (1..<16).map {
            String(format: "player-allrelease-%02d-%02d", phase, $0)
        } + ["player-source-s-neutral"]
        let textures = try names.map(texture)
        let moveID = "player_move_s_00"
        let idleID = "player_idle_s_00"
        let move = ClipFrameLibrary.Clip(clipId: "player_move", actorRole: "player", directions: ["s"],
            framesPerSecond: 1, authoredTiming: nil, loop: true,
            anchor: VecI(x: 32, y: 56), frameIds: [moveID])
        let idle = ClipFrameLibrary.Clip(clipId: "player_idle", actorRole: "player", directions: ["s"],
            framesPerSecond: 1, authoredTiming: nil, loop: true,
            anchor: VecI(x: 32, y: 56), frameIds: [idleID])
        let frames = ClipFrameLibrary(clips: ["player_move": move, "player_idle": idle],
            deliveredPaths: [moveID: entry, idleID: names[16]])
        let library = try XCTUnwrap(SpriteLibrary(benchmarkFrames: frames,
            benchmarkTextures: [entry: textures[0], names[16]: textures[16]]))
        let renderer = WorldRenderer(sprites: library)
        renderer.benchmarkPlayerRegistration = (
            CGSize(width: 64, height: 416.0 / 6.0),
            CGPoint(x: 0.5, y: 1 - 336.0 / 416.0))
        renderer.benchmarkPlayerSettleSequences[ObjectIdentifier(textures[0])] = .init(
            direction: "s", frames: textures,
            timing: try ClipTiming(unitsPerSecond: 128, frameUnits: Array(repeating: 3, count: 17)))
        return (renderer, textures, names)
    }

    func testAllNewReleasePosesUseExactSourceTexturesAndRegistration() throws {
        let timing = try ClipTiming(unitsPerSecond: 128, frameUnits: Array(repeating: 3, count: 17))
        XCTAssertEqual(timing.frameIndex(atTickOffset: 22), 15)
        XCTAssertEqual(timing.frameIndex(atTickOffset: 23), 16)
        let state = try Simulation.make(seed: 1).state
        var records: [[String: Any]] = []
        for phase in newPhases {
            let (renderer, textures, names) = try candidate(phase)
            let view = SKView(frame: CGRect(x: 0, y: 0, width: 704, height: 326))
            let scene = SKScene(size: view.bounds.size)
            scene.backgroundColor = UIColor(white: 0.2, alpha: 1)
            scene.addChild(renderer.root)
            view.presentScene(scene)
            defer { view.presentScene(nil) }
            var snap = PresentationSnapshot(state)
            snap.playerDirection = "s"
            snap.playerClipId = "player_move"
            snap.tick = 0
            renderer.render(snap)
            let player = try XCTUnwrap(renderer.root.childNode(withName: "//sprite-player") as? SKSpriteNode)
            let root = player.position
            let crop = CGRect(x: root.x - 96, y: root.y - 48, width: 192, height: 144)
            snap.playerClipId = "player_idle"
            for pose in 0..<17 {
                let offset = try XCTUnwrap((UInt64(0)...23).first { timing.frameIndex(atTickOffset: $0) == pose })
                snap.tick = 1 + offset
                renderer.render(snap)
                XCTAssertTrue(player.texture === textures[pose], "release \(phase), pose \(pose)")
                XCTAssertEqual(player.position, root)
                XCTAssertEqual(player.size, CGSize(width: 64, height: CGFloat(Float(416.0 / 6.0))))
                XCTAssertEqual(player.anchorPoint, CGPoint(x: 0.5, y: CGFloat(Float(1 - 336.0 / 416.0))))
                renderer.root.enumerateChildNodes(withName: "//" + WorldRenderer.outlineName) { node, _ in
                    node.isHidden = true
                }
                let capture = try XCTUnwrap(view.texture(from: renderer.root, crop: crop))
                let attachment = XCTAttachment(image: UIImage(cgImage: capture.cgImage()))
                attachment.name = String(format: "allrelease-native-%02d-pose-%02d", phase, pose)
                attachment.lifetime = .keepAlways
                add(attachment)
                let sourceURL = try XCTUnwrap(Bundle(for: Self.self).url(forResource: names[pose], withExtension: "png"))
                let sourceDigest = SHA256.hash(data: try Data(contentsOf: sourceURL)).map { String(format: "%02x", $0) }.joined()
                records.append(["phase": phase, "pose": pose, "tickOffset": offset,
                                "source": names[pose], "sourceSHA256": sourceDigest, "capture": attachment.name ?? "",
                                "diagnostic": "static SpriteKit pose, not live or shared-scene acceptance"])
            }
        }
        XCTAssertEqual(records.count, 14 * 17)
        let attachment = XCTAttachment(data: try JSONSerialization.data(withJSONObject: records,
            options: [.prettyPrinted, .sortedKeys]), uniformTypeIdentifier: "public.json")
        attachment.name = "allrelease-native-pose-records"
        attachment.lifetime = .keepAlways
        add(attachment)
    }

    func testAllNewReleasesBypassAndCancelForReducedMotion() throws {
        let state = try Simulation.make(seed: 1).state
        for phase in newPhases {
            for reducedAtEntry in [false, true] {
                let (renderer, textures, _) = try candidate(phase)
                var snap = PresentationSnapshot(state)
                snap.playerDirection = "s"
                snap.playerClipId = "player_move"
                snap.tick = 0
                renderer.render(snap)
                let player = try XCTUnwrap(renderer.root.childNode(withName: "//sprite-player") as? SKSpriteNode)
                snap.playerClipId = "player_idle"
                snap.tick = 1
                renderer.render(snap, reducedMotion: reducedAtEntry)
                XCTAssertTrue(player.texture === textures[reducedAtEntry ? 16 : 0])
                snap.tick = 8
                renderer.render(snap, reducedMotion: true)
                XCTAssertTrue(player.texture === textures[16])
                snap.tick = 9
                renderer.render(snap, reducedMotion: false)
                XCTAssertTrue(player.texture === textures[16], "Cancelled release must not resurrect")
                XCTAssertEqual(renderer.benchmarkPlayerSettleSequences.count, 1)
            }
        }
    }
}
#endif
