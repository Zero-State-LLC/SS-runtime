import Foundation
import Testing
@testable import SurveillanceCore

/// Contract loading rejects `true` where an integer is required and `1` where
/// a boolean is required. That depends on telling the two apart after
/// `JSONSerialization`, on every platform the core builds for.
@Suite struct JSONScalarTests {
    private func decode(_ json: String) throws -> [String: Any] {
        try #require(JSONSerialization.jsonObject(with: Data(json.utf8)) as? [String: Any])
    }

    @Test func booleansAreBooleans() throws {
        let object = try decode(#"{"t": true, "f": false}"#)
        #expect(JSONScalar.isBool(object["t"]))
        #expect(JSONScalar.isBool(object["f"]))
    }

    @Test func numbersAreNotBooleans() throws {
        let object = try decode(#"{"zero": 0, "one": 1, "big": 150, "fraction": 0.5}"#)
        for key in ["zero", "one", "big", "fraction"] {
            #expect(!JSONScalar.isBool(object[key]), "\(key)")
        }
    }

    @Test func nonNumbersAreNotBooleans() throws {
        let object = try decode(#"{"s": "true", "n": null}"#)
        #expect(!JSONScalar.isBool(object["s"]))
        #expect(!JSONScalar.isBool(object["n"]))
        #expect(!JSONScalar.isBool(nil))
    }
}
