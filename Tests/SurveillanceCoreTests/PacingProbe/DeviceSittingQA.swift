import Foundation
import Testing
@testable import SurveillanceCore

/// Headless stand-in for the device sitting's three play styles.
///
/// Opt-in (`SS_DEVICE_SITTING=1`, `scripts/device_sitting_qa.sh`). One daily
/// seed, Ricochet Pulse, four pilots. Medal rows are checked against the
/// run. Opening-line comprehension, phone frame time, and the art rows are
/// not claimed here.
@Suite struct DeviceSittingQA {
    private struct Row {
        var name: String
        var profile: ProbePilot.Profile
        var outcome: RunOutcome
        var ticks: UInt64
        var integrity: Int
        var court: UInt64
        var medals: [String]
        var cameras: Int
        var blackout: Bool
        var quiet: Bool
        var failure: String?
        var damage: [String: Int]
    }

    /// UTC 2026-11-02, the day this probe was measured on runtime `15b1c94`.
    private static let day = DailyRun.Day(year: 2026, month: 11, day: 2)

    private static let rows: [Row] = [
        Row(name: "natural-lower-bound", profile: .firstRun, outcome: .failure,
            ticks: 18018, integrity: 0, court: 15849, medals: [],
            cameras: 8, blackout: true, quiet: false, failure: "playerDeath",
            damage: ["algorithmicModerate": 2, "algorithmicModerateProjectile": 37,
                     "algorithmicModerateSafetyRationale": 36, "autonomousInformant": 3,
                     "cableCarCorrelator": 2, "improperSearchDaemon": 14,
                     "sutroSignalWitchProjectile": 15, "victorianVendorMine": 66]),
        Row(name: "natural-style", profile: .competent, outcome: .success,
            ticks: 18921, integrity: 7, court: 13229, medals: ["BLACKOUT", "SWIFT"],
            cameras: 8, blackout: true, quiet: false, failure: nil,
            damage: ["algorithmicModerate": 8, "algorithmicModerateProjectile": 13,
                     "algorithmicModerateSafetyRationale": 63, "autonomousInformant": 2,
                     "improperSearchDaemon": 30, "sutroSignalWitchProjectile": 15,
                     "victorianVendorMine": 12]),
        Row(name: "sneaky", profile: .stealth, outcome: .success,
            ticks: 15681, integrity: 11, court: 10012, medals: ["GHOST", "SWIFT"],
            cameras: 5, blackout: false, quiet: true, failure: nil,
            damage: ["algorithmicModerate": 3, "algorithmicModerateProjectile": 22,
                     "algorithmicModerateSafetyRationale": 54, "autonomousInformant": 3,
                     "improperSearchDaemon": 45, "sutroSignalWitchProjectile": 20]),
        Row(name: "loud", profile: .loud, outcome: .success,
            ticks: 19479, integrity: 18, court: 13491, medals: ["BLACKOUT", "SWIFT"],
            cameras: 8, blackout: true, quiet: false, failure: nil,
            damage: ["algorithmicModerate": 3, "algorithmicModerateProjectile": 9,
                     "algorithmicModerateSafetyRationale": 45, "autonomousInformant": 10,
                     "improperSearchDaemon": 39, "sutroSignalWitchProjectile": 45,
                     "victorianVendorMine": 6]),
    ]

    @Test(.enabled(if: ProcessInfo.processInfo.environment["SS_DEVICE_SITTING"] == "1"))
    func pinnedDailySeed() throws {
        let daily = try DailyRun(day: Self.day)
        #expect(daily.seed == 9_972_847_794_717_746_389)
        #expect(daily.salt == 0)
        print("day \(Self.day.label) seed \(daily.seed) upgrade ricochetPulse")
        print("comprehension NOT SEEN; art rows NOT SEEN; phone interruptions NOT SEEN")
        for row in Self.rows {
            let result = try PacingProbe.run(
                seed: daily.seed, upgrade: .ricochetPulse, profile: row.profile)
            let court = result.milestones["bossActivated"]
            let clock = Self.clock(result.ticks)
            print("\(row.name) | \(result.outcome.rawValue) | \(clock) | integrity \(result.playerIntegrity) | medals \(result.medals)")
            #expect(result.outcome == row.outcome, "\(row.name) outcome")
            #expect(result.ticks == row.ticks, "\(row.name) ticks")
            #expect(result.playerIntegrity == row.integrity, "\(row.name) integrity")
            #expect(court == row.court, "\(row.name) court")
            #expect(result.medals == row.medals, "\(row.name) medals")
            #expect(result.camerasDestroyed == row.cameras, "\(row.name) cameras")
            #expect(result.networkBlackout == row.blackout, "\(row.name) blackout")
            #expect(result.quietApproach == row.quiet, "\(row.name) quiet")
            #expect(result.stalledOn == nil, "\(row.name) stalled")
            #expect(result.failureReason == row.failure, "\(row.name) failure")
            #expect(result.damageBySource == row.damage, "\(row.name) damage")
            #expect(result.medals.contains("SWIFT") == (result.outcome == .success && result.ticks < Medal.swiftTicks))
            #expect(result.medals.contains("SURGICAL") == (result.outcome == .success && result.playerIntegrity * 2 >= 150))
            #expect(result.medals.contains("BLACKOUT") == (result.outcome == .success && result.networkBlackout))
            #expect(result.medals.contains("GHOST") == (result.outcome == .success && result.quietApproach))
        }
    }

    private static func clock(_ ticks: UInt64) -> String {
        let seconds = Int(ticks / 60)
        return String(format: "%d:%02d", seconds / 60, seconds % 60)
    }
}
