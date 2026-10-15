# Knee transition in the whole-character source cycle

Status: source joint treatment candidate, not art admission.

An authored 2.2-unit-radius joint cover is centered on each solved knee. Its anterior direction follows the knee's displacement from the hip-to-ankle line, keeping the pad on the front of the bend. Retained knee-pad pixels map only to the anterior sector; the rear uses provisional plain cloth. The thigh's longitudinal paint mapping now stops before the original pad region so that the pad is not stretched along the thigh and duplicated onto the joint.

The joint participates in the shared lower-body depth buffer. The sixteen-pose sheet was inspected: the previously exposed calf ends are covered in the reviewed recovery poses. The overall source still has weak boot detailing, repetitive calf cloth and simple torso/coat motion. This does not establish complete joint-range acceptance, anatomical accuracy, final proportions or benchmark fidelity. Radius and texture mapping are explicit authored choices, not recovered anatomy.

check_joints.py verifies all 32 projected knee-center samples are opaque and have finite surface depth in front of the source joint center. This is a narrow coverage check, not proof that every contour/intersection is correct. Assembly reproduces sixteen distinct fixed-canvas images and retains the existing 0.5-second source duration; slow GIF uses 125ms/frame. Both scripts completed exit 0. Original source art remains preserved in the archive.

Authority: SS-specs d602775 controlled-character-source.md/BP-002/BP-008, which requires authored hidden surfaces and pose-range review. No active runtime code/art/metadata or specification pin changes. Latest clean core result remains 773 tests in 109 suites; no new simulator/device acceptance.

Reproduce with Python + NumPy + Pillow: assemble.py, then check_joints.py. The archive includes the exact layered source, rig, pose samples, boot/calf images and depth arrays, editable thigh/joint/assembly code and review artifacts. Next remains boot/material refinement and whole-source motion/occlusion review before the four-facing and real-renderer travel gates.
