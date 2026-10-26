# Source-backed settling lifecycle matrix — 2026-10-19

Accepted duration:0.375s, exact17-pose timing3/128s per hold. Added `testSourceBackedSettleInterruptionsKeepConfigurationInstalled` without modifying existing tests or production behavior.

Result:1 focused native test passed, zero failures/skips. Exported attachment contains442 unique cells: releases5/13 ×17 poses ×13 triggers. Triggers: completion, movement, reversal, hurt, missing hurt, dodge, extraction, defeat, success, Reduced Motion, reset, tick rewind and idle-facing change. Repeated ticks preserve selected phase. Candidate configuration remains installed through the interrupted state, immediate return to idle and later idle. Fresh backed southward movement can start a new settling occurrence; cancellation without a new movement sample cannot resurrect the old one.

The actual entry/intermediate/neutral textures come from the current source candidate. Other states use single-frame sentinels from available bundled state/facing textures; missing art stays unbacked. Backed south hurt is explicitly required. Legacy north art is a lifecycle control, not newly approved facing art. The matrix verifies texture identity and selected-state parity against an independent renderer without settling. It does not exercise live action cadence, physical video presentation, complete reaction animation or simulation replay; those are separate existing checks.

Evidence: source-backed-result.json, source-backed-attachments/, source-backed-inputs.json. Post-run source/fixture hashes match. Removing only the new test from the working source reproduces the exact prior22-test-suite input hash; all other inventoried inputs also match. Thus prior regression evidence is preserved, but this is not claimed as a new23-test full-suite run. Fresh core regression passed:779 tests in110 suites,481.180 seconds, process exit0. Full log: source-backed-core-tests.log.

No renderer fix was needed for these tested cases. Remaining work: source contact/cadence, all other release phases, other facings/actions and complete-family/production/device gates.
