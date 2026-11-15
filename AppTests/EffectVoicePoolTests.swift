import Testing
@testable import SSRuntime

@MainActor
struct EffectVoicePoolTests {
    @Test func protectsPriorityAndStealsOldestTie() {
        let pool = EffectVoicePool()
        var stopped: [Int] = []
        for i in 0..<8 {
            #expect(pool.admit(priority: 2, isPlaying: { true }, stop: { stopped.append(i) }))
        }
        #expect(!pool.admit(priority: 3, isPlaying: { true }, stop: {}))
        #expect(stopped.isEmpty)
        #expect(pool.admit(priority: 2, isPlaying: { true }, stop: {}))
        #expect(stopped == [0])
        #expect(pool.count == 8)
        pool.stopAll()
        #expect(pool.count == 0)
        #expect(stopped == Array(0..<8))
    }

    @Test func stealsOldestWorstPriorityRatherThanOldestProtectedVoice() {
        let pool = EffectVoicePool()
        var stopped: [Int] = []
        let priorities = [1, 4, 2, 4, 1, 2, 3, 1]
        for (index, priority) in priorities.enumerated() {
            #expect(pool.admit(priority: priority, isPlaying: { true }, stop: { stopped.append(index) }))
        }
        #expect(pool.admit(priority: 3, isPlaying: { true }, stop: {}))
        #expect(stopped == [1])
        #expect(pool.admit(priority: 4, isPlaying: { true }, stop: {}))
        #expect(stopped == [1, 3])
        #expect(!pool.admit(priority: 5, isPlaying: { true }, stop: {}))
        #expect(stopped == [1, 3])
        #expect(pool.count == 8)
    }

    @Test func completedVoiceIsReusedBeforeStealing() {
        let pool = EffectVoicePool()
        var active = true
        var stops = 0
        #expect(pool.admit(priority: 1, isPlaying: { active }, stop: { stops += 1 }))
        for _ in 0..<7 {
            #expect(pool.admit(priority: 1, isPlaying: { true }, stop: {}))
        }
        active = false
        #expect(pool.admit(priority: 9, isPlaying: { true }, stop: {}))
        #expect(pool.count == 8)
        #expect(stops == 1)
    }
}
