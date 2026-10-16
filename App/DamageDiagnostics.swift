import Foundation
import SurveillanceCore

/// Opt-in, local QA evidence. Never read by the simulation.
struct DamageDiagnostic: Codable, Equatable {
    struct Point: Codable, Equatable {
        let xQ8: Int64
        let yQ8: Int64
        init(_ p: VecQ8) { xQ8 = p.x.raw; yQ8 = p.y.raw }
    }
    struct Source: Codable, Equatable {
        let id: UInt64
        let kind: String
        let position: Point
        let radius: Int
        let state: String
    }
    let tick: UInt64
    let sourceID: UInt64?
    let amount: Int
    let playerBefore: Point
    let playerAfter: Point
    let playerRadius: Int
    var viewCenterBefore: Point? = nil
    let candidates: [Source]
    let classification: String
    let warningsBefore: [String]
    var authoritativeEventJSON: String? = nil

    static func capture(before: WorldState, after: WorldState, events: [AuthoritativeEvent]) -> [Self] {
        events.filter { $0.type == .playerDamaged }.map { event in
            let id = event.secondaryEntityId
            var sources: [Source] = []
            if let projectile = after.projectiles.first(where: { $0.id == id })
                ?? before.projectiles.first(where: { $0.id == id }) {
                sources.append(Source(id: projectile.id.raw, kind: "projectile:\(projectile.kind)",
                                      position: Point(projectile.position), radius: projectile.radius,
                                      state: "previous=\(projectile.previous.x.raw),\(projectile.previous.y.raw); velocity=\(projectile.velocity.x.raw),\(projectile.velocity.y.raw); alive=\(projectile.alive)"))
            }
            if let enemy = after.enemies.first(where: { $0.id == id })
                ?? before.enemies.first(where: { $0.id == id }) {
                sources.append(Source(id: enemy.id.raw, kind: "enemy:\(enemy.archetype.rawValue)",
                                      position: Point(enemy.position), radius: enemy.radius,
                                      state: "before=\(String(describing: before.enemies.first { $0.id == id }?.state)); after=\(enemy.state)"))
            }
            // Older evidence named only the owner. D-103 names the mine itself.
            for mine in before.mines where (mine.id == id || mine.ownerId == id) && !after.mines.contains(where: { $0.id == mine.id }) {
                sources.append(Source(id: mine.id.raw, kind: "removed-mine", position: Point(mine.position),
                                      radius: mine.radius, state: "armRemaining=\(mine.armRemaining); lifeRemaining=\(mine.lifeRemaining)"))
            }
            let amount: Int
            if case .integer(let value) = event.payload["amount"] { amount = Int(value) } else { amount = 0 }
            return Self(tick: event.tick, sourceID: id?.raw, amount: amount,
                        playerBefore: Point(before.player.position), playerAfter: Point(after.player.position),
                        playerRadius: PlayerBody.radiusUnits, candidates: sources,
                        classification: event.payload["damageKind"] != nil ? "authoritative-event-evidence" : (sources.isEmpty ? "unresolved-source" : "source-candidates-not-cause-proof"),
                        warningsBefore: PresentationSnapshot(before).telegraphs.map {
                            "owner=\($0.ownerId.raw); kind=\($0.kind); origin=\($0.x),\($0.y); heading=\($0.headingMilli); range=\($0.rangeUnits); halfAngle=\($0.halfAngleMilli); width=\($0.widthUnits); remaining=\($0.remainingTicks)"
                        }, authoritativeEventJSON: event.payload["damageKind"] != nil ? event.canonical().serialize() : nil)
        }
    }
}

struct DamageDiagnosticRun: Encodable {
    struct Command: Codable {
        let tick: UInt64
        let moveX: Int16
        let moveY: Int16
        let dodge: Bool
        let upgrade: UInt8?
        init(_ value: PlayerCommand) {
            tick = value.tick; moveX = value.moveX; moveY = value.moveY
            dodge = value.dodgePressed; upgrade = value.upgradeChoiceIndex
        }
    }
    let schema = "ss-damage-qa-001"
    let seed: UInt64
    let device: String
    let droppedRecords: Int
    let damage: [DamageDiagnostic]
    let commands: [Command]
}
