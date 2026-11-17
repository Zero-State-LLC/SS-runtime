#if DEBUG
import CryptoKit
import SpriteKit
import SurveillanceCore
import UIKit

/// BP-001/007/012 T1045. Explicit local review, never an admitted asset family.
/// Keeps the live renderer and gameplay projection. Does not install broad BenchmarkReviewArt.
@MainActor
struct KioskPlayableReview {
    static let solidID = "solid-03-transit-kiosk"
    static let manifestSHA256 = "11fd5f08aaeac28e2940005534802d2f9cf1d4366a8856ec0bf060ef59503264"
    enum Arm: String { case current, candidate }
    struct Request: Equatable {
        let arm: Arm
        let root: URL
    }
    enum Invalid: Error, CustomStringConvertible {
        case arguments, path, manifest, registration, source, authority
        var description: String { "Kiosk review rejected: \(String(describing: self.code))" }
        private var code: String {
            switch self {
            case .arguments: "arguments"
            case .path: "noncanonical or missing resource path"
            case .manifest: "manifest identity"
            case .registration: "authored registration"
            case .source: "source bytes or dimensions"
            case .authority: "authoritative kiosk bounds"
            }
        }
    }
    struct Source: Decodable, Equatable {
        let role: String
        let file: String
        let sha256: String
        let canvasPixels: [Double]
        let rootPixelsTopLeft: [Double]
        let worldPosition: [Double]
        let drawSizeWorld: [Double]
        var size: CGSize { .init(width: drawSizeWorld[0], height: drawSizeWorld[1]) }
        var anchor: CGPoint { .init(x: rootPixelsTopLeft[0] / canvasPixels[0], y: 1 - rootPixelsTopLeft[1] / canvasPixels[1]) }
        var position: CGPoint { .init(x: worldPosition[0], y: worldPosition[1]) }
    }
    private struct Manifest: Decodable {
        let schema: String
        let solidID: String
        let authoritativeBounds: [Double]
        let ownerAcceptance: Bool
        let productionAdmitted: Bool
        let sources: [Source]
    }
    let arm: Arm
    let building: Source
    let base: Source
    private let buildingTexture: SKTexture
    private let baseTexture: SKTexture

    /// Absence does no filesystem or image work. Both flags are required once opted in.
    static func request(arguments: [String]) throws -> Request? {
        let armFlags = arguments.indices.filter { arguments[$0] == "-SSKioskReview" }
        let rootFlags = arguments.indices.filter { arguments[$0] == "-SSKioskReviewRoot" }
        if armFlags.isEmpty && rootFlags.isEmpty { return nil }
        guard armFlags.count == 1, rootFlags.count == 1,
              let a = armFlags.first, let r = rootFlags.first,
              a + 1 < arguments.count, r + 1 < arguments.count,
              let arm = Arm(rawValue: arguments[a + 1]), arguments[r + 1].hasPrefix("/") else {
            throw Invalid.arguments
        }
        let path = arguments[r + 1]
        guard !path.split(separator: "/").contains(".."), !path.split(separator: "/").contains(".") else { throw Invalid.path }
        return Request(arm: arm, root: URL(fileURLWithPath: path, isDirectory: true))
    }

    nonisolated static func digest(_ data: Data) -> String {
        CryptoKit.SHA256.hash(data: data).map { String(format: "%02x", $0) }.joined()
    }

    static func validate(_ source: Source) throws {
        let expected: (String, [Double], [Double], [Double], [Double])
        switch source.role {
        case "current": expected = ("c411e33b79e0ffc5b0eb86143cd8785a564e573b5819bc1d4c399ef5d3b60264", [1000,1200], [500,1160], [512,640], [200,240])
        case "candidate": expected = ("5a1c7fa1cf23d7bd85bc5676b4a0e297662071404cbb3ec454c9153a7d97c931", [1000,1060], [500,1020], [512,640], [200,212])
        case "base": expected = ("c3313e0475e6aac62f1ec66ff7db4e254ae95e4ef193c5079bf5921e1e90d63b", [230,136], [115,95], [525,653], [57.5,34])
        default: throw Invalid.registration
        }
        guard source.file == source.role + ".png", source.sha256 == expected.0,
              source.canvasPixels == expected.1, source.rootPixelsTopLeft == expected.2,
              source.worldPosition == expected.3, source.drawSizeWorld == expected.4 else { throw Invalid.registration }
    }

