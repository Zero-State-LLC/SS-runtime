import CryptoKit
import SpriteKit
import SwiftUI
import UIKit
import XCTest
@testable import SSRuntime
@testable import SurveillanceCore

#if DEBUG
/// Slice10, accepted intent/2026-11-16-benchmark-faithful-scene.md, BP-001–BP-012.
/// Static existing-art diagnostics only. No benchmark injection or production changes.
final class ExistingArtViewportTests: XCTestCase {
    private struct Fixture {
        let name: String
        let size: CGSize
        let insets: UIEdgeInsets
    }

    // Safe sizes come from HUDLayout and HUDMappingTests. Insets are synthetic,
    // NOT observations of a particular device, notch, OS or orientation.
    private var fixtures: [Fixture] {
        [Fixture(name: "se", size: CGSize(width: 667, height: 375), insets: .zero),
         Fixture(name: "reference", size: CGSize(width: 844, height: 390), insets: .zero),
         Fixture(name: "inset", size: CGSize(width: 844, height: 390),
                 insets: UIEdgeInsets(top: 0, left: 47, bottom: 8, right: 47))]
    }

    @MainActor private final class InsetView: SKView {
        var diagnosticInsets: UIEdgeInsets = .zero
        override var safeAreaInsets: UIEdgeInsets { diagnosticInsets }
    }

    private func sha(_ bytes: Data) -> String {
        SHA256.hash(data: bytes).map { String(format: "%02x", $0) }.joined()
    }

    /// Broad reachable PNG inventory, NOT proof each file was drawn. Fail if the
    /// resolver falls back to workspace source rather than a built bundle.
    private func resources() throws -> [[String: Any]] {
        let catalog = try AssetCatalog.bundled()
        let reachable = try RuntimeBundleFilter.reachableAssetIds()
        var records: [[String: Any]] = []
        for entry in catalog.entries.sorted(by: { $0.record.assetId < $1.record.assetId }) {
            guard reachable.contains(entry.record.assetId),
                  entry.admissionDecision == .adaptedAdmitted || entry.admissionDecision == .originalAccepted,
                  let path = entry.record.runtimePath, path.lowercased().hasSuffix(".png") else { continue }
            let url = try XCTUnwrap(RuntimeAssetBundle.url(forFile: path), path)
            XCTAssertTrue(url.path.contains(".bundle/") || url.path.contains(".app/"),
                          "Workspace fallback is not bundled provenance: \(path)")
            let data = try Data(contentsOf: url)
            records.append(["assetID": entry.record.assetId, "path": path,
                            "sha256": sha(data), "bytes": data.count])
        }
        XCTAssertFalse(records.isEmpty)
        return records
    }

    private func attachJSON(_ record: [String: Any], name: String) throws {
        let data = try JSONSerialization.data(withJSONObject: record, options: [.prettyPrinted, .sortedKeys])
        let attachment = XCTAttachment(data: data, uniformTypeIdentifier: "public.json")
        attachment.name = name
        attachment.lifetime = .keepAlways
        add(attachment)
    }

    @MainActor private func attachPNG(_ image: UIImage, name: String) throws -> [String: Any] {
        let data = try XCTUnwrap(image.pngData())
        let cg = try XCTUnwrap(image.cgImage)
        // Attach the same bytes we hash, avoiding an independent UIImage encoding.
        let attachment = XCTAttachment(data: data, uniformTypeIdentifier: "public.png")
        attachment.name = name
        attachment.lifetime = .keepAlways
        add(attachment)
        return ["attachment": name, "sha256": sha(data), "pixels": [cg.width, cg.height]]
    }

