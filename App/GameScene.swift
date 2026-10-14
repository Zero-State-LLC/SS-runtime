import SpriteKit
import SurveillanceCore
import UIKit
import os

final class GameSession {
    private(set) var simulation: Simulation
    private var cameraHUD = CameraHUDProjector()
    private var heatCaption = HeatCaptionProjector()
    /// D-083 heat caption, derived from the tick's events; nil when none shows.
    private(set) var reinforcementCopy: String?
    /// D-101 quiet-approach tag and captions, read from the authoritative latch.
    private var quietApproach = QuietApproachProjector()
    private(set) var quietFrame = QuietApproachProjector.Frame(tagVisible: true, caption: nil)
    /// D-089 "first unaware enemy on screen" copy, derived from the snapshot.
    private var awarenessHint = AwarenessHintProjector()
    private(set) var awarenessHintCopy: String?
    private var audioProjector = AudioProjector()
    /// Hurt, stagger, and defeat clips driven by authoritative events.
    private var reactions = (try? ReactionClipTracker.bundled()) ?? .empty
    /// Last tick's audio projection, consumed by the device layer.
    private(set) var audio = AudioProjection.silent
    /// D-094 on-screen caption stack, fed from each tick's captioned cues.
    private(set) var captionBoard = CaptionBoard()
    var audioSettings: PresentationAudioSettings = .enabled
    private(set) var cameraHUDProjection = CameraHUDProjection(
        notchesVisible: false,
        notchFilled: [false, false, false],
        tamperVisible: false,
        tamperCopy: ""
    )
    private(set) var terminalReceiptStored = false
    /// D-088: the last step's authoritative events, for the VFX layer. Read
    /// after the step; never fed back.
    private(set) var lastEvents: [AuthoritativeEvent] = []
    /// D-083 reinforcements granted to waves that started in the last tick.
    private(set) var lastHeatReinforcements = 0
    var moveX: Int16 = 0
    var moveY: Int16 = 0
    var dodgePressed = false
    var pendingUpgradeChoice: UInt8?
    /// `run-shell.md` § 10.2: every command that advanced this run, in tick
    /// order, so a successful run can be stored and replayed as the ghost.
    /// Written after each step; never read back into the simulation.
    private(set) var commandLog: [PlayerCommand] = []
    var damageDiagnosticsEnabled = false
    var damageViewCenter: VecQ8?
    private(set) var damageDiagnostics: [DamageDiagnostic] = []
    private(set) var droppedDamageDiagnostics = 0
    private(set) var latestDamageDiagnostics: [DamageDiagnostic] = []
    /// True once a debug scenario has written authoritative state directly.
    /// Such a run cannot be replayed from its commands, so it is never stored
    /// as a best.
    private(set) var scenarioSeeded = false
    /// D-095 medals and D-097/D-098 feel. Fed after each step; never read by
    /// the simulation.
    private(set) var feel = FeelPassPresenter()

    init(simulation: Simulation) { self.simulation = simulation }

    init(seed: UInt64 = 1) {
        simulation = try! Simulation.make(seed: seed)
    }

    func step() {
        let tick = simulation.state.tick + 1
        let diagnosticBefore = damageDiagnosticsEnabled ? simulation.state : nil
        let enemiesBefore = simulation.state.enemies
        feel.willStep(simulation.state)
        let result: TickResult
        var command: PlayerCommand?
        if simulation.state.upgrade.pending {
            if let choice = pendingUpgradeChoice {
                command = PlayerCommand(
                    tick: tick,
                    moveX: 0,
                    moveY: 0,
                    dodgePressed: false,
                    upgradeChoiceIndex: choice
                )
                pendingUpgradeChoice = nil
            }
        } else {
            command = PlayerCommand(
                tick: tick,
                moveX: moveX,
                moveY: moveY,
                dodgePressed: dodgePressed
            )
        }
        result = simulation.step(command: command)
        lastEvents = result.events
        latestDamageDiagnostics = diagnosticBefore.map {
            DamageDiagnostic.capture(before: $0, after: simulation.state, events: result.events)
        } ?? []
        for index in latestDamageDiagnostics.indices {
            latestDamageDiagnostics[index].viewCenterBefore = damageViewCenter.map(DamageDiagnostic.Point.init)
        }
        damageDiagnostics.append(contentsOf: latestDamageDiagnostics)
        if damageDiagnostics.count > 512 {
            let excess = damageDiagnostics.count - 512
            droppedDamageDiagnostics += excess
            damageDiagnostics.removeFirst(excess)
        }
        // Log only a command the simulation consumed: one that advanced the
        // tick. A held upgrade gate and a finished run do not advance.
        if let command, simulation.state.tick == tick {
            commandLog.append(command)
        }
        reactions.ingest(result, previousEnemies: enemiesBefore, currentEnemies: simulation.state.enemies)
        applyCameraHUD(result)
        lastHeatReinforcements = HeatCaptionProjector.reinforcements(
            events: result.events,
            detection: simulation.state.exposure.detectionState,
            heat: simulation.state.content.heat
        )
        reinforcementCopy = heatCaption.project(
            tick: result.tick,
            events: result.events,
            detection: simulation.state.exposure.detectionState,
            heat: simulation.state.content.heat
        )
        quietFrame = quietApproach.project(tick: result.tick, events: result.events, state: simulation.state)
        feel.didStep(events: result.events, enemiesBefore: enemiesBefore, state: simulation.state)
        applyAudio(result)
        audio = feel.decorate(audio)
        captionBoard.ingest(tick: result.tick, cues: audio.captionCues)
        awarenessHintCopy = awarenessHint.project(PresentationSnapshot(simulation.state))
        persistTerminalReceiptIfNeeded()
    }

