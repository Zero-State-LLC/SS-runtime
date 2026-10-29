import Foundation
import Testing
@testable import SurveillanceCore

/// SS-runtime #148: the `upgrades` block of the combat content contract is
/// validated against the values the simulation compiles in. Changing either
/// side alone fails closed instead of shipping a contract with no effect.
@Suite struct UpgradesContractParityTests {
    private static func bundledRoot() throws -> [String: Any] {
        let data = BundledResource.data(name: "combat-content-006", subdirectory: "contracts")
        return try #require(JSONSerialization.jsonObject(with: data) as? [String: Any])
    }

    private static func decodeError(_ mutate: (inout [String: Any]) -> Void) throws -> CombatContentError? {
        var root = try bundledRoot()
        mutate(&root)
        let data = try JSONSerialization.data(withJSONObject: root)
        do {
            _ = try CombatContent.decode(data)
            return nil
        } catch let error as CombatContentError {
            return error
        }
    }

    private static func setting(_ upgrade: String, _ field: String, to value: Any) -> (inout [String: Any]) -> Void {
        { root in
            var upgrades = root["upgrades"] as! [String: Any]
            var block = upgrades[upgrade] as! [String: Any]
            block[field] = value
            upgrades[upgrade] = block
            root["upgrades"] = upgrades
        }
    }

    @Test func bundledContractMatchesTheSimulation() throws {
        #expect(try Self.decodeError { _ in } == nil)
    }

    @Test(arguments: [
        ("ricochetPulse", "range", 120),
        ("ricochetPulse", "enemyDamage", 7),
        ("ricochetPulse", "cameraDamage", 2),
        ("ricochetPulse", "continuations", 2),
        ("ghostStep", "dodgeSpeed", 600),
        ("ghostStep", "dodgeTicks", 14),
        ("ghostStep", "cooldown", 60),
        ("ghostStep", "postDodgeCameraImmunity", 30),
        ("signalJammer", "contactReduction", 2),
        ("signalJammer", "minimumContact", 0),
        ("signalJammer", "index", 2),
    ])
    func aChangedValueFailsClosed(upgrade: String, field: String, value: Int) throws {
        let error = try Self.decodeError(Self.setting(upgrade, field, to: value))
        #expect(error == .simulationMismatch("upgrades.\(upgrade).\(field)"))
    }

    @Test func aChangedPulseRatioFailsClosed() throws {
        let error = try Self.decodeError(Self.setting("signalJammer", "pulseRatio", to: [50, 100]))
        #expect(error == .simulationMismatch("upgrades.signalJammer.pulseRatio[0]"))
    }

    @Test func malformedValuesAreTypeErrors() throws {
        #expect(try Self.decodeError(Self.setting("ricochetPulse", "range", to: true))
            == .wrongType("upgrades.ricochetPulse.range"))
        #expect(try Self.decodeError(Self.setting("signalJammer", "pulseRatio", to: [75]))
            == .wrongType("upgrades.signalJammer.pulseRatio"))
        #expect(try Self.decodeError(Self.setting("ghostStep", "speedBoost", to: 1))
            == .wrongType("upgrades.ghostStep.speedBoost"))
    }

    @Test func unknownOrMissingUpgradesFailClosed() throws {
        #expect(try Self.decodeError { root in
            var upgrades = root["upgrades"] as! [String: Any]
            upgrades["phantomUpgrade"] = [:] as [String: Any]
            root["upgrades"] = upgrades
        } == .wrongType("upgrades.phantomUpgrade"))
        #expect(try Self.decodeError { root in root.removeValue(forKey: "upgrades") } == .missingField("upgrades"))
        #expect(try Self.decodeError { root in
            var upgrades = root["upgrades"] as! [String: Any]
            upgrades.removeValue(forKey: "ghostStep")
            root["upgrades"] = upgrades
        } == .missingField("upgrades.ghostStep"))
    }
}
