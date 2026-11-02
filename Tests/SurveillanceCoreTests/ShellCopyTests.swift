import Testing
@testable import SurveillanceCore

/// `run-shell.md` § 5 (D-120): START, SETTINGS, and RESTART stay the existing labels.
@Suite struct ShellCopyTests {
    @Test func existingLabels() {
        #expect(HUDLayout.startControlCopy == "START")
        #expect(HUDLayout.settingsControlCopy == "SETTINGS")
        #expect(HUDLayout.restartControlCopy == "RESTART")
    }
}