    @MainActor
    func testExistingArtViewportEvidence() throws {
        let inventory = try resources()
        var records: [[String: Any]] = []
        for fixture in fixtures {
            for accessible in [false, true] {
                let view = InsetView(frame: CGRect(origin: .zero, size: fixture.size))
                view.diagnosticInsets = fixture.insets
                view.isPaused = true
                let session = GameSession(seed: 1)
                let scene = GameScene(size: fixture.size, session: session)
                view.presentScene(scene)
                defer { view.presentScene(nil) }
                var settings = PresentationSettings.defaults
                settings.audio = .init(effectsEnabled: false, hapticsEnabled: false, musicEnabled: false)
                settings.hudScale = accessible ? .extraLarge : .standard
                settings.vfx.reducedMotion = accessible
                settings.ghostEnabled = false
                scene.apply(settings: settings)
                _ = scene.skipIntroIfRunning()
                scene.update(1)
                // One manually stepped frame, not post-action/live-cadence evidence.
                let camera = try XCTUnwrap(scene.camera)
                let hudRoots = camera.children.filter { $0.zPosition == 1000 }
                XCTAssertEqual(hudRoots.count, 1)
                let player = try XCTUnwrap(scene.childNode(withName: "//sprite-player") as? SKSpriteNode)
                XCTAssertNotNil(player.texture)
                let layout = try XCTUnwrap(scene.controlLayout)
                let safe = CGRect(x: 0, y: 0,
                    width: fixture.size.width - fixture.insets.left - fixture.insets.right,
                    height: fixture.size.height - fixture.insets.top - fixture.insets.bottom)
                // Existing controls already have rule tests. Record actual produced
                // layout here instead of inventing a pixel-fit/visual tolerance.
                let crop = CGRect(x: camera.position.x - scene.size.width / 2,
                    y: camera.position.y - scene.size.height / 2,
                    width: scene.size.width, height: scene.size.height)
                let texture = try XCTUnwrap(view.texture(from: scene, crop: crop))
                let source = UIImage(cgImage: texture.cgImage())
                let fit = min(fixture.size.width / scene.size.width, fixture.size.height / scene.size.height)
                let fitted = CGSize(width: scene.size.width * fit, height: scene.size.height * fit)
                let format = UIGraphicsImageRendererFormat()
                format.scale = 1
                format.opaque = true
                let image = UIGraphicsImageRenderer(size: fixture.size, format: format).image { context in
                    UIColor.black.setFill()
                    context.fill(CGRect(origin: .zero, size: fixture.size))
                    source.draw(in: CGRect(x: (fixture.size.width - fitted.width) / 2,
                        y: (fixture.size.height - fitted.height) / 2, width: fitted.width, height: fitted.height))
                }
                let name = "viewport-\(fixture.name)-\(accessible ? "xl-reduced" : "standard")"
                var record = try attachPNG(image, name: name)
                record["fixture"] = fixture.name
                record["kind"] = "GameScene-offscreen-aspectFit"
                record["logicalSize"] = [fixture.size.width, fixture.size.height]
                record["syntheticInsetsTLBR"] = [fixture.insets.top, fixture.insets.left,
                                                 fixture.insets.bottom, fixture.insets.right]
                record["safeSize"] = [safe.width, safe.height]
                record["hudScale"] = settings.hudScale.rawValue
                record["reducedMotion"] = accessible
                record["tick"] = scene.currentTick
                record["hudChildCount"] = hudRoots[0].children.count
                record["dodgeRect"] = [layout.dodgeRect.minX, layout.dodgeRect.minY,
                                        layout.dodgeRect.width, layout.dodgeRect.height]
                record["pauseRect"] = [layout.pauseRect.minX, layout.pauseRect.minY,
                                        layout.pauseRect.width, layout.pauseRect.height]
                record["playerTexturePixels"] = [player.texture!.cgImage().width, player.texture!.cgImage().height]
                records.append(record)
            }
        }
        // Actual production SwiftUI choice surface hosted in a window, not a
        // reconstructed label/card drawing. Existing tests own column/choice rules.
        for fixture in fixtures.prefix(2) {
            for accessible in [false, true] {
                let model = UpgradeSelectionModel()
                model.synchronize(pending: true)
                var choices = 0
                let host = UIHostingController(rootView: UpgradeSelectionView(model: model,
                    onChoose: { _ in choices += 1 })
                    .environment(\.dynamicTypeSize, accessible ? .accessibility3 : .large))
                let window = UIWindow(frame: CGRect(origin: .zero, size: fixture.size))
                window.rootViewController = host
                window.makeKeyAndVisible()
                defer { window.isHidden = true }
                host.view.frame = window.bounds
                host.view.setNeedsLayout()
                host.view.layoutIfNeeded()
                let format = UIGraphicsImageRendererFormat()
                format.scale = 1
                let image = UIGraphicsImageRenderer(size: fixture.size, format: format).image { _ in
                    XCTAssertTrue(host.view.drawHierarchy(in: host.view.bounds, afterScreenUpdates: true))
                }
                XCTAssertFalse(model.submitted)
                XCTAssertEqual(choices, 0)
                let name = "upgrade-\(fixture.name)-\(accessible ? "ax3" : "large")"
                var record = try attachPNG(image, name: name)
                record["kind"] = "hosted-production-UpgradeSelectionView"
                record["dynamicType"] = accessible ? "accessibility3" : "large"
                record["logicalSize"] = [fixture.size.width, fixture.size.height]
                record["logicalSizeRole"] = "requested-output-canvas-not-host"
                record["requestedSize"] = [fixture.size.width, fixture.size.height]
                record["hostViewBounds"] = [host.view.bounds.minX, host.view.bounds.minY,
                    host.view.bounds.width, host.view.bounds.height]
                record["windowBounds"] = [window.bounds.minX, window.bounds.minY,
                    window.bounds.width, window.bounds.height]
                record["captureMapping"] = "drawHierarchy at host bounds into requested-size canvas, clipped if larger, no resize"
                record["observedInsetsTLBR"] = [host.view.safeAreaInsets.top, host.view.safeAreaInsets.left,
                    host.view.safeAreaInsets.bottom, host.view.safeAreaInsets.right]
                records.append(record)
            }
        }
        XCTAssertEqual(records.count, 10)
        try attachJSON(["schema": "existing-art-viewports-001", "captures": records,
            "resourceInventory": inventory,
            "resourceScope": "reachable bundled PNG superset, not per-node consumption or executed-source attestation",
            "unsupported": ["physical-device operation", "VoiceOver focus or speech", "Switch Control interaction",
                "upgrade scroll reachability", "Dynamic Type applied to SpriteKit HUD", "terminal/settings/title surfaces",
                "live cadence", "orientation transitions", "visual benchmark acceptance", "coherent-source acceptance"]],
            name: "existing-art-viewports-records")
    }
}
#endif
