# Boss, daemon, and upgrade cues

Read 2026-11-03 from `AudioProjector` and `BossSystem` on `241c167`. No cue was added.

`BossSystem` is the writer of `bossAttackStarted`, and the payload `attackId` is a `BossAttackID` raw value. The four values are `safetyRationale`, `narrowTailoring`, `temporaryOrder`, and `independentReview`. None of them contains `query` or `dash`, so each plays `boss_telegraph_` plus that raw value. The haptic is warning, the priority is 2, and the caption is the `CaptainCaptions.telegraph` string.

| Attack | Cue | Caption |
|---|---|---|
| `safetyRationale` | `boss_telegraph_safetyRationale` | Cone: for your safety |
| `narrowTailoring` | `boss_telegraph_narrowTailoring` | 3 bolts: narrowly tailored |
| `temporaryOrder` | `boss_telegraph_temporaryOrder` | Field: temporary, indefinitely |
| `independentReview` | `boss_telegraph_independentReview` | Ring, 1 gap: independently reviewed |

The projector also maps an attack id that contains `query` to `daemon_query` with caption `Query: just a quick search`, and one that contains `dash` to `daemon_dash` with caption `Dash: reasonable suspicion`. No current `BossAttackID` takes those branches. The elite cycle does not emit `bossAttackStarted`.

A `bossPhaseChanged` event plays `boss_phase_` plus the phase raw value. The haptic is heavy and the priority is 2.

| Phase | Cue | Caption |
|---|---|---|
| `publicSafety` | `boss_phase_publicSafety` | Public Safety: nothing to hide? |
| `civilLiberties` | `boss_phase_civilLiberties` | Civil Liberties: duly balanced |
| `temporarySafeguard` | `boss_phase_temporarySafeguard` | Safeguard: until further notice |
| `independentReview` | `boss_phase_independentReview` | Review: the Authority finds no fault |

An `upgradeSelected` event plays `upgrade_selected_` plus the upgrade id. The haptic is success, the priority is 7, and the caption is `Upgrade selected`. The three ids are `signalJammer`, `ricochetPulse`, and `ghostStep`.

The lethal warning has an empty audio id, haptic warning, priority 1, an empty caption, and `consumesEffectVoice` false. It fires on the rising edge, then again only after 60 ticks clear. `play` returns on an empty audio id, so the missing file is not recorded as a missing asset. The HUD card is the caption.

Every `CaptainCaptions` string is at most 40 characters. This does not add a caption.
