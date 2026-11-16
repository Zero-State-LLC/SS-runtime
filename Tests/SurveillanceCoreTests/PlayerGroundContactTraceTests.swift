import Foundation
import XCTest
@testable import SurveillanceCore

/// BP-008 slice2: real Simulation.step traces. Setup hooks only position isolated
/// fixtures. No movement, collision, dodge or normalization is reimplemented.
final class PlayerGroundContactTraceTests: XCTestCase {
    struct Row: Codable, Equatable {
        let sample: Int
        let tick: UInt64
        let commandX: Int16
        let commandY: Int16
        let dodgePressed: Bool
        let paused: Bool
        let xRaw: Int64
        let yRaw: Int64
        let dxRaw: Int64
        let dyRaw: Int64
        let dodgeRemaining: Int
    }
    struct Trace: Codable {
        let name: String
        let setup: String
        let rows: [Row]
        let finalDigest: String
    }
    struct Packet: Codable {
        let evidenceKind: String
        let traces: [Trace]
    }

    func testAuthoritativeMovementMatrix() throws {
        var traces: [Trace] = []
        let cases = ["quarter", "half", "full", "cardinal-quarter", "cardinal-half",
                     "cardinal-full", "collision-stop", "wall-slide", "reversal", "dodge", "pause", "stationary"]
        for name in cases {
            func run() throws -> Trace {
                var simulation = try Simulation.make(seed: 1)
                simulation.testing_setPlayerPosition(VecI(x: 736, y: 654))
                let isolated = name == "collision-stop" || name == "wall-slide"
                if isolated {
                    simulation.testing_setCollisionSolids([
                        AABB(center: VecI(x: 680, y: 654), halfSize: VecI(x: 8, y: 400))
                    ])
                }
                let movementTicks = name.contains("quarter") ? 300 : (name.contains("half") ? 150 : 75)
                var rows: [Row] = []
                for sample in 0...(movementTicks + 15) {
                    let paused = name == "pause" && (31...45).contains(sample)
                    let active = sample > 0 && sample <= movementTicks && name != "stationary"
                    let magnitude: Int16 = name.contains("quarter") ? (name.hasPrefix("cardinal") ? 8192 : 5792)
                        : (name.contains("half") ? (name.hasPrefix("cardinal") ? 16384 : 11585) : 32767)
                    let axis: Int16 = active ? (name == "reversal" && sample > 38 ? magnitude : -magnitude) : 0
                    let y: Int16 = name.hasPrefix("cardinal") || name == "collision-stop" ? 0 : axis
                    let dodge = name == "dodge" && sample == 31
                    let before = simulation.state.player.position
                    if sample > 0 && !paused {
                        _ = simulation.step(command: PlayerCommand(tick: simulation.state.clock.tick + 1,
                            moveX: axis, moveY: y, dodgePressed: dodge))
                    }
                    let after = simulation.state.player.position
                    rows.append(Row(sample: sample, tick: simulation.state.clock.tick,
                        commandX: axis, commandY: y, dodgePressed: dodge, paused: paused,
                        xRaw: after.x.raw, yRaw: after.y.raw,
                        dxRaw: after.x.raw - before.x.raw, dyRaw: after.y.raw - before.y.raw,
                        dodgeRemaining: simulation.state.player.dodgeActiveRemaining))
                }
                return Trace(name: name,
                    setup: isolated ? "seed1, player736/654, test wall680/654 half8/400; existing core collision" : "seed1 bundled arena, player736/654 as existing shared projected harness",
                    rows: rows, finalDigest: simulation.state.digest())
            }
            let first = try run(), replay = try run()
            XCTAssertEqual(first.rows, replay.rows, "Every Q8 position must reproduce")
            XCTAssertEqual(first.finalDigest, replay.finalDigest)
            XCTAssertEqual(first.rows.first?.tick, 0)
            if name == "collision-stop" {
                XCTAssertTrue(first.rows.contains { $0.commandX != 0 && $0.dxRaw == 0 && $0.sample > 1 })
            }
            if name == "wall-slide" {
                XCTAssertTrue(first.rows.contains { $0.commandX != 0 && $0.dxRaw == 0 && $0.dyRaw != 0 })
            }
            if name == "reversal" {
                XCTAssertTrue(first.rows.contains { $0.dxRaw < 0 })
                XCTAssertTrue(first.rows.contains { $0.dxRaw > 0 })
            }
            if name == "dodge" {
                XCTAssertTrue(first.rows.contains { $0.dodgeRemaining > 0 })
            }
            if name == "pause" {
                let held = first.rows.filter(\.paused)
                XCTAssertEqual(held.count, 15)
                XCTAssertEqual(Set(held.map(\.tick)).count, 1)
                XCTAssertTrue(held.allSatisfy { $0.dxRaw == 0 && $0.dyRaw == 0 })
            }
            if name == "stationary" {
                XCTAssertTrue(first.rows.allSatisfy { $0.dxRaw == 0 && $0.dyRaw == 0 })
            }
            traces.append(first)
        }
        if let path = ProcessInfo.processInfo.environment["SS_GROUND_CONTACT_OUTPUT"] {
            let packet = Packet(evidenceKind: "Actual public Simulation.step execution. Fixture setup uses existing test hooks. Pause means withholding step, not native lifecycle evidence.", traces: traces)
            let encoder = JSONEncoder()
            encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
            try encoder.encode(packet).write(to: URL(fileURLWithPath: path), options: .atomic)
        }
        XCTAssertEqual(traces.count, 12)
    }
}
