# Game-wide visual coverage matrix

Every visual row is **NOT ACCEPTED**: no owner visual acceptance has been recorded for any of them. "Technical" describes how the evidence was verified, not its quality. Rows marked NOT CAPTURED have no evidence. The quiet fixture does not stand in for any other row.

| Row | Captured | Technical | Visual | Evidence (docs/review/) | Note |
|---|---|---|---|---|---|
| Quiet street, control vs diagnostic | captured | verified (verify_capture + 7 offline) | NOT ACCEPTED | `whole-scene-benchmark-20261116/capture` | This packet. Static only. |
| Dense legal encounter (ghost-step tick4976) | captured | verified in BP001 trial | NOT ACCEPTED | `bp001-reference-trial-20261116/plates` | Previous art only; no whole-scene diagnostic arm. |
| Hostile/legal projected framing | captured | earlier capture | NOT ACCEPTED | `hostile-framing` | Previous art. |
| Occlusion: perimeter study | captured | earlier capture | NOT ACCEPTED | `occlusion-perimeter/review.md` | Test-only probe; front/rear/corner sides not separately covered for this scene. |
| Occlusion: front/rear/corner, this scene | NOT CAPTURED | — | NOT ACCEPTED | — | NOT CAPTURED. |
| South movement contact (native static) | captured | verified (verify_native + 14 offline) | NOT ACCEPTED | `player-ground-contact-20261116/native-results.md` | Static renderer, not live. |
| South release phases (native static) | captured | verified | NOT ACCEPTED | `player-release-variation-native-20261116` | Proposals, not accepted. |
| North/east/west facings | captured | source only | NOT ACCEPTED | `player-side-source-20261116` | Source sheets; no native whole-scene capture. |
| Camera integrity states / damage markers | captured | earlier capture | NOT ACCEPTED | `camera-damage-markers/review.md` | Not in this scene fixture. |
| Camera field-off | captured | staged view only | NOT ACCEPTED | `whole-scene-benchmark-20261116/capture` | Staged presentation flag only, not a gameplay field-off state. |
| Enemy roles (all existing) | NOT CAPTURED | — | NOT ACCEPTED | — | NOT CAPTURED in this published coverage packet. Local first-sample source work is unpublished and is not evidence here. No native whole-scene capture of any enemy. |
| Combat effects (hits, bolts, mines, telegraphs) | NOT CAPTURED | — | NOT ACCEPTED | — | NOT CAPTURED in whole-scene review. |
| UI states (pause, upgrade, results, lethal warning) | NOT CAPTURED | — | NOT ACCEPTED | — | NOT CAPTURED in whole-scene review. |
| Screen sizes / safe areas | captured | measurements only | NOT ACCEPTED | `stable-hud-reservation/README.md` | Not whole-scene visual. |
| Accessibility (Reduced Motion, HUD scale, VoiceOver) | captured | Reduced Motion only | NOT ACCEPTED | `reduced-motion-validation/README.md` | HUD scale and VoiceOver whole-scene NOT CAPTURED. |
| Live cadence | captured | diagnostic, issue #237 open | NOT ACCEPTED | `live-playback/README.md` | Not accepted; callback gaps remain. |
| Physical device | NOT CAPTURED | — | NOT ACCEPTED | — | NOT CAPTURED for this scene. device-qa notes are code reads, not captures. |
