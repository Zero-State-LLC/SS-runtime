import Testing
@testable import SurveillanceCore

/// `run-shell.md` § 14 (D-107): the Rehearse Court control, its copy, and the
/// rehearsal card. The session and scene behaviour is covered in AppTests.
@Suite struct CourtRehearsalPresentationTests {
    static let sizes = TerminalSurfaceGeometryTests.sizes

    @Test func rehearseIsInsideThePanelAndMeetsTheTouchTarget() {
        for (w, h) in Self.sizes {
            let panel = HUDLayout.terminalPanel(safeWidth: w, safeHeight: h)
            let rehearse = HUDLayout.terminalRehearse(safeWidth: w, safeHeight: h)
            #expect(rehearse.width >= HUDLayout.minimumTouchTargetPoints)
            #expect(rehearse.height >= HUDLayout.minimumTouchTargetPoints)
            #expect(rehearse.x >= panel.x && rehearse.y >= panel.y)
            #expect(rehearse.x + rehearse.width <= panel.x + panel.width)
            #expect(rehearse.y + rehearse.height <= panel.y + panel.height)
        }
    }

    /// Rehearse, Restart and Share sit on one row and never overlap, so a tap
    /// reaches exactly one of them; Rehearse mirrors Share on the left.
    @Test func theThreeControlsDoNotOverlap() {
        for (w, h) in Self.sizes {
            let restart = HUDLayout.terminalRestart(safeWidth: w, safeHeight: h)
            let share = HUDLayout.terminalShare(safeWidth: w, safeHeight: h)
            let rehearse = HUDLayout.terminalRehearse(safeWidth: w, safeHeight: h)
            #expect(rehearse.y == restart.y)
            #expect(rehearse.x + rehearse.width <= restart.x)
            #expect(rehearse.x + rehearse.width <= share.x)
            #expect(rehearse.width == share.width)
        }
    }

    @Test func rehearsalCopy() {
        #expect(HUDLayout.terminalRehearsalCopy(for: .success) == "REHEARSAL COMPLETE")
        #expect(HUDLayout.terminalRehearsalCopy(for: .failure) == "REHEARSAL DOWN")
        #expect(HUDLayout.terminalRehearsalCopy(for: .playing) == nil)
        #expect(HUDLayout.terminalRehearsalCopy(for: .upgradeSelectionPending) == nil)
        #expect(HUDLayout.rehearseControlCopy == "REHEARSE COURT")
    }

    /// § 14.3: one `REHEARSAL` row with the Court time; no medals.
    @Test func rehearsalCardHasOneRowAndNoMedals() {
        let card = RunCard(rehearsalCourtTicks: 54 * 60 + 30)
        #expect(card.isRehearsal)
        #expect(card.rows == [RunCard.Row(label: "REHEARSAL", value: "0:54")])
        #expect(card.medals.isEmpty)
        #expect(card.newMedals.isEmpty)
    }

    @Test func aRunCardIsNotARehearsal() throws {
        let sim = try Simulation.make(seed: 1)
        #expect(!RunCard(state: sim.state, dateLabel: nil, bestTicks: nil).isRehearsal)
    }
}
