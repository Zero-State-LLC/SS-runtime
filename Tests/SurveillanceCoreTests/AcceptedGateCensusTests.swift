import Foundation
import Testing
@testable import SurveillanceCore

/// T902/T908, #257. Census from acceptance.md at the pinned b1ed874 specification.
struct AcceptedGateCensusTests {
    private let omittedByOldRegistry = ["A-013A", "D-022", "D-023", "D-024", "E-021"]

    private var acceptedIDs: [String] {
        let counts = [("A", 22), ("B", 17), ("C", 11), ("D", 24),
                      ("E", 21), ("F", 17), ("G", 7)]
        return counts.flatMap { family, count in
            (1...count).map { String(format: "%@-%03d", family, $0) }
        } + ["A-013A"]
    }

    private func inputs(omitting id: String? = nil, failing failed: String? = nil) -> ExpansionGateInputs {
        ExpansionGateInputs(
            gateResults: acceptedIDs.filter { $0 != id }.map {
                GatePassRecord(gateId: $0, passed: $0 != failed, source: .manualReview)
            },
            d013Settled: true, d021Settled: true
        )
    }

    @Test func registryExactlyMatchesAcceptedCensusWithoutDuplicates() {
        #expect(Set(GateRegistry.allGateIds) == Set(acceptedIDs))
        #expect(GateRegistry.allGateIds.count == acceptedIDs.count)
        #expect(acceptedIDs.count == 120)
        #expect(Set(ExpansionGateEvaluator.requiredGateFamilies.joined()) == Set(acceptedIDs))
    }

    @Test func eachPreviouslyOmittedGateBlocksExpansionWhenMissing() {
        for id in omittedByOldRegistry {
            #expect(ExpansionGateEvaluator.evaluate(inputs(omitting: id)) == .notComputable,
                    "Missing accepted gate \(id) must block expansion")
        }
    }

    @Test func eachPreviouslyOmittedGateFailsExpansionWhenFailed() {
        for id in omittedByOldRegistry {
            #expect(ExpansionGateEvaluator.evaluate(inputs(failing: id)) == .failed,
                    "Failed accepted gate \(id) must fail expansion")
        }
    }

    @Test func completeSyntheticCensusIsOnlyAnEvaluatorUnitTest() {
        #expect(ExpansionGateEvaluator.evaluate(inputs()) == .passed)
        #expect(ExpansionGateEvaluator.evaluate(.init()) == .notComputable)
        for id in omittedByOldRegistry {
            #expect(!GateRegistry.automatedGateIds.contains(id))
            #expect(GateRegistry.unmappedGateIds().contains(id))
        }
    }
}
