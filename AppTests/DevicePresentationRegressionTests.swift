import SpriteKit
import Testing
@testable import SSRuntime
@testable import SurveillanceCore

@Suite(.serialized)
@MainActor
struct DevicePresentationRegressionTests {
    @Test func cameraFieldStartsAtEmitterAndStopsAtCover() throws {
        let simulation = try Simulation.make(seed: 1)
        var camera = try #require(PresentationSnapshot(simulation.state).cameras.first)
        camera.x = 0; camera.y = 0
        camera.fieldOrigin = VecI(x: 30, y: 0).asQ8
        camera.range = 200; camera.headingMilli = 0; camera.fieldAngleMilli = 90_000
        let wall = AABB(center: VecI(x: 110, y: 0), halfSize: VecI(x: 10, y: 200))
        let path = CameraFieldGeometry.path(.init(camera: camera, solids: [wall]))
        #expect(!path.contains(CGPoint(x: 10, y: 0)))
        #expect(path.contains(CGPoint(x: 80, y: 0)))
        #expect(!path.contains(CGPoint(x: 120, y: 0)))
        let open = CameraFieldGeometry.path(.init(camera: camera, solids: []))
        #expect(open.contains(CGPoint(x: 120, y: 0)))
    }

    @Test func cameraUsesClockwiseHeadingAndNarrowCornerOcclusion() throws {
        var camera = try #require(PresentationSnapshot(Simulation.make(seed: 1).state).cameras.first)
        camera.fieldOrigin = VecI(x: 0, y: 0).asQ8
        camera.headingMilli = 90_000; camera.fieldAngleMilli = 90_000; camera.range = 240
        let path = CameraFieldGeometry.path(.init(camera: camera, solids: []))
        #expect(path.contains(CGPoint(x: 0, y: -100)))
        #expect(!path.contains(CGPoint(x: 0, y: 100)))
        camera.headingMilli = 0
        let narrow = AABB(center: VecI(x: 100, y: 7), halfSize: VecI(x: 2, y: 1))
        let clipped = CameraFieldGeometry.path(.init(camera: camera, solids: [narrow]))
        #expect(!clipped.contains(CGPoint(x: 200, y: 14)))
        #expect(clipped.contains(CGPoint(x: 200, y: -14)))
    }

    @Test func snapshotPreservesAuthoritativeEmitterPosition() throws {
        let simulation = try Simulation.make(seed: 1)
        let snapshot = PresentationSnapshot(simulation.state)
        for camera in snapshot.cameras {
            let source = try #require(simulation.state.cameras.first { $0.entityId == camera.id })
            #expect(camera.fieldOrigin == source.fieldOrigin)
        }
    }

    @Test func cameraFieldRebuildsWhenCoverChanges() throws {
        var snapshot = PresentationSnapshot(try Simulation.make(seed: 1).state)
        var camera = try #require(snapshot.cameras.first)
        camera.fieldOrigin = .zero; camera.x = 0; camera.y = 0
        camera.headingMilli = 0; camera.range = 240; camera.fieldAngleMilli = 90_000
        camera.fieldVisible = true
        snapshot.cameras = [camera]; snapshot.captainField = nil
        snapshot.solids = []; snapshot.solidIds = []
        let renderer = WorldRenderer()
        renderer.render(snapshot)
        let field = try #require(renderer.root.childNode(withName: "//field-\(camera.id.raw)") as? SKShapeNode)
        #expect(try #require(field.path).contains(CGPoint(x: 180, y: 0)))
        snapshot.solids = [AABB(center: VecI(x: 100, y: 0), halfSize: VecI(x: 10, y: 300))]
        snapshot.solidIds = ["qa-wall"]
        renderer.render(snapshot)
        #expect(!(try #require(field.path)).contains(CGPoint(x: 180, y: 0)))
    }

    @Test func returningCameraReattachesItsAnimation() throws {
        var snapshot = PresentationSnapshot(try Simulation.make(seed: 1).state)
        let camera = try #require(snapshot.cameras.first)
        snapshot.cameras = [camera]
        let renderer = WorldRenderer()
        renderer.render(snapshot)
        let name = "//sprite-camera-\(camera.id.raw)"
        let first = try #require(renderer.root.childNode(withName: name) as? SKSpriteNode)
        #expect(first.hasActions())
        snapshot.cameras = []
        renderer.render(snapshot)
        #expect(renderer.root.childNode(withName: name) == nil)
        snapshot.cameras = [camera]
        renderer.render(snapshot)
        let returned = try #require(renderer.root.childNode(withName: name) as? SKSpriteNode)
        #expect(returned !== first)
        #expect(returned.hasActions())
    }

