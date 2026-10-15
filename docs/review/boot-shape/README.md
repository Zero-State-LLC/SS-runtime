# Boot shoe-volume refinement

Status: source shape candidate; not benchmark art or runtime admission.

Two Catmull-Clark passes refine the closed shoe loft. Constraints preserve its authored local sole plane and front/back end planes. The original material ownership and forward-only tongue patch remain. The source includes smooth.py and the exact prior volume recipe, so the shape is editable and reproduced for all 32 leg poses.

The first attempt also subdivided the two-ring capped shin and shaft components. Those became pinched capsules and visibly separated. rejected-tube-collapse.png records that failed result. The final recipe smooths only the shoe loft and retains the original attachment components exactly. This avoids introducing that regression; it does not establish a unified production ankle mesh.

The revised surface sheet was inspected. Shoe contours are less angular, but shaft/ankle construction, seams, sole detailing, costume-material richness and whole-character motion are still below the benchmark. Do not admit this proxy merely because mesh checks pass. No change to source gait, original raw artwork, active game resources, renderer or specs.

Verification: all 32 pose exports finished with exit 0. The independent shape check found two incident faces for every component edge and sole-plane deviation below 1e-9 source units across all poses. This checks component topology/constraints, not intersections between components or visual/anatomical acceptance. The source material check still restricts the laced patch to one forward tongue face per boot.

Authority: SS-specs d602775 controlled-character-source.md/BP-002/BP-008. Source-only refinement under existing editable-source requirements; no new product behavior. Previous clean core run remains 773 tests in 109 suites; no new simulator or device claim.

Reproduce with Python + NumPy + Pillow: material.py. source.zip includes the mesh recipe, retained raw source/registration, exact poses, 32 material renders, shape observations and failed comparison. Next must address the continuous ankle/shaft construction and full-character costume integration; a smoother isolated shoe is not the completed art pass.
