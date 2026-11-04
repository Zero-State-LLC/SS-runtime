# Presentation settings

Read 2026-11-04 from `PresentationSettings` on `93f6d67`. These values stay out of the simulation.

The settings are local. They are excluded from the state digest and from replay authority. The defaults are audio enabled, visual effects standard, HUD scale standard, handedness right, the camera counter unpinned, tutorials on, the ghost on, and captions important.

Audio enabled means effects, haptics, and music are on, and reduced sensory is off. Visual effects standard means reduced motion and reduced flash are off. HUD scale standard is 1000, large is 1150, and extra large is 1300. Caption values are `important`, `all`, and `off`.

A saved file with no `ghostEnabled` decodes as on. A missing or unknown `captions` value decodes as important. Each mix level clamps to 0…100, and a missing key takes its default. The stored defaults are master 100, music 70, effects 85, voice 100, and haptics 80. [mix-and-blackout-2026-11-03.md](mix-and-blackout-2026-11-03.md) records the engine gains those percentages produce. Bus gain folds the master in as `master/100 * level/100`. The buses are music, effects, voice, and haptics.

The receipt may declare tutorials, HUD scale, handedness, reduced motion, reduced flash, and reduced sensory. The mix, the ghost, and captions are not receipt metadata. The ghost remains presentation only.
