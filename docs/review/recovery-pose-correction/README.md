# Recovery contact-key source correction

Status: authored key geometry, not final art, not a complete gait and not admitted to runtime.

The prior source knee projected to (218.28, 281.77) on the 384px source canvas, while the visible raised knee-pad center is approximately (214,244). That annotation describes a visible pad, not a measured hidden anatomical joint. Prior registration kept the upper body while using a different lower-limb pose, so boot paint alone could not resolve the source mismatch.

solve_key.py authors a replacement key with the existing hip and both 13.5-unit segment lengths. It constrains the knee's projected vertical coordinate to the approximate pad center, chooses the forward sphere/plane intersection, and places the ankle on the shin-length sphere toward the prior ankle. Knee lateral coordinate 3.55 is authored. Heel/toe follow the existing foot pitch. These are explicit proposed hidden coordinates, not reconstructed anatomy. The new projected knee is (213.3,244). No nonuniform image registration or limb stretch is used.

The owned boot surfaces are regenerated from that pose. The full-character comparison places the mesh behind retained paint and also exposes it as an overlay. This improves knee registration but the proxy boot still needs silhouette, ankle/shaft continuity, proportions and costume-material refinement; it is not benchmark art. Painting and animated interpolation remain open. The existing block.py timing curve is deliberately not presented as updated by this single-key solve.

Authority: SS-specs d602775 controlled-character-source.md requires reviewed source keys and explicitly authored hidden landmarks before in-betweening. This source experiment stays within that authority; no active metadata, simulation or renderer code changes.

Reproduce with Python + NumPy + Pillow: solve_key.py, then orientation.py. Exact source files and generated key JSON are included. Segment lengths and source ownership assertions passed. Four isolated views and full-character comparison were inspected. The character artwork itself is unchanged.

Core validation: swift test --disable-sandbox finished with exit 0; 773 tests in 109 suites passed in 405.259 seconds. The earlier plain swift test reported the same test total but exit 1 due to nested sandbox manifest initialization, so it was not counted as a clean pass. No new simulator or physical-device result is claimed.
