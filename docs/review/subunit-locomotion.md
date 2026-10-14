# BP-008 sub-unit locomotion correction

Specification pin: 262f4d66ddb271f5d4199be4ccfa130325f62221. Runtime implementation is in the commit containing this record.

Observed defect: Simulation records movedUnitsLastTick as the integer floor of actual distance. PresentationSnapshot uses zero in that counter to choose player_idle. At analog input ±2000/32767, unobstructed position changes by less than one world unit each tick, yet the old GameSession snapshot reports idle. The new regression reproduced three player_idle-versus-player_move failures before the implementation change; actual position-change and replay digest assertions passed.

GameSession now samples the exact fixed-point position before and after an advancing simulation tick. Its presentation snapshot uses that boolean only when the base clip is idle or move, before reaction overrides. Dodge, extraction and terminal clips are not replaced. No advancing tick leaves the prior sample intact; restart and debug scenario replacement clear it. The simulation distance counter, authoritative velocity, events and digest are unchanged. Standalone snapshots without position history retain their existing fallback; the real gameplay scene uses the session projection.

The regression drives the same commands through GameSession and a bare Simulation, checks digest equality, confirms the whole-unit counter stays zero, requires movement animation for actual sub-unit travel, returns to idle after neutral input, and verifies restart clears the motion sample. This fixes clip selection only; playback speed at partial input, source pose quality, contact slip and the full BP-008 movement matrix remain open.

Local exact-commit parity: all 21 contract/fixture files match the adopted spec, with the D-065 catalog pin exception; all four pin sources agree. Targeted core checks passed: 17 tests / 4 suites (ContractVersions, AssetCatalog, ClipTiming, ReactionClipTracker). Full core suite previously passed 764 tests at the timing foundation; it was not repeated for this app-only presentation fix and pin adoption.

Post-fix iOS simulator validation: 83 Swift Testing tests / 13 suites passed in 38.233 seconds, including the previously failing sub-unit regression; three XCTest checks also completed in the run. Destination: iPhone 17 Pro iOS 26.5 simulator. No physical-device testing.
