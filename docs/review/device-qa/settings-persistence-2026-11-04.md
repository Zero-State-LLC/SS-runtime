# Settings persistence

Read 2026-11-04 from `SettingsStore` on `5d954be`. No default was changed.

The stored values stay in [presentation-settings-2026-11-04.md](presentation-settings-2026-11-04.md).

The settings JSON lives in UserDefaults at `com.zer0state.surveillancesurvivor.presentationSettings`. A missing value, or a value that fails to decode, loads `PresentationSettings.defaults`. Each change encodes the settings back to that key.

Reduced motion follows the iOS Reduce Motion value read when the store is created, until the player changes reduced motion. That change sets `com.zer0state.surveillancesurvivor.reducedMotionChosen`. While the key is unset, a later launch still takes the value captured at that launch. `resetToDefaults` removes the key, loads the contract defaults, and then sets reduced motion to the iOS value captured when this store was created.

This does not enter the digest.
