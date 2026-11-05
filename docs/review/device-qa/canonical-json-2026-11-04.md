# Canonical JSON

Read 2026-11-04 from `CanonicalJSON` on `fcab4e5`. No encoding was changed.

`serialize` writes one string. Object keys go out through `keys.sorted()`. There is no insignificant whitespace. Integers and unsigned values are decimal. `sha256Hex` is `SHA256.hex` of that string's UTF-8 bytes.

The cases are object, array, string, integer, unsigned, bool, and null. Bool writes `true` or `false`. Null writes `null`. A string is quoted. The escapes are `"` to `\"`, `\` to `\\`, backspace to `\b`, form feed to `\f`, line feed to `\n`, carriage return to `\r`, and tab to `\t`. Any other scalar below `0x20` is `\u` plus four lowercase hex digits. A higher scalar is copied through.

`parse` accepts, in this order: `NSNull`, `Bool`, `String`, an array, a string-keyed object, `Int`, `Int64`, `UInt64`, and `NSNumber` through `int64Value`. Anything else returns nil. One rejected element rejects the array or the object that holds it.
