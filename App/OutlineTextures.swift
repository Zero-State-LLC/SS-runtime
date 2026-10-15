import CoreGraphics
import SpriteKit
import SurveillanceCore

/// D-094 faction outlines as pre-rendered textures (`animation.md` § 8b).
///
/// For each source frame an actor shows, this builds once, on the CPU, a
/// texture holding a one-logical-pixel ring around the frame's opaque pixels:
/// cool white and unbroken for the Player, warm red-orange and dashed for
/// enemies. The ring is padded one pixel outside the frame so it is never
/// clipped by the frame's edge. Drawing it is one extra sprite per actor and
/// no per-frame filter work on a cache hit. BP-007 separates source storage
/// density from the bounded logical mask used for stroke and dash spacing.
@MainActor
final class OutlineTextures {
    struct Entry {
        let texture: SKTexture
        /// Mask pixels, not source-image pixels.
        let pad: Int
        let maskSize: CGSize
        var byteCost: Int { (Int(maskSize.width) + 2 * pad) * (Int(maskSize.height) + 2 * pad) * 4 }
    }

    /// Preserves the existing reference-framing stroke in logical mask units.
    nonisolated static let thicknessPixels = 1
    /// Alpha at or above which a source pixel counts as part of the body.
    nonisolated static let opaqueThreshold: UInt8 = 64
    /// Mask budget is independent of the source image's storage density.
    nonisolated static let maxPixels = 256 * 256
    nonisolated static let maxSourceDimension = 1024

    private struct Key: Hashable {
        let texture: ObjectIdentifier
        let faction: ActorContrast.Faction
        let width: Int
        let height: Int
        let samplingScale: Int
    }

    private struct Cached {
        let entry: Entry?
        // Prevent ObjectIdentifier reuse, including failed entries, until eviction.
        let source: SKTexture
    }
    private var cache: [Key: Cached] = [:]
    private var recency: [Key] = []
    private let maxEntries: Int
    private let maxBytes: Int
    private(set) var retainedMaskBytes = 0

    var count: Int { cache.count }

    // Engineering bounds, not a device residency/performance claim.
    init(maxEntries: Int = 128, maxBytes: Int = 4 * 1024 * 1024) {
        self.maxEntries = max(0, maxEntries)
        self.maxBytes = max(0, maxBytes)
    }

    func outline(for texture: SKTexture, faction: ActorContrast.Faction, logicalSize: CGSize, samplingScale: Int = 1) -> Entry? {
        guard let size = Self.maskDimensions(logicalSize, samplingScale: samplingScale) else { return nil }
        let key = Key(texture: ObjectIdentifier(texture), faction: faction, width: size.width, height: size.height, samplingScale: samplingScale)
        if let hit = cache[key] {
            recency.removeAll { $0 == key }; recency.append(key)
            return hit.entry
        }
        let made = Self.make(from: texture.cgImage(), faction: faction, logicalSize: logicalSize, samplingScale: samplingScale)
        let cost = made?.byteCost ?? 0
        guard maxEntries > 0, cost <= maxBytes else { return made }
        while !recency.isEmpty && (cache.count >= maxEntries || retainedMaskBytes + cost > maxBytes) {
            let old = recency.removeFirst()
            retainedMaskBytes -= cache.removeValue(forKey: old)?.entry?.byteCost ?? 0
        }
        cache[key] = Cached(entry: made, source: texture)
        recency.append(key); retainedMaskBytes += cost
        return made
    }

    nonisolated private static func maskDimensions(_ size: CGSize, samplingScale: Int = 1) -> (width: Int, height: Int)? {
        guard (1...3).contains(samplingScale), size.width.isFinite, size.height.isFinite,
              size.width > 0, size.height > 0, size.width <= 256, size.height <= 256 else { return nil }
        // SpriteKit stores geometry at Float precision. Nearest logical pixels
        // prevent a recovered 64.000002 canvas from becoming a different mask.
        let width = max(1, Int(size.width.rounded())) * samplingScale
        let height = max(1, Int(size.height.rounded())) * samplingScale
        guard width <= 256, height <= 256 else { return nil }
        return (width, height)
    }

