import Foundation

/// D-119. Presentation only. Reads the world and predicts the existing
/// damage-taken scale on copies. It writes nothing back, emits no event,
/// and is not part of the gameplay digest.
public enum LethalWarning {
    public static let card = "LETHAL THREAT"
    public static let contactHorizonTicks = 60

    public static func isOn(_ state: WorldState) -> Bool {
        discreteWouldExhaust(state) || contactWouldExhaust(state)
    }

    /// Sixty ticks of one constant contact rate, through the accumulator and
    /// the damage-taken scale, on copies. `dps` is already the three-highest
    /// cap. Integrity that starts at or below zero is not a warning.
    public static func contactWouldExhaust(
        integrity: Int,
        remainderHundredths: Int,
        accumulator: Int,
        dps: Int,
        percent: Int,
        ticks: Int = contactHorizonTicks
    ) -> Bool {
        var integrity = integrity
        var remainder = remainderHundredths
        var accumulator = accumulator
        guard integrity > 0, dps > 0, ticks > 0 else { return false }
        for _ in 0..<ticks {
            accumulator += dps
            let points = accumulator / 60
            accumulator %= 60
            guard points > 0 else { continue }
            let removed = Simulation.scaleDamageTaken(points, percent: percent, remainder: &remainder)
            integrity -= removed
            if integrity <= 0 { return true }
        }
        return false
    }

    private static func contactWouldExhaust(_ state: WorldState) -> Bool {
        var threats: [(dps: Int, id: EntityID)] = []
        for enemy in state.enemies where enemy.alive && !enemy.isUnaware {
            let combined = Int64(PlayerBody.radiusUnits + enemy.radius) * Q8.scale
            if state.player.position.distanceSquared(to: enemy.position) <= combined * combined {
                threats.append((enemy.contactDps, enemy.id))
            }
        }
        threats.sort {
            if $0.dps != $1.dps { return $0.dps > $1.dps }
            return $0.id < $1.id
        }
        let dps = threats.prefix(3).reduce(0) { $0 + $1.dps }
        return contactWouldExhaust(
            integrity: state.player.integrity,
            remainderHundredths: state.player.damageRemainderHundredths,
            accumulator: state.player.contactAccumulator,
            dps: dps,
            percent: state.content.player.damageTakenPercent
        )
    }

    private static func discreteWouldExhaust(_ state: WorldState) -> Bool {
        if bossTelegraphWouldExhaust(state) { return true }
        let percent = state.content.player.damageTakenPercent
        for enemy in state.enemies where enemy.alive && !enemy.isUnaware {
            switch enemy.archetype {
            case .improperSearchDaemon where enemy.state == .queryTelegraph:
                let amount = DaemonQuery.damage(
                    playerPosition: state.player.position,
                    markers: enemy.queryMarkers
                )
                if wouldExhaust(amount, state: state, percent: percent) { return true }
            case .sutroSignalWitch where enemy.state == .telegraph && enemy.stateTicks > 0:
                guard let shot = state.content.standardEnemies[.sutroSignalWitch]?.shot else { continue }
                let velocity = Targeting.direct(
                    from: enemy.position,
                    to: state.player.position,
                    speed: Steering.speedQ8(shot.speed)
                )
                if boltContainsPlayer(
                    from: enemy.position,
                    velocity: velocity,
                    radius: shot.radius,
                    lifetime: shot.lifetime,
                    state: state
                ), wouldExhaust(shot.damage, state: state, percent: percent) {
                    return true
                }
            default:
                continue
            }
        }
        return false
    }

