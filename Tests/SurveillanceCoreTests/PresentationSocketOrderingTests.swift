import Testing
@testable import SurveillanceCore

/// Runtime #260: deterministic presentation only, never reorder authored spawn selection.
struct PresentationSocketOrderingTests {
    @Test func canonicalEncounterOrderPreservesAuthoredSocketsAndSuffix() throws {
        let state = try Simulation.make(seed: 1).state
        let authored = state.arena.enemySpawnSockets
        let expected = try ["M-A", "M-B", "M-C"].flatMap { key in
            try #require(authored[key]).map { VecI(x: $0.x, y: $0.y) }
        } + [VecI(x: state.arena.eliteSpawn.x, y: state.arena.eliteSpawn.y),
             VecI(x: state.arena.bossSpawn.x, y: state.arena.bossSpawn.y)]
        let digest = state.digest()
        #expect(PresentationSnapshot(state).spawnSockets == expected)
        #expect(state.arena.enemySpawnSockets == authored)
        #expect(state.digest() == digest)
    }

    @Test func insertionHistoriesHaveIdenticalFullSnapshotsAndDigests() throws {
        let original = try Simulation.make(seed: 1).state
        let authored = original.arena.enemySpawnSockets
        let keys = ["M-A", "M-B", "M-C"]
        let baseline = PresentationSnapshot(original)
        let digest = original.digest()
        for iteration in 0..<24 {
            var state = original
            state.arena.enemySpawnSockets = [:]
            let order = iteration.isMultiple(of: 2) ? keys : Array(keys.reversed())
            for offset in 0..<keys.count {
                let key = order[(offset + iteration) % keys.count]
                state.arena.enemySpawnSockets[key] = authored[key]
            }
            #expect(state.arena.enemySpawnSockets == authored)
            #expect(state.digest() == digest)
            #expect(PresentationSnapshot(state) == baseline)
            #expect(state.digest() == digest)
        }
    }

    @Test func utf8KeyOrderAndAuthoredArrayOrderAreIndependent() throws {
        var state = try Simulation.make(seed: 1).state
        let sockets = try #require(state.arena.enemySpawnSockets["M-A"])
        #expect(sockets.count >= 3)
        let keys = ["é", "z", "A"]
        state.arena.enemySpawnSockets = [:]
        for (index, key) in keys.enumerated() {
            state.arena.enemySpawnSockets[key] = [sockets[index], sockets[(index + 2) % sockets.count]]
        }
        let authored = state.arena.enemySpawnSockets
        let digest = state.digest()
        let expected = ["A", "z", "é"].flatMap { key in
            authored[key]!.map { VecI(x: $0.x, y: $0.y) }
        } + [VecI(x: state.arena.eliteSpawn.x, y: state.arena.eliteSpawn.y),
             VecI(x: state.arena.bossSpawn.x, y: state.arena.bossSpawn.y)]
        #expect(PresentationSnapshot(state).spawnSockets == expected)
        #expect(state.arena.enemySpawnSockets == authored)
        #expect(state.digest() == digest)
    }

    @Test func independentSessionsProduceEqualFullSnapshots() throws {
        let baseline = try Simulation.make(seed: 1)
        let digest = baseline.state.digest()
        for _ in 0..<8 {
            let independent = try Simulation.make(seed: 1)
            #expect(independent.state.digest() == digest)
            #expect(PresentationSnapshot(independent.state) == PresentationSnapshot(baseline.state))
            #expect(independent.state.digest() == digest)
        }
    }
}
