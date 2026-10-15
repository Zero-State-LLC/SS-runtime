# Retained toe detail in the whole-character source

Status: source material refinement, not final art admission.

The high-resolution retained lead-boot image now supplies toe leather and the visible front sole edge in addition to the forward tongue lace patch. Mapping uses foot-local coordinates, so the paint follows the authored boot through all sixteen poses rather than being pasted in screen space.

The first broad upper-surface mapping included rear upper faces and sampled lace pixels there. boot/rejected-rear-paint-leak.png records the rejected result. The corrected mapping requires a source face center forward of local Y=-3.5 and an upward/forward normal, then constrains the registered source image vertical sample to rows 350–374 (toe region). The existing lace patch remains exclusive to the forward shaft tongue. The rear contact views and full-character material comparison were inspected after this correction; the rejected rear lace fragments are absent in those inspected views. This is not a claim of exhaustive all-angle textured-surface acceptance.

The toe is closer to the retained painting than the previous flat proxy. Shaft/heel detail, transitions between sampled and authored material, repeated calf cloth, proportions and whole-character motion quality still need work. Raw lighting is baked into the retained toe image, and the rear is still authored plain leather. The benchmark has not been met and no source frame is admitted to runtime.

Authority: SS-specs d602775 controlled-character-source.md/BP-002/BP-008. No new gameplay, active renderer/art/metadata or spec pin changes. boot/material.py and assemble.py completed exit 0, producing 32 boot renders/depth arrays and sixteen distinct whole-character poses. Latest clean core validation remains 773 tests / 109 suites; unchanged runtime was not retested for this material-only study.

Reproduce with Python + NumPy + Pillow: boot/material.py, then assemble.py. The archive retains the exact source art, registration, geometry/material recipes, layered body, poses, outputs and rejected comparison. Next is remaining boot construction/material refinement and full-source motion review before the existing facing and renderer gates.
