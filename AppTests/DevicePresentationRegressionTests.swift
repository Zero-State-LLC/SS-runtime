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
}
