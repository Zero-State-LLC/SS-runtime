# Boot ankle proportion comparison

Status: proposed source proportion candidate, not anatomical measurement or runtime admission.

The retained east-facing boot was inspected before side-material projection. Approximate foreground visible landmarks are heel x156, toe x224 and lower-shaft center x173 in the registered 384px source. The shaft sits nearer the heel than in the current model's ankleBehindToe=5 on a length-10 shoe. These are visible silhouette/shaft annotations, NOT a recovered ankle-joint center. A painted view does not establish exact anatomy.

compare.py constructs a 7.5-unit ankle-behind-toe candidate. It retains every original heel/toe position, foot pitch, hip position and both 13.5-unit segment lengths in all 32 sampled leg poses. The knee is re-solved with the existing forward-branch/lateral constraint. The connected vamp opening moves from local Y[-6,-3] to [-9,-6], keeping the shaft attached to the newly proposed ankle position.

The actual candidate boot meshes, materials and whole-character cycle were regenerated. character-comparison.png was inspected against the prior key: the shaft is repositioned, but the recovery knee also changes. This does not preserve the earlier approximate painted-knee fit, and it is not automatically an art improvement. The side source motivates the comparison; it does not prove the numerical choice. The existing candidate remains preserved for review. No runtime or final source selection is claimed.

Verification: all 32 source poses remain reachable, both limb lengths pass 1e-9 construction checks, and heel/toe arrays are exactly unchanged. Boot material export and whole-character assembly each completed exit 0. These checks do not establish continuous source-curve interpolation, displayed contact, skin deformation or benchmark quality. Candidate samples are the pose authority; inherited block.py is retained as a helper and is not claimed to reproduce this candidate curve by itself.

Authority: SS-specs d602775 controlled-character-source.md/BP-002/BP-008 already require distinguishing visible annotations from authored hidden landmarks and reviewing full pose range. No new gameplay/renderer policy, active art, metadata or pins changed. Previous clean core result remains 773 tests / 109 suites.

Reproduce: compare.py; copy candidate-samples.json to candidate/boot/samples.json and candidate/source/samples.json; run candidate/boot/material.py and candidate/assemble.py. Exact inputs and outputs are archived. Side/rear material transitions and whole-motion/facing/renderer gates remain open; the benchmark has not been met.