    private func persistTerminalReceiptIfNeeded() {
        guard !terminalReceiptStored, simulation.state.outcome != .playing else { return }
        if (try? ReceiptStore.persistTerminalReceipt(for: simulation.state)) != nil {
            terminalReceiptStored = true
        }
    }

    func restartRun(seed: UInt64 = 1) {
        simulation = try! Simulation.make(seed: seed)
        commandLog = []
        damageDiagnostics = []
        latestDamageDiagnostics = []
        droppedDamageDiagnostics = 0
        lastEvents = []
        scenarioSeeded = false
        terminalReceiptStored = false
        audioProjector.reset()
        captionBoard.reset()
        heatCaption.reset()
        reinforcementCopy = nil
        quietApproach.reset()
        quietFrame = QuietApproachProjector.Frame(tagVisible: true, caption: nil)
        awarenessHint.reset()
        awarenessHintCopy = nil
        feel.reset()
        reactions.reset()
        audio = AudioProjection.silent
        pendingUpgradeChoice = nil
        moveX = 0
        moveY = 0
        dodgePressed = false
    }

    /// audio-haptics-001: presentation projects authoritative events and never
    /// feeds anything back into the simulation.
    private func applyAudio(_ result: TickResult) {
        audio = audioProjector.project(
            tick: result.tick,
            events: result.events,
            world: AudioWorldQuery.from(simulation.state),
            settings: audioSettings
        )
    }

    private func applyCameraHUD(_ result: TickResult) {
        let state = simulation.state
        let selected = Targeting.select(
            player: state.player,
            enemies: state.enemies,
            cameras: state.cameras,
            solids: state.liveSolids,
            unawarePatrolRange: state.content.patrol.sightUnits
        )
        var query = CameraHUDQuery.none
        if let selected, let camera = state.cameras.first(where: { $0.entityId == selected.0 }) {
            query = CameraHUDQuery(
                targetIntegrity: camera.integrity,
                damageable: camera.isDamageable,
                targeted: true,
                inRange: true,
                damaged: camera.integrity < 3
            )
        }
        cameraHUDProjection = cameraHUD.project(tick: result.tick, events: result.events, query: query)
    }

#if DEBUG
    func seedScenario(_ scenario: String) -> Bool {
        let seeded = simulation.debug_seedScenario(scenario)
        if seeded {
            scenarioSeeded = true
            feel.observe(simulation.state)
        }
        return seeded
    }
#endif

    var snapshot: PresentationSnapshot {
        var snapshot = PresentationSnapshot(simulation.state)
        snapshot.combatFeedback = simulation.combatFeedback
        reactions.apply(to: &snapshot)
        return snapshot
    }
}

final class GameScene: SKScene {
    let session: GameSession
    override init(size: CGSize) {
        session = GameSession()
        super.init(size: size)
    }
    init(size: CGSize, session: GameSession) {
        self.session = session
        super.init(size: size)
    }
    required init?(coder: NSCoder) {
        session = GameSession()
        super.init(coder: coder)
    }
    let upgradeSelection = UpgradeSelectionModel()
    private let combatFeedbackRenderer = CombatFeedbackRenderer()
    private let instrumentation = RunInstrumentation()
    private let deviceRunTracker = DeviceRunTracker()
    private var terminalEvidenceStored = false
    private let renderer = WorldRenderer()
    /// D-088: effects, hit-stop, and shake. Presentation only.
    private let vfx = VFXRenderer()
    private let cameraNode = SKCameraNode()
    private var cameraFollow = CameraFollow()
    private var lastDisplayTime: TimeInterval?
    private var displayDelta: TimeInterval = 1.0 / 60
    private let qaEnabled = ProcessInfo.processInfo.arguments.contains("-SSQA")
    private var qaFrames = 0
    private static let qaLog = Logger(subsystem: "com.zer0state.surveillancesurvivor", category: "device-qa")
    private let hud = HUDRenderer()
    /// D-094 Lockdown tint: world layer only, under the HUD.
    private let lockdownTint = LockdownTintLayer()
    /// D-096 court light and boss telegraph countdown rings.
    let court = BossCourtRenderer()
    private let soundEngine = AudioEngine()
    private var controller = TouchController()
    private var projector: HUDProjector?
    var controlLayout: ControlLayout? { hud.controlLayout }
    /// player-controller-001 PC-008: pause creates no simulation ticks.
    private var runPaused = false
    /// Raised when the player presses Pause; SwiftUI owns the surface itself.
    var onPauseRequested: (() -> Void)?
    private var settings: PresentationSettings = .defaults
    /// `run-shell.md` § 10.1: the Daily Run this scene is playing. Nil only for
    /// a debug harness run that skipped the title.
    private var dailyRun: DailyRun?
    /// `run-shell.md` § 10.2: the ghost. Presentation only — it owns its own
    /// simulation and nothing flows from it into `session`.
    private var ghost: GhostRun?
    /// Bumped on every run start, so a ghost verified in the background for an
    /// earlier run is never attached to a later one.
    private var ghostGeneration = 0
    /// `run-shell.md` § 11: built once, when the run reaches a terminal outcome.
    private var runCard: RunCard?
    /// D-098 intro beat; non-nil and unfinished means no tick may run.
    private(set) var intro: IntroSequence?
    private let introOverlay = IntroOverlay()
    /// D-097 near-miss cone edges, drawn beside the cones.
    private let nearMissEdges = NearMissEdgeLayer()
    /// D-099 world grade, ground only.
    private let gradeLayer = DailyGradeLayer()
    /// D-099 today's look, set with the Daily Run.
    private(set) var flavour: DailyFlavour?
    /// Display frames drawn, for the near-miss pulse. Presentation clock only.
    private var presentationFrame: UInt64 = 0
    /// The live run's tick, for intro evidence and tests.
    var currentTick: UInt64 { session.simulation.state.tick }
#if DEBUG
    /// `-SSHoldIntro <frame>`: hold the intro at that frame for a screenshot.
    private var introHoldFrame: Int?
    private var feelHoldArmed = false
    private var feelHoldSeen = 0
    private var quietLostLogged = false
    private var nearMissLogged = false
#endif
#if DEBUG
    private var autopilot: DebugAutopilot?
    private var frameLogTick: UInt64 = 0
    /// The `--console-pty` stream drops on long runs; the unified log survives,
    /// so a full playthrough stays observable after the pipe closes.
    private static let autopilotLog = Logger(
        subsystem: "com.zer0state.surveillancesurvivor",
        category: "autopilot"
    )
#endif

