import XCTest
import CryptoKit
import SpriteKit
import UIKit
@testable import SSRuntime
@testable import SurveillanceCore

#if SS_RENDERER_TEST_SUPPORT
/// ADAPT AllReleaseSourceTests:14-129. Actual paired static renderer delivery,
/// not live cadence, production selection or art admission.
@MainActor
final class ReleaseVariationSourceTests: XCTestCase {
    private let phases = (1...16).filter { ![5, 13].contains($0) }
    private let families = ["baseline", "variation"]

    private func sourceNames(_ phase: Int, _ family: String) -> [String] {
        let prefix = family == "baseline" ? "player-allrelease" : "player-releasevariation"
        return [String(format: "player-source-s-%02d", phase - 1)] + (1..<16).map {
            String(format: "\(prefix)-%02d-%02d", phase, $0)
        } + ["player-source-s-neutral"]
    }

    private func candidate(_ phase: Int, _ family: String) throws -> (WorldRenderer, [SKTexture], [String], SpriteLibrary) {
        let names = sourceNames(phase, family)
        let bundle = Bundle(for: Self.self)
        let hashURL = try XCTUnwrap(bundle.url(forResource: "release-variation-resource-hashes", withExtension: "json"))
        let expected = try JSONDecoder().decode([String: String].self, from: Data(contentsOf: hashURL))
        let textures = try names.map { name -> SKTexture in
            let url = try XCTUnwrap(bundle.url(forResource: name, withExtension: "png"))
            let data = try Data(contentsOf: url)
            let digest = SHA256.hash(data: data).map { String(format: "%02x", $0) }.joined()
            XCTAssertEqual(digest, expected[name], "Exact bundled source \(name)")
            let image = try XCTUnwrap(UIImage(data: data))
            XCTAssertEqual(image.size, CGSize(width: 384, height: 416))
            let texture = SKTexture(image: image)
            texture.filteringMode = .linear
            return texture
        }
        let moveID = "player_move_s_00", idleID = "player_idle_s_00"
        let move = ClipFrameLibrary.Clip(clipId: "player_move", actorRole: "player", directions: ["s"],
            framesPerSecond: 1, authoredTiming: nil, loop: true, anchor: VecI(x: 32, y: 56), frameIds: [moveID])
        let idle = ClipFrameLibrary.Clip(clipId: "player_idle", actorRole: "player", directions: ["s"],
            framesPerSecond: 1, authoredTiming: nil, loop: true, anchor: VecI(x: 32, y: 56), frameIds: [idleID])
        let clips = ClipFrameLibrary(clips: ["player_move": move, "player_idle": idle],
            deliveredPaths: [moveID: names[0], idleID: names[16]])
        let library = try XCTUnwrap(SpriteLibrary(benchmarkFrames: clips,
            benchmarkTextures: [names[0]: textures[0], names[16]: textures[16]]))
        let renderer = WorldRenderer(sprites: library)
        renderer.benchmarkPlayerRegistration = (CGSize(width: 64, height: 416.0 / 6.0),
            CGPoint(x: 0.5, y: 1 - 336.0 / 416.0))
        renderer.benchmarkPlayerSettleSequences[ObjectIdentifier(textures[0])] = .init(direction: "s", frames: textures,
            timing: try ClipTiming(unitsPerSecond: 128, frameUnits: Array(repeating: 3, count: 17)))
        return (renderer, textures, names, library)
    }

    private func player(_ renderer: WorldRenderer) throws -> SKSpriteNode {
        try XCTUnwrap(renderer.root.childNode(withName: "//sprite-player") as? SKSpriteNode)
    }

    private func snapshot() throws -> PresentationSnapshot {
        var snap = PresentationSnapshot(try Simulation.make(seed: 1).state)
        snap.playerDirection = "s"
        snap.playerClipId = "player_move"
        snap.tick = 0
        return snap
    }

