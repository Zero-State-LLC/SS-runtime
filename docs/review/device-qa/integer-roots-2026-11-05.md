# The integer roots

Read 2026-11-05 from `IntMath` on `ef68565`. No root was changed. `divHalfAway` and `mulDivHalfAway` stay in [q8-scale-2026-11-04.md](q8-scale-2026-11-04.md). The 30-degree product stays in [target-order-2026-11-04.md](target-order-2026-11-04.md). The travelled-distance `isqrt` stays in [projectile-step-2026-11-04.md](projectile-step-2026-11-04.md).

`abs` of a negative value is the wrapping subtraction of that value from 0 (`0 &- value`). A value that is not negative is returned as it is.

`gcd` takes absolute values, then replaces the pair with the remainder until the remainder is 0, and returns the other value.

`isqrt` preconditions `n >= 0`. A value below 2 is returned as itself. Otherwise `x0` starts at `n` and `x1` is `(x0 + n / x0) / 2`. While `x1 < x0`, `x0` becomes `x1` and the same step runs again. The function returns `x0`. The source comment calls that flooring.

`quadraticDiscriminant` builds a 128-bit `b²` and a 128-bit `ac`. The sign of `ac` is negative when `a` and `c` differ in sign. `4ac` overflows when the high word of `ac`, shifted right by 62, is not 0. When `ac` is negative and that shift overflows, the function returns `Int64.max`. When `ac` is not negative and that shift overflows, it returns nil. When `b²` is below `4ac`, it returns nil. Otherwise it returns the 128-bit sum or difference through `fitNonNegative`.

`fitNonNegative` returns `Int64.max` when the high word is not 0 or the low word is above `Int64.max`.

`UInt128Product` stores the full-width product of two `UInt64` values. `times` multiplies by a factor and preconditions that neither the high multiply nor the add overflowed. Comparison reads the high word, then the low word.

This does not change a quantity.
