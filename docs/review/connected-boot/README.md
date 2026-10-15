# Connected boot and shaft source

Status: connected source geometry candidate, not final art or runtime admission.

The prior shoe and shaft were independently closed intersecting components. The new source removes a three-face top-vamp patch, uses its eight-edge boundary as the start of an ankle transition, and lofts it into four shaft rings with a top cap. Shoe and shaft are therefore one component before subdivision. The cloth tube remains separate and overlaps the cuff; it is not claimed as part of the boot topology.

The existing two-pass refinement preserves authored sole/end constraints. Forward tongue material remains separate surface detail, using the retained source patch. Its mapping is not duplicated on the rear. The new ankle transition and ring positions are authored source choices, not measurements of concealed anatomy.

Verification: material.py exported all 32 boot poses, exit 0. check_mesh.py independently verifies each boot is one connected component with two incident faces per edge, opposing edge traversal, Euler characteristic 2 and authored sole-plane deviation below 1e-9. These checks do not rule out self-intersections or prove anatomical/benchmark quality. The front/back contact sheet was inspected; the disconnected-component construction is removed, while material richness, precise boot silhouette and full-character cloth/depth integration remain open.

Authority: SS-specs d602775 controlled-character-source.md/BP-002/BP-008 already require editable hidden surfaces and pose-range review. No new gameplay/presentation policy, active art, metadata, renderer code or spec pins changed. Latest core run remains 773 tests / 109 suites; no new device/simulator evidence.

Reproduction: Python 3 + NumPy + Pillow; run material.py and check_mesh.py. source.zip contains exact geometry, refinement and material recipes, raw retained source/registration, all sampled poses and material outputs. Next is whole-character source integration and material/seam detailing; topology alone cannot admit this boot into the benchmark build.
