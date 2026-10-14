# Specification Baseline

Status: PINNED

| Identity | Value |
|---|---|
| Specification repository | `scrimshawlife-ctrl/SS-specs` |
| Specification commit | `c0163b9de92d0033f8a1f9907b4d9365ca11bf44` |
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
