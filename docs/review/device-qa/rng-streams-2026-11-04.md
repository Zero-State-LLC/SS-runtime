# Combat and cosmetic streams

Read 2026-11-04 from `SplitMix64` and `Xoshiro256StarStar` on `fcab4e5`. No stream was reseeded. The placement mix stays in [placed-cameras-2026-11-04.md](placed-cameras-2026-11-04.md). The digest's `rng` object stays in [state-digest-2026-11-04.md](state-digest-2026-11-04.md).

`SplitMix64.next` adds `0x9E3779B97F4A7C15`, then applies the multiply-xorshift constants `0xBF58476D1CE4E5B9` and `0x94D049BB133111EB`. `mix` is one `next`. `expand` is four.

The combat stream is `Xoshiro256StarStar` seeded by expanding the run seed. An all-zero state is rejected. One draw is `rotl(s1 * 5, 7) * 9`, and the state then shifts by the xoshiro256** step.

`next(below:)` for a range of 1 returns 0. A power of two is masked. Any other range draws again while the value is below `(0 &- n) % n`, then reduces the accepted value modulo `n`. A shuffle walks from the last index down to 1 and swaps with an index chosen in that prefix.

The cosmetic stream constant is `0x434F_534D_4554_3031`, ASCII `COSMET01`. Its seed is `SplitMix64.mix` of the run seed xor that constant. The digest records the combat words.

This does not add a stream.
