# State digest

Read 2026-11-04 from `StateDigest.canonical` on `fcab4e5`. No field was added. Local settings stay in [presentation-settings-2026-11-04.md](presentation-settings-2026-11-04.md).

The digest is the SHA-256 hex of one canonical object.

The object carries the four identity strings (`rulesetVersion`, `contentVersion`, `arenaVersion`, and `schemaVersion` for the replay schema), the seed, the tick, and the outcome. The player fields are id, x, y, integrity, dodge ticks still active, the dodge-ready tick, and the damage remainder in hundredths.

Cameras are sorted by entity id. Each record is id, socket id, integrity, and housing. Living enemies are sorted by id. Each record is id, archetype, x, y, integrity, and awareness. A patrol member also records route, target, dwell remaining, and facing x and y.

Exposure records its value, detection state, no-contact ticks, whether lockdown has been entered, and quiet approach. The upgrade is the selected id, or null. Extraction records armed and remaining. The object also carries elite defeated, boss defeated, and `allocatorNext`.

`allocatorNext` is the next raw id. A run starts the allocator at 1. Each id issued is the current value, and the counter then advances by one.

The `rng` object is the combat stream's four words, `s0` through `s3`.

This does not change a hashed field.
