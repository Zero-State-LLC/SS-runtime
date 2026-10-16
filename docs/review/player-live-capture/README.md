# Revised player: first live renderer integration

BP-002/BP-007/BP-008. Specs remain d602775. Test-only source candidate; active production art and metadata are unchanged.

The isolated fixture uses WorldRenderer, SpriteLibrary exact timing and GameSession simulation. It projects ground Y by 0.5 while a compensating parent preserves the elevated player artwork. The 384×416 source draws at 64×69⅓ with anchor (0.5, 1−336/416). Candidate textures and exact half-second timing live exclusively in the test bundle/library. Post-action records identify the actual selected SpriteKit texture; they are not inferred from simulation phase.

Final simulator result: 107 executions (105 named tests including a three-case parameterized test), zero failures. Core: swift test --disable-sandbox exited 0; 773 tests in 109 suites passed in 654.926 seconds. Runtime graph refreshed: 6,943 nodes / 29,429 edges.

Two earlier runs failed and are retained: first the completion check incorrectly depended on candidate availability and the initial sprite scale changed reported height; second the assertion incorrectly demanded south facing for the initial east-facing idle. Issue #130 records both corrections. The final assertions retain actual travel and changing frames, verify every candidate frame is south/move with correct dimensions, and require an explicit idle record after movement. No timeout extension or reduced movement requirement was used.

Observed limitation: only source frames 0 and 15 were captured before the south arena boundary stops motion. Synchronous image extraction perturbs display cadence, so these stills are not a continuous video or a performance benchmark. The emitted contact analysis combines source annotations with actual frame identities/root positions; sparse samples cannot establish acceptable slip. Full unobstructed-cycle capture without image extraction in the measured interval is still required.

Visual limitation: this fixture retains the inherited white outline as a control, which remains visibly heavy. It is not the approved benchmark finish. Ground-only context omits the building, cameras, HUD and encounters; this does not close their shared-scene gates. Other facings, partial input, diagonal travel, reversal, dodge and device acceptance remain open.
