import CryptoKit
import Foundation
import Testing
@testable import SurveillanceCore

/// Hurt, defeat, and extraction ship one PNG per frame index in every direction.
/// The test reads those file bytes. It does not require any other clip to stay distinct.
@Suite struct CopiedDirectionBytesTests {
    private let hurtFrame01 = "a83d382295db881c942d6d2b43185cd67a5aeefa2e397e6ca9599956d06c02d5"

    @Test func hurtDefeatAndExtractionMatchTheSouthFile() throws {
        let clips = [
            ("player_hurt", 3),
            ("player_defeat", 5),
            ("player_extraction", 8),
        ]
        for (clip, count) in clips {
            for index in 1...count {
                let frame = String(format: "%02d", index)
                let southName = "actor_\(clip)_s_\(frame)@1x.png"
                let south = try bytes(southName)
                for direction in ["n", "e", "w"] {
                    let name = "actor_\(clip)_\(direction)_\(frame)@1x.png"
                    #expect(try bytes(name) == south)
                }
            }
        }
        for direction in ["n", "e", "s", "w"] {
            let name = "actor_player_hurt_\(direction)_01@1x.png"
            #expect(sha256(try bytes(name)) == hurtFrame01)
        }
    }

    private func bytes(_ name: String) throws -> Data {
        let url = try #require(RuntimeAssetBundle.url(forFile: name))
        return try Data(contentsOf: url)
    }

    private func sha256(_ data: Data) -> String {
        SHA256.hash(data: data).map { String(format: "%02x", $0) }.joined()
    }
}
