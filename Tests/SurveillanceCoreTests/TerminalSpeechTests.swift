import Testing
@testable import SurveillanceCore

/// `acceptance.md` F-007, `hud-tutorial.md` (sentence case for VoiceOver): what
/// VoiceOver reads for the results surface.
@Suite struct TerminalSpeechTests {
    private func state(_ outcome: RunOutcome, tick: UInt64) throws -> WorldState {
        var state = try Simulation.make(seed: 1).state
        state.outcome = outcome
        state.clock = SimulationClock(tick: tick)
        return state
    }

    @Test func aSuccessReadsEveryRowInSentenceCase() throws {
        let card = RunCard(
            state: try state(.success, tick: 18_720),
            dateLabel: "2026-10-30",
            bestTicks: 18_000,
            storesBest: false,
            medals: [.ghost, .swift],
            newMedals: [.swift]
        )
        #expect(TerminalSpeech.summary(title: "RUN COMPLETE", card: card) == [
            "Run complete",
            "Date 2026-10-30",
            "Time 5 minutes 12 seconds",
            "Cameras 0 of 8",
            "Peak detection hidden",
            "Ghost 12 seconds behind your best",
            "Medals: Ghost; Swift, new",
        ].joined(separator: ". ") + ".")
    }

    @Test func aFailureHasNoGhostOrMedals() throws {
        let card = RunCard(state: try state(.failure, tick: 3_600), dateLabel: nil, bestTicks: 100)
        #expect(TerminalSpeech.summary(title: "PLAYER DOWN", card: card)
            == "Player down. Time 1 minute. Cameras 0 of 8. Peak detection hidden.")
    }

    @Test func aRehearsalReadsItsCourtTime() {
        let card = RunCard(rehearsalCourtTicks: 3_660)
        #expect(TerminalSpeech.summary(title: "REHEARSAL DOWN", card: card)
            == "Rehearsal down. Rehearsal 1 minute 1 second.")
    }

    @Test func withoutACardOnlyTheTitleIsRead() {
        #expect(TerminalSpeech.summary(title: "RUN INVALID", card: nil) == "Run invalid.")
    }

    @Test func blackoutAndGhostGapsAreSpoken() {
        let card = RunCard(rehearsalCourtTicks: 0)
        #expect(TerminalSpeech.spoken(.init(label: "CAMERAS", value: "8/8 NETWORK BLACKOUT"), card: card)
            == "Cameras 8 of 8, network blackout")
        #expect(TerminalSpeech.ghost("NEW BEST") == "new best")
        #expect(TerminalSpeech.ghost("-0:05") == "5 seconds ahead of your best")
        #expect(TerminalSpeech.ghost("+0:00") == "level with your best")
        #expect(TerminalSpeech.duration("12:01") == "12 minutes 1 second")
    }

    @Test func controlsHaveSpokenNames() {
        #expect(TerminalSpeech.sentence(HUDLayout.rehearseControlCopy) == "Rehearse court")
        #expect(TerminalSpeech.rehearse == "Rehearse Court", "the Court is a proper name")
    }
}

extension TerminalSpeechTests {
    /// The reflowed card reads its header and its rows separately; together
    /// they are the drawn panel's summary.
    @Test func theSummaryIsTheTitleThenTheRows() {
        let card = RunCard(rehearsalCourtTicks: 3_660)
        #expect(TerminalSpeech.rows(card) == "Rehearsal 1 minute 1 second.")
        #expect(TerminalSpeech.summary(title: "REHEARSAL DOWN", card: card)
            == "Rehearsal down. " + TerminalSpeech.rows(card))
    }
}
