import Testing
@testable import SurveillanceCore

@Suite struct CombatFeedbackTests {
    private func hit(_ projectile: UInt64, _ target: UInt64, _ kind: String, x: Int64) -> AuthoritativeEvent {
        AuthoritativeEvent(tick: 4, phase: 9, type: .projectileHit, primary: EntityID(projectile),
            secondary: EntityID(target), payload: ["projectileId": .string(String(projectile)),
                "targetEntityId": .string(String(target)), "projectileKind": .string(kind),
                "impactXQ8": .integer(x), "impactYQ8": .integer(0)], insertion: 0)
    }
    @Test func unrelatedHitsNeverMakeAChain() throws {
        var projector = VFXProjector()
        let projection = projector.project(tick: 4, events: [hit(1, 10, "civicPulse", x: 0), hit(2, 11, "civicPulse", x: 100)], catalog: try .bundled())
        #expect(projection.presentations.allSatisfy { $0.recipeId != "ricochet" })
    }
    @Test func independentChainsRetainTheirOwnPoints() throws {
        var projector = VFXProjector()
        let events = [hit(1, 10, "civicPulse", x: 0), hit(2, 20, "civicPulse", x: 1000),
                      hit(2, 21, "ricochet", x: 1200), hit(1, 11, "ricochet", x: 200)]
        let chains = projector.project(tick: 4, events: events, catalog: try .bundled()).presentations.filter { $0.recipeId == "ricochet" }
        #expect(chains.count == 2)
        #expect(chains.map { $0.impactPoints.map { $0.x.raw } } == [[0, 200], [1000, 1200]])
    }
    @Test func incompleteOrDuplicateTargetChainDoesNotDraw() throws {
        var projector = VFXProjector()
        let events = [hit(1, 10, "ricochet", x: 0), hit(2, 20, "civicPulse", x: 0), hit(2, 20, "ricochet", x: 1)]
        #expect(projector.project(tick: 4, events: events, catalog: try .bundled()).presentations.allSatisfy { $0.recipeId != "ricochet" })
    }
    @Test func distinctDamageSourcesAreNotCoalescedTogether() throws {
        var projector = VFXProjector()
        let events = ["10", "11"].map { id in
            AuthoritativeEvent(tick: 1, phase: 12, type: .playerDamaged, primary: EntityID(1),
                payload: ["sourceEntityId": .string(id)], insertion: 0)
        }
        let effects = projector.project(tick: 1, events: events, catalog: try .bundled()).presentations
        #expect(effects.filter { $0.recipeId == "playerHit" }.count == 2)
    }
    @Test func copyStatesCorrectImmunityAndAmbush() {
        let card = UpgradePresentation.card(for: .ghostStep)
        #expect(card.numericSummary.contains("0.5 s"))
        #expect(card.numericSummary.contains("no damage immunity"))
        #expect(card.voiceOverLabel.contains("thirty ticks"))
        #expect(AwarenessHintProjector.copy.contains("TRIPLE DAMAGE"))
    }
}
