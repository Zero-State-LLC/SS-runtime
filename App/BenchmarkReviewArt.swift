import SpriteKit

/// Review-only texture injection. The test target owns all candidate files.
/// It cannot alter simulation geometry or asset admission records.
@MainActor
struct BenchmarkReviewArt {
    struct GroundPatch {
        let texture: SKTexture
        let bounds: CGRect
        let tileUnits: CGFloat
    }
    struct GroundLine {
        let start: CGPoint
        let end: CGPoint
        let width: CGFloat
        let color: SKColor
    }
    struct Placement {
        let texture: SKTexture
        let size: CGSize
        let anchor: CGPoint
        let position: CGPoint
    }
    let player: SKTexture
    let camera: SKTexture
    let building: Placement
    let buildingID: String
    let props: [Placement]
    let paving: SKTexture
    var cameraStates: [Int: SKTexture] = [:]
    var groundPatches: [GroundPatch] = []
    var groundLines: [GroundLine] = []
}