    func testPairedAllPosesUseExactSourceTexturesAndTiming() throws {
        let timing = try ClipTiming(unitsPerSecond: 128, frameUnits: Array(repeating: 3, count: 17))
        XCTAssertEqual(timing.frameIndex(atTickOffset: 22), 15)
        XCTAssertEqual(timing.frameIndex(atTickOffset: 23), 16)
        XCTAssertEqual(Double(16 * 3) / 128, 0.375)
        var records: [[String: Any]] = []
        for phase in phases {
            for family in families {
                let (renderer, textures, names, _) = try candidate(phase, family)
                let view = SKView(frame: CGRect(x: 0, y: 0, width: 704, height: 326))
                let scene = SKScene(size: view.bounds.size)
                scene.backgroundColor = UIColor(white: 0.2, alpha: 1)
                scene.addChild(renderer.root)
                view.presentScene(scene)
                defer { view.presentScene(nil) }
                var snap = try snapshot()
                renderer.render(snap)
                let sprite = try player(renderer), root = sprite.position
                let crop = CGRect(x: root.x - 96, y: root.y - 48, width: 192, height: 144)
                snap.playerClipId = "player_idle"
                for pose in 0..<17 {
                    let offset = try XCTUnwrap((UInt64(0)...23).first { timing.frameIndex(atTickOffset: $0) == pose })
                    snap.tick = 1 + offset
                    renderer.render(snap)
                    XCTAssertTrue(sprite.texture === textures[pose], "\(family) phase\(phase) pose\(pose)")
                    XCTAssertEqual(sprite.position, root)
                    XCTAssertEqual(sprite.size, CGSize(width: 64, height: CGFloat(Float(416.0 / 6.0))))
                    XCTAssertEqual(sprite.anchorPoint, CGPoint(x: 0.5, y: CGFloat(Float(1 - 336.0 / 416.0))))
                    renderer.root.enumerateChildNodes(withName: "//" + WorldRenderer.outlineName) { node, _ in node.isHidden = true }
                    let capture = try XCTUnwrap(view.texture(from: renderer.root, crop: crop))
                    let attachment = XCTAttachment(image: UIImage(cgImage: capture.cgImage()))
                    attachment.name = String(format: "releasevariation-\(family)-%02d-pose-%02d", phase, pose)
                    attachment.lifetime = .keepAlways
                    add(attachment)
                    let url = try XCTUnwrap(Bundle(for: Self.self).url(forResource: names[pose], withExtension: "png"))
                    let digest = SHA256.hash(data: try Data(contentsOf: url)).map { String(format: "%02x", $0) }.joined()
                    records.append(["family": family, "phase": phase, "pose": pose, "tickOffset": offset,
                        "source": names[pose], "sourceSHA256": digest, "capture": attachment.name ?? "",
                        "diagnostic": "actual static SpriteKit source selection, not live cadence"])
                }
            }
        }
        XCTAssertEqual(records.count, 476)
        let attachment = XCTAttachment(data: try JSONSerialization.data(withJSONObject: records, options: [.prettyPrinted, .sortedKeys]), uniformTypeIdentifier: "public.json")
        attachment.name = "releasevariation-pose-records"
        attachment.lifetime = .keepAlways
        add(attachment)
    }

    func testBothFamiliesBypassAndCancelReducedMotion() throws {
        for phase in phases {
            for family in families {
                for reducedAtEntry in [false, true] {
                    let (renderer, textures, _, _) = try candidate(phase, family)
                    var snap = try snapshot()
                    renderer.render(snap)
                    let sprite = try player(renderer)
                    snap.playerClipId = "player_idle"; snap.tick = 1
                    renderer.render(snap, reducedMotion: reducedAtEntry)
                    XCTAssertTrue(sprite.texture === textures[reducedAtEntry ? 16 : 0])
                    snap.tick = 8; renderer.render(snap, reducedMotion: true)
                    XCTAssertTrue(sprite.texture === textures[16])
                    snap.tick = 9; renderer.render(snap, reducedMotion: false)
                    XCTAssertTrue(sprite.texture === textures[16], "Cancelled release must not resurrect")
                }
            }
        }
    }

    func testBothFamiliesInterruptAndRestartWithoutStalePose() throws {
        for phase in phases {
            for family in families {
                let (renderer, textures, _, _) = try candidate(phase, family)
                var snap = try snapshot()
                renderer.render(snap)
                let sprite = try player(renderer), root = sprite.position
                snap.playerClipId = "player_idle"; snap.tick = 1; renderer.render(snap)
                snap.tick = 13; renderer.render(snap)
                XCTAssertTrue(sprite.texture === textures[8])
                for _ in 0..<3 { renderer.render(snap) }
                XCTAssertTrue(sprite.texture === textures[8], "Paused tick must not advance")
                snap.playerClipId = "player_move"; snap.tick = 14; renderer.render(snap)
                XCTAssertTrue(sprite.texture === textures[0], "Movement interrupts release")
                snap.playerClipId = "player_idle"; snap.tick = 15; renderer.render(snap)
                XCTAssertTrue(sprite.texture === textures[0], "Fresh stop restarts at exact entry")
                snap.tick = 37; renderer.render(snap)
                XCTAssertTrue(sprite.texture === textures[15])
                snap.tick = 38; renderer.render(snap)
                XCTAssertTrue(sprite.texture === textures[16], "Neutral first eligible tick is offset23")
                XCTAssertEqual(sprite.position, root)
                renderer.reset()
                snap.tick = 39; renderer.render(snap)
                XCTAssertTrue(try player(renderer).texture === textures[16], "Reset while idle must not resurrect release")
            }
        }
    }
}
#endif
