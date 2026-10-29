import Foundation
import SurveillanceCore

/// ER-006: persists terminal run receipts to Application Support.
enum ReceiptStore {
    private static let subdirectory = "RunReceipts"

    static func directoryURL() throws -> URL {
        let base = try FileManager.default.url(
            for: .applicationSupportDirectory,
            in: .userDomainMask,
            appropriateFor: nil,
            create: true
        )
        return base.appendingPathComponent(subdirectory, isDirectory: true)
    }

    static func archive() throws -> ReceiptArchive {
        ReceiptArchive(directory: try directoryURL())
    }

    /// Archives the receipt of a finished run. `upgradeSelectionPending` is not
    /// finished (`RunOutcome.isTerminal`): treating "not playing" as over
    /// archived the upgrade gate and then never the run's real end.
    @discardableResult
    static func persistTerminalReceipt(for state: WorldState) throws -> ReceiptArchiveEntry? {
        guard state.outcome.isTerminal else { return nil }
        let receipt = RunReceipt(state)
        return try archive().store(receipt)
    }
}
