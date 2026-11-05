# Combat authority node

Read 2026-11-04 from `CombatAuthoritySnapshot.project` on `aaa7919`. No node was added. The first-seen phase list stays in [boss-attack-clock-2026-11-04.md](boss-attack-clock-2026-11-04.md).

When extraction is armed, the node is `extraction`, ahead of the incomplete-mob checks. Otherwise the node is the first incomplete of `M-A`, `M-B`, and `M-C`. Otherwise it is `improperSearchDaemon` while the elite is undefeated, then `algorithmicModerate` while the boss is undefeated, then `extraction`.

`complete` is three completed mob flags, the elite defeated, and the boss defeated. `mobEncountersRequired` is 3. Completion stands while extraction is still unarmed.

`bossPhasesReached` is `BossPhase.canonicalPhasesReached`: receipt order `publicSafety`, `civilLiberties`, `temporarySafeguard`, `independentReview`, filtered to the phases the run has visited. The live list is first-seen order. The snapshot reorders it.

The mob nodes are the strings `M-A`, `M-B`, and `M-C`. The node raw values for the elite and the boss are the camelCase case names. The hyphenated receipt ids are `EncounterDirector.eliteReceiptId` and `bossReceiptId`.

This does not arm the extraction.
