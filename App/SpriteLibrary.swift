import SpriteKit
import SurveillanceCore

/// Loads admitted clip frames as SpriteKit textures, and says plainly when a
/// clip has no art.
///
/// `legacy-admission.md` makes partial coverage a defined state: an unbacked
/// frame falls back to the authored blockout, and a frame from another role,
/// direction, or clip must never be substituted. `ClipFrameLibrary` enforces
/// that all-or-nothing rule; this type only turns the result into textures.
@MainActor
final class SpriteLibrary {
    private let frames: ClipFrameLibrary
    /// Textures by delivered file name, loaded once.
    private var textures: [String: SKTexture] = [:]
    /// Cached animation actions by clip and direction.
    private var animations: [String: SKAction] = [:]

    let coverage: (backed: Int, total: Int)

    init(frames suppliedFrames: ClipFrameLibrary? = nil) {
        let library = suppliedFrames ?? (try? ClipFrameLibrary.bundled())
            ?? ClipFrameLibrary(clips: [:], deliveredPaths: [:])
        frames = library
        coverage = library.coverage
    }

    var isEmpty: Bool { coverage.backed == 0 }

#if DEBUG
    /// Observe the texture selected by SpriteKit; never infer it from tick phase.
    func deliveredPath(for texture: SKTexture) -> String? {
        textures.keys.sorted().first { textures[$0] === texture }
    }
#endif


    func isBacked(clipId: String, direction: String? = nil) -> Bool {
        frames.isBacked(clipId: clipId, direction: direction)
    }

    /// First frame of a clip, for a static presentation.
    func firstTexture(clipId: String, direction: String? = nil) -> SKTexture? {
        guard let paths = frames.deliveredFrames(clipId: clipId, direction: direction),
              let first = paths.first
        else { return nil }
        return texture(named: first)
    }

    /// Settled appearance from the authored terminal frame, without replaying motion.
    func lastTexture(clipId: String, direction: String? = nil) -> SKTexture? {
        guard let paths = frames.deliveredFrames(clipId: clipId, direction: direction),
              let last = paths.last
        else { return nil }
        return texture(named: last)
    }

    /// Event-driven one-shots sample the same tick phase as their lifetime tracker.
    func texture(clipId: String, direction: String?, elapsedTicks: UInt64, reducedMotion: Bool) -> SKTexture? {
        guard let paths = frames.deliveredFrames(clipId: clipId, direction: direction),
              let timing = frames.timing(clipId: clipId, direction: direction),
              timing.frameUnits.count == paths.count else { return nil }
        let index = reducedMotion ? paths.count - 1 : timing.frameIndex(atTickOffset: elapsedTicks)
        return texture(named: paths[index])
    }

    /// A repeating or one-shot animation for a clip, at its authored frame rate.
    func animation(clipId: String, direction: String? = nil) -> SKAction? {
        let key = "\(clipId)|\(direction ?? "-")"
        if let cached = animations[key] { return cached }
        guard let clip = frames.clip(clipId),
              let paths = frames.deliveredFrames(clipId: clipId, direction: direction)
        else { return nil }
        let textures = paths.compactMap { texture(named: $0) }
        guard textures.count == paths.count, !textures.isEmpty else { return nil }

        guard let timing = frames.timing(clipId: clipId, direction: direction),
              timing.frameUnits.count == textures.count else { return nil }
        guard let sequence = Self.sequence(textures: textures, timing: timing) else { return nil }
        let action = clip.loop ? SKAction.repeatForever(sequence) : sequence
        animations[key] = action
        return action
    }

    /// Shared renderer boundary for uniform and authored variable holds.
    static func sequence(textures: [SKTexture], timing: ClipTiming) -> SKAction? {
        guard textures.count == timing.frameUnits.count, !textures.isEmpty else { return nil }
        let holds = timing.frameSeconds
        let sequence: SKAction
        if Set(timing.frameUnits).count == 1 {
            sequence = SKAction.animate(with: textures, timePerFrame: holds[0], resize: false, restore: false)
        } else {
            sequence = SKAction.sequence(zip(textures, holds).map { texture, hold in
                SKAction.animate(with: [texture], timePerFrame: hold, resize: false, restore: false)
            })
        }
        return sequence
    }

    /// Authored anchor for a clip, as a SpriteKit unit anchor point.
    ///
    /// The contract's anchor is in sprite-box pixels measured from the top-left;
    /// SpriteKit anchors are 0…1 from the bottom-left, so y inverts.
    func anchorPoint(clipId: String, boxHeight: CGFloat, boxWidth: CGFloat) -> CGPoint {
        guard let clip = frames.clip(clipId), boxWidth > 0, boxHeight > 0 else {
            return CGPoint(x: 0.5, y: 0.5)
        }
        return CGPoint(
            x: CGFloat(clip.anchor.x) / boxWidth,
            y: 1 - CGFloat(clip.anchor.y) / boxHeight
        )
    }

    private func texture(named name: String) -> SKTexture? {
        if let cached = textures[name] { return cached }
        guard let url = RuntimeAssetBundle.url(forFile: name),
              let image = UIImage(contentsOfFile: url.path)
        else { return nil }
        let texture = SKTexture(image: image)
        // visual-language-001: nearestNeighbor. Authored pixels stay crisp.
        texture.filteringMode = .nearest
        textures[name] = texture
        return texture
    }
}
