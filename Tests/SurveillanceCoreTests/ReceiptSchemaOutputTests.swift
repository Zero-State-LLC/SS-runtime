import Foundation
import Testing
@testable import SurveillanceCore

/// RC-001...RC-004/RC-007: exercise the production serializer and archive, not
/// a copied JSON template. Scenario hooks establish terminal states but do not
/// constitute complete-play, pacing or device acceptance evidence.
@Suite(.serialized)
struct ReceiptSchemaOutputTests {
    @Test func exportRepresentativeReceipts() throws {
        let suppliedDirectory = ProcessInfo.processInfo.environment["SS_RECEIPT_SCHEMA_OUTPUT"]
        let directory = suppliedDirectory.map { URL(fileURLWithPath: $0, isDirectory: true) }
            ?? FileManager.default.temporaryDirectory.appendingPathComponent("receipt-schema-\(UUID())")
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
        defer {
            if suppliedDirectory == nil { try? FileManager.default.removeItem(at: directory) }
        }
        let selections: [UpgradeID?] = [nil, .signalJammer, .ricochetPulse, .ghostStep]
        var produced = 0
        for outcome in [RunOutcome.success, .failure, .invalid] {
            for (index, upgrade) in selections.enumerated() {
                // Success cannot bypass the protected mandatory upgrade choice.
                if outcome == .success && upgrade == nil { continue }
                var sim = try Simulation.make(seed: upgrade == nil ? UInt64.max : 1)
                if outcome == .success {
                    _ = sim.testing_completeRunSuccess(upgrade: try #require(upgrade))
                } else {
                    if let upgrade {
                        sim.testing_completeEncounter("M-A")
                        sim.testing_armUpgradeSelection()
                        _ = sim.step(command: PlayerCommand(
                            tick: sim.state.tick + 1, moveX: 0, moveY: 0,
                            dodgePressed: false, upgradeChoiceIndex: upgrade.selectionIndex
                        ))
                    }
                    // Cover no Camera destruction, partial blackout and full blackout.
                    let cameras = [0, 1, 7, 8][index]
                    for camera in 0..<cameras {
                        sim.testing_destroyCameraAtIndex(camera)
                        _ = sim.step(command: .neutral(tick: sim.state.tick + 1))
                    }
                    if outcome == .failure {
                        sim.testing_setPlayerIntegrity(0)
                        _ = sim.step(command: .neutral(tick: sim.state.tick + 1))
                    } else {
                        _ = sim.step(command: .neutral(tick: sim.state.tick + 2))
                    }
                }
                #expect(sim.state.outcome == outcome)
                let digestBefore = sim.state.digest()
                let presentation = PresentationReceiptMetadata(
                    tutorialsEnabled: false, hudScale: .extraLarge, handedness: .left,
                    reducedMotion: true, reducedFlash: true, reducedSensory: true
                )
                let receipt = RunReceipt(sim.state, presentation: presentation)
                #expect(receipt.schemaVersion == ContractVersions.runReceipt)
                #expect(receipt.upgrade == upgrade)
                #expect(receipt.finalDigest == sim.state.terminalDigest)
                #expect(receipt.bossPhases == receipt.combatAuthority.bossPhasesReached)
                #expect(receipt.camerasDestroyed == receipt.cameraDestructionSummary.camerasDestroyed)
                #expect(receipt.cameraDestructionSummary.objectiveDestroyed == receipt.camerasDestroyed)
                #expect(receipt.networkBlackout == receipt.cameraDestructionSummary.objectiveComplete)
                #expect(sim.state.digest() == digestBefore)
                // The existing golden test retains all three exact expected digests.
                let standard = RunReceipt(sim.state)
                #expect(receipt.finalDigest == standard.finalDigest)
                let archiveDirectory = directory.appendingPathComponent("archive-\(produced)")
                let archive = ReceiptArchive(directory: archiveDirectory)
                let entry = try archive.store(receipt)
                let archivedBytes = try Data(contentsOf: archiveDirectory.appendingPathComponent(entry.filename))
                #expect(String(decoding: archivedBytes, as: UTF8.self) == receipt.canonical().serialize())
                let name = "\(outcome.rawValue)-\(upgrade?.rawValue ?? "none").json"
                try archivedBytes.write(to: directory.appendingPathComponent(name), options: .atomic)
                try FileManager.default.removeItem(at: archiveDirectory)
                produced += 1
            }
        }
        #expect(produced == 11)
    }
}
