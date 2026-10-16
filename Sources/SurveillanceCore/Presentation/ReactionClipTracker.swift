import Foundation

/// Event-driven reaction clips: hurt, stagger, and defeat.
///
/// `clip-metadata-001` binds these clips to authoritative event markers —
/// `playerDamaged`, `entityDamaged`, `entityDied`, `eliteDefeated`,
/// `bossDefeated` — but no state machine reaches them, because damage and death
/// are events, not states. Until this type existed none was ever selected: the
/// Player's hurt, the Improper Search Daemon's hurt and defeat, and the
/// Algorithmic Moderate's stagger and defeat were delivered art that never
/// played. A defeated enemy also left the snapshot on the tick it died, so a
/// defeat clip had nothing to play on.
///
/// The tracker reads each tick's authoritative events and holds a reaction for
/// exactly its clip's duration. Which clip reacts to which event comes from the
/// clip's own marker, so a role gains reactions by adding clips to the
/// contract, with no mapping table here to fall out of date.
///
/// Commit clips are tracked here too (D-072). The Fog Analytics Cloud, Sutro
/// Signal Witch, and Victorian Vendor resolve their attack on the tick they
/// leave `TELEGRAPH` for `COOLDOWN` and never sit in an attack state, so their
/// commit is read from consecutive states and held for its duration. The
/// Autonomous Informant's commit is its contact hit, found through its clip's
/// `playerDamaged` marker. A held commit replaces the state clip, so hurt and
/// defeat still cut it only through the commit's own cancel windows.
///
/// Presentation only (`animation.md` §1): it reads events and never writes
/// simulation state, so the replay digest cannot change. A reaction is also a
/// preference, not a replacement — the renderer tries it first and falls back
/// to the state clip, so an unbacked reaction can never hide a telegraph.
public struct ReactionClipTracker: Sendable {
    public struct Reaction: Equatable, Sendable {
        public var clipId: String
        /// Exclusive: the reaction shows while `tick < endTick`.
        public var endTick: UInt64
        public var occurrence: ClipOccurrence
    }

    /// A defeated enemy held on screen for its defeat clip after it has left
    /// authoritative state.
    public struct Remains: Equatable, Sendable {
        public var sprite: PresentationSnapshot.CircleSprite
        public var endTick: UInt64
    }

    static let damageMarker = "entityDamaged"
    static let playerDamageMarker = "playerDamaged"
    static let defeatMarkers: Set<String> = ["entityDied", "eliteDefeated", "bossDefeated"]
    /// D-072: roles whose attack resolves on the telegraph-to-cooldown step.
    static let transitionCommitRoles: [ArchetypeID] = [.fogAnalyticsCloud, .sutroSignalWitch, .victorianVendor]

    private let clipsById: [String: ClipRecord]
    private let hurtClipByRole: [String: ClipRecord]
    private let defeatClipByRole: [String: ClipRecord]
    private let playerHurtClip: ClipRecord?
    private let transitionCommitByRole: [ArchetypeID: ClipRecord]
    private let contactCommitByRole: [String: ClipRecord]

    public private(set) var reactions: [EntityID: Reaction] = [:]
    public private(set) var remains: [EntityID: Remains] = [:]
    public private(set) var playerReaction: Reaction?
    public private(set) var commits: [EntityID: Reaction] = [:]

