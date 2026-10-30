import Testing
@testable import SurveillanceCore

/// D-112, run-shell.md § 11 (RS-041, RS-042): Share as an incident report.
@Suite struct IncidentReportShareTests {
    private func state(_ outcome: RunOutcome) throws -> WorldState {
        var state = try Simulation.make(seed: 1).state
        state.outcome = outcome
        return state
    }

    @Test func rs041HeaderAndOutcome() throws {
        let cases: [(RunOutcome, String)] = [
            (.success, "OUTCOME: SUBJECT EXTRACTED"),
            (.failure, "OUTCOME: SUBJECT DETAINED"),
            (.invalid, "OUTCOME: REPORT VOID"),
        ]
        for (outcome, line) in cases {
            let card = RunCard(state: try state(outcome), dateLabel: "2026-10-30", bestTicks: nil)
            let lines = card.shareText.split(separator: "\n").map(String.init)
            #expect(lines[0] == RunCard.gameName)
            #expect(lines[1] == "INCIDENT REPORT · DATE 2026-10-30")
            #expect(lines[2] == line)
        }
    }

    @Test func withoutADateTheHeaderStandsAlone() throws {
        let card = RunCard(state: try state(.failure), dateLabel: nil, bestTicks: nil)
        #expect(card.shareText.split(separator: "\n").map(String.init)[1] == "INCIDENT REPORT")
    }

    @Test func rs042RowsReadAsObservationAndTampering() throws {
        let card = RunCard(state: try state(.success), dateLabel: "2026-10-30", bestTicks: nil, medals: [.swift], newMedals: [])
        let lines = card.shareText.split(separator: "\n").map(String.init)
        #expect(lines.contains { $0.hasPrefix("TIME UNDER OBSERVATION ") })
        #expect(lines.contains { $0.hasPrefix("CAMERAS TAMPERED WITH ") })
        #expect(lines.contains { $0.hasPrefix("PEAK DETECTION ") })
        #expect(lines.last == "MEDALS SWIFT")
        #expect(!lines.contains { $0.hasPrefix("DATE ") }, "the date is in the header, not repeated")
    }

    /// The on-screen card keeps its own labels.
    @Test func theCardIsUnchanged() throws {
        let card = RunCard(state: try state(.success), dateLabel: "2026-10-30", bestTicks: nil)
        #expect(card.rows.map(\.label).prefix(4) == ["DATE", "TIME", "CAMERAS", "PEAK DETECTION"])
    }
}
