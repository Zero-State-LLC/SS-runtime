import Foundation
import Testing
@testable import SurveillanceCore

struct FeelProjectionParityTests {
    /// Frozen pre-optimization copy path, kept independent of the direct query.
    struct Legacy {
        var labels = EncounterLabelGate()
        var queue = TutorialLineQueue()
        var objective: String?
        var line: String?
        var nearMiss: [EntityID] = []
        mutating func observe(_ state: WorldState) {
            let snap = PresentationSnapshot(state)
            nearMiss = PatrolNearMiss.members(state)
            objective = labels.project(snap, state: state)
            var hints: [String] = []
            if PatrolTutorial.coneOnScreen(snap) { hints.append(PatrolTutorial.copy) }
            if FeelPassPresenter.unawareNonPatrolOnScreen(snap) { hints.append(AwarenessHintProjector.copy) }
            let card = snap.tutorialCopyIsSafetyMessage ? nil : snap.tutorialCopy
            let blocked = snap.upgradePending || snap.tutorialCopyIsSafetyMessage
                || labels.isFresh(snap.objectiveNode, tick: snap.tick)
            line = queue.update(card: card, hints: hints, blocked: blocked)
        }
    }

    static func compare(_ state: WorldState, _ direct: inout FeelPassPresenter, _ legacy: inout Legacy) {
        direct.observe(state)
        legacy.observe(state)
        #expect(direct.nearMiss == legacy.nearMiss)
        #expect(direct.objectiveCopy == legacy.objective)
        #expect(direct.tutorialLine == legacy.line)
        #expect(direct.tutorial == legacy.queue)
        #expect(direct.encounterLabels == legacy.labels)
    }

    @Test func viewportPatrolMembershipAndCopyPriorityMatchSnapshot() throws {
        var sim = try Simulation.make(seed: 1)
        sim.step(command: .neutral(tick: 1))
        let member = try #require(sim.state.enemies.first { $0.patrol != nil })
        for position in [VecI(x: 0, y: 0), VecI(x: 1100, y: 700), VecI(x: 2304, y: 1536)] {
            for offset in [VecI(x: 352, y: 163), VecI(x: 353, y: 164), VecI(x: -352, y: -163), VecI(x: -353, y: -164)] {
                for condition in 0..<6 {
                    for mode in 0..<5 {
                        var state = sim.state
                        state.player.position = position.asQ8
                        let center = PresentationCamera.follow(player: position, heading: state.player.facing, bounds: state.arena.boundsUnits).center
                        var enemy = member
                        enemy.position = VecI(x: center.x + offset.x, y: center.y + offset.y).asQ8
                        if condition == 1 { enemy.patrol = nil }
                        if condition == 2 { enemy.patrol?.facing = .zero }
                        if condition == 3 { enemy.awareness = .aware }
                        if condition == 4 { enemy.integrity = 0 }
                        if condition == 5 { enemy.awareness = .struck }
                        state.enemies = [enemy]
                        state.tutorial.phase = mode == 0 ? .complete : .move
                        state.tutorial.lockdownPreempts = mode == 2
                        state.tutorial.extractionPreempts = mode == 3 ? .lockedContact : nil
                        state.upgrade.pending = mode == 4
                        var direct = FeelPassPresenter()
                        var legacy = Legacy()
                        Self.compare(state, &direct, &legacy)
                    }
                }
            }
        }
    }

    @Test func lifecycleEncounterTransitionsExpiryRewindAndResetMatchSnapshot() throws {
        var sim = try Simulation.make(seed: 1)
        sim.step(command: .neutral(tick: 1))
        var state = sim.state
        var direct = FeelPassPresenter()
        var legacy = Legacy()
        for tick in 1...760 {
            state.clock = SimulationClock(tick: UInt64(tick))
            if tick == 2 { state.encounters["M-A"]?.activated = true }
            if tick == 160 { state.encounters["M-A"]?.completed = true; state.encounters["M-B"]?.activated = true }
            if tick == 320 { state.encounters["M-B"]?.completed = true; state.encounters["M-C"]?.activated = true }
            if tick == 480 { state.encounters["M-C"]?.completed = true }
            if tick == 500 { state.eliteDefeated = true }
            if tick == 520 { state.bossDefeated = true }
            if tick == 540 { state.extraction.armed = true }
            state.tutorial.phase = tick < 180 ? .move : .complete
            state.upgrade.pending = (200..<220).contains(tick)
            state.tutorial.lockdownPreempts = (230..<260).contains(tick)
            Self.compare(state, &direct, &legacy)
        }
        state.clock = SimulationClock(tick: 1)
        Self.compare(state, &direct, &legacy)
        direct.reset(); legacy = Legacy()
        Self.compare(state, &direct, &legacy)
    }
    @Test func mixedHintsKeepPatrolBeforeGeneralAwareness() throws {
        var sim = try Simulation.make(seed: 1)
        sim.step(command: .neutral(tick: 1))
        var state = sim.state
        var patrol = try #require(state.enemies.first { $0.patrol != nil })
        patrol.position = state.player.position
        var other = patrol
        other.id = EntityID(99_999)
        other.patrol = nil
        state.enemies = [other, patrol]
        state.tutorial.phase = .complete
        var direct = FeelPassPresenter()
        var legacy = Legacy()
        Self.compare(state, &direct, &legacy)
        #expect(direct.tutorial.pending == [PatrolTutorial.copy, AwarenessHintProjector.copy])
    }

    /// Diagnostic only: identical state, both ordering directions, no timing
    /// threshold. This measures CPU projection cost, not display or device FPS.
    @Test func isolatedObservationTiming() throws {
        var sim = try Simulation.make(seed: 1)
        sim.step(command: .neutral(tick: 1))
        let state = sim.state
        var direct = FeelPassPresenter()
        var legacy = Legacy()
        for _ in 0..<10 { Self.compare(state, &direct, &legacy) }
        for directFirst in [false, true] {
            var directTimes: [Double] = []
            var legacyTimes: [Double] = []
            for _ in 0..<100 {
                func sampleDirect() {
                    let start = DispatchTime.now().uptimeNanoseconds
                    direct.observe(state)
                    directTimes.append(Double(DispatchTime.now().uptimeNanoseconds - start) / 1_000_000)
                }
                func sampleLegacy() {
                    let start = DispatchTime.now().uptimeNanoseconds
                    legacy.observe(state)
                    legacyTimes.append(Double(DispatchTime.now().uptimeNanoseconds - start) / 1_000_000)
                }
                if directFirst { sampleDirect(); sampleLegacy() } else { sampleLegacy(); sampleDirect() }
                #expect(direct.tutorial == legacy.queue)
                #expect(direct.encounterLabels == legacy.labels)
                #expect(direct.nearMiss == legacy.nearMiss)
            }
            let record: [String: Any] = ["directFirst": directFirst, "directMs": directTimes, "legacyMs": legacyTimes]
            let data = try JSONSerialization.data(withJSONObject: record, options: [.sortedKeys])
            print("FEEL_PROJECTION_TIMING " + String(decoding: data, as: UTF8.self))
        }
    }

}
