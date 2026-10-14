import Testing
@testable import SurveillanceCore

struct ClipTimingTests {
    @Test func exactMigrationVectors() throws {
        let ordinary = try ClipTiming(unitsPerSecond: 32, frameUnits: Array(repeating: 1, count: 16))
        #expect(try ordinary.durationTicks(at: 60) == 30)
        let elite = try ClipTiming(unitsPerSecond: 112, frameUnits: Array(repeating: 3, count: 16))
        #expect(elite.totalUnits == 48)
        #expect(try elite.durationTicks(at: 60) == 26)
        #expect(try elite.durationTicks(at: 112) == 48)
        let variable = try ClipTiming(unitsPerSecond: 24, frameUnits: [1, 2, 1, 2])
        #expect(try variable.durationTicks(at: 60) == 15)
        let expectedSeconds: [Double] = [1.0/24.0, 2.0/24.0, 1.0/24.0, 2.0/24.0]
        #expect(variable.frameSeconds == expectedSeconds)
    }

    @Test func selectionKeepsDirectionHoldsAndOrder() throws {
        let timing = try ClipTiming(unitsPerSecond: 12, frameUnits: [1, 2, 3, 4])
        #expect(try timing.selecting([0, 2]).frameUnits == [1, 3])
        #expect(try timing.selecting([1, 3]).durationTicks(at: 60) == 30)
        #expect(throws: ClipTiming.Failure.index) { try timing.selecting([2, 1]) }
        #expect(throws: ClipTiming.Failure.index) { try timing.selecting([1, 1]) }
        #expect(throws: ClipTiming.Failure.index) { try timing.selecting([4]) }
    }

    @Test func malformedAndOverflowFailClosed() throws {
        #expect(throws: ClipTiming.Failure.invalid) { try ClipTiming(unitsPerSecond: 0, frameUnits: [1]) }
        #expect(throws: ClipTiming.Failure.invalid) { try ClipTiming(unitsPerSecond: 12, frameUnits: []) }
        #expect(throws: ClipTiming.Failure.invalid) { try ClipTiming(unitsPerSecond: 12, frameUnits: [0]) }
        #expect(throws: ClipTiming.Failure.invalid) { try ClipTiming(unitsPerSecond: 12, frameUnits: [-1]) }
        #expect(throws: ClipTiming.Failure.overflow) { try ClipTiming(unitsPerSecond: 1, frameUnits: [Int.max, 1]) }
        let huge = try ClipTiming(unitsPerSecond: Int.max, frameUnits: [Int.max])
        #expect(try huge.durationTicks(at: 1) == 1)
        #expect(throws: ClipTiming.Failure.overflow) { try huge.durationTicks(at: 60) }
    }

    @Test func allDeliveredV1DirectionsKeepTheirCadence() throws {
        let catalog = try ClipCatalog.bundled()
        let library = try ClipFrameLibrary.bundled()
        for clip in catalog.clips {
            for direction in clip.directions.isEmpty ? ["none"] : clip.directions {
                let timing = try clip.timing(forDirection: direction)
                let count = clip.frameIds(forDirection: direction).count
                // Independent legacy formula is safe for the bounded bundled records.
                let expectedTicks = UInt64((count * 60 + clip.framesPerSecond - 1) / clip.framesPerSecond)
                #expect(try timing.durationTicks(at: 60) == expectedTicks)
                #expect(ReactionClipTracker.durationTicks(clip) == expectedTicks)
                #expect(library.timing(clipId: clip.clipId, direction: clip.directions.isEmpty ? nil : direction) == timing)
                #expect(timing.frameSeconds == Array(repeating: 1.0 / Double(clip.framesPerSecond), count: count))
            }
        }
    }
}
