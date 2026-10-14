import Foundation
import Testing
@testable import SurveillanceCore

struct ClipMetadataV2Tests {
    private func converted(_ mutate: (inout [[String: Any]]) -> Void = { _ in }) throws -> Data {
        var root = try JSONSerialization.jsonObject(with: SpecBundle.contract("clip-metadata-001")) as! [String: Any]
        root["schemaVersion"] = "clip-metadata-002"
        var clips = root["clips"] as! [[String: Any]]
        for i in clips.indices {
            let fps = clips[i].removeValue(forKey: "framesPerSecond") as! Int
            let count = (clips[i]["frameIds"] as! [String]).count
            clips[i]["timing"] = ["unitsPerSecond": fps, "frameUnits": Array(repeating: 1, count: count)]
        }
        mutate(&clips); root["clips"] = clips
        return try JSONSerialization.data(withJSONObject: root)
    }

    @Test func everyV1FacingHasIdenticalV2TimingAndFrames() throws {
        let before = try ClipCatalog.bundled()
        let data = try converted()
        let after = try ClipCatalogLoader.decode(data)
        let library = try ClipFrameLibrary.make(clipJSON: data, catalog: AssetCatalog.bundled())
        #expect(after.schemaVersion == "clip-metadata-002")
        #expect(after.clips.count == before.clips.count)
        for (old, new) in zip(before.clips, after.clips) {
            var restored = new
            restored.framesPerSecond = old.framesPerSecond
            restored.authoredTiming = nil
            #expect(restored == old)
            #expect(new.framesPerSecond == nil)
            #expect(new.frameIds == old.frameIds)
            #expect(new.anchor == old.anchor)
            #expect(new.loop == old.loop)
            #expect(new.authoritativeEventMarker == old.authoritativeEventMarker)
            #expect(new.cancelWindows == old.cancelWindows)
            for facing in old.directions.isEmpty ? ["none"] : old.directions {
                let expected = try old.timing(forDirection: facing)
                #expect(try new.timing(forDirection: facing) == expected)
                #expect(library.timing(clipId: new.clipId, direction: facing) == expected)
                #expect(library.frameIds(clipId: new.clipId, direction: facing) == old.frameIds(forDirection: facing))
            }
        }
    }

    @Test func interleavedFacingsKeepTheirOwnVariableHolds() throws {
        let data = try converted { clips in
            let original = clips[0]["frameIds"] as! [String]
            let groups = ClipCatalog.fourDirections.map { dir in original.filter { $0.contains("_\(dir)_") } }
            clips[0]["frameIds"] = (0..<groups[0].count).flatMap { i in groups.map { $0[i] } }
            clips[0]["timing"] = ["unitsPerSecond": 24,
                                   "frameUnits": (0..<groups[0].count).flatMap { _ in [1,2,3,4] }]
        }
        let clip = try #require(ClipCatalogLoader.decode(data).clips.first)
        let library = try ClipFrameLibrary.make(clipJSON: data, catalog: AssetCatalog.bundled())
        for (direction, hold, ticks) in [("n",1,10),("e",2,20),("s",3,30),("w",4,40)] {
            let timing = try clip.timing(forDirection: direction)
            #expect(timing.frameUnits == Array(repeating: hold, count: 4))
            #expect(try timing.durationTicks(at: 60) == UInt64(ticks))
            #expect(library.timing(clipId: clip.clipId, direction: direction) == timing)
        }
        #expect(library.timing(clipId: clip.clipId, direction: "invalid") == nil)
    }

    @Test func malformedV2FailsThroughBothLoaders() throws {
        let catalog = try AssetCatalog.bundled()
        let mutations: [(inout [[String: Any]]) -> Void] = [
            { $0[0]["framesPerSecond"] = 12 },
            { $0[0].removeValue(forKey: "timing") },
            { $0[0]["timing"] = ["unitsPerSecond": true, "frameUnits": [1]] },
            { $0[0]["timing"] = ["unitsPerSecond": 0, "frameUnits": Array(repeating: 1, count: 16)] },
            { $0[0]["timing"] = ["unitsPerSecond": 12, "frameUnits": Array(repeating: 1.5, count: 16)] },
            { $0[0]["timing"] = ["unitsPerSecond": 12, "frameUnits": Array(repeating: false, count: 16)] },
            { $0[0]["timing"] = ["unitsPerSecond": 12, "frameUnits": Array(repeating: -1, count: 16)] },
            { $0[0]["timing"] = ["unitsPerSecond": 12, "frameUnits": Array(repeating: Int.max, count: 16)] },
            { $0[0]["timing"] = ["unitsPerSecond": 12, "frameUnits": Array(repeating: Int.max / 16, count: 16)] },
            { $0[0]["timing"] = ["unitsPerSecond": 12, "frameUnits": [1]] },
            { $0[0]["timing"] = ["unitsPerSecond": 12, "frameUnits": Array(repeating: 1, count: 16), "extra": 1] }
        ]
        for mutate in mutations {
            let data = try converted(mutate)
            #expect(throws: (any Error).self) { try ClipCatalogLoader.decode(data) }
            #expect(throws: (any Error).self) { try ClipFrameLibrary.make(clipJSON: data, catalog: catalog) }
        }
    }
}