    /// The outline ring for `image`, or nil when it cannot be read.
    nonisolated static func make(from image: CGImage, faction: ActorContrast.Faction, logicalSize: CGSize? = nil, samplingScale: Int = 1) -> Entry? {
        guard image.width > 0, image.height > 0,
              image.width <= maxSourceDimension, image.height <= maxSourceDimension,
              let size = maskDimensions(logicalSize ?? CGSize(width: image.width, height: image.height), samplingScale: samplingScale) else { return nil }
        let width = size.width, height = size.height
        guard width * height <= maxPixels,
              let source = rgba(image, width: width, height: height) else { return nil }
        let pad = thicknessPixels * samplingScale
        let outWidth = width + 2 * pad
        let outHeight = height + 2 * pad
        let colour = ActorContrast.outlineColour(faction)
        let r = UInt8((colour.red * 255).rounded())
        let g = UInt8((colour.green * 255).rounded())
        let b = UInt8((colour.blue * 255).rounded())

        func opaque(_ x: Int, _ y: Int) -> Bool {
            guard x >= 0, y >= 0, x < width, y < height else { return false }
            return source[(y * width + x) * 4 + 3] >= opaqueThreshold
        }

        var out = [UInt8](repeating: 0, count: outWidth * outHeight * 4)
        for oy in 0..<outHeight {
            for ox in 0..<outWidth {
                let sx = ox - pad
                let sy = oy - pad
                if opaque(sx, sy) { continue }
                var near = false
                search: for dy in -pad...pad {
                    for dx in -pad...pad where opaque(sx + dx, sy + dy) {
                        near = true
                        break search
                    }
                }
                guard near, ActorContrast.outlinePixelOn(x: ox / samplingScale, y: oy / samplingScale, faction: faction) else { continue }
                let index = (oy * outWidth + ox) * 4
                out[index] = r
                out[index + 1] = g
                out[index + 2] = b
                out[index + 3] = 255
            }
        }
        guard let texture = texture(pixels: out, width: outWidth, height: outHeight, smooth: false) else { return nil }
        return Entry(texture: texture, pad: pad, maskSize: CGSize(width: width, height: height))
    }

    /// Premultiplied RGBA bytes, rows top first.
    nonisolated static func rgba(_ image: CGImage, width requestedWidth: Int? = nil, height requestedHeight: Int? = nil) -> [UInt8]? {
        let width = requestedWidth ?? image.width
        let height = requestedHeight ?? image.height
        var bytes = [UInt8](repeating: 0, count: width * height * 4)
        let drawn = bytes.withUnsafeMutableBytes { buffer -> Bool in
            guard let context = CGContext(
                data: buffer.baseAddress,
                width: width,
                height: height,
                bitsPerComponent: 8,
                bytesPerRow: width * 4,
                space: CGColorSpaceCreateDeviceRGB(),
                bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue
            ) else { return false }
            context.interpolationQuality = .none
            context.draw(image, in: CGRect(x: 0, y: 0, width: width, height: height))
            return true
        }
        return drawn ? bytes : nil
    }

    /// A texture from premultiplied RGBA bytes laid out like `rgba(_:)`.
    nonisolated static func texture(pixels: [UInt8], width: Int, height: Int, smooth: Bool) -> SKTexture? {
        var bytes = pixels
        let image: CGImage? = bytes.withUnsafeMutableBytes { buffer in
            CGContext(
                data: buffer.baseAddress,
                width: width,
                height: height,
                bitsPerComponent: 8,
                bytesPerRow: width * 4,
                space: CGColorSpaceCreateDeviceRGB(),
                bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue
            )?.makeImage()
        }
        guard let image else { return nil }
        let texture = SKTexture(cgImage: image)
        // Actor art is nearest-neighbour (visual-language-001); the outline
        // matches it. The shadow is soft, so it filters linearly.
        texture.filteringMode = smooth ? .linear : .nearest
        return texture
    }
}
