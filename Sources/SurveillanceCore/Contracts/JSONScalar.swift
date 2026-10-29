import Foundation
import CoreFoundation

/// `JSONSerialization` bridges both JSON booleans and numbers to `NSNumber`,
/// so `as? Int` accepts `true` and `as? Bool` accepts `1`. The CoreFoundation
/// type tells them apart. `CoreFoundation` is imported explicitly because
/// Foundation re-exports it on Darwin but not on Linux.
enum JSONScalar {
    static func isBool(_ value: Any?) -> Bool {
        guard let number = value as? NSNumber else { return false }
        return CFGetTypeID(number) == CFBooleanGetTypeID()
    }
}
