# South lower-leg pose block — BP-002 / BP-008

Status: EDITABLE SOURCE GEOMETRY EXPERIMENT; not final artwork, accepted gait or runtime integration.

## Authority and research

SS-specs 492d921027c11d809ff18e3a35f520118e13de84 already requires authored lower-leg contacts, elevated depth keys and world-travel comparison. No product specification change is necessary for this bounded source experiment. Runtime base is 37181b6. Original painted character remains unchanged.

Animation Mentor's [Animating Dynamic Run Cycles](https://www.animationmentor.com/blog/animating-dynamic-run-cycles/), retrieved 2026-10-14, recommends reference-led blocking of stride, down, passing and push-off, with airborne periods distinguishing running from walking. This motivates the support/flight comparison. The article does not supply SS measurements, support durations or camera angle. Its video was not viewed.

## Editable source

Run `python3 block.py` with Python 3 and Pillow. parameters.json contains every proposed dimension, projection and timing parameter. sixteen-samples.json saves the lower-body positions at the sixteen distinct sample times; 0.5 seconds is the repeated first pose and is not exported as a seventeenth frame. The slow GIF uses 125ms diagnostic holds, explicitly not production cadence. Full-body anatomy, costume, mesh, lighting and runtime are absent.

Coordinates: x lateral, y forward, z up. The candidate front projection is x to screen x and y*sin(elevation)-z*cos(elevation) to screen y. Anatomical right appears on image left. The 30-degree elevation is an authored comparison value, not a camera inferred from the concept. Source drawings use 6 pixels per model unit. The retained neutral is shown unmodified at its 384px canvas size beside the block; this does not establish registration.

The two-segment chain solves hip to ankle with fixed lengths and a forward knee branch. A simple sole rectangle carries distinct heel and toe points. During proposed support the toe remains at one nominal world location while the foot rolls about it. During recovery the ankle follows an editable trajectory. These are authored candidate surfaces and landmarks; they are not measurements of hidden anatomy in the neutral image. The source supplies 3D positions, so projected segment lengths can change without changing model lengths.

The only inherited numeric choices are 240 units/second full-input nominal speed and the initial 0.5-second cycle. Support lasts 0.1 seconds per leg, offset by 0.25 seconds; dimensions, compression, recovery lift, forefoot pivot and camera are PROPOSED experiment parameters. They do not define gameplay, sprint, analog policy or the final gait.

## Findings and verification

The eight-key sheet shows each side in initial support, compressed support, toe-off and flight, paired with side diagnostics. Both views were inspected. The front projection visibly foreshortens limbs; the side diagnostic exposes knee flexion and heel lift. This is useful pose geometry, not evidence of benchmark-quality character art.

The initial recovery curve stopped horizontal ankle travel abruptly at support boundaries. A cubic endpoint-velocity attempt exceeded chain reach. The final bounded endpoint correction preserves the requested support-relative velocity without automatic limb stretching. Body-height and lift curves have zero endpoint slope. Dense sampling covers 1,001 times over one cycle; exact boundary samples and finite differences are recorded separately. These are source checks, not simulation or runtime tests.

Recorded measurements:
- Maximum segment-length numerical residual: 5.33e-15 model units.
- Minimum sampled heel/toe height: 0; no sampled landmark below the ground.
- Continuous nominal support-toe drift: 0.
- Last-to-first local position difference: 0.
- Maximum one-sided finite-difference velocity mismatch at inspected boundaries: about 0.000604 units/second at epsilon 1e-7 seconds. No visual acceptance threshold is implied.
- Uniformly holding sixteen samples yields up to 7.44 units of nominal support-toe drift in the dense comparison. At the proposed front projection this corresponds to 3.72 logical vertical units, before output display scaling. The exact .03125-second hold allows up to 7.5 units of travel before the next sample; measured 7.44 reflects the sample grid. This is not an observed shipping-renderer slip value.

The continuous model's zero contact residual therefore does not transfer to discrete sprite playback. Actual simulation positions, animation sampling/phase, render interpolation, cardinal and diagonal movement, collision stops, reversals and interrupts still need BP-008 review. Do not reduce controller speed or assert that sixteen source frames automatically pass foot contact. Numerical slip acceptance remains unchosen in the spec.

## Next production step

Fit/review the candidate lower-body proportions against the retained painted source and author coherent depth surfaces for the contact, toe-off and recovery keys. Review the full hooded silhouette and garment occlusion with those keys before in-betweening. Keep four distinct elevated facings and the complete character/camera/environment benchmark scope. This geometry diagram cannot replace the required artwork or real-renderer scene.

No production code, textures, metadata, spec pins or gameplay changed. The existing 773-test core result at f724a50 remains the latest core evidence; this artifact-only change does not claim a new core run. Reproduction assertions cover source reach, lengths, ground landmarks, nominal contact and positional closure only. Physical-device testing remains deferred.
