import Testing
@testable import SurveillanceCore

/// D-113 (upgrades.md, enemies-and-encounters.md § Heat): Ricochet continues
/// from an enemy hit only when the hit defeats it. Signal Jammer removes heat
/// reinforcements: one per wave under D-113, two under D-115, which is all
/// the heat table ever adds.
@Suite(.serialized)
struct UpgradeParityD113Tests {
    /// Ricochet selected, two stationary Informants side by side in the open,
    /// and a Civic Pulse injected on the first.
    private static func ricochetHit(firstIntegrity: Int) throws -> Simulation {
        var sim = try Simulation.make(seed: 1)
        sim.testing_completeEncounter("M-A")
        sim.testing_selectUpgrade(.ricochetPulse)
        let origin = sim.state.player.position
        let first = VecI(x: origin.x.unitsTruncated + 90, y: origin.y.unitsTruncated)
        let second = VecI(x: origin.x.unitsTruncated + 150, y: origin.y.unitsTruncated)
        sim.testing_spawnInformant(at: first, integrity: firstIntegrity, speed: 0)
        sim.testing_spawnInformant(at: second, integrity: 100, speed: 0)
        sim.testing_injectPulseHitting(position: first.asQ8)
        _ = sim.step(command: .neutral(tick: sim.state.tick + 1))
        return sim
    }

    /// The continuation resolves in the same damage phase (upgrades.md), so
    /// the evidence is the second Informant's Integrity, not a live projectile.
    private static func secondIntegrity(_ sim: Simulation) -> Int? {
        let origin = sim.state.player.position
        let second = VecI(x: origin.x.unitsTruncated + 150, y: origin.y.unitsTruncated).asQ8
        return sim.state.enemies.first { $0.position == second }?.integrity
    }

    @Test func aHitThatDefeatsTheEnemyContinues() throws {
        let sim = try Self.ricochetHit(firstIntegrity: 5)
        #expect(Self.secondIntegrity(sim) == 90)
    }

    @Test func aHitTheEnemySurvivesDoesNotContinue() throws {
        let sim = try Self.ricochetHit(firstIntegrity: 100)
        #expect(Self.secondIntegrity(sim) == 100)
    }

    @Test func theRuleIsOn() {
        #expect(Targeting.ricochetContinuationRequiresEnemyKill)
        #expect(ExposureState.jammerHeatReinforcementReduction == 2)
    }

    /// UP-013 (D-115): no wave gains heat reinforcements under the Jammer.
    @Test func jammerCancelsHeatReinforcements() {
        let heat = CombatContent.bundled().heat
        let expected: [DetectionState: (Int, Int)] = [
            .hidden: (0, 0), .observed: (0, 0), .tracked: (1, 0), .hunted: (2, 0), .lockdown: (2, 0)
        ]
        for (state, (plain, jammer)) in expected {
            #expect(heat.reinforcements(encounter: "M-A", state: state, signalJammer: false) == plain, "\(state)")
            #expect(heat.reinforcements(encounter: "M-A", state: state, signalJammer: true) == jammer, "\(state)")
        }
        #expect(heat.reinforcements(encounter: "M-C", state: .hunted, signalJammer: true) == 0)
    }

    /// The caption reads the same count as the spawn queue, so the HUD never
    /// announces reinforcements the Jammer removed.
    @Test func theCaptionAgreesWithTheJammer() {
        let heat = CombatContent.bundled().heat
        let wave = [AuthoritativeEvent(tick: 9, phase: 15, type: .waveStarted,
                                       payload: ["encounterId": .string("M-A"), "waveId": .string("A1")], insertion: 0)]
        #expect(HeatCaptionProjector.reinforcements(events: wave, detection: .hunted, heat: heat, signalJammer: true) == 0)
        var projector = HeatCaptionProjector()
        #expect(projector.project(tick: 9, events: wave, detection: .tracked, heat: heat, signalJammer: true) == nil)
        #expect(projector.project(tick: 10, events: wave, detection: .lockdown, heat: heat, signalJammer: true) == nil)
        #expect(projector.project(tick: 11, events: wave, detection: .hunted, heat: heat, signalJammer: false)
            == "REINFORCEMENTS +2 • HUNTED")
    }
}
