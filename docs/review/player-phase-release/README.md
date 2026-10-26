# Every displayed-phase release: current bounded player

2026-10-19: three affected native Simulator tests pass, zero failures, 134.620 seconds. The new release matrix passes 32 cases: 16 post-action movement textures × Standard/Reduced Motion, at 1.25× tracked view. Both six-variant traversal controls also pass.

Driver observes the actual texture, records releaseTick, then supplies zero movement on the next simulation step. Independent Simulation replay uses that observed release tick and verifies every world position plus final state digest. Assertions retain first supported idle texture, correct selected clip, terminal neutral, root projection, unsupported startup facing and zero outline readbacks. coverage.json verifies all 32 unique target/mode pairs against exported records; no phase is inferred from tick arithmetic.

Scope: continuous state delivery into held neutral. No authored settling animation, production policy, asset/anchor change or new input delay. This run does not prove visual stop smoothness, restart/reversal, missing facings/actions, or physical-device readiness. The earlier 16-test suite passed before this test-driver extension; all three affected tests were rerun afterward.
