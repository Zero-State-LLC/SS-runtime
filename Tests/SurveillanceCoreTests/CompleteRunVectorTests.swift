import Testing
@testable import SurveillanceCore

@Suite(.serialized)
struct CompleteRunVectorTests {
    private struct ExpectedVector: Sendable {
        var elapsedTicks: UInt64
        var terminalDigest: String
    }

    private static let expectedVectors: [UpgradeID: ExpectedVector] = [
        .signalJammer: ExpectedVector(
            elapsedTicks: 302,
            terminalDigest: "3606fe66eacc3bc93b6219ec67bf8457fd6f03e301c897521327678bf6c555e6"
        ),
        .ricochetPulse: ExpectedVector(
            elapsedTicks: 302,
            terminalDigest: "41b081038151a2e8f286c2edb864f42f75ccac40a9ae86bca94e137b889de389"
        ),
        .ghostStep: ExpectedVector(
            elapsedTicks: 302,
            terminalDigest: "e960e78d2d1d2d35425fb30b169734160fea514735644ff7012a70ebc6e6959c"
        )
    ]

    @Test(arguments: UpgradeID.allCases)
    func completeRunT705GoldenVectorSucceedsWithZeroCamerasDestroyed(upgrade: UpgradeID) throws {
        var sim = try Simulation.make(seed: 1)
        let result = sim.testing_completeRunSuccess(upgrade: upgrade)
        let receipt = RunReceipt(sim.state)
        #expect(result.outcome == .success)
        #expect(sim.state.destructions.count == 0)
        #expect(!sim.state.networkBlackout)
        #expect(sim.state.upgrade.selected == upgrade)
        #expect(receipt.upgrade == upgrade)
        #expect(receipt.camerasDestroyed == 0)
        #expect(!receipt.networkBlackout)
        #expect(receipt.extractionArmed)
        #expect(receipt.combatAuthority.complete)
        #expect(receipt.bossDefeated)
        #expect(sim.state.terminalDigest != nil)
        let expected = Self.expectedVectors[upgrade]!
        #expect(sim.state.tick == expected.elapsedTicks)
        #expect(sim.state.terminalDigest == expected.terminalDigest)
        #expect(receipt.finalDigest == expected.terminalDigest)
    }

    @Test(arguments: UpgradeID.allCases)
    func completeRunT706NoCameraDestructionExploit(upgrade: UpgradeID) throws {
        var sim = try Simulation.make(seed: 1)
        testing_preparePostUpgradeCombat(sim: &sim, upgrade: upgrade)
        sim.testing_destroyCameraAtIndex(0)
        _ = sim.step(command: .neutral(tick: sim.state.tick + 1))
        let extract = sim.state.arena.extraction.center
        sim.testing_setPlayerPosition(VecI(x: extract.x, y: extract.y))
        sim.testing_setExtractionRemaining(0)
        let result = sim.step(command: .neutral(tick: sim.state.tick + 1))
        let receipt = RunReceipt(sim.state)
        #expect(sim.state.destructions.count == 1)
        #expect(receipt.camerasDestroyed == 1)
        #expect(result.outcome != .success || receipt.camerasDestroyed != 0)
    }

    @Test(arguments: UpgradeID.allCases)
    func completeRunT706UpgradeIsolationPreserved(upgrade: UpgradeID) throws {
        var sim = try Simulation.make(seed: 1)
        testing_preparePostUpgradeCombat(sim: &sim, upgrade: upgrade)
        #expect(sim.state.upgrade.selected == upgrade)
        for other in UpgradeID.allCases where other != upgrade {
            #expect(sim.state.upgrade.selected != other)
        }
    }

    @Test func completeRunT706SignalJammerDoesNotBlockForcedLockdown() {
        var state = ExposureState(exposure: 200, detectionState: .observed)
        let result = state.resolveTick(
            survivingContactCount: 1,
            tamperAmounts: [],
            signalJammer: true,
            forceLockdown: true
        )
        #expect(state.lockdownEntered)
        #expect(result.reason == .forcedLockdown)
    }

    @Test func completeRunT706GhostStepDoesNotGrantDamageImmunity() throws {
        var sim = try Simulation.make(seed: 1)
        sim.testing_selectUpgrade(.ghostStep)
        let dodgeTick = sim.state.tick + 1
        _ = sim.step(
            command: PlayerCommand(
                tick: dodgeTick,
                moveX: PlayerCommand.axisMaximum,
                moveY: 0,
                dodgePressed: true
            )
        )
        let before = sim.state.player.integrity
        sim.testing_injectHostileBolt()
        let hitTick = sim.state.tick + 1
        _ = sim.step(command: .neutral(tick: hitTick))
        // D-090: 50% of the bolt's 10.
        #expect(sim.state.player.integrity == before - 5)
    }

    @Test func completeRunT706RicochetCannotDoubleHitSameTarget() {
        let id = IsolatedKernel.ricochetSkipsDestroyedCamera()
        #expect(id == 9)
    }

    private func testing_preparePostUpgradeCombat(sim: inout Simulation, upgrade: UpgradeID) {
        sim.testing_completeEncounter("M-A")
        sim.testing_selectUpgrade(upgrade)
        sim.testing_completeCombatGraph()
        _ = sim.step(command: .neutral(tick: sim.state.tick + 1))
    }
}
