import Foundation

/// Resolves a clip's frames to delivered files, and answers honestly when a
/// frame is not backed.
///
/// `legacy-admission.md` makes partial coverage a defined state: an unbacked
/// frame ID falls back to the authored blockout, and the renderer MUST NOT
/// substitute a frame from another role, direction, or clip. This type is where
/// that rule is enforced, so no call site has to remember it.
public struct ClipFrameLibrary: Sendable {
    public struct Clip: Equatable, Sendable {
        public var clipId: String
        public var actorRole: String
        public var directions: [String]
        public var framesPerSecond: Int
        public var loop: Bool
        public var anchor: VecI
        /// Frame IDs in authored contract order; facing is encoded in each ID.
        public var frameIds: [String]

        public var framesPerDirection: Int {
            directions.isEmpty ? frameIds.count : frameIds.count / directions.count
        }
    }

    public private(set) var clips: [String: Clip]
    /// Asset ID to delivered file name, for admitted frames only.
    public private(set) var deliveredPaths: [String: String]

    public init(clips: [String: Clip], deliveredPaths: [String: String]) {
        self.clips = clips
        self.deliveredPaths = deliveredPaths
    }

    /// Loads the clip contract and pairs it with the accepted catalog entries.
    public static func bundled() throws -> ClipFrameLibrary {
        try make(
            clipJSON: SpecBundle.contract("clip-metadata-001"),
            catalog: AssetCatalog.bundled()
        )
    }

    static func make(clipJSON: Data, catalog: AssetCatalog) throws -> ClipFrameLibrary {
        // Delivery must use the same schema and semantic validation as reactions.
        // In particular, future timing keys cannot be silently dropped here.
        let validated = try ClipCatalogLoader.decode(clipJSON)
        let clips = Dictionary(uniqueKeysWithValues: validated.clips.map { clip in
            (clip.clipId, Clip(
                clipId: clip.clipId,
                actorRole: clip.actorRole,
                directions: clip.directions,
                framesPerSecond: clip.framesPerSecond,
                loop: clip.loop,
                anchor: VecI(x: clip.anchor.x, y: clip.anchor.y),
                frameIds: clip.frameIds
            ))
        })

        // Only an admitted, accepted sprite contributes a file.
        var delivered: [String: String] = [:]
        for entry in catalog.entries
        where (entry.admissionDecision == .adaptedAdmitted
            || entry.admissionDecision == .originalAccepted)
            && entry.record.productionStatus == .accepted
            && entry.record.kind == .sprite
        {
            if let path = entry.record.runtimePath {
                delivered[entry.record.assetId] = path
            }
        }
        return ClipFrameLibrary(clips: clips, deliveredPaths: delivered)
    }

    // MARK: - Queries

    public func clip(_ clipId: String) -> Clip? { clips[clipId] }

    /// Frame IDs for one direction of a clip, in contract order.
    public func frameIds(clipId: String, direction: String?) -> [String] {
        guard let clip = clips[clipId] else { return [] }
        guard let direction, !clip.directions.isEmpty else { return clip.frameIds }
        guard clip.directions.contains(direction) else { return [] }
        // Match ClipRecord's authored-facing selection, even when facings are
        // interleaved. Array position alone cannot identify a frame's facing.
        return clip.frameIds.filter { $0.contains("_\(direction)_") }
    }

    /// Delivered file names for one direction, or `nil` when the clip is not
    /// fully backed. All-or-nothing on purpose: a half-delivered animation would
    /// otherwise pop between real frames and gaps.
    public func deliveredFrames(clipId: String, direction: String?) -> [String]? {
        let ids = frameIds(clipId: clipId, direction: direction)
        guard !ids.isEmpty else { return nil }
        var paths: [String] = []
        paths.reserveCapacity(ids.count)
        for id in ids {
            guard let path = deliveredPaths[id] else { return nil }
            paths.append(path)
        }
        return paths
    }

    public func timing(clipId: String, direction: String?) -> ClipTiming? {
        guard let clip = clips[clipId] else { return nil }
        return try? .uniform(frameCount: frameIds(clipId: clipId, direction: direction).count,
                             framesPerSecond: clip.framesPerSecond)
    }

    public func isBacked(clipId: String, direction: String? = nil) -> Bool {
        deliveredFrames(clipId: clipId, direction: direction) != nil
    }

    /// Backed frame count over the whole contract, for evidence and reporting.
    public var coverage: (backed: Int, total: Int) {
        let total = clips.values.reduce(0) { $0 + $1.frameIds.count }
        let backed = clips.values.reduce(0) { sum, clip in
            sum + clip.frameIds.filter { deliveredPaths[$0] != nil }.count
        }
        return (backed, total)
    }

    /// Compass direction for a facing vector, using the clip contract's letters.
    ///
    /// World `+y` is north (up the screen, and `Cordic.headingUnit(270_000)`),
    /// so a positive `y` component faces `n` and shows the back view; `s` is
    /// the front view. Matches `ClipAlignment.cardinalDirection(headingMilli:)`.
    public static func direction(forFacing facing: VecQ8) -> String {
        let x = facing.x.raw
        let y = facing.y.raw
        if x == 0 && y == 0 { return "s" }
        if abs(x) >= abs(y) {
            return x > 0 ? "e" : "w"
        }
        return y > 0 ? "n" : "s"
    }
}
