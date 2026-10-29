import SurveillanceCore
import Testing
@testable import SSRuntime

/// ER-006 / D-059: only a finished run is archived. The upgrade gate is not a
/// run end, and archiving it there used to block the real terminal receipt.
@Suite struct TerminalReceiptTests {
    @Test(arguments: [RunOutcome.playing, .upgradeSelectionPending])
    func anUnfinishedRunIsNotArchived(outcome: RunOutcome) throws {
        var state = try Simulation.make(seed: 1).state
        state.outcome = outcome
        #expect(try ReceiptStore.persistTerminalReceipt(for: state) == nil)
    }
}
