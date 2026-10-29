import SurveillanceCore
import Testing
@testable import SSRuntime

/// T905/T907: terminal evidence is recorded once per run, at its real end.
@Suite struct RunEndEvidenceTests {
    @Test func theUpgradeGateIsNotARunEnd() {
        #expect(!GameScene.recordsTerminalEvidence(outcome: .upgradeSelectionPending, alreadyStored: false))
        #expect(!GameScene.recordsTerminalEvidence(outcome: .playing, alreadyStored: false))
    }

    @Test func everyTerminalOutcomeIsRecordedOnce() {
        for outcome in [RunOutcome.success, .failure, .invalid] {
            #expect(GameScene.recordsTerminalEvidence(outcome: outcome, alreadyStored: false))
            #expect(!GameScene.recordsTerminalEvidence(outcome: outcome, alreadyStored: true))
        }
    }

    /// The tracker reaches the T905 threshold only if the upgrade gate is not
    /// fed to it as an outcome.
    @Test func threeSuccessfulRunsReachTheThreshold() {
        let tracker = DeviceRunTracker()
        for _ in 0..<3 {
            for outcome in [RunOutcome.playing, .upgradeSelectionPending, .playing, .success]
            where GameScene.recordsTerminalEvidence(outcome: outcome, alreadyStored: false) {
                tracker.noteTerminalOutcome(outcome)
            }
        }
        #expect(tracker.consecutiveCompleteRuns == 3)
    }
}
