---
title: Verify SpriteKit property storage before asserting exact literals
author: Daniel
date: 2026-11-16
branch: qa/bp001-projection-decision-20261116
id: l-f6c801e6
scope: repo
status: active
src: agent
touches:
  - ".github/workflows/ci.yml"
  - docs/handoff/NEXT.md
---

## Decided
- Keep exact depth witnesses, but compare against the measured storage representation. The V8 witness expected Double0.1 while an actual SpriteKit property probe returned0.10000000149011612, exactly CGFloat(Float(0.1)). Correct that oracle, not the renderer, and add observed property diagnostics.
- Open a defect before correcting a failing oracle. Preserve the failed native result, frozen old source/input hashes and logs, then independently bind the retry to its freshly built and actually loaded executable.
## Tried and ruled out
- Adding a broad float tolerance or dropping the depth assertion would conceal unrelated depth changes. Three exact-storage/sourceguard regressions protect the narrow correction.
## Watch out
- A macOS SpriteKit probe is not retroactive inspection of the failed iOS node. Keep that distinction and the initial failure in the record.
In the code: AppTests/FootprintGroundSceneTests.swift, docs/review/footprint-ground-repair-20261116/scene/test_ground_storage.py, docs/review/footprint-ground-repair-20261116/NATIVE-ORACLE-253.md. Issue253. Native2321 passed1test after the exact oracle repair; native2317 remains failed.