    override func didMove(to view: SKView) {
        session.damageDiagnosticsEnabled = qaEnabled
        backgroundColor = .init(red: 0.055, green: 0.075, blue: 0.10, alpha: 1)
        view.preferredFramesPerSecond = 60
        view.ignoresSiblingOrder = true
        size = CGSize(width: CGFloat(PresentationCamera.visibleWidth), height: CGFloat(PresentationCamera.visibleHeight))
        scaleMode = .aspectFit
        addChild(renderer.root)
        renderer.root.addChild(combatFeedbackRenderer.root)
        addChild(cameraNode)
        camera = cameraNode
        cameraNode.addChild(lockdownTint.node)
        cameraNode.addChild(court.lightNode)
        renderer.root.addChild(court.ringLayer)
        // D-099 grade and D-097 near-miss edges sit inside the world tree at
        // fractional depths between `WorldRenderer` layers; D-098's intro
        // card is screen space, under the HUD.
        renderer.root.addChild(gradeLayer.node)
        renderer.root.addChild(nearMissEdges.node)
        cameraNode.addChild(introOverlay.node)
        vfx.install(in: self, camera: cameraNode, worldRoot: renderer.root)
        // `ignoresSiblingOrder` makes draw order depend on zPosition alone, and
        // ties are undefined. WorldRenderer assigns its layers 0...8 while the
        // HUD left everything at the default 0, so world sprites could draw over
        // HUD elements — visible immediately once a centred panel exists, but
        // true of every HUD element that a sprite happened to overlap.
        hud.root.zPosition = 1000
        cameraNode.addChild(hud.root)
        view.isMultipleTouchEnabled = true
        NotificationCenter.default.addObserver(
            forName: UIApplication.didReceiveMemoryWarningNotification,
            object: nil,
            queue: .main
        ) { [weak self] _ in
            MainActor.assumeIsolated {
                self?.instrumentation.noteMemoryWarning()
            }
        }
#if DEBUG
        let arguments = ProcessInfo.processInfo.arguments
        // `-SSMute` silences a harness run. Verification launches the app dozens
        // of times, and a simulator has no volume control of its own.
        if let flag = arguments.firstIndex(of: "-SSHoldIntro"),
           arguments.index(after: flag) < arguments.endIndex
        {
            introHoldFrame = Int(arguments[arguments.index(after: flag)])
        }
        if arguments.contains("-SSMute") {
            session.audioSettings = PresentationAudioSettings(
                effectsEnabled: false,
                hapticsEnabled: false,
                musicEnabled: false
            )
            soundEngine.settings = session.audioSettings
            soundEngine.mix = AudioEngine.Mix(master: 0, music: 0, effects: 0, voice: 0, haptics: 0)
        }
        // `-SSDaily` plays today's Daily Run seed in a harness run that skips
        // the title, so the Daily Run surfaces can be observed under the pilot.
        if arguments.contains("-SSDaily"), let run = try? DailyRun(day: DailyRun.Day(utc: Date())) {
            beginDailyRun(run)
        }
        autopilot = DebugAutopilot.fromLaunchArguments(arguments, arena: session.simulation.state.arena)
        configureVFXEvidence(arguments)
        // `-SSSeed <scenario>` puts the simulation into a named legal late-game
        // state so the renderer can be observed there. Presentation evidence
        // only: a seeded run says nothing about balance or the acceptance gates.
        if let seedFlag = arguments.firstIndex(of: "-SSSeed"),
           arguments.index(after: seedFlag) < arguments.endIndex
        {
            let scenario = arguments[arguments.index(after: seedFlag)]
            let seeded = session.seedScenario(scenario)
            Self.autopilotLog.notice("seed \(scenario, privacy: .public) -> \(seeded, privacy: .public)")
        }
#endif
        configureHUD(for: view)
        redraw()
    }

    override func didChangeSize(_ oldSize: CGSize) {
        super.didChangeSize(oldSize)
        if let view { configureHUD(for: view) }
    }