    public init(clips: [ClipRecord]) {
        // Deterministic when a role ever declares two clips for one marker:
        // the lowest clip ID wins.
        let ordered = clips.sorted { $0.clipId.utf8LessThan($1.clipId) }
        var byId: [String: ClipRecord] = [:]
        var hurt: [String: ClipRecord] = [:]
        var defeat: [String: ClipRecord] = [:]
        var playerHurt: ClipRecord?
        var contactCommit: [String: ClipRecord] = [:]
        for clip in ordered {
            byId[clip.clipId] = clip
            let marker = clip.authoritativeEventMarker
            if clip.actorRole == "player" {
                if marker == Self.playerDamageMarker, playerHurt == nil { playerHurt = clip }
                continue
            }
            if marker == Self.damageMarker, hurt[clip.actorRole] == nil { hurt[clip.actorRole] = clip }
            if Self.defeatMarkers.contains(marker), defeat[clip.actorRole] == nil { defeat[clip.actorRole] = clip }
            if marker == Self.playerDamageMarker, contactCommit[clip.actorRole] == nil {
                contactCommit[clip.actorRole] = clip
            }
        }
        clipsById = byId
        hurtClipByRole = hurt
        defeatClipByRole = defeat
        playerHurtClip = playerHurt
        contactCommitByRole = contactCommit
        var transition: [ArchetypeID: ClipRecord] = [:]
        for role in Self.transitionCommitRoles {
            transition[role] = byId["\(role.rawValue)_commit"]
        }
        transitionCommitByRole = transition
    }

    public init(catalog: ClipCatalog) {
        self.init(clips: catalog.clips)
    }

    public static func bundled() throws -> ReactionClipTracker {
        try ReactionClipTracker(catalog: .bundled())
    }

    /// A tracker with no clips: reacts to nothing. The fallback when the
    /// contract cannot load, so presentation degrades to state clips.
    public static let empty = ReactionClipTracker(clips: [])

    /// Selected-facing duration at 60 Hz, rounded up from exact authored timing.
    public static func durationTicks(_ clip: ClipRecord, direction: String? = nil) -> UInt64 {
        guard let timing = try? clip.timing(forDirection: direction ?? clip.directions.first ?? "none"),
              let ticks = try? timing.durationTicks(at: 60) else { return 0 }
        return ticks
    }

    private static func reaction(_ clip: ClipRecord, direction: String, tick: UInt64) -> Reaction? {
        let duration = durationTicks(clip, direction: direction)
        let end = tick.addingReportingOverflow(duration)
        guard duration > 0, !end.overflow else { return nil }
        return Reaction(clipId: clip.clipId, endTick: end.partialValue,
                        occurrence: ClipOccurrence(direction: direction, startTick: tick))
    }

    /// Records the reactions `result`'s events call for.
    ///
    /// `previousEnemies` is the enemy list from before the step and
    /// `currentEnemies` the list after it. A defeated enemy may already be gone
    /// from the second, so its last position and facing are taken from
    /// whichever list still holds it, preferring the later.
    public mutating func ingest(_ result: TickResult, previousEnemies: [EnemyBody], currentEnemies: [EnemyBody], playerDirection: String = "s") {
        let tick = result.tick
        prune(at: tick)
        func enemy(_ id: EntityID) -> EnemyBody? {
            currentEnemies.first { $0.id == id } ?? previousEnemies.first { $0.id == id }
        }
        let died = Set(result.events.filter { $0.type == .entityDied }.compactMap(\.primaryEntityId))
        for body in currentEnemies where body.state == .cooldown {
            guard let clip = transitionCommitByRole[body.archetype],
                  previousEnemies.first(where: { $0.id == body.id })?.state == .telegraph
            else { continue }
            commits[body.id] = Self.reaction(clip, direction: ActorClipProjection.direction(for: body.velocity), tick: tick)
        }
        for event in result.events {
            switch event.type {
            case .entityDied:
                guard let id = event.primaryEntityId, let body = enemy(id),
                      let clip = defeatClipByRole[body.archetype.rawValue],
                      let playback = Self.reaction(clip, direction: ActorClipProjection.direction(for: body.velocity), tick: tick) else { continue }
                reactions[id] = nil
                commits[id] = nil
                remains[id] = Remains(
                    sprite: PresentationSnapshot.CircleSprite(
                        id: body.id,
                        x: body.position.x.unitsTruncated,
                        y: body.position.y.unitsTruncated,
                        radius: body.radius,
                        role: body.archetype.rawValue,
                        silhouette: ActorSilhouette.enemy(body.archetype),
                        clipId: clip.clipId,
                        direction: playback.occurrence.direction,
                        heldClipOccurrence: playback.occurrence
                    ),
                    endTick: playback.endTick
                )
            case .entityDamaged:
                // Cameras take entityDamaged too; they are not enemies and are
                // skipped by the lookup. A killing blow shows defeat, not hurt.
                guard let id = event.primaryEntityId, !died.contains(id), let body = enemy(id),
                      let clip = hurtClipByRole[body.archetype.rawValue] else { continue }
                reactions[id] = Self.reaction(clip, direction: ActorClipProjection.direction(for: body.velocity), tick: tick)
            case .playerDamaged:
                if let source = event.secondaryEntityId, !died.contains(source), let body = enemy(source),
                   let commit = contactCommitByRole[body.archetype.rawValue]
                {
                    commits[source] = Self.reaction(commit, direction: ActorClipProjection.direction(for: body.velocity), tick: tick)
                }
                guard let clip = playerHurtClip else { continue }
                playerReaction = Self.reaction(clip, direction: playerDirection, tick: tick)
            default:
                continue
            }
        }
    }

