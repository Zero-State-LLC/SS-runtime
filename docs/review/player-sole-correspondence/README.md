# Source toe / boot-edge correspondence — 2026-10-19

Status: diagnostic evidence, not Player admission or native sole tracking.

`inspect_contacts.py` verifies every current source-record hash, projects authored heel/toe landmarks with the recorded root(192,336), six source pixels per logical unit, and source ground-y scale0.5. The plate places original lower-leg pixels beside annotated pixels for all16 poses; cyan marks declared support, amber marks lift. Source images remain unchanged.

Eight support observations (zero-based0–3/right,8–11/left) place the bottom alpha>=128 row in a five-pixel-wide toe-center band0.5–1 source pixel above the modeled toe. The band searches±12 rows around the target. These are diagnostic sampling parameters, not passing tolerances. Visual inspection of the plate places the marked toe at the visible front boot edge; alpha occupancy cannot identify material ownership or a hidden heel by itself.

`compare_trace_contacts.py` carries that measured source-row offset through all18 existing isolated native root traces. Standard full/half/quarter maximum alpha-edge proxy drift is2.8333/6.1667/8.6667 logical units for fixed timing, versus2.8333/3.5/3.5 for the paired distance candidate. This preserves the earlier result: partial-input cadence remains consequential; the small source landmark offset does not explain the whole drift. This inference does not choose playback policy, acceptance threshold or production scale.

The proxy combines source pixels with archived rendered roots. It does not track physical screen pixels, prove sole/ground contact through filtering/occlusion, or validate other facings. Those remain open alongside normal-speed cadence, quarter-speed inspection and timing approval. No anchor or artwork adjustment is justified solely by these measurements.

Reproduce from repository root:

```sh
python3 docs/review/player-sole-correspondence/inspect_contacts.py
python3 docs/review/player-sole-correspondence/compare_trace_contacts.py
```

The second script reads the archived current-contact audit; both outputs retain input identities. No runtime or fixture files are modified.
