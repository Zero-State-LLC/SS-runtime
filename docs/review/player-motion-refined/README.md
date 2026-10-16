# Narrower stance and arm swing

Source candidate responding to user feedback. Built from SS-boot-proportion/candidate; not admitted runtime art.

Foot separation reduced from 10 to 8 source units (20%). Hips, forward/vertical foot trajectories, foot pitch, 16 samples and 0.5-second cycle retained. Knees re-solved with both segment lengths held at 13.5 units; all 32 poses verified within 1e-9. Contact positions shift sideways with the feet.

Arms now alternate forward/back through projected elbow (4px) and hand (10px) movement, opposite the same-side leg. Shoulder attachment stays fixed relative to the torso. The initial larger planar rotation was rejected because it spread both arms together. These are authored source adjustments; arms remain layered artwork, not a finished 3D arm rig.

The updated reviewer compares the prior rearward-ankle candidate against this revision. World-travel contact, side-facing motion, complete occlusion and real-renderer/device acceptance remain outstanding.

Authority: specs d602775, controlled-character-source.md/BP-002/BP-008 already require pose-range review and separate projected from anatomical measurements. No new gameplay policy or spec pin is required for this proposed source adjustment.

Validation: 16 distinct exported RGBA frames; all 32 source leg lengths pass 1e-9 checks; all 32 knee center pixels have opaque surface coverage in front of the joint; all 32 assembled elbow center pixels are opaque. These point checks do not prove full contour continuity or depth ordering. Runtime code, active art and metadata are unchanged; the previous clean core result remains 773 tests in 109 suites.

Reproduce from archived source: use the exact source/samples.json and boot/samples.json (authoritative revised poses), run boot/material.py, then assemble.py, then check_joints.py with Python, NumPy and Pillow. Inherited block.py is a helper, not a generator for this revised pose sequence.
