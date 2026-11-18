import XCTest

final class UpgradeInteractionTests: XCTestCase {
    @MainActor
    private func capture(_ app: XCUIApplication, _ name: String) {
        let attachment = XCTAttachment(screenshot: app.screenshot())
        attachment.name = name
        attachment.lifetime = .keepAlways
        add(attachment)
    }

    @MainActor
    private func exercise(argument: String?, target: String, index: Int, requiresScroll: Bool) throws {
        continueAfterFailure = false
        XCUIDevice.shared.orientation = .landscapeLeft
        let app = XCUIApplication()
        if let argument { app.launchArguments = [argument] }
        app.launch()
        defer { app.terminate() }
        let result = app.staticTexts["review-selection-result"]
        XCTAssertTrue(result.waitForExistence(timeout: 15))
        XCTAssertEqual(result.label, "selected=none;count=0")
        let scroll = app.scrollViews.firstMatch
        XCTAssertTrue(scroll.waitForExistence(timeout: 5))
        let choice = app.buttons["upgrade-\(target)"]
        let initiallyHittable = choice.exists && choice.isHittable
        capture(app, "\(target)-\(argument ?? "default")-before")
        var swipes = 0
        while !(choice.exists && choice.isHittable) && swipes < 40 {
            scroll.swipeUp()
            swipes += 1
        }
        XCTAssertTrue(choice.exists && choice.isHittable, "Last upgrade must be reachable by actual swipes")
        if requiresScroll {
            XCTAssertFalse(initiallyHittable)
            XCTAssertGreaterThan(swipes, 0)
        }
        XCTAssertFalse(choice.label.isEmpty)
        XCTAssertEqual(result.label, "selected=none;count=0", "Scrolling must not select")
        let spokenLabel = choice.label
        capture(app, "\(target)-\(argument ?? "default")-reachable")
        choice.tap()
        let selected = NSPredicate(format: "label == %@", "selected=\(index);count=1")
        expectation(for: selected, evaluatedWith: result)
        waitForExpectations(timeout: 5)
        XCTAssertFalse(choice.isEnabled, "Production model disables repeated submission")
        capture(app, "\(target)-\(argument ?? "default")-selected")
        let record: [String: Any] = [
            "status": "ACTUAL_XCUI_INTERACTION_ISOLATED_PRODUCTION_VIEW_NOT_FULL_GAME",
            "dynamicTypeArgument": argument ?? "default-large",
            "target": target, "selectionIndex": index, "swipes": swipes,
            "initiallyHittable": initiallyHittable, "selectionResult": result.label,
            "accessibilityLabel": spokenLabel,
            "windowWidth": app.windows.firstMatch.frame.width,
            "windowHeight": app.windows.firstMatch.frame.height,
            "voiceOverSession": false, "physicalDevice": false,
            "gameResumeVerified": false
        ]
        let attachment = XCTAttachment(data: try JSONSerialization.data(withJSONObject: record, options: [.prettyPrinted, .sortedKeys]), uniformTypeIdentifier: "public.json")
        attachment.name = "upgrade-interaction-\(argument ?? "default")"
        attachment.lifetime = .keepAlways
        add(attachment)
    }

    @MainActor func testDefaultTouchSelectsFirst() throws {
        try exercise(argument: nil, target: "signalJammer", index: 0, requiresScroll: false)
    }
    @MainActor func testAccessibility3ScrollsToLastAndSelects() throws {
        try exercise(argument: "--accessibility3", target: "ghostStep", index: 2, requiresScroll: true)
    }
    @MainActor func testAccessibility5ScrollsToLastAndSelects() throws {
        try exercise(argument: "--accessibility5", target: "ghostStep", index: 2, requiresScroll: true)
    }
}
