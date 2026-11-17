import Foundation

// Compile together with Sources/SurveillanceCore/Determinism/SHA256.swift.
// Isolated hashing microbenchmark, not evidence of frame rate or device qualification.
@main struct HashBenchmark {
    static func main() throws {
        var rows: [[String: Any]] = []
        for size in [0, 64, 1024, 4096, 65536] {
            let inputs = (0..<16).map { salt in
                (0..<size).map { UInt8(truncatingIfNeeded: $0 &* 73 &+ salt) }
            }
            let iterations = size > 4096 ? 100 : 1000
            var checksum = 0
            func measure(_ operation: ([UInt8]) -> String) -> Double {
                let start = DispatchTime.now().uptimeNanoseconds
                for index in 0..<iterations {
                    checksum &+= operation(inputs[index % inputs.count]).utf8.reduce(0) { $0 + Int($1) }
                }
                return Double(DispatchTime.now().uptimeNanoseconds - start) / 1_000_000
            }
            for input in inputs {
                precondition(SHA256.hex(input) == legacyHex(input))
            }
            // Warm both paths, then alternate measurement order across five rounds.
            _ = measure(SHA256.hex)
            _ = measure(legacyHex)
            var native: [Double] = []
            var portable: [Double] = []
            for round in 0..<5 {
                if round.isMultiple(of: 2) {
                    native.append(measure(SHA256.hex))
                    portable.append(measure(legacyHex))
                } else {
                    portable.append(measure(legacyHex))
                    native.append(measure(SHA256.hex))
                }
            }
            rows.append(["bytes": size, "iterationsPerRound": iterations,
                         "optimizedMs": native, "legacyMs": portable,
                         "medianSpeedup": portable.sorted()[2] / native.sorted()[2],
                         "checksum": checksum])
        }
        let output = try JSONSerialization.data(withJSONObject: rows, options: [.prettyPrinted, .sortedKeys])
        print(String(decoding: output, as: UTF8.self))
    }

    static func legacyHex(_ input: [UInt8]) -> String {
        SHA256.portableHash(input).map { String(format: "%02x", $0) }.joined()
    }
}