    static func load(_ request: Request) throws -> Self {
        let root = request.root.standardizedFileURL
        guard root.path == request.root.path, root.resolvingSymlinksInPath().path == root.path else { throw Invalid.path }
        let names = try FileManager.default.contentsOfDirectory(atPath: root.path)
        guard Set(names) == Set(["manifest.json", "current.png", "candidate.png", "base.png"]) else { throw Invalid.manifest }
        func bytes(_ name: String) throws -> Data {
            let path = root.appendingPathComponent(name)
            guard path.resolvingSymlinksInPath().path == path.path else { throw Invalid.path }
            return try Data(contentsOf: path)
        }
        let data = try bytes("manifest.json")
        guard digest(data) == manifestSHA256 else { throw Invalid.manifest }
        let manifest = try JSONDecoder().decode(Manifest.self, from: data)
        guard manifest.schema == "debug-playable-kiosk-review-001", manifest.solidID == solidID,
              manifest.authoritativeBounds == [512,640,640,768], !manifest.ownerAcceptance, !manifest.productionAdmitted,
              manifest.sources.map(\.role) == ["current", "candidate", "base"] else { throw Invalid.manifest }
        var textures: [String: SKTexture] = [:]
        for source in manifest.sources {
            try validate(source)
            let png = try bytes(source.file)
            guard digest(png) == source.sha256,
                  Array(png.prefix(8)) == [137,80,78,71,13,10,26,10],
                  let image = UIImage(data: png), let cg = image.cgImage,
                  Double(cg.width) == source.canvasPixels[0], Double(cg.height) == source.canvasPixels[1] else { throw Invalid.source }
            let texture = SKTexture(cgImage: cg)
            texture.filteringMode = .linear
            textures[source.role] = texture
        }
        guard let building = manifest.sources.first(where: { $0.role == request.arm.rawValue }),
              let base = manifest.sources.last, let buildingTexture = textures[request.arm.rawValue],
              let baseTexture = textures["base"] else { throw Invalid.source }
        return Self(arm: request.arm, building: building, base: base,
                    buildingTexture: buildingTexture, baseTexture: baseTexture)
    }

    func validateAuthority(_ snapshot: PresentationSnapshot) throws {
        guard snapshot.solidIds.count == snapshot.solids.count,
              snapshot.solidIds.filter({ $0 == Self.solidID }).count == 1,
              let index = snapshot.solidIds.firstIndex(of: Self.solidID) else { throw Invalid.authority }
        let box = snapshot.solids[index]
        guard box.minX == 512, box.minY == 640, box.maxX == 640, box.maxY == 768 else { throw Invalid.authority }
    }

    /// Source-local composition, not a world projection change. V9 orders base before kiosk.
    /// The base's authored world offset is projected only inside this one painted source group.
    func makeNode() -> SKNode {
        let root = SKNode()
        root.name = "kiosk-playable-review"
        root.position = building.position
        let baseNode = SKSpriteNode(texture: baseTexture, size: base.size)
        baseNode.name = "kiosk-review-v9-base"
        baseNode.anchorPoint = base.anchor
        let delta = CGPoint(x: base.position.x - building.position.x, y: base.position.y - building.position.y)
        baseNode.position = BenchmarkProjectionGeometry.project(delta)
        baseNode.zPosition = 0
        root.addChild(baseNode)
        let buildingNode = SKSpriteNode(texture: buildingTexture, size: building.size)
        buildingNode.name = "kiosk-review-building"
        buildingNode.anchorPoint = building.anchor
        buildingNode.zPosition = 0.01
        root.addChild(buildingNode)
        return root
    }
}
#endif
