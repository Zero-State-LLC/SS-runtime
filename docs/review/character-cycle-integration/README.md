# Whole-character source cycle integration

Status: integrated source candidate, below benchmark and not admitted to runtime.

Sixteen poses now combine the retained hood, coat, equipment, arm layers and original thigh paint with the connected boot source. Pelvis height drives body bob. Existing arm controls supply a restrained authored counter-swing (6-degree shoulder, 4-degree elbow); coat hem displacement is 4 pixels with fixed root rows. These amplitudes are candidate authoring choices, not documented biomechanical prescriptions or final design acceptance.

The first assembly used affine thigh projection. It visibly flipped the painted knee/thigh when the projected hip-to-knee vector became short or reversed. rejected-flat-thigh.png records that failed pass. The revision uses an authored three-dimensional thigh surface and maps retained paint only to its forward half. The forward direction remains attached to the limb and is allowed to face away; it is not forcibly flipped toward the camera. Rear cloth is explicitly provisional plain material. This avoids substituting a flat rotated picture for depth, but does not establish final anatomy or costume fidelity.

The sixteen-pose sheet was inspected. Remaining visible failures include plain thin shins against detailed thighs, exposed joint/cap transitions, incomplete knee-pad coverage and simple cloth/arm movement. Each limb is sorted by average source depth; the boot and thigh are separate renders, so shared per-pixel depth and knee occlusion are not yet solved. The torso/coat layer policy also needs pose-range review. Do not admit these frames or describe them as the finished character animation.

Source verification: assembly completed exit 0, sixteen distinct RGBA hashes, fixed 384x416 canvas, sixteen timestamps over the existing 0.5-second cycle without a duplicate closing sample. Slow GIF is 125ms/frame for review, not shipping cadence. These checks do not prove visual quality, continuous seam deformation, actual world travel, native-size rendering or other facings.

Authority: SS-specs d602775 controlled-character-source.md/BP-002/BP-008; this is the required full-source pose-range review under existing intent. No active runtime art, code, metadata or spec pin changed. Latest clean core validation remains 773 tests in 109 suites. No new simulator/device claim.

Reproduce: Python 3 + NumPy + Pillow, run assemble.py. The source archive includes editable assembly/thigh recipes, original source layers, rig controls, exact poses and boot renders. Next is unified lower-limb depth/joint treatment and richer shin/boot materials, followed by the existing four-facing and real-renderer travel gates. The benchmark is unchanged.
