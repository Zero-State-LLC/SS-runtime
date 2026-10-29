# Specification Baseline

Status: PINNED

| Identity | Value |
|---|---|
| Specification repository | `scrimshawlife-ctrl/SS-specs` |
| Specification commit | `0f0fb95fd84a9b0e85009500038310698e169797` |
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

BP-003 event-facing adoption: one-shot occurrences carry event-facing/start tick, select exact lifetime and tick-sampled frames, preserve live-state fallback and expire without extension. Core and simulator evidence: docs/review/reaction-occurrence/review.md. Visual turning acceptance and active v2 delivery migration remain open.

BP-002 controlled-source pilot adoption: editable character rig and measured contact/limb continuity experiment, followed by benchmark costume/facing and renderer gates. A rig scaffold is not admitted art; production resources and gameplay identities stay unchanged.

BP-007 high-resolution outline clarification adoption: explicit source-pixel/logical-mask separation, constant equal-framing faction treatment, post-action frame correctness and bounded allocation/cache evidence. Runtime #124 remains open; pin adoption alone does not fix or accept 384px production assets.

BP-010 comparison adoption: compare existing, reduced-opacity and absent Player border in the benchmark fixture before selecting painted-art contrast. Normal play retains D-094; gameplay identities and contract payloads apart from the specification pin remain unchanged.

BP-002 layered-source clarification adoption: setup-pose part ownership, preserved costume proportions, authored hidden overlaps and joint-range review precede the south cycle. Pin adoption does not admit the partial layered study. See docs/review/layered-source/review.md. Gameplay identities, active clips, fixtures and production textures remain unchanged.

BP-002/BP-008 elevated-motion clarification adoption: source/anatomical measurements are distinct from projected lengths; layered motion requires reviewed depth treatment and authored foot contacts. The eight-joint source scaffold is not a gait. Gameplay identities, fixtures and active artwork remain unchanged. See docs/review/projected-motion/review.md.

BP-008 displayed-playback clarification adoption: source, exported-frame and actual displayed contact are distinct evidence. Moving benchmark observations must retain playback and record post-action frame identity with authoritative and rendered positions. Static composition remains a separate fixture; no phase policy or art admission follows from this pin change.

BP-001/BP-010 field contrast adoption: compare existing fill, dark contour and paired contour on the unchanged solid-clipped field path. D-104/T1045–T1046; presentation comparison only, no ruleset/content/arena/replay or active art migration. Recorded selection and coordinated visual-contract update remain required before changing shipping treatment.

BP-001 street-surface comparison adoption: separate repeating surfaces from placed continuous curb/embedded rails in the benchmark fixture. T1042/T1046; authored presentation parameters only, no arena, ruleset, content or active art migration. Legal arena integration and visual acceptance remain open.

D-105/D-106 adoption: SS-specs #67 (device checks no longer wait for the D-104 art review) and #68 (`run-shell.md` § 13 interruptions, T1050, RS-025–RS-032). No contract or fixture changed between `d6027758` and `a2119c93` (`git diff --stat` on `contracts/` and `fixtures/` is empty), so this is a pin move only. Ruleset, content, arena, replay and presentation identities are unchanged. T1050 is implemented in this runtime change; the iOS interruption sequence itself still needs a physical-device session.

D-107/D-108 adoption: SS-specs #73 (`run-shell.md` § 14 Court rehearsal, T1051, RS-033–RS-040), #74 (BP-011 palette report, BP-012 breadth-first bar) and #75 (status). No contract or fixture changed between `a2119c93` and `0f0fb95f`, so this is a pin move only. T1051 is implemented in this runtime change. Ruleset, content, arena, replay and presentation identities are unchanged.
