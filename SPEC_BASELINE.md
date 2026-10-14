# Specification Baseline

Status: PINNED

| Identity | Value |
|---|---|
| Specification repository | `scrimshawlife-ctrl/SS-specs` |
| Specification commit | `9a87f95ae52f3f174392418e333573a56c04100a` |
| Ruleset | `ss-rules-008` |
| Content | `civic-seam-content-006` |
| Arena | `civic-seam-arena-004` |
| Replay schema | `runtime-kernel-001` |

Changing any pinned identity requires:

1. an adopted SS-specs commit;
2. affected contract and task IDs;
3. fixture review;
4. an explicit version migration or fail-closed incompatibility;
5. this file and `ContractVersions.swift` updated together.

Legacy evidence is frozen at `scrimshawlife-ctrl/Surveillance-Survivor@3b20d88d6a6e1fe8f07f45f581359d371fa65d98`. Copying legacy files is prohibited. Bounded reimplementation must follow `legacy-admission.md`.

D-102 adoption: [SS-specs PR #61](https://github.com/Zero-State-LLC/SS-specs/pull/61). Merge the specification before this runtime change. Ruleset-006 replays fail closed; fixture review is in `docs/review/D102.md`.

D-103 candidate adoption: combat-causality.md, T1030–T1034, CC-001–CC-007. Ruleset-007 replays fail closed. Fixture review: docs/review/D103.md. The paired spec branch must merge before the runtime PR; no release merge is claimed.

T1035 / CC-008 phase-3 adoption: weapon/upgrade presentation and protected SwiftUI choice overlay. Presentation evidence stays outside authoritative state; no ruleset, content, arena, event or fixture identity change. Art/device acceptance remains open.

D-104 / BP-001–BP-006 candidate adoption: shared benchmark production contract, T1042–T1046. The exact spec pin now includes source/frame delivery, named 16-frame locomotion scope, persistent Camera states, geometry evidence and staged asset migration. This pin adoption does not declare existing art compliant. Ruleset/content/arena/clip/fixture identities remain unchanged until accepted production assets require a presentation migration. Open runtime gaps and evidence are recorded in `docs/review/D104.md`; spec PR #62 must land before the dependent runtime PR.

BP-007 candidate adoption adds resolution/framing comparisons and explicit ground registration evidence. Gameplay identities and contract/fixture payloads remain unchanged. The reviewed composition remains a test fixture, not admitted production art.

BP-003 timing foundation adoption: exact duration design in animation-timing-migration.md. Existing v1 clips adapt into a shared duration model; no v2 production metadata or new art is admitted. Evidence and remaining migration work: docs/review/animation-timing-foundation.md.

BP-008 adoption: gait/displacement evidence and exact post-collision position sampling for sub-unit locomotion. No controller or digest changes. See docs/review/subunit-locomotion.md.

BP-004 damage marker adoption: persistent world-space damage-stage notches, distinct from HUD remaining integrity. Static Reduced Motion behavior and destruction/removal reconciliation verified. See docs/review/camera-damage-markers/review.md. Camera animation and art acceptance remain open.

BP-005/BP-007 ground-plan clarification adoption: distinguish wall contacts from baked walkable apron; unknown hidden corners cannot be inferred from roof or alpha bounds. No arena, collision or production art change. Study evidence: docs/review/building-wall-study/review.md.

BP-009 adoption: occlusion must preserve Player ground position and solid-boundary readability without false elevation. Lifecycle and continuous/encounter acceptance remain open; current treatments are comparison fixtures only. See docs/review/ground-cue/review.md.

BP-003 target-schema adoption: clip-metadata-002.schema.json and mechanical conversion checks define the next decoder target. Active metadata, animation version, frame IDs and gameplay identities remain v1/current. No v2 delivery or new art is admitted.
