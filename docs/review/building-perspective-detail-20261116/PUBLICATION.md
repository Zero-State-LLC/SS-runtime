# Publication validation, November 16 22:44 UTC

A sparse export from `git write-tree` was extracted into a fresh scratch directory, containing only staged/tracked source packets, AppTests and Sources. None of the unrelated untracked editable-master/family/enemy packets was copied.

The exact CI commands passed all13kiosk,11context and41scene tests with ResourceWarning treated as errors. The first retained check then correctly rejected the export because it lacked Git tracking or an explicit tracking receipt. Its raw output is `clean-export-first-2242.log`.

Initialized a separate Git index inside that exported directory and added only the exported files. This exposed one omitted already-tracked dependency, `intent/2026-11-16-scene-qa-repair.md`, retained in `clean-export-tracking-2243.log`. Enumerating all assembly dependency paths confirmed that was the sole omitted file. Exported that exact file from the same staged tree and indexed it. No validator, evidence, source or tolerance changed.

The final unchanged retained verifier, nine-image exact RGBA baseline checker and both actual-v7-required Node suites passed, exit0 in `clean-export-final-2244.log`. This establishes portable staged-tree evidence validation, not another native run or remote CI success. The independently rehashed native executable provenance was checked separately against the real2237 result before this export.

No production source/assets, old evidence, specification pin or unrelated untracked work is part of the staged publication. The new CI step enforces source replay, retained evidence and gallery failure behavior. Remote CI must be checked on the exact published head before any passing claim. No automatic polling chain, merge or issue closure.
