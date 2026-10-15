# BP-002 / BP-008 elevated-motion reconciliation

Adopts SS-specs 492d921027c11d809ff18e3a35f520118e13de84. Four runtime pins move together. No active clip, production art, gameplay identity or fixture changes.

The source scaffold at 435b984 preserves its 2D rigid segment lengths. This proves transform consistency only, not anatomical length, depth correctness or world foot contact. The updated specification distinguishes those quantities and requires reviewed elevated keys and authored contact landmarks. Existing source rig records already label their pivots approximate and their limits explicitly; they remain review artifacts, not production delivery.

Next source work: separate boot/cloth controls; author the contact model and missing surfaces; compare depth-treated south keys before in-betweening. Do not claim a visible sole point is an unseen heel, or constant projected length is an anatomical constraint. Retain BP-008 actual movement, cadence, analog, interruption and world-slip comparisons. No new source technology or skeletal runtime is selected by the spec adoption.

Specification and timing validators passed before adoption. Runtime parity and core results follow in this directory. Device and complete benchmark gates remain open.

Verified: exact-pin parity passed. Core regression passed all 773 tests in 109 suites in 407.912 seconds. Source-control preparation preserves the neutral exactly but leaves the new boot/cloth seams and contact model unfinished; its archive is under source-controls/. No simulator/device result is implied by this core run.
