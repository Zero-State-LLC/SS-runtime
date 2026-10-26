# Current source contact comparison — 2026-10-19

Status: measured model evidence; visual acceptance and production adoption remain open.

Source: bounded-proportion south/front16-frame cycle and its current pose record. Every delivered PNG matches the pre-run source inventory and the source export record. The pose-record hash is recorded explicitly; it is source metadata, not renderer output. Native traces come from the full playback run archived at `work/player-native-pose-full-suite.xcresult`. Its existing playback tests pass; its unrelated new static-capture fixture initially failed setup.

The historical2026-10-16 audit remains historical: its pose-record hash differs from the current source. Do not carry its numbers forward as current validation.

## Paired distance-phase experiment

| Input | Motion mode | Fixed-time support range (logical units) | Distance-phase support range (logical units) |
|---|---|---:|---:|
| Full | Standard | 2.75–2.75 | 2.75–2.75 |
| Full | Reduced | 4.75–4.75 | 2.75–2.75 |
| Half | Standard | 6.25–6.25 | 3.50–3.50 |
| Half | Reduced | 2.75–6.25 | 3.50–3.50 |
| Quarter | Standard | 8.75–8.75 | 3.50–3.50 |
| Quarter | Reduced | 8.25–8.75 | 3.50–3.50 |

Ranges are min/max across observed support segments, not confidence intervals. Three backing pixels per logical unit in these captures:3.5 units corresponds to10.5 captured pixels. All paired traces contain the16 movement poses; individual support-segment observations may omit a pose. The JSON retains every observation and distinct-pose count. The controls and candidates run the existing input-specific test routes; do not compare aggregate segment counts as equivalent elapsed motion.

## Interpretation and next action

OBSERVED: the existing distance-phase candidate reduces modeled partial-input support drift while preserving the authored source and authoritative travel tested by the harness. Full-input Standard ranges are equal. Reduced Motion retains residual variation; no zero-slip claim follows.

PROPOSED: continue the existing distance-phase comparison in the shared renderer at full/half/quarter input with the same seed, source, projection, scale and commands. Keep normal-speed cadence separate from quarter-speed contact inspection. Compare collision-stopped input, wall slide and reversal against actual displacement; preserve the existing state/reaction precedence and replay identity. Select no cadence policy from this table alone.

Required remaining evidence: actual sole-pixel/ground-marker correspondence through declared support intervals, native visual review of foot travel and16→1 seam, and device/Release validation. The current formula uses authored toe landmarks and rendered roots; it is not pixel tracking. Do not translate the whole player to conceal drift or alter simulation speed.

Reproduce: `python3 docs/review/player-contact-audit/analyze_current_contacts.py` from the runtime repository. Inputs and hashes are in `current-contact-audit.json`; exported xcresult manifests retain test/device identities. This is evidence-only work; no runtime behavior, source art, timing selection or production pin changed.
