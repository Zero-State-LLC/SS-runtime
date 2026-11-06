# The hash padding

Read 2026-11-05 from `SHA256.hash` on `ef68565`. No digest was changed. `sha256Hex` stays in [canonical-json-2026-11-04.md](canonical-json-2026-11-04.md). The state object stays in [state-digest-2026-11-04.md](state-digest-2026-11-04.md).

`emptyDigest` is `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

`hash` appends `0x80`, then zero bytes until the length modulo 64 is 56, then eight big-endian bytes of `UInt64(data.count) * 8`. Each 64-byte chunk loads sixteen big-endian words. A later schedule word is `w[i - 16] &+ s0 &+ w[i - 7] &+ s1`. `s0` rotates the word fifteen back by 7 and by 18, then shifts it right by 3. `s1` rotates the word two back by 17 and by 19, then shifts it right by 10.

Each of the 64 rounds rotates `e` by 6, 11, and 25, and `a` by 2, 13, and 22. Choice is `(e & f) ^ (~e & g)`. Majority is `(a & b) ^ (a & c) ^ (b & c)`. The adds are wrapping. The digest is those eight words written big-endian, 32 bytes.

`hex` of bytes formats that digest with `%02x` and joins it. `hex` of a string hashes its UTF-8 bytes. `rotateRight` is the right shift combined with the complementary left shift.

This does not change a digest.
