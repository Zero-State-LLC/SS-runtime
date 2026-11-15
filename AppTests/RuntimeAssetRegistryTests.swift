import Testing
@testable import SSRuntime

struct RuntimeAssetRegistryTests {
    @Test func unknownIDNeverEscapesGate() {
        var diagnostics: [String] = []
        let result = RuntimeAssetRegistry.require("audit_unregistered", diagnose: { diagnostics.append($0) })
        #expect(result == RuntimeAssetRegistry.unavailable)
        #expect(diagnostics.count == 1)
        #expect(diagnostics[0].contains("audit_unregistered"))
    }
    @Test func reachableIDSurvivesGate() {
        var diagnostics: [String] = []
        #expect(RuntimeAssetRegistry.require("hud_integrity_frame", diagnose: { diagnostics.append($0) }) == "hud_integrity_frame")
        #expect(diagnostics.isEmpty)
    }
}