    /// Writes the reactions active at `snapshot.tick` into it.
    public func apply(to snapshot: inout PresentationSnapshot) {
        let tick = snapshot.tick
        snapshot.playerReactionClipId = nil
        snapshot.playerReactionOccurrence = nil
        for index in snapshot.enemies.indices {
            if snapshot.enemies[index].heldClipOccurrence != nil {
                snapshot.enemies[index].clipId = snapshot.enemies[index].fallbackClipId
            }
            snapshot.enemies[index].reactionClipId = nil
            snapshot.enemies[index].reactionOccurrence = nil
            snapshot.enemies[index].heldClipOccurrence = nil
            snapshot.enemies[index].fallbackClipId = nil
            if let commit = commits[snapshot.enemies[index].id], commit.endTick > tick {
                snapshot.enemies[index].fallbackClipId = snapshot.enemies[index].clipId
                snapshot.enemies[index].clipId = commit.clipId
                snapshot.enemies[index].heldClipOccurrence = commit.occurrence
            }
            let sprite = snapshot.enemies[index]
            guard let reaction = reactions[sprite.id], reaction.endTick > tick,
                  let clip = clipsById[reaction.clipId],
                  mayInterrupt(sprite.clipId, with: clip)
            else { continue }
            snapshot.enemies[index].reactionClipId = reaction.clipId
            snapshot.enemies[index].reactionOccurrence = reaction.occurrence
        }
        snapshot.defeated = remains.values
            .filter { $0.endTick > tick }
            .map(\.sprite)
            .sorted { $0.id < $1.id }
        if let reaction = playerReaction, reaction.endTick > tick,
           let clip = clipsById[reaction.clipId],
           mayInterrupt(snapshot.playerClipId, with: clip)
        {
            snapshot.playerReactionClipId = reaction.clipId
            snapshot.playerReactionOccurrence = reaction.occurrence
        }
    }

    /// `animation.md` §4 `cancel_windows`: a reaction may cut the clip already
    /// playing only when that clip lists the reaction's state. No clip at all
    /// (a blockout) can always be interrupted.
    func mayInterrupt(_ base: String?, with reaction: ClipRecord) -> Bool {
        guard let base, let current = clipsById[base] else { return true }
        return current.cancelWindows.contains(reaction.state)
    }

    public mutating func reset() {
        reactions = [:]
        remains = [:]
        playerReaction = nil
        commits = [:]
    }

    private mutating func prune(at tick: UInt64) {
        reactions = reactions.filter { $0.value.endTick > tick }
        remains = remains.filter { $0.value.endTick > tick }
        commits = commits.filter { $0.value.endTick > tick }
        if let reaction = playerReaction, reaction.endTick <= tick { playerReaction = nil }
    }
}