    /// Rebuilds the HUD projection whenever the safe rectangle can have changed.
    private func configureHUD(for view: SKView) {
        let insets = view.safeAreaInsets
        let projector = HUDProjector(
            viewSize: view.bounds.size,
            safeInsets: EdgeInsetsPoints(
                top: insets.top,
                left: insets.left,
                bottom: insets.bottom,
                right: insets.right
            ),
            sceneSize: size
        )
        self.projector = projector
        // D-094 outlines are one screen point wide.
        renderer.outlineWidthUnits = 1 / projector.pointsPerSceneUnit
        hud.configure(
            projector: projector,
            // Handedness is a local setting, not authoritative state.
            handedness: settings.handedness,
            hudScale: settings.hudScale
        )
    }

    /// Local setting; excluded from replay authority.
    private var hudScaleSetting: HUDScaleSetting { settings.hudScale }

    /// Applies presentation settings. Nothing here reaches the simulation:
    /// ER-007 requires the digest and receipt to be unchanged by a settings
    /// change, and none of these values is a simulation input.
    func apply(settings: PresentationSettings) {
        let wasGhostEnabled = self.settings.ghostEnabled
        self.settings = settings
        session.audioSettings = settings.audio
        soundEngine.settings = settings.audio
        vfx.settings = settings.vfx
        soundEngine.mix = AudioEngine.Mix(
            master: Float(settings.mix.master) / 100,
            music: Float(settings.mix.music) / 100,
            effects: Float(settings.mix.effects) / 100,
            voice: Float(settings.mix.voice) / 100,
            haptics: Float(settings.mix.haptics) / 100
        )
        hud.pinCameraCounter = settings.pinCameraCounter
        hud.tutorialsEnabled = settings.tutorialsEnabled
        if let view { configureHUD(for: view) }
        // § 10.2: the ghost can be turned off, and back on, from Settings.
        // Only a change to the toggle itself touches it, so moving a slider
        // never restarts a verification in flight.
        if settings.ghostEnabled != wasGhostEnabled {
            if settings.ghostEnabled {
                if !session.simulation.isTerminal { loadGhost() }
            } else {
                ghost = nil
                ghostGeneration += 1
            }
        }
    }

    func setPaused(_ paused: Bool) {
        runPaused = paused
        renderer.root.isPaused = paused
        lastDisplayTime = nil
        // Input must not survive a pause boundary.
        //
        // Pause is reached by tapping the Pause control while the other hand may
        // still be holding the stick, and SwiftUI then covers the scene — so the
        // scene is not guaranteed to receive `touchesEnded` for that held touch.
        // Without this the run resumes walking with no finger down, a buffered
        // Dodge fires on the first tick back, and `stickTouch` stays bound to a
        // token that can never end, which makes `began` refuse every future
        // stick press for the rest of the run.
        controller.reset()
    }

    override func update(_ currentTime: TimeInterval) {
        displayDelta = lastDisplayTime.map { max(0, currentTime - $0) } ?? 1.0 / 60
        lastDisplayTime = currentTime
        instrumentation.frameTimes.recordFrame(timestamp: currentTime)
        if qaEnabled {
            qaFrames += 1
            if qaFrames % 300 == 0 {
                let summary = instrumentation.frameTimes.summarize()
                Self.qaLog.notice("QA device=\(DeviceTelemetrySample.hardwareModel, privacy: .public) tick=\(self.currentTick, privacy: .public) n=\(summary.sampleCount, privacy: .public) p50=\(summary.p50Ms, privacy: .public) p95=\(summary.p95Ms, privacy: .public) p99=\(summary.p99Ms, privacy: .public) worst=\(summary.worstMs, privacy: .public)")
            }
        }
        guard !runPaused else { return }
        // D-088 hit-stop: a frozen frame neither steps the simulation nor
        // redraws the world. No tick, no command, so no digest change.
        if vfx.consumeHitStopFrame() {
            cameraNode.position = vfx.frozenCameraPosition()
            return
        }
        // D-098 intro beat: frames pass, ticks do not. No command is sampled
        // and the simulation is not stepped until it finishes or is skipped.
        if advanceIntroIfRunning() { return }
#if DEBUG
        if autopilot != nil {
            let snapshot = session.snapshot
            // Harness uses the same validated action as the SwiftUI buttons.
            // This is action coverage, not evidence of UI hit testing.
            if snapshot.upgradePending {
                chooseUpgrade(autopilot!.upgradeChoice.selectionIndex)
            }
            let steer = autopilot!.command(snapshot)
            session.moveX = steer.moveX
            session.moveY = steer.moveY
            session.dodgePressed = steer.dodge
            if snapshot.tick % 60 == 0 {
                let line = """
                    tick=\(snapshot.tick) \
                    player=\(snapshot.player.x),\(snapshot.player.y) \
                    hp=\(snapshot.playerIntegrity) exposure=\(snapshot.exposure) \
                    detection=\(snapshot.detection.rawValue) \
                    enemies=\(snapshot.enemies.count) shots=\(snapshot.projectiles.count) \
                    telegraphs=\(snapshot.telegraphs.count) boss=\(snapshot.boss?.integrity ?? -1) \
                    node=\(snapshot.objectiveNode.rawValue) upgrade=\(snapshot.upgrade?.rawValue ?? "-") \
                    armed=\(snapshot.extractionArmed) outcome=\(snapshot.outcome.rawValue) \
                    music=\(soundEngine.musicState.rawValue) \
                    sprites=\(renderer.spriteCoverage.backed)/\(renderer.spriteCoverage.total) \
                    gates=\(snapshot.solidIds.filter { snapshot.gateIds.contains($0) }.joined(separator: ",")) \
                    pilot=[\(autopilot!.lastDecision)]
                    """
                Self.autopilotLog.notice("\(line, privacy: .public)")
            }
            if autopilot!.stalled {
                Self.autopilotLog.error("stalled on node \(snapshot.objectiveNode.rawValue, privacy: .public)")
            }
        } else {
            applyController()
        }
#else
        applyController()
#endif
        if qaEnabled {
            session.damageViewCenter = VecQ8(
                x: Q8(raw: Int64((cameraNode.position.x * CGFloat(Q8.scale)).rounded())),
                y: Q8(raw: Int64((cameraNode.position.y * CGFloat(Q8.scale)).rounded())))
        }
        session.step()
        if qaEnabled {
            for hit in session.latestDamageDiagnostics {
                if let data = try? JSONEncoder().encode(hit), let line = String(data: data, encoding: .utf8) {
                    Self.qaLog.notice("QA_DAMAGE \(line, privacy: .public)")
                }
            }
        }
        // D-097: the takedown's hit-stop and ring, after the step that made it.
        vfx.takedown(targets: session.feel.lastTakedowns)
#if DEBUG
        noteFeelEvidence()
#endif
        if !session.lastEvents.isEmpty {
            vfx.ingest(
                tick: session.simulation.state.tick,
                events: session.lastEvents,
                snapshot: session.snapshot,
                heatReinforcements: session.lastHeatReinforcements
            )
        }
        // § 10.2: one ghost tick for each tick of the live run, after the live
        // step and never before it.
        ghost?.advance(to: session.simulation.state.tick)
        finishRunIfNeeded()
        soundEngine.apply(session.audio)
        instrumentation.recordSimulation(session.simulation.state)
        persistDeviceEvidenceIfNeeded()
        redraw()
#if DEBUG
        // D-088 frame budget: frame times with the VFX layer live.
        if session.simulation.state.tick % 600 == 0, session.simulation.state.tick != frameLogTick {
            frameLogTick = session.simulation.state.tick
            let frames = instrumentation.frameTimes.summarize()
            Self.autopilotLog.notice(
                "frames tick=\(self.session.simulation.state.tick, privacy: .public) n=\(frames.sampleCount, privacy: .public) p50=\(frames.p50Ms, privacy: .public) p95=\(frames.p95Ms, privacy: .public) p99=\(frames.p99Ms, privacy: .public) worst=\(frames.worstMs, privacy: .public) vfxLive=\(self.vfx.liveEffectCount, privacy: .public) frozen=\(self.vfx.frozenFrames, privacy: .public) freezes=\(self.vfx.freezes, privacy: .public)"
            )
        }
#endif
    }

