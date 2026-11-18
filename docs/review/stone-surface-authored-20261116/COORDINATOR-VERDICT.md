# Coordinator verdict and technical publication repair

## Visual verdict, November 16, 2026 08:44 UTC

Coordinator verdict: **NOT RECOMMENDED**. Recorded as directed by coordinator stallion in the November 16, 2026 08:47:30 UTC finalization message. This is not owner acceptance or production admission. No native integration, third visual sample or further visual-design pass is authorized. The existing second sample is retained unchanged.

## Publication repair

Coordinator independently inspected current `comparison.png` at08:43: recognizably authored structure and recessed apertures, but compact cube/short entry proportions, flat uniform roof/window masses, and polygonal surface patches remain unlike the worn painterly benchmark. This is a visual failure, not a topology defect. Actual Brave08:46 loaded all7images with native224x192, half112x96, full1120x960 source, correctly proportioned comparison/grayscale/registration views, and no horizontal overflow. These display checks do not change the NOT RECOMMENDED verdict.

The coordinator found two live entrypoint dependencies on the unpublished `stone-editable-master-20261116` sibling: `author_mesh.py` loaded its mesh and `replay.py` loaded its registration. They now read exact packet-local immutable copies in `inputs/`. `inputs/provenance.json` records original paths, purposes and SHA-256 identities. Historical source hashes and source citations in retained inputs are provenance, not executable dependencies. Archived failed attempts remain immutable historical evidence, not supported replay entrypoints.

Current entrypoints are root `author_mesh.py`, `replay.py` and `replay_painted.py`. The first retains the original authored foundation/stair inputs, the second consumes explicit saved mesh/paint and local registration, and the third consumes saved mesh and hand-painted PNGs. Only the tracked unchanged benchmark and arena contract are required outside this packet. No gameplay, collision, source geometry, paint or output pixels are changed by this repair.

Run from the repository root:

```sh
python3 docs/review/stone-surface-authored-20261116/verify_clean_copy.py
```

The verifier constructs a separate root containing this packet and `git show HEAD` exports of only the tracked benchmark and arena contract, asserts that the old sibling is absent, invokes the real author/replay/direct-painted entrypoints, checks exact mesh and existing PNG/SVG bytes and unchanged registration mapping, then runs the existing nine focused source checks without relaxing them. Upon success it refreshes only the current registration source-hash metadata. It does not regenerate this packet's visual exports. Verification output is retained in `clean-copy-verification.log`.

Verification completed November 16, 2026 08:50:59 UTC with exit 0 using `/usr/local/bin/python3` and Pillow 12.3.0. The actual author entrypoint reproduced all 144 mesh components byte-for-byte. Full replay regenerated the eight source/group/comparison PNGs and 102 surface PNG/SVG files identically. The comparison pass also retained the pre-existing overlay and painted preview unchanged, for 112 existing exports checked. The painted entrypoint was then executed independently and reproduced the full-resolution source bytes. All nine existing source tests passed in 29.275 seconds in the isolated tree. Registration mapping stayed identical, and only executable/input source-hash metadata was refreshed in the working packet. The old sibling directory was absent from that tree.

No commit or push. No unfiltered Swift retry, consistent with the active accepted intent and existing repeated-timeout stop condition. This is Python source-packet finalization only, not Swift/native runtime validation.
