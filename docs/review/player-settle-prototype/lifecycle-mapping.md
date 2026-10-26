# Settling integration mapping — review-only prototype

Current behavior inspected 2026-10-19:
- Sources/SurveillanceCore/Presentation/PresentationSnapshot.swift: playerClip chooses terminal outcome, Dodge, Extraction, then idle/move.
- App/GameScene.swift: GameSession.snapshot corrects sub-unit movement classification only for idle/move, then applies reactions.
- Sources/SurveillanceCore/Presentation/ReactionClipTracker.swift: apply and mayInterrupt preserve cancellation windows and occurrence lifetime.
- App/WorldRenderer.swift: renderActors attempts eligible reaction art first, then the live state; playClip owns texture actions and occurrence identity.

The review-only settle is an optional idle-only presentation layer beneath those selections, with separate diagnostics and no mutation of snapshot/player state. WorldRenderer now contains an opt-in prototype; no sequences are installed by default. Full lifecycle requirements live in benchmark-production.md. User feedback: half-second source settle is better, but too slow. A 0.25-second comparison preserves the same 17 poses, contact geometry and 32fps walking cadence. Timing remains proposed pending review. Native cancellation regression verification is tracked separately.