    /// Outlines follow the frame each animation action just chose.
    override func didEvaluateActions() {
        super.didEvaluateActions()
        renderer.syncOutlines()
    }

    private func applyController() {
        let command = controller.takeCommand()
        session.moveX = command.moveX
        session.moveY = command.moveY
        session.dodgePressed = command.dodgePressed
    }

    private func persistDeviceEvidenceIfNeeded() {
        guard !terminalEvidenceStored, session.simulation.state.outcome != .playing else { return }
        terminalEvidenceStored = true
        if qaEnabled {
            let report = DamageDiagnosticRun(seed: session.simulation.state.seed,
                device: DeviceTelemetrySample.hardwareModel, droppedRecords: session.droppedDamageDiagnostics,
                damage: session.damageDiagnostics, commands: session.commandLog.map(DamageDiagnosticRun.Command.init))
            do {
                let directory = try FileManager.default.url(for: .documentDirectory, in: .userDomainMask,
                                                           appropriateFor: nil, create: true)
                let url = directory.appendingPathComponent("SS-damage-QA-latest.json")
                try JSONEncoder().encode(report).write(to: url, options: .atomic)
                Self.qaLog.notice("QA_DAMAGE_EXPORT \(url.lastPathComponent, privacy: .public)")
            } catch {
                Self.qaLog.error("QA_DAMAGE_EXPORT failed: \(String(describing: error), privacy: .public)")
            }
        }
        deviceRunTracker.noteTerminalOutcome(session.simulation.state.outcome)
        let snapshot = instrumentation.evidence()
        let deviceEvidence = snapshot.makeDeviceRunEvidence(
            deviceClass: DeviceTelemetrySample.hardwareModel,
            consecutiveCompleteRuns: deviceRunTracker.consecutiveCompleteRuns,
            atlasMemoryBytes: nil
        )
        _ = try? ReleaseEvidenceStore.exportDeviceRunEvidence(deviceEvidence)
        if deviceRunTracker.consecutiveCompleteRuns >= 3,
           let simulationCeilings = try? D021CeilingEvaluator.profileAndMeasure(),
           let settled = deviceEvidence.settledD021Ceilings(from: simulationCeilings) {
            _ = try? ReleaseEvidenceStore.exportReleaseCandidateWithBundledPlaytests(
                deviceEvidence: [deviceEvidence],
                d021DeviceProfiling: settled
            )
        }
    }

    /// `run-shell.md` § 8 Start: begins the Daily Run the title computed.
    func beginDailyRun(_ run: DailyRun) {
        dailyRun = run
        let look = DailyFlavour(day: run.day)
        flavour = look
        renderer.fogDensity = CGFloat(look.fogMultiplier)
        restartRun(seed: run.seed)
        gradeLayer.apply(look.grade, arena: session.simulation.state.arena.boundsUnits.aabb)
        startIntro()
    }

