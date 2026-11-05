# Damage log

Read 2026-11-05 from `DamageDiagnostic.capture` on `5a71391`. No damage amount was changed.

The export paths, the `QA_DAMAGE` lines, and the three-success bundle stay in [retest-checklist.md](retest-checklist.md). Which outcomes are finished stays in [terminal-seal-2026-11-04.md](terminal-seal-2026-11-04.md).

`damageDiagnosticsEnabled` defaults to false. `GameScene` sets it from `qaEnabled`, the `-SSQA` argument. Capture runs only while the flag is true, and only for `playerDamaged` events. The amount is the payload integer `amount`, or 0 when that integer is absent.

A projectile with that id, in the after state or else the before state, is listed as `projectile:<kind>` with its previous point, velocity, and alive flag. An enemy with that id is listed as `enemy:<archetype>` with the before state and the after state. A mine in the before state, whose id or owner id matches, and which is gone after the step, is listed as `removed-mine` with arm remaining and life remaining.

The classification is `authoritative-event-evidence` when the payload has `damageKind`, and then `authoritativeEventJSON` is that event's canonical serialization. With no `damageKind`, an empty source list is `unresolved-source`, and any listed source is `source-candidates-not-cause-proof`. The warnings are the before snapshot's telegraph strings.

The session keeps the last 512 records. Each record past that is dropped from the front and counted in `droppedDamageDiagnostics`. While QA is on, and before `session.step`, `damageViewCenter` is the camera position times `Q8.scale`, rounded, as a `VecQ8`. Each new record stores that point as `viewCenterBefore`. Ordinary play leaves the flag false, so the list stays empty.

`recordsTerminalEvidence` is a terminal outcome that is not already stored. The tracker notes that outcome on every such end. The file writes run only while QA is on. The export schema is `ss-damage-qa-001`. When `consecutiveCompleteRuns` is at least 3, a detached utility task profiles D021 and calls `exportReleaseCandidateWithBundledPlaytests`.

This does not paint a damage mark.
