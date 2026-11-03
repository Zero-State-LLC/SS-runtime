# Haptic patterns

Read 2026-11-03 from the runtime sources on `241c167`. No pattern was changed. Specs #63 stays open.

`AudioEngine.fire` is the device call. It returns without a tap when haptics are disabled, reduced sensory is on, or `mix.haptics` is not greater than 0. Before that, `AudioProjector` sets a cue's pattern to `none` when haptics are disabled.

| Pattern | Call |
|---|---|
| `none` | no tap |
| `light` | `UIImpactFeedbackGenerator` style `.light`, `impactOccurred` |
| `rigid` | style `.rigid`, `impactOccurred` |
| `heavy` | style `.heavy`, `impactOccurred` |
| `warning` | `UINotificationFeedbackGenerator`, `.warning` |
| `success` | `UINotificationFeedbackGenerator`, `.success` |

Light, rigid, and heavy pass intensity `mix.haptics`. The default mix value is `0.80`, recorded with the mix note.

`prepareHaptics` starts a `CHHapticEngine` when the hardware supports haptics, and it prepares the four UIKit generators. The engine is not asked to play a `CHHapticPattern`.
