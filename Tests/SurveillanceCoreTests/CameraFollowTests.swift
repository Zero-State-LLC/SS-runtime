import Testing
@testable import SurveillanceCore

struct CameraFollowTests {
    let bounds = AABB(center: VecI(x: 1200, y: 800), halfSize: VecI(x: 1200, y: 800))
    @Test func turnDoesNotSnapByTheLookAheadDistance() throws {
        var camera = CameraFollow()
        let player = VecI(x: 1000, y: 800)
        for _ in 0..<120 { camera.update(player: player, heading: VecI(x: 1, y: 0).asQ8, bounds: bounds, deltaTime: 1.0 / 60) }
        let before = try #require(camera.x)
        camera.update(player: player, heading: VecI(x: -1, y: 0).asQ8, bounds: bounds, deltaTime: 1.0 / 60)
        let after = try #require(camera.x)
        #expect(before - after > 0 && before - after < 15)
    }
    @Test func motionInsideDeadZoneDoesNotMoveTheAnchor() throws {
        var camera = CameraFollow()
        camera.update(player: VecI(x: 1000, y: 800), heading: .zero, bounds: bounds, deltaTime: 1.0 / 60)
        camera.update(player: VecI(x: 1037, y: 824), heading: .zero, bounds: bounds, deltaTime: 1.0 / 60)
        #expect(camera.x == 1000 && camera.y == 800)
        camera.update(player: VecI(x: 1040, y: 826), heading: .zero, bounds: bounds, deltaTime: 1.0 / 60)
        #expect(try #require(camera.x) > 1000)
        #expect(try #require(camera.y) > 800)
    }
    @Test func verticalHeadingHasNoSpuriousHorizontalLookAhead() {
        var camera = CameraFollow()
        for _ in 0..<120 { camera.update(player: VecI(x: 1000, y: 800), heading: VecI(x: 0, y: 1).asQ8, bounds: bounds, deltaTime: 1.0 / 60) }
        #expect(camera.x == 1000)
        #expect((camera.y ?? 0) > 840)
    }
    @Test func clampsAndResetsAcrossRuns() {
        var camera = CameraFollow()
        camera.update(player: VecI(x: 0, y: 0), heading: .zero, bounds: bounds, deltaTime: 1)
        #expect(camera.x == 352 && camera.y == 163)
        camera.reset()
        camera.update(player: VecI(x: 1200, y: 900), heading: .zero, bounds: bounds, deltaTime: 0)
        #expect(camera.x == 1200 && camera.y == 900)
    }
}