    @Test func isolatedSlowFramesAreNotASustainedStreak() {
        let collector = FrameTimeCollector()
        var time = 0.0
        collector.recordFrame(timestamp: time)
        for ms in [40.0, 16, 40, 16, 40] {
            time += ms / 1000
            collector.recordFrame(timestamp: time)
        }
        #expect(!collector.summarize().sustainedBelowFloorFps)
        for _ in 0..<3 { time += 0.05; collector.recordFrame(timestamp: time) }
        #expect(collector.summarize().sustainedBelowFloorFps)
    }
    @Test func solidFootprintsRemainVisibleAcrossTransparentArt() throws {
        let snapshot = PresentationSnapshot(try Simulation.make(seed: 1).state)
        let renderer = WorldRenderer()
        renderer.render(snapshot)
        for (index, box) in snapshot.solids.enumerated() {
            let id = snapshot.solidIds[index]
            guard !id.hasPrefix(SelectedCamera.mountSolidPrefix), !snapshot.gateIds.contains(id) else { continue }
            let foundation = try #require(renderer.root.childNode(withName: "//solid-footprint-\(id)") as? SKShapeNode)
            #expect(foundation.fillColor.cgColor.alpha == 1)
            #expect(foundation.path?.boundingBox.width == CGFloat(box.halfSize.x * 2))
            #expect(foundation.path?.boundingBox.height == CGFloat(box.halfSize.y * 2))
        }
    }

    @Test func cameraHousingAndHeadUseTheSameGroundAnchor() throws {
        let snapshot = PresentationSnapshot(try Simulation.make(seed: 1).state)
        let renderer = WorldRenderer()
        renderer.render(snapshot)
        for camera in snapshot.cameras where camera.housingFamily != nil {
            let housing = try #require(renderer.root.childNode(withName: "//housing-\(camera.id.raw)") as? SKSpriteNode)
            let head = try #require(renderer.root.childNode(withName: "//sprite-camera-\(camera.id.raw)") as? SKSpriteNode)
            #expect(housing.anchorPoint == head.anchorPoint)
            #expect(head.texture != nil) // Visible even before SKActions evaluate.
        }
    }

    @Test func damageDiagnosticsPreserveRemovedMineAndUnknownSources() throws {
        var before = try Simulation.make(seed: 1).state
        let owner = EntityID(900)
        before.mines = [MineBody(id: EntityID(901), ownerId: owner,
            position: before.player.position, armRemaining: 0, lifeRemaining: 50, radius: 24, damage: 5)]
        var after = before
        after.mines = []
        let event = AuthoritativeEvent(tick: 1, phase: 12, type: .playerDamaged,
            primary: before.player.id, secondary: owner,
            payload: ["amount": .integer(5)], insertion: 0)
        let hit = try #require(DamageDiagnostic.capture(before: before, after: after, events: [event]).first)
        #expect(hit.sourceID == owner.raw)
        #expect(hit.amount == 5)
        #expect(hit.candidates.first?.kind == "removed-mine")
        #expect(hit.candidates.first?.id == 901)
        let unknown = AuthoritativeEvent(tick: 1, phase: 12, type: .playerDamaged,
            secondary: EntityID(999), insertion: 1)
        #expect(DamageDiagnostic.capture(before: before, after: after, events: [unknown]).first?.classification == "unresolved-source")
        #expect(try JSONDecoder().decode(DamageDiagnostic.self, from: JSONEncoder().encode(hit)) == hit)
    }

    @Test func diagnosticsNeverChangeAuthorityAndResetWithRun() {
        let observed = GameSession(seed: 1)
        let control = GameSession(seed: 1)
        observed.damageDiagnosticsEnabled = true
        for _ in 0..<120 { observed.step(); control.step() }
        #expect(observed.simulation.state.digest() == control.simulation.state.digest())
        #expect(observed.commandLog == control.commandLog)
        observed.restartRun()
        #expect(observed.damageDiagnostics.isEmpty)
        #expect(observed.latestDamageDiagnostics.isEmpty)
        #expect(observed.droppedDamageDiagnostics == 0)
    }

    @Test func pausingFreezesWorldActionsWithoutAdvancingTicks() throws {
        let view = SKView(frame: CGRect(x: 0, y: 0, width: 844, height: 390))
        view.isPaused = true
        let scene = GameScene(size: view.bounds.size)
        view.presentScene(scene)
        defer { view.presentScene(nil) }
        let sprite = try #require(scene.childNode(withName: "//sprite-player"))
        var world = sprite
        while let parent = world.parent, parent !== scene { world = parent }
        scene.setPaused(true)
        let tick = scene.currentTick
        scene.update(1)
        #expect(world.isPaused)
        #expect(scene.currentTick == tick)
        scene.setPaused(false)
        #expect(!world.isPaused)
    }

}
