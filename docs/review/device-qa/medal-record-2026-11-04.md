# Medal record

Read 2026-11-04 from `MedalTracker`, `MedalRecord`, and `MedalStore` on `006304e`. No medal threshold was changed.

The five predicates stay in [medal-predicates-2026-11-03.md](medal-predicates-2026-11-03.md). This note is how the tracker is fed, and what is stored.

`FeelPassPresenter.willStep` calls `notePatrol` before the step. `didStep` calls `ingest` on that tick's events. `GameSession` calls `willStep` before `step` and `didStep` after it. `notePatrol` inserts every enemy whose `patrol` is set. `enemyAlerted`, while `mobAStarted` is still false, sets `patrolAlertedBeforeMobA` when the primary id is in that set. `waveStarted` whose `encounterId` is `CombatAuthorityNode.mobA.rawValue` (`M-A`) sets `mobAStarted`. `replayMedals` calls `notePatrol`, then `step`, then `ingest`, while the simulation is short of terminal and commands remain. `medals(for:)` is empty unless the outcome is success.

`MedalRecord.earned` is empty unless the stored seed and the stored replay identity both match. `merging` keeps the union. The medals new this time are the earned set minus what was already stored. The record's list is `Medal.allCases` filtered to that union.

`MedalStore.record` returns an empty set and writes nothing when the earned list is empty. Otherwise it writes that seed's JSON atomically and deletes the other seed files in the medal directory. A load that fails to decode, or whose stored seed differs, is absent. A failed write still returns the medals that were new.

The title asks `MedalStore.earned` and draws `seal.fill` for an earned medal and `seal` for the others, with `Medal.name`. `MedalGoal.glyph` is `◆` when earned and `◇` otherwise. The title draws the seal images.
