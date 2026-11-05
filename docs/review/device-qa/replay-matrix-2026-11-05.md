# Replay matrix

Read 2026-11-05 from `ReplayMatrix.tripleRunDigest` on `ef68565`. No digest was changed.

The envelope load stays in [replay-commands-2026-11-04.md](replay-commands-2026-11-04.md).

The fixture version is `replay-matrix-001`. `load` requires that version and an `entries` array. Each entry needs an id, a fixture name, and an `expectedFinalDigest` of 64 characters. `tripleRunRequired` is the bool on the entry, or true when the value is absent or not a bool.

`execute` loads the fixture. When that envelope's expected digest is nil, the run uses the entry's digest, and an `invalid` outcome throws `digestMismatch` with the result digest. When the envelope already carries an expected digest, a result digest that differs from the entry's digest throws `digestMismatch`. A failed execute throws `executionFailed`.

`tripleRunDigest` runs `execute` three times. It throws `tripleRunMismatch` unless the three digests are equal, and then it returns that digest.

This does not change a fixture.
