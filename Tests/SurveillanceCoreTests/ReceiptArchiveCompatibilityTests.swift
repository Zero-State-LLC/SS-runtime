import Foundation
import Testing
@testable import SurveillanceCore

@Suite(.serialized)
struct ReceiptArchiveCompatibilityTests {
    private func temporaryDirectory() -> URL {
        FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString)
    }

    @Test func mixedReadsPreserveExactBytesWithoutCertifyingStructure() throws {
        let directory = temporaryDirectory()
        defer { try? FileManager.default.removeItem(at: directory) }
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
        // Deliberately incomplete and schema-invalid legacy evidence remains recognizable.
        let samples: [(String, ReceiptArchiveFormatStatus)] = [
            (" {\n\"schemaVersion\":\"run-receipt-001\",\"upgrade\":\"signalJammer\"}\n", .historicalUnverified),
            ("{\"schemaVersion\":\"run-receipt-002\",\"player\":false}", .currentUnverified),
            ("{\"schemaVersion\":\"future\"}", .unrecognized),
            ("{\"schemaVersion\":\"run-receipt-001\",", .unrecognized),
            ("{}", .unrecognized),
            ("{\"schemaVersion\":42}", .unrecognized),
            ("{\"schemaVersion\":null}", .unrecognized),
            ("[\"run-receipt-002\"]", .unrecognized),
            ("\"run-receipt-002\"", .unrecognized)
        ]
        for (index, sample) in samples.enumerated() {
            try Data(sample.0.utf8).write(to: directory.appendingPathComponent("sample-\(index).json"))
        }
        let entries = try ReceiptArchive(directory: directory).listEntries()
        #expect(entries.count == samples.count)
        for (index, sample) in samples.enumerated() {
            let entry = try #require(entries.first { $0.filename == "sample-\(index).json" })
            #expect(entry.formatStatus == sample.1)
            #expect(Data(entry.serialized.utf8) == Data(sample.0.utf8))
            #expect(try Data(contentsOf: directory.appendingPathComponent(entry.filename)) == Data(sample.0.utf8))
        }
    }

    @Test func observedNonconformingV1ReceiptRemainsHistoricalWithoutRewrite() throws {
        let root = URL(fileURLWithPath: #filePath)
            .deletingLastPathComponent().deletingLastPathComponent().deletingLastPathComponent()
        let original = try Data(contentsOf: root.appendingPathComponent("scripts/fixtures/receipt-v1-observed.json"))
        let directory = temporaryDirectory()
        defer { try? FileManager.default.removeItem(at: directory) }
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
        let historicalURL = directory.appendingPathComponent("observed-v1.json")
        try original.write(to: historicalURL)
        let archive = ReceiptArchive(directory: directory)
        let receipt = RunReceipt(try Simulation.make(seed: 1).state)
        _ = try archive.store(receipt)
        let entries = try archive.listEntries()
        let historical = try #require(entries.first { $0.filename == "observed-v1.json" })
        #expect(historical.formatStatus == .historicalUnverified)
        #expect(Data(historical.serialized.utf8) == original)
        #expect(try Data(contentsOf: historicalURL) == original)
        #expect(entries.count == 2)
    }

    @Test func unsupportedWritesHaveNoDirectoryOrRetentionSideEffects() throws {
        let root = temporaryDirectory()
        defer { try? FileManager.default.removeItem(at: root) }
        let directory = root.appendingPathComponent("archive")
        let archive = ReceiptArchive(directory: directory)
        var receipt = RunReceipt(try Simulation.make(seed: 1).state)
        for identity in ["run-receipt-001", "future", ""] {
            receipt.schemaVersion = identity
            #expect(throws: ReceiptArchiveError.invalidReceipt) { try archive.store(receipt) }
            #expect(!FileManager.default.fileExists(atPath: directory.path))
        }
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
        for index in 0..<51 {
            try Data("legacy-\(index)".utf8).write(to: directory.appendingPathComponent("old-\(index).json"))
        }
        for identity in ["run-receipt-001", "future", ""] {
            receipt.schemaVersion = identity
            #expect(throws: ReceiptArchiveError.invalidReceipt) { try archive.store(receipt) }
            #expect(try FileManager.default.contentsOfDirectory(atPath: directory.path).count == 51)
            for index in 0..<51 {
                #expect(try Data(contentsOf: directory.appendingPathComponent("old-\(index).json")) == Data("legacy-\(index)".utf8))
            }
        }
    }

    @Test func currentWritesRetainNewestFiftyAcrossMixedEntries() throws {
        let directory = temporaryDirectory()
        defer { try? FileManager.default.removeItem(at: directory) }
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
        let identities = ["run-receipt-001", "run-receipt-002", "future"]
        for index in 0..<50 {
            let text = "{\"schemaVersion\":\"\(identities[index % identities.count])\"}"
            try Data(text.utf8).write(to: directory.appendingPathComponent(String(format: "old-%02d.json", index)))
        }
        let archive = ReceiptArchive(directory: directory)
        let before = try archive.listEntries()
        let oldest = try #require(before.first)
        let receipt = RunReceipt(try Simulation.make(seed: 1).state)
        #expect(receipt.schemaVersion == "run-receipt-002")
        let stored = try archive.store(receipt)
        #expect(stored.formatStatus == .currentUnverified)
        #expect(stored.serialized == receipt.canonical().serialize())
        let after = try archive.listEntries()
        #expect(after.count == 50)
        #expect(!after.contains { $0.filename == oldest.filename })
        #expect(after.contains(stored))
        for entry in before.dropFirst() {
            #expect(after.contains(entry))
            #expect(try Data(contentsOf: directory.appendingPathComponent(entry.filename)) == Data(entry.serialized.utf8))
        }
        #expect(try FileManager.default.contentsOfDirectory(atPath: directory.path).count == 50)
    }
}