    /// D-098: "After Start, a 2-second intro plays before the first tick."
    private func startIntro() {
        intro = IntroSequence(
            cameraIds: session.simulation.state.cameras.map(\.entityId),
            reducedMotion: settings.vfx.reducedMotion
        )
        redraw()
    }

    /// Advances the intro one display frame. True while it is still running,
    /// meaning this frame must not step the simulation.
    private func advanceIntroIfRunning() -> Bool {
#if DEBUG
        let hold = introHoldFrame
#else
        let hold: Int? = nil
#endif
        let wasRunning = intro != nil
        let frame = Self.introFrame(&intro, holdAt: hold)
        for id in frame.chirps {
            soundEngine.playPresentationCue(.presentation(audioId: IntroSequence.chirpCueId, sourceEntityId: id))
        }
#if DEBUG
        if let current = intro, current.frame == 1 || current.isFinished, !frame.held {
            Self.autopilotLog.notice("intro frame=\(current.frame, privacy: .public) finished=\(current.isFinished, privacy: .public) tick=\(self.session.simulation.state.tick, privacy: .public)")
        }
#endif
        if wasRunning { redraw() }
        return !frame.mayStep
    }

    /// One display frame of the D-098 intro gate, apart from the scene so it
    /// can be tested against a real session: while the intro runs, the frame
    /// advances it and the simulation may not step; on the first frame after
    /// it ends (or is skipped) the intro is cleared and stepping resumes.
    struct IntroFrame: Equatable {
        var mayStep: Bool
        var chirps: [EntityID]
        var held = false
    }

    nonisolated static func introFrame(_ intro: inout IntroSequence?, holdAt hold: Int? = nil) -> IntroFrame {
        guard var current = intro else { return IntroFrame(mayStep: true, chirps: []) }
        guard !current.isFinished else {
            intro = nil
            return IntroFrame(mayStep: true, chirps: [])
        }
        if let hold, current.frame >= hold {
            return IntroFrame(mayStep: false, chirps: [], held: true)
        }
        let chirps = current.advance()
        intro = current
        return IntroFrame(mayStep: false, chirps: chirps)
    }

    /// D-098: any touch skips the intro.
    @discardableResult
    func skipIntroIfRunning() -> Bool {
        guard var current = intro, !current.isFinished else { return false }
        current.skip()
        intro = current
        return true
    }

    /// § 10.2 / § 11 bookkeeping for a run that just ended: build the run card
    /// against the best stored *before* this run, then store this run if it
    /// beats that best. Presentation and local storage only.
    private func finishRunIfNeeded() {
        let state = session.simulation.state
        guard state.outcome.isTerminal, runCard == nil else { return }
        var bestTicks: UInt64?
        if let dailyRun,
           let stored = GhostStore.load(seed: dailyRun.seed),
           stored.identity == state.identity
        {
            bestTicks = stored.ticks
        }
        let storesBest = dailyRun != nil && !session.scenarioSeeded
        if storesBest, let record = GhostRecord(successfulRun: state, commands: session.commandLog) {
            GhostStore.storeIfBest(record)
        }
        // § 12: medals from this run's own events and terminal state, stored
        // beside the day's best under the same rule (a debug-seeded run is
        // never stored, so it never claims `NEW`).
        let medals = session.feel.earnedMedals(state)
        var newMedals: Set<Medal> = []
        if storesBest, let dailyRun {
            newMedals = MedalStore.record(earned: medals, seed: dailyRun.seed)
        }
        let card = RunCard(
            state: state,
            dateLabel: dailyRun?.day.label,
            bestTicks: bestTicks,
            storesBest: storesBest,
            medals: medals,
            newMedals: newMedals
        )
#if DEBUG
        Self.autopilotLog.notice("run card outcome=\(state.outcome.rawValue, privacy: .public) medals=\(medals.map(\.name).joined(separator: ","), privacy: .public) new=\(newMedals.map(\.name).sorted().joined(separator: ","), privacy: .public) takedowns=\(self.session.feel.takedowns.total, privacy: .public)")
#endif
        runCard = card
        hud.runCard = card
    }

    /// Loads today's best and verifies it off the main thread: a full replay
    /// is thousands of ticks. The ghost catches up to the live tick on attach.
    private func loadGhost() {
        ghost = nil
        ghostGeneration += 1
        guard settings.ghostEnabled,
              let dailyRun,
              let record = GhostStore.load(seed: dailyRun.seed)
        else { return }
        let generation = ghostGeneration
        let seed = dailyRun.seed
        Task.detached(priority: .utility) { [weak self] in
            let verified = GhostRun(record: record, liveIdentity: .current, liveSeed: seed)
            await self?.attachGhost(verified, generation: generation)
        }
    }

    private func attachGhost(_ verified: GhostRun?, generation: Int) {
        guard generation == ghostGeneration, settings.ghostEnabled, var verified else { return }
        verified.advance(to: session.simulation.state.tick)
        ghost = verified
    }

    func restartRun(seed: UInt64? = nil) {
        let nextSeed = seed ?? session.simulation.state.seed
        session.restartRun(seed: nextSeed)
        runCard = nil
        hud.runCard = nil
        loadGhost()
        soundEngine.reset()
        renderer.reset()
        combatFeedbackRenderer.reset()
        cameraFollow.reset()
        lastDisplayTime = nil
        lockdownTint.reset()
        court.reset()
        vfx.reset()
        nearMissEdges.reset()
        // Restart is not Start: the intro plays only after Start (D-098).
        intro = nil
        instrumentation.reset()
        // `GameSession.restartRun` zeroes the session's command, but the
        // controller holds its own copy and `applyController` overwrites the
        // session from it on the very next tick. A player who was holding the
        // stick when the run ended would otherwise carry that heading — and
        // that dead `stickTouch` binding — straight into the new run.
        controller.reset()
        terminalEvidenceStored = false
        redraw()
    }

