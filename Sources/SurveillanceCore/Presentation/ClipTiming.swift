/// Exact presentation durations. Conversion to seconds belongs at the renderer boundary.
public struct ClipTiming: Equatable, Sendable {
    public enum Failure: Error, Equatable { case invalid, overflow, index }
    public let unitsPerSecond: Int
    public let frameUnits: [Int]
    public let totalUnits: Int

    public init(unitsPerSecond: Int, frameUnits: [Int]) throws {
        guard unitsPerSecond > 0, !frameUnits.isEmpty,
              frameUnits.allSatisfy({ $0 > 0 }) else { throw Failure.invalid }
        var total = 0
        for units in frameUnits {
            let sum = total.addingReportingOverflow(units)
            guard !sum.overflow else { throw Failure.overflow }
            total = sum.partialValue
        }
        self.unitsPerSecond = unitsPerSecond
        self.frameUnits = frameUnits
        self.totalUnits = total
    }

    /// Adapter for the unchanged v1 delivery, not a new metadata schema.
    public static func uniform(frameCount: Int, framesPerSecond: Int) throws -> Self {
        guard frameCount > 0, framesPerSecond > 0 else { throw Failure.invalid }
        return try Self(unitsPerSecond: framesPerSecond, frameUnits: Array(repeating: 1, count: frameCount))
    }

    /// Select with exactly the same indices used to select frame IDs.
    public func selecting(_ indices: [Int]) throws -> Self {
        guard !indices.isEmpty, indices.allSatisfy({ frameUnits.indices.contains($0) }),
              zip(indices, indices.dropFirst()).allSatisfy({ $0.0 < $0.1 }) else { throw Failure.index }
        return try Self(unitsPerSecond: unitsPerSecond, frameUnits: indices.map { frameUnits[$0] })
    }

    public var frameSeconds: [Double] {
        frameUnits.map { Double($0) / Double(unitsPerSecond) }
    }

    public func durationTicks(at ticksPerSecond: Int) throws -> UInt64 {
        guard ticksPerSecond > 0 else { throw Failure.invalid }
        let product = totalUnits.multipliedReportingOverflow(by: ticksPerSecond)
        guard !product.overflow else { throw Failure.overflow }
        let whole = product.partialValue / unitsPerSecond
        // Avoid adding denominator-1 to the numerator, which can overflow.
        return UInt64(whole) + (product.partialValue % unitsPerSecond == 0 ? 0 : 1)
    }
}
