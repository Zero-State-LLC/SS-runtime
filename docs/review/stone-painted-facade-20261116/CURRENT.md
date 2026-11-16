# Current supported stone review source

The final `output/preview-alpha.png` includes the registered independent roof prop. `output/building-alpha.png` intentionally excludes it. See `FINAL-ROOF.md` for issue246's exact three-texel derivative and preserved red attempts, and `COORDINATOR-REVIEW.md` for the November16 10:15UTC bounded scene recommendation and unresolved fidelity deficits. This is not owner acceptance or production admission.

The coordinator independently reran all13 building and9 roof tests plus actual OBJ/MTL roundtrip and mutation checks at10:14UTC. All passed. Supported commands, Python3 with the packet's existing Pillow dependency:

```sh
python3 -B -W error::ResourceWarning docs/review/stone-painted-facade-20261116/test_source.py
python3 -B -W error::ResourceWarning docs/review/stone-painted-facade-20261116/test_roof_layer.py
python3 -B -W error::ResourceWarning docs/review/stone-painted-facade-20261116/verify_exports.py
```

Earlier README/final-roof checkpoints saying coordinator review is pending describe their original point in time. They are not rewritten as past acceptance. Source metadata remains historical. Current decision is separately recorded and hash-bound by the scene assembly. Do not recursively discover tests in preserved attempt directories as a new green suite.