    /// Sole UI selection boundary: accepts once, with neutral movement.
    @discardableResult
    func chooseUpgrade(_ index: UInt8) -> Bool {
        guard session.simulation.state.upgrade.pending,
              session.pendingUpgradeChoice == nil,
              upgradeSelection.submit(index) else { return false }
        clearGameplayInput()
        session.pendingUpgradeChoice = index
        return true
    }

    private func clearGameplayInput() {
        controller.reset()
        session.moveX = 0
        session.moveY = 0
        session.dodgePressed = false
    }

    // MARK: - Input

    private func token(_ touch: UITouch) -> TouchController.TouchToken {
        TouchController.TouchToken(id: ObjectIdentifier(touch))
    }

    /// Touch position in safe-rectangle point space.
    private func points(_ touch: UITouch) -> CGPoint? {
        guard let projector else { return nil }
        return projector.points(fromScenePoint: touch.location(in: cameraNode))
    }

    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        for touch in touches {
            guard let point = points(touch) else { continue }
            if beginTouch(token: token(touch), atPoints: point) { return }
        }
    }

    /// The production point-space boundary also exercised by PC-009 tests.
    /// True consumes the remainder of a touch batch (intro or terminal action).
    @discardableResult
    func beginTouch(token: TouchController.TouchToken, atPoints point: CGPoint) -> Bool {
        guard let projector else { return false }
        if skipIntroIfRunning() { return true }
        let snap = session.snapshot
        if snap.outcome.isTerminal {
            if hud.terminalRestartHit(atPoints: point, projector: projector) {
                restartRun()
            } else if hud.terminalShareHit(atPoints: point, projector: projector) {
                presentShare()
            }
            return true
        }
        // SwiftUI owns the protected selection surface. World taps are inert.
        if snap.upgradePending || runPaused { return true }
        if controller.began(token: token, atPoints: point, layout: hud.controlLayout ?? .empty) == .pause {
            onPauseRequested?()
        }
        return false
    }

    override func touchesMoved(_ touches: Set<UITouch>, with event: UIEvent?) {
        for touch in touches {
            guard let point = points(touch) else { continue }
            moveTouch(token: token(touch), toPoints: point)
        }
    }

    func moveTouch(token: TouchController.TouchToken, toPoints point: CGPoint) {
        guard !session.simulation.state.upgrade.pending, !runPaused else { return }
        guard let layout = hud.controlLayout else { return }
        controller.moved(token: token, toPoints: point, layout: layout)
    }

    override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent?) {
        for touch in touches { endTouch(token: token(touch)) }
    }

    override func touchesCancelled(_ touches: Set<UITouch>, with event: UIEvent?) {
        for touch in touches { endTouch(token: token(touch)) }
    }

    func endTouch(token: TouchController.TouchToken) {
        controller.ended(token: token)
    }

    /// § 11 Share: the system share sheet contains only the run card copy.
    private func presentShare() {
        guard let text = runCard?.shareText,
              let view,
              var presenter = view.window?.rootViewController
        else { return }
        while let next = presenter.presentedViewController { presenter = next }
        guard !(presenter is UIActivityViewController) else { return }
        let sheet = UIActivityViewController(activityItems: [text], applicationActivities: nil)
        if let popover = sheet.popoverPresentationController {
            popover.sourceView = view
            popover.sourceRect = CGRect(x: view.bounds.midX, y: view.bounds.midY, width: 1, height: 1)
        }
        presenter.present(sheet, animated: true)
    }

    /// The ghost as the renderer draws it, or nil when there is none to draw.
    private func ghostPresentation(liveTick: UInt64) -> WorldRenderer.Ghost? {
        guard let ghost else { return nil }
        let fade = ghost.fade(liveTick: liveTick, reducedMotion: settings.vfx.reducedMotion)
        guard fade > 0 else { return nil }
        let position = ghost.playerPosition
        return WorldRenderer.Ghost(
            position: CGPoint(x: position.x, y: position.y),
            fade: CGFloat(fade)
        )
    }

