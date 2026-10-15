import SpriteKit
import Testing
import UIKit
@testable import SSRuntime
@testable import SurveillanceCore

/// BP-004: exercise the real renderer and delivered clips, not a parallel policy.
@Suite(.serialized)
@MainActor
struct CameraPlaybackTests {
    private func snapshot() throws -> PresentationSnapshot {
        PresentationSnapshot(try Simulation.make(seed: 1).state)
    }

    private func sprite(_ renderer: WorldRenderer, _ snap: PresentationSnapshot) throws -> SKSpriteNode {
        let id = try #require(snap.cameras.first?.id.raw)
        return try #require(renderer.root.childNode(withName: "//sprite-camera-\(id)") as? SKSpriteNode)
    }

    @Test func criticalIntegrityWinsOverTransientHitClip() throws {
        var snap = try snapshot()
        snap.cameras[0].integrity = 1
        snap.cameras[0].presentationState = .hit
        snap.cameras[0].clipId = "camera_hit"
        let renderer = WorldRenderer()
        renderer.render(snap)
        let node = try sprite(renderer, snap)
        let action = try #require(node.action(forKey: "camera-state"))
        let expected = try #require(SpriteLibrary().animation(clipId: "camera_critical_enter"))
        #expect(action.duration == expected.duration)
        snap.cameras[0].presentationState = .critical
        snap.cameras[0].clipId = "camera_critical_enter"
        renderer.render(snap)
        #expect(node.action(forKey: "camera-state") === action)
        #expect(node.position == CGPoint(x: snap.cameras[0].x, y: snap.cameras[0].y))
        // SpriteKit round-trips anchors at Float precision. Keep an exact
        // comparison to that representation of the contract's (32,88).
        #expect(node.anchorPoint == CGPoint(x: 0.5, y: CGFloat(Float(1 - 88.0 / 96.0))))
    }

    @Test func destructionSurvivesNextSnapshotAndDropsFieldImmediately() throws {
        var snap = try snapshot()
        let renderer = WorldRenderer()
        renderer.render(snap)
        let node = try sprite(renderer, snap)
        let live = try #require(node.action(forKey: "camera-state"))
        snap.cameras[0].integrity = 0
        snap.cameras[0].fieldVisible = false
        snap.cameras[0].presentationState = .destroying
        snap.cameras[0].clipId = "camera_destroy"
        renderer.render(snap)
        let destruction = try #require(node.action(forKey: "camera-state"))
        #expect(destruction !== live)
        #expect(renderer.root.childNode(withName: "//field-\(snap.cameras[0].id.raw)") == nil)
        snap.cameras[0].presentationState = .dormant
        snap.cameras[0].clipId = "camera_destroyed_idle"
        renderer.render(snap)
        #expect(node.action(forKey: "camera-state") === destruction)
    }

    @Test func reducedMotionImmediatelySettlesEveryIntegrityAndCancelsRunningResponse() throws {
        var snap = try snapshot()
        let renderer = WorldRenderer()
        let library = SpriteLibrary()
        for (integrity, clip) in [(3, "camera_operational_idle"), (2, "camera_hit"),
                                  (1, "camera_critical_enter"), (0, "camera_destroyed_idle")] {
            snap.cameras[0].integrity = integrity
            renderer.render(snap)
            let node = try sprite(renderer, snap)
            #expect(node.hasActions())
            renderer.render(snap, reducedMotion: true)
            #expect(!node.hasActions())
            let actual = try #require(node.texture)
            let expected = try #require(library.lastTexture(clipId: clip))
            #expect(UIImage(cgImage: actual.cgImage()).pngData() == UIImage(cgImage: expected.cgImage()).pngData())
        }
    }

    @Test func newerIntegrityCancelsOlderResponseWithoutRecreatingTheNode() throws {
        var snap = try snapshot()
        let renderer = WorldRenderer()
        var previous: SKAction?
        var original: SKSpriteNode?
        for integrity in [3, 2, 1, 0] {
            snap.cameras[0].integrity = integrity
            renderer.render(snap)
            let node = try sprite(renderer, snap)
            if let original { #expect(node === original) } else { original = node }
            let action = try #require(node.action(forKey: "camera-state"))
            if let previous { #expect(action !== previous) }
            previous = action
            renderer.render(snap)
            #expect(node.action(forKey: "camera-state") === action)
        }
    }
    private final class BundleAnchor {}

    static func candidateFrames() throws -> [String: [SKTexture]] {
        let bundle = Bundle(for: BundleAnchor.self)
        let records = [("camera_operational_idle", "operationalIdle", 4),
            ("camera_hit", "hit", 2), ("camera_critical_enter", "criticalEnter", 3),
            ("camera_destroy", "destroy", 4), ("camera_field_off", "fieldOff", 1),
            ("camera_destroyed_idle", "destroyedIdle", 2)]
        var result: [String: [SKTexture]] = [:]
        for (clip, stem, count) in records {
            result[clip] = try (1...count).map { index in
                let name = String(format: "actor_camera_%@_none_%02d@4x", stem, index)
                let url = try #require(bundle.url(forResource: name, withExtension: "png"))
                let image = try #require(UIImage(contentsOfFile: url.path))
                let texture = SKTexture(image: image)
                texture.filteringMode = .nearest
                return texture
            }
        }
        return result
    }

    @Test func completeCameraCandidatesUseShippingIntegrityPolicy() throws {
        let candidates = try Self.candidateFrames()
        let renderer = WorldRenderer()
        #expect(renderer.installBenchmarkCameraFrames(candidates))
        var snap = try snapshot()
        var original: SKSpriteNode?
        var oldAction: SKAction?
        for (integrity, settled) in [(3, "camera_operational_idle"), (2, "camera_hit"),
                                     (1, "camera_critical_enter"), (0, "camera_destroyed_idle")] {
            snap.cameras[0].integrity = integrity
            snap.cameras[0].fieldVisible = integrity > 0
            renderer.render(snap)
            let node = try sprite(renderer, snap)
            if let original { #expect(node === original) } else { original = node }
            #expect(renderer.root.childNode(withName: "//housing-\(snap.cameras[0].id.raw)") == nil)
            let action = try #require(node.action(forKey: "camera-state"))
            if let oldAction { #expect(action !== oldAction) }
            renderer.render(snap)
            #expect(node.action(forKey: "camera-state") === action)
            oldAction = action
            if integrity == 0 {
                #expect(renderer.root.childNode(withName: "//field-\(snap.cameras[0].id.raw)") == nil)
            }
            renderer.render(snap, reducedMotion: true)
            #expect(!node.hasActions())
            #expect(node.texture === candidates[settled]?.last)
            #expect(node.position == CGPoint(x: snap.cameras[0].x, y: snap.cameras[0].y))
        }
    }

    @Test func incompleteCameraCandidateFamilyCannotReplaceTextures() throws {
        let library = SpriteLibrary()
        let before = try #require(library.firstTexture(clipId: "camera_hit"))
        var candidates = try Self.candidateFrames()
        candidates["camera_destroy"]?.removeLast()
        #expect(!library.installBenchmarkCameraFrames(candidates))
        #expect(library.firstTexture(clipId: "camera_hit") === before)
    }

}
