"""Offline geometry diagnostic for BP-007's existing comparison, not runtime proof."""
import argparse
import hashlib
import json
import math
from pathlib import Path

R = math.sqrt(0.5)


def project(x, y):
    return R * (x - y), R * (x + y) / 2


def inverse(x, y):
    return (x + 2 * y) / (2 * R), (2 * y - x) / (2 * R)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    directions = [('E', 1, 0), ('NE', 1, 1), ('N', 0, 1), ('NW', -1, 1),
                  ('W', -1, 0), ('SW', -1, -1), ('S', 0, -1), ('SE', 1, -1)]
    rows = []
    for name, x, y in directions:
        length = math.hypot(x, y)
        world = x / length, y / length
        screen = project(*world)
        recovered = inverse(*screen)
        assert all(math.isclose(a, b, abs_tol=1e-12) for a, b in zip(world, recovered))
        rows.append(dict(worldDirection=name, worldUnitVector=world,
                         projectedVector=screen,
                         screenAngleDegrees=math.degrees(math.atan2(screen[1], screen[0]))))
    # Unequal projection axes change apparent speed; never normalize this away in world rules.
    assert math.isclose(math.hypot(*project(R, R)), 0.5)
    assert math.isclose(math.hypot(*project(R, -R)), 1.0)
    down = inverse(0, -1)
    down_world = [v / math.hypot(*down) for v in down]
    assert math.isclose(down_world[0], -R) and math.isclose(down_world[1], -R)
    source = Path(__file__).resolve().parents[1] / 'AppTests/BenchmarkCaptureTests.swift'
    report = dict(status='OFFLINE_COMPARISON_GEOMETRY_NOT_RUNTIME_ACCEPTANCE',
                  coordinateConvention='SpriteKit scene: right +x, up +y',
                  transform='rotate +45 degrees then scale y by 0.5; translation omitted for vectors',
                  fixtureSourceSHA256=hashlib.sha256(source.read_bytes()).hexdigest(),
                  directions=rows, screenDownWorldUnitVector=down_world,
                  checks=['eight-direction inverse round trips', 'projected diagonal speed ratio',
                          'screen-down inverse direction'],
                  limitations=['Independent algebra, not execution of the Swift helper',
                               'No facing sector or hysteresis policy selected',
                               'No input conversion, source yaw, occlusion or live travel acceptance'])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print('PASS: 8 direction round trips; projected speed ratio; screen-down maps to world SW')


if __name__ == '__main__':
    main()