#if DEBUG
    /// `-SSHoldOnFeel <takedown|nearMiss|quietLost>:<frames>[:<nth>]` freezes the
    /// view that many frames after the first takedown, the first lit near-miss
    /// edge, or the D-101 `QUIET APPROACH LOST` caption, so a screenshot can
    /// catch it. Evidence harness only; all three are logged.
    private func noteFeelEvidence() {
        let feel = session.feel
        let tick = session.simulation.state.tick
        if !feel.lastTakedowns.isEmpty {
            Self.autopilotLog.notice("takedown tick=\(tick, privacy: .public) ids=\(feel.lastTakedowns.map(\.decimalString).joined(separator: ","), privacy: .public) streak=\(feel.takedowns.streak, privacy: .public)")
        }
        if !feel.nearMiss.isEmpty, !nearMissLogged {
            nearMissLogged = true
            Self.autopilotLog.notice("near miss tick=\(tick, privacy: .public) ids=\(feel.nearMiss.map(\.decimalString).joined(separator: ","), privacy: .public)")
        }
        let quietLost = session.quietFrame.caption == QuietApproachProjector.lostCopy
        if quietLost, !quietLostLogged {
            quietLostLogged = true
            Self.autopilotLog.notice("quiet approach lost tick=\(tick, privacy: .public) state=\(self.session.simulation.state.exposure.detectionState.rawValue, privacy: .public)")
        }
        guard !feelHoldArmed,
              let flag = ProcessInfo.processInfo.arguments.firstIndex(of: "-SSHoldOnFeel"),
              flag + 1 < ProcessInfo.processInfo.arguments.count
        else { return }
        let parts = ProcessInfo.processInfo.arguments[flag + 1].split(separator: ":")
        let kind = parts.first.map(String.init) ?? ""
        let frames = parts.count > 1 ? Int(parts[1]) ?? 0 : 0
        let hit = (kind == "takedown" && !feel.lastTakedowns.isEmpty)
            || (kind == "nearMiss" && !feel.nearMiss.isEmpty)
            || (kind == "quietLost" && quietLost)
        guard hit else { return }
        // An optional third part holds on the Nth occurrence instead.
        feelHoldSeen += 1
        let nth = parts.count > 2 ? Int(parts[2]) ?? 1 : 1
        guard feelHoldSeen >= nth else { return }
        feelHoldArmed = true
        Task { @MainActor [weak self] in
            try? await Task.sleep(nanoseconds: UInt64(max(0, frames)) * 16_666_667)
            self?.view?.isPaused = true
            Self.autopilotLog.notice("feel hold kind=\(kind, privacy: .public) after \(frames, privacy: .public) frames")
        }
    }

    /// `-SSHoldOnVFX <recipeId>:<frames>` freezes the view that many frames
    /// after the named recipe is first drawn, so a screenshot can catch an
    /// effect mid-flight. Evidence harness only; every drawn recipe is logged.
    private func configureVFXEvidence(_ arguments: [String]) {
        var hold: (recipe: String, frames: Int)?
        if let flag = arguments.firstIndex(of: "-SSHoldOnVFX"), arguments.index(after: flag) < arguments.endIndex {
            let parts = arguments[arguments.index(after: flag)].split(separator: ":")
            if let recipe = parts.first {
                hold = (String(recipe), parts.count > 1 ? Int(parts[1]) ?? 0 : 0)
            }
        }
        vfx.onAdmit = { [weak self] presentation in
            let tick = self?.session.simulation.state.tick ?? 0
            Self.autopilotLog.notice(
                "vfx tick=\(tick, privacy: .public) recipe=\(presentation.recipeId, privacy: .public) language=\(presentation.language, privacy: .public) hitStopMs=\(presentation.hitStopMs, privacy: .public) shake=\(presentation.screenShake, privacy: .public)"
            )
            guard let hold, presentation.recipeId == hold.recipe else { return }
            let frames = max(0, hold.frames)
            Task { @MainActor [weak self] in
                try? await Task.sleep(nanoseconds: UInt64(frames) * 16_666_667)
                self?.view?.isPaused = true
                Self.autopilotLog.notice("vfx hold recipe=\(hold.recipe, privacy: .public) after \(frames, privacy: .public) frames")
            }
        }
    }
#endif

    private func redraw() {
        presentationFrame &+= 1
        var snap = session.snapshot
        if snap.upgradePending && !upgradeSelection.isPresented { clearGameplayInput() }
        upgradeSelection.synchronize(pending: snap.upgradePending)
        // D-098: during the intro a Camera's field is drawn only once it has
        // powered on. Presentation copy of the snapshot; state is untouched.
        if let intro, !intro.isFinished {
            for index in snap.cameras.indices where !intro.isPowered(snap.cameras[index].id) {
                snap.cameras[index].fieldVisible = false
            }
        }
        cameraFollow.update(
            player: VecI(x: snap.player.x, y: snap.player.y),
            heading: session.simulation.state.player.facing,
            bounds: snap.arenaBounds,
            deltaTime: displayDelta
        )
        cameraNode.position = vfx.cameraPosition(base: CGPoint(x: cameraFollow.x ?? 0, y: cameraFollow.y ?? 0))
        nearMissEdges.update(
            snap,
            nearMiss: session.feel.nearMiss,
            frame: presentationFrame,
            reducedMotion: settings.vfx.reducedMotion
        )
        introOverlay.update(intro, dailyLabel: dailyRun?.titleLabel, headline: flavour?.headline)
        hud.objectiveCopy = session.feel.objectiveCopy
        hud.tutorialLine = intro.map { $0.isFinished } == false ? nil : session.feel.tutorialLine
        hud.takedownStreakCopy = session.feel.streakCopy
        renderer.render(
            snap,
            reducedMotion: settings.vfx.reducedMotion,
            ghost: ghostPresentation(liveTick: snap.tick)
        )
        combatFeedbackRenderer.update(snap, events: session.lastEvents, settings: settings.vfx)
        vfx.render(snap)
        lockdownTint.update(snap, settings: settings.vfx)
        court.update(snap, settings: settings.vfx)
        hud.knobOffsetPoints = controller.knobOffset
        hud.dodgePressed = controller.dodgeTouch != nil
        hud.captions = session.captionBoard.visible(at: snap.tick, setting: settings.captions)
        hud.reinforcementCopy = session.reinforcementCopy
        hud.quietFrame = session.quietFrame
        hud.awarenessHintCopy = session.awarenessHintCopy
        hud.render(snap, cameraHUD: session.cameraHUDProjection, paused: runPaused)
    }
}
