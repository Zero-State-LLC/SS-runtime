# Settings surface

Read 2026-11-04 from `SettingsView` on `d873e91`. No default was changed.

The stored numbers stay in [presentation-settings-2026-11-04.md](presentation-settings-2026-11-04.md). The file and the Reduce Motion latch stay in [settings-persistence-2026-11-04.md](settings-persistence-2026-11-04.md).

The title is `Settings`. Resume is the confirmation button, and its hint is `Closes settings and resumes the run`.

Audio has five sliders, labelled `Master`, `Music`, `Effects`, `Voice and captions`, and `Haptics`. Each step is 1. The value is the rounded integer, then `MixLevels.clamp`, on the range 0 through 100. Toggles are `Effects`, `Music`, and `Haptics`. The captions picker is `Important`, `All`, or `Off`.

Display picks HUD scale `Standard`, `Large`, or `Extra large`, and handedness `Right` or `Left` as a segment. Toggles are `Always show Camera counter` and `Ghost`. Accessibility toggles are `Reduced motion`, `Reduced flash`, and `Reduced sensory`. Gameplay toggles `Tutorial prompts`. `Reset to defaults` calls `resetToDefaults`.

This does not change a default.
