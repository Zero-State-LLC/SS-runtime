# Cadence comparison — proposed experiment

The existing BP-008 contract requires comparing partial-input policies before adoption. The recorded south route now has an offline comparison: see phase-comparison.json. No runtime playback policy has changed.

| Input | Existing support range | Distance-phase counterfactual |
|---|---:|---:|
| Full | 4.50–4.75 px | 2.25–2.75 px |
| Half | 7.25 px | 3.50 px |
| Quarter | 7.75–8.75 px | 3.50 px |

Ranges are modeled projected toe displacement over support observations, not pixel tracking. Each comparison uses exactly the same recorded roots; reduced cadence yields fewer support intervals. All 16 frame identities occur in each record. A held frame cannot continuously keep its foot fixed while its root travels. This comparison establishes a useful next experiment, not an acceptance threshold.

Apple provides action rate control: https://developer.apple.com/documentation/spritekit/skaction . Unity compares movement-driven and animation-driven approaches: https://docs.unity.cn/540/Documentation/Manual/nav-CouplingAnimationAndNavigation.html . SS must keep gameplay authoritative; neither source selects SS stride or partial-input appearance.

Next: test-only live comparison with explicit interruption/reset semantics and original cadence control, then normal/quarter-speed visual review. Do not admit distance scheduling, change timing metadata, or stretch sprites on this evidence alone.
