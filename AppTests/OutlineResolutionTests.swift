import CoreGraphics
import SpriteKit
import Testing
@testable import SSRuntime
@testable import SurveillanceCore

@Suite(.serialized)
@MainActor
struct OutlineResolutionTests {
    private func source(density: Int, shifted: Bool = false) throws -> SKTexture {
        let edge = 64 * density
        var pixels = [UInt8](repeating: 0, count: edge * edge * 4)
        let left = shifted ? 32 : 8
        for y in (16 * density)..<(48 * density) {
            for x in (left * density)..<((left + 16) * density) {
                let i = (y * edge + x) * 4
                pixels[i] = 255; pixels[i + 3] = 255
            }
        }
        return try #require(OutlineTextures.texture(pixels: pixels, width: edge, height: edge, smooth: false))
    }

    @Test func sourceDensityDoesNotChangeStrokeOrEnemyDashes() throws {
        for faction in [ActorContrast.Faction.player, .enemy] {
            var baseline: [UInt8]?
            for density in [1, 4, 6] {
                let texture = try source(density: density)
                let entry = try #require(OutlineTextures.make(from: texture.cgImage(), faction: faction,
                    logicalSize: CGSize(width: 64, height: 64)))
                #expect(entry.maskSize == CGSize(width: 64, height: 64))
                #expect(entry.pad == 1)
                let image = entry.texture.cgImage()
                #expect(image.width == 66 && image.height == 66)
                let bytes = try #require(OutlineTextures.rgba(image))
                if let baseline { #expect(bytes == baseline) } else { baseline = bytes }
                let count = stride(from: 3, to: bytes.count, by: 4).filter { bytes[$0] > 0 }.count
                if faction == .player { #expect(count == 100) }
                else { #expect(count > 0 && count < 100) }
            }
        }
    }

    @Test func cacheSeparatesLogicalGeometryFactionAndBoundsChurn() throws {
        let cache = OutlineTextures(maxEntries: 2, maxBytes: 2 * 66 * 66 * 4)
        let a = try source(density: 6)
        let first = try #require(cache.outline(for: a, faction: .player, logicalSize: CGSize(width: 64, height: 64)))
        let same = try #require(cache.outline(for: a, faction: .player, logicalSize: CGSize(width: 64, height: 64)))
        #expect(first.texture === same.texture)
        let resized = try #require(cache.outline(for: a, faction: .player, logicalSize: CGSize(width: 32, height: 64)))
        #expect(resized.maskSize == CGSize(width: 32, height: 64))
        #expect(resized.texture !== first.texture)
        let enemy = try #require(cache.outline(for: a, faction: .enemy, logicalSize: CGSize(width: 64, height: 64)))
        #expect(enemy.texture !== first.texture)
        for _ in 0..<12 {
            let frame = try source(density: 1)
            #expect(cache.outline(for: frame, faction: .player, logicalSize: CGSize(width: 64, height: 64)) != nil)
            #expect(cache.count <= 2)
            #expect(cache.retainedMaskBytes <= 2 * 66 * 66 * 4)
        }
        let bytesLimited = OutlineTextures(maxEntries: 128, maxBytes: 66 * 66 * 4)
        _ = bytesLimited.outline(for: a, faction: .player, logicalSize: CGSize(width: 64, height: 64))
        _ = bytesLimited.outline(for: a, faction: .enemy, logicalSize: CGSize(width: 64, height: 64))
        #expect(bytesLimited.count == 1)
        #expect(bytesLimited.retainedMaskBytes == 66 * 66 * 4)
    }

    @Test func invalidSizesAndOversizeSourceFailWithoutAllocationGrowth() throws {
        let texture = try source(density: 6)
        let cache = OutlineTextures()
        for size in [CGSize.zero, CGSize(width: CGFloat.nan, height: 64),
                     CGSize(width: 64, height: CGFloat.infinity), CGSize(width: 257, height: 64)] {
            #expect(cache.outline(for: texture, faction: .player, logicalSize: size) == nil)
        }
        #expect(cache.count == 0 && cache.retainedMaskBytes == 0)
        let pixels = [UInt8](repeating: 255, count: 1025 * 4)
        let oversized = try #require(OutlineTextures.texture(pixels: pixels, width: 1025, height: 1, smooth: false))
        #expect(cache.outline(for: oversized, faction: .player, logicalSize: CGSize(width: 64, height: 64)) == nil)
        #expect(cache.count == 1 && cache.retainedMaskBytes == 0)
    }

    @Test func rendererRefreshKeepsAnchorAndDropsStaleFrameInBothMotionModes() throws {
        let snapshot = PresentationSnapshot(try Simulation.make(seed: 1).state)
        let first = try source(density: 6)
        let next = try source(density: 6, shifted: true)
        let tooWide = try #require(OutlineTextures.texture(pixels: [UInt8](repeating: 255, count: 1025 * 4),
                                                         width: 1025, height: 1, smooth: false))
        for reduced in [false, true] {
            let renderer = WorldRenderer()
            renderer.render(snapshot, reducedMotion: reduced)
            let sprite = try #require(renderer.root.childNode(withName: "//sprite-player") as? SKSpriteNode)
            sprite.removeAllActions()
            sprite.size = CGSize(width: 64, height: 64)
            sprite.anchorPoint = CGPoint(x: 0.25, y: 0.125)
            let position = sprite.position
            sprite.texture = first
            renderer.syncOutlines()
            let outline = try #require(sprite.childNode(withName: WorldRenderer.outlineName) as? SKSpriteNode)
            #expect(!outline.isHidden)
            #expect(outline.size == CGSize(width: 66, height: 66))
            #expect(abs(outline.anchorPoint.x - 17.0 / 66) < 0.00001)
            #expect(abs(outline.anchorPoint.y - 9.0 / 66) < 0.00001)
            #expect(outline.position == .zero && sprite.position == position)
            let originalOutline = try #require(outline.texture)
            // #124: child geometry must not apply an actor's zoom a second time.
            for (sx, sy) in [(CGFloat(1.5), CGFloat(1.25)), (CGFloat(1.1), CGFloat(1.3))] {
                sprite.xScale = sx
                sprite.yScale = sy
                renderer.syncOutlines()
                #expect(abs(outline.size.width - 66) < 0.0001)
                #expect(abs(outline.size.height - 66) < 0.0001)
                #expect(outline.texture === originalOutline)
                #expect(abs(outline.anchorPoint.x - 17.0 / 66) < 0.00001)
                #expect(abs(outline.anchorPoint.y - 9.0 / 66) < 0.00001)
            }
            sprite.texture = next
            renderer.syncOutlines()
            #expect(outline.texture !== originalOutline)
            sprite.texture = tooWide
            renderer.syncOutlines()
            #expect(outline.isHidden)
            sprite.texture = first
            renderer.syncOutlines()
            #expect(!outline.isHidden && outline.texture === originalOutline)
            #expect(sprite.position == position)
        }
    }
}
