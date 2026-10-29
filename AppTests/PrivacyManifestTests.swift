import Foundation
import Testing

/// App Store submission requires a privacy manifest that declares every
/// required-reason API the app uses. This checks the manifest ships in the app
/// bundle and still declares no tracking and no collected data.
@Suite struct PrivacyManifestTests {
    @Test func manifestShipsAndDeclaresTheUsedAPIs() throws {
        let url = try #require(Bundle.main.url(forResource: "PrivacyInfo", withExtension: "xcprivacy"))
        let plist = try #require(
            PropertyListSerialization.propertyList(from: Data(contentsOf: url), format: nil) as? [String: Any]
        )
        #expect(plist["NSPrivacyTracking"] as? Bool == false)
        #expect((plist["NSPrivacyCollectedDataTypes"] as? [Any])?.isEmpty == true)
        let declared = (plist["NSPrivacyAccessedAPITypes"] as? [[String: Any]] ?? [])
            .compactMap { $0["NSPrivacyAccessedAPIType"] as? String }
        #expect(declared.contains("NSPrivacyAccessedAPICategoryUserDefaults"))
        #expect(declared.contains("NSPrivacyAccessedAPICategoryFileTimestamp"))
    }
}
