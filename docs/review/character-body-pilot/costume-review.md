# Costume construction refinement — revisions 5–6

2026-10-14. **Source experiment only; benchmark art gate remains failed.**

## Changes

Revision 5 replaces separate thigh/shin ellipsoids with continuous trouser meshes and blended knee weights. Knee reinforcement is flatter and darker. The coat now has a shaped opening, longitudinal drape stations and continuous rolled front edges. The previously front-only strap now wraps over the shoulder, down the back and around the hip.

Front and rear 384px renders of revision 5 exposed an angular, floating rear strap. Revision 6 resamples its closed loop and projects the strip to the actual coat surface. 271 of 280 vertices found coat intersections; the remaining 9 are near the open front or shoulder limits and remain a visual-review concern. A count of intersections is not proof that the strap fits or deforms correctly.

Exact revision 6 service artifact metadata is retained in costume-evidence.json. Service ETags are not local file hashes. The source is retained in hosted project `e428d4b6-3697-4c74-ae65-78764240abde`; no local .blend download is claimed.

## Visual verification

- Revision 5: frame 1, rig rotations 0° and 180°, same camera/light setup; both images inspected.
- Revision 6: frame 1, rig rotations 90° and 180°, same camera/light setup; both images inspected.
- These are actual rotations of one mesh/rig, not mirrored raster views. Angles are source rotations, not a claimed mapping to runtime cardinal directions.
- Front leg continuity improved. Rear strap bend is smoother in the revision 6 render. The side view exposes an unfinished shoulder/sleeve junction, and the rear coat has dark surface artifacts that still require diagnosis.
- The model remains too smooth and generic relative to the approved reference. Hands, garment construction, material treatment, shoulder junctions and costume readability remain inadequate. There is no basis to claim native-size benchmark fidelity or artifact-free deformation.

## Scope and next decision

The controlled-source specification already requires rejection of mannequin-quality art; these changes do not relax it. Retain this rig for contact and pose experiments, but do not export it as replacement game art. Before investing in a full animation family, compare a higher-quality painted/layered costume treatment against the approved reference, or bring this master to that same standard. A production method must demonstrate the target aesthetic as well as stable motion.

Four neutral facings at one final revision, peak/intermediate deformation after these edits, south locomotion/world-travel contact, and the real shared renderer comparison remain unverified. No runtime resource, active contract or gameplay changed. Six local Python recipes parsed successfully before the final evidence write; hosted mutations and four render exports succeeded. No Swift tests or physical-device tests were run for this art-only work.
