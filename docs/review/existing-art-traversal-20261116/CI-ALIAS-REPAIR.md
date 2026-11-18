# CI temporary-root alias repair (#244)

## Remote integration evidence

Exact repair head `be7db0d8cbdf95c84f94456389bb22433a86d59d`, run43833371384, spec-parity job133183856803 completed SUCCESS. Fetched job log at08:58UTC confirms the new real-symlink regression passed, all23traversal tests passed in5.482s, and the final bidirectional contract/fixture byte comparison succeeded against unchanged pin `b1ed874e1e8eb0e61b2174b9093201e9a61e1a4b` at08:46:46UTC. Retained raw log: `ci-repair-parity-success.log`; exact-head job metadata: `ci-repair-parity-success.json`. This proves this CI job, not every job or later publication heads. No merge or issue closure inferred.

Run43828925099, exact head d2a9fe0e993274c7a7aaab4702cd37b596970e81, passed the repaired whole-scene step but failed the later traversal evidence step. The failed comparison used `/var/folders/...` fixture roots against resolved `/private/var/folders/...` attachment paths. The retained-evidence fixture and offline verifier had the same mixed-root assumption. This is separate from #242's missing published enemy packet.

Canonicalize the three temporary roots before comparison. The production attachment/resource validators and their escape assertions are unchanged. Added a regression accepting an aliased export root while rejecting both a real outward symlink and an existing `../outside.json` target.

## Validation, November 16 08:41 UTC

- Replayed the old exact test from `git show HEAD` under an explicit scratch-root symlink: expected failure, canonical versus aliased path mismatch.
- Corrected traversal suite under that same aliased root: 23 tests passed in10.312s, including existing mutation tests and new real symlink escape cases.
- Offline retained verifier under the alias:52captures,824rows,51textures,1073resources, existing-art diagnostic only.
- Default local temporary-root run:23tests passed in9.441s. Default local paths did not reproduce the failure, so this was not presented as the red test.
- Downstream suites:7viewport,28encounter and7retained playback tests passed. An initial command used the singular encounter directory by mistake, ran no encounter tests, and was corrected to the actual plural directory.
- Raw red/green output retained in `alias-red-green.log`; failed CI job log retained in `ci-failure.log`.

At08:40UTC, exact original run still had Debug running, Release/Swift/device-sitting successful, spec-parity failed. No full CI success or issue closure claimed. No production source, acceptance gate, pin, or assertion relaxation.
