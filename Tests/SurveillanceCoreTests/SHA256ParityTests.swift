import Foundation
import Testing
@testable import SurveillanceCore

struct SHA256ParityTests {
    @Test func publishedVectorsMatchBothImplementations() {
        let vectors: [(String, String)] = [
            ("", SHA256.emptyDigest),
            ("abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
            ("abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq",
             "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"),
            (String(repeating: "a", count: 1_000_000),
             "cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0")
        ]
        for (input, expected) in vectors {
            let bytes = Array(input.utf8)
            #expect(SHA256.hex(bytes) == expected)
            #expect(legacyHex(bytes) == expected)
            #expect(SHA256.hash(bytes) == SHA256.portableHash(bytes))
        }
    }

    @Test func paddingBoundariesAndBinaryInputsPreserveExactBytes() {
        // Includes every short padding offset, every possible byte, and multi-block payloads.
        let sizes = Array(0...257) + [511, 512, 513, 1023, 1024, 4095, 4096, 65536]
        for count in sizes {
            let bytes = (0..<count).map { UInt8(truncatingIfNeeded: $0 &* 73 &+ count) }
            let digest = SHA256.hash(bytes)
            #expect(digest.count == 32)
            #expect(digest == SHA256.portableHash(bytes))
            #expect(SHA256.hex(bytes) == legacyHex(bytes))
        }
    }

    @Test func stringOverloadPreservesUTF8AndLowercaseHex() {
        for input in ["\u{0000}", "café", "cafe\u{0301}", "👁️ 城市", "\n\r\t"] {
            let bytes = Array(input.utf8)
            let actual = SHA256.hex(input)
            #expect(actual == legacyHex(bytes))
            #expect(actual.utf8.count == 64)
            #expect(actual.utf8.allSatisfy { (48...57).contains($0) || (97...102).contains($0) })
        }
        #expect(SHA256.hex("café") != SHA256.hex("cafe\u{0301}"))
    }

    private func legacyHex(_ data: [UInt8]) -> String {
        SHA256.portableHash(data).map { String(format: "%02x", $0) }.joined()
    }
}