    private static func bossTelegraphWouldExhaust(_ state: WorldState) -> Bool {
        guard let runtime = state.bossRuntime,
              runtime.telegraphRemaining > 0,
              let attack = runtime.currentAttack,
              let boss = state.enemies.first(where: { $0.archetype == .algorithmicModerate && $0.alive })
        else { return false }
        let percent = state.content.player.damageTakenPercent
        switch attack {
        case .safetyRationale:
            let heading = Cordic.atan2Milli(
                y: state.player.position.y.raw - boss.position.y.raw,
                x: state.player.position.x.raw - boss.position.x.raw
            )
            let contains = Collision.pointInCone(
                origin: boss.position,
                point: state.player.position,
                headingMilli: heading,
                halfFieldMilli: 35_000,
                rangeUnits: 260
            ) && Collision.lineOfFireClear(
                from: boss.position,
                to: state.player.position,
                solids: state.liveSolids
            )
            return contains && wouldExhaust(18, state: state, percent: percent)
        case .narrowTailoring:
            let heading = Cordic.atan2Milli(
                y: state.player.position.y.raw - boss.position.y.raw,
                x: state.player.position.x.raw - boss.position.x.raw
            )
            var sum = 0
            for offset in [-12_000, 0, 12_000] {
                let velocity = boltVelocity(headingMilli: MilliDeg.normalize(heading + offset), speed: 420)
                if boltContainsPlayer(
                    from: boss.position,
                    velocity: velocity,
                    radius: 7,
                    lifetime: 72,
                    state: state
                ) {
                    sum += 9
                }
            }
            return wouldExhaust(sum, state: state, percent: percent)
        case .temporaryOrder:
            return false
        case .independentReview:
            let toPlayer = Cordic.atan2Milli(
                y: state.player.position.y.raw - boss.position.y.raw,
                x: state.player.position.x.raw - boss.position.x.raw
            )
            var sum = 0
            for lane in BossSystem.independentReviewLanes(toPlayerMilli: toPlayer) {
                let velocity = boltVelocity(headingMilli: lane, speed: 360)
                if boltContainsPlayer(
                    from: boss.position,
                    velocity: velocity,
                    radius: 7,
                    lifetime: 90,
                    state: state
                ) {
                    sum += 8
                }
            }
            return wouldExhaust(sum, state: state, percent: percent)
        }
    }

    /// One attack's summed authored damage, scaled on a fresh remainder copy.
    private static func wouldExhaust(_ amount: Int, state: WorldState, percent: Int) -> Bool {
        guard amount > 0, state.player.integrity > 0 else { return false }
        var remainder = state.player.damageRemainderHundredths
        let removed = Simulation.scaleDamageTaken(amount, percent: percent, remainder: &remainder)
        return removed >= state.player.integrity
    }

    /// The velocity `BossSystem.fire` gives a bolt. Duplicated so the
    /// prediction matches the spawn without firing one.
    private static func boltVelocity(headingMilli: Int, speed: Int) -> VecQ8 {
        let unit = Cordic.headingUnit(milliDegrees: headingMilli)
        let speedQ8 = Steering.speedQ8(speed)
        return VecQ8(
            x: Q8(raw: IntMath.mulDivHalfAway(Int64(unit.x), speedQ8, Int64(Cordic.q15))),
            y: Q8(raw: IntMath.mulDivHalfAway(Int64(unit.y), speedQ8, Int64(Cordic.q15)))
        )
    }

    /// True when the bolt spawned the way `fire` spawns one would hit the
    /// Player before a solid consumes it. The first tick does not move an
    /// age-1 bolt again, and a bolt that ages past its lifetime is not swept.
    private static func boltContainsPlayer(
        from: VecQ8,
        velocity: VecQ8,
        radius: Int,
        lifetime: Int,
        state: WorldState
    ) -> Bool {
        var position = from + velocity
        var previous = from
        var age = 1
        var travelled = IntMath.isqrt(velocity.lengthSquaredRaw)
        let maxTravel = Int64(10_000) * Q8.scale
        let bounds = state.arena.boundsUnits
        while age <= lifetime {
            if age > 1 {
                previous = position
                position = position + velocity
                travelled += IntMath.isqrt(velocity.lengthSquaredRaw)
            }
            age += 1
            if position.x.raw < 0 || position.y.raw < 0
                || position.x.raw > Int64(bounds.maxX) * Q8.scale
                || position.y.raw > Int64(bounds.maxY) * Q8.scale
                || age > lifetime
                || travelled > maxTravel
            {
                return false
            }
            var wallT: Int64?
            for solid in state.liveSolids {
                if let entry = Collision.segmentEntryTime(previous, position, box: solid.box) {
                    wallT = min(wallT ?? entry, entry)
                }
            }
            if let playerT = Collision.sweepCircleTime(
                from: previous,
                to: position,
                radius: radius,
                target: state.player.position,
                targetRadius: PlayerBody.radiusUnits
            ) {
                if let wallT, wallT <= playerT { return false }
                return true
            }
            if wallT != nil { return false }
        }
        return false
    }
}
